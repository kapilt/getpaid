from zope import interface
from zope.app.annotation.interfaces import IAnnotations

from getpaid.core import interfaces

from interfaces import IPaymentechOptions

import xml.dom.minidom
import zc.ssl

import httplib

CARD_SEC_VAL = ['Visa', 'Discover', 'Mastercard']
LAST_FOUR = "getpaid.paymentech.cc_last_four"
APPROVAL_KEY = "getpaid.paymentech.approval_code"

cvv2_codes = {'M': 'CVV match',
              'N': 'CVV no match',
              'P': 'CVV not processed',
              'S': 'CVV should have been present',
              'U': 'CVV unsupported by issuer'}

def createAuthorizeXMLFile(message_type, options, order, payment):
    """
    Creates the XML file to send to the Paymentech Interface
    """
    merchant_id = options.merchant_id
    if len(merchant_id) == 6:
        bin_number = "000001" # corresponds to 6 digit Salem Division Number
    else:
        bin_number = "000002" # corresponds to 12 digit PNS Merchant ID
    terminal_id = options.terminal_id
    card_number = payment.credit_card
    card_exp_date = payment.cc_expiration.strftime('%m%y') # MMYY
    card_sec_val = ""
    if payment.credit_card_type in CARD_SEC_VAL:
        card_sec_val = """<CardSecValInd>1</CardSecValInd>"""
    card_sec_value = payment.cc_cvc
    order_id = order.getOrderId()
    amount = str(int(order.getTotalPrice() * 100)) # $50.00 should be sent as 5000
    xml_text = """\
<Request>
  <NewOrder>
    <IndustryType>EC</IndustryType>
    <MessageType>%(message_type)s</MessageType>
    <BIN>%(bin_number)s</BIN>
    <MerchantID>%(merchant_id)s</MerchantID>
    <TerminalID>%(terminal_id)s</TerminalID>
    <AccountNum>%(card_number)s</AccountNum>
    <Exp>%(card_exp_date)s</Exp>
    <CurrencyCode>840</CurrencyCode>
    <CurrencyExponent>2</CurrencyExponent>
    %(card_sec_val)s
    <CardSecVal>%(card_sec_value)s</CardSecVal>
    <CustomerProfileFromOrderInd>O</CustomerProfileFromOrderInd>
    <CustomerProfileOrderOverrideInd>NO</CustomerProfileOrderOverrideInd>
    <OrderID>%(order_id)s</OrderID>
    <Amount>%(amount)s</Amount>
  </NewOrder>
</Request>
""" % locals()
    
    dom = xml.dom.minidom.parseString(xml_text)
    data = dom.toxml('utf-8')
    return xml_text

def createCaptureXMLFile(options, order, trans_ref_num, amount):
    """
    Creates the XML file to send to the Paymentech Interface
    """
    merchant_id = options.merchant_id
    if len(merchant_id) == 6:
        bin_number = "000001" # corresponds to 6 digit Salem Division Number
    else:
        bin_number = "000002" # corresponds to 12 digit PNS Merchant ID
    terminal_id = options.terminal_id
    order_id = order.getOrderId()
    amount = str(int(amount * 100)) # $50.00 should be sent as 5000
    xml_text = """\
<Request>
  <MarkForCapture>
    <OrderID>%(order_id)s</OrderID>
    <Amount>%(amount)s</Amount>
    <BIN>%(bin_number)s</BIN>
    <MerchantID>%(merchant_id)s</MerchantID>
    <TerminalID>%(terminal_id)s</TerminalID>
    <TxRefNum>%(trans_ref_num)s</TxRefNum>
  </MarkForCapture>
</Request>
""" % locals()
    
    dom = xml.dom.minidom.parseString(xml_text)
    data = dom.toxml('utf-8')
    return xml_text

def getElement(result, tag_name):
    """
    Get the value corresponding to a xml tag
    """
    if result.getElementsByTagName(tag_name):
        node = result.getElementsByTagName(tag_name)[0]
        if node.childNodes:
            child_node = node.childNodes[0]
            return child_node.nodeValue
    return None

class PaymentechConnection(object):
    
    def __init__(self, data, server, options, timeout=None):
        self.server = server
        self.timeout = timeout
        self.data = data
        self.options = options
    
    def sendTransaction(self):
        """
        Creates the HTTPS/POST connection to the Paymentech server
        """
        conn = zc.ssl.HTTPSConnection(self.server, self.timeout)
        
        # setup the MIME HEADERS
        conn.putrequest('POST', '/authorize')
        conn.putheader('MIME-Version', '1.1')
        conn.putheader('Content-type', 'application/PTI41')
        conn.putheader('Content-length', len(self.data))
        conn.putheader('Content-transfer-encoding', 'text')
        conn.putheader('Request-number', '1')
        conn.putheader('Document-type', 'Request')
        conn.putheader('Merchant-id', self.options.merchant_id)
        conn.endheaders()
        
        conn.send(self.data)
        return conn.getresponse()

class PaymentechResult(object):
    
    def __init__(self, response):
        self.response = response
        read_response = self.response.read()
        # need to do a check on weird characters that paymentech
        # returns sometime (like \x00)
        read_response = read_response.replace('\x00', '')
        self.result_resp = xml.dom.minidom.parseString(read_response)
        # ProcStatus is the only element that is returned in all response scenarios
        self.proc_status = getElement(self.result_resp, 'ProcStatus')
        # ApprovalStatus shows if ProcStatus = 0
        # 0 – Decline, 1 – Approved, 2 – Message/System Error 
        self.approval_status = getElement(self.result_resp, 'ApprovalStatus')
        self.trans_ref_num = getElement(self.result_resp, 'TxRefNum')
        self.cvv2_resp_code = getElement(self.result_resp, 'HostCVV2RespCode')
        self.status_msg = getElement(self.result_resp, 'StatusMsg')

class PaymentechAdapter(object):
    interface.implements(interfaces.IPaymentProcessor)

    options_interface = IPaymentechOptions

    _sites = dict(
        Production1 = "orbital1.paymentech.net:443",
        Production2 = "orbital2.paymentech.net:443",
        Test1 = "orbitalvar1.paymentech.net:443",
        Test2 = "orbitalvar2.paymentech.net:443",
        )

    def __init__(self, context):
        self.context = context
        self.options = IPaymentechOptions(self.context)
        self.server = self._sites.get(self.options.server_url)

    def authorize(self, order, payment):
        """
        Authorize the supplied information.
        This transaction type should be used for deferred billing transactions.
        """
        # A - Authorization request
        data = createAuthorizeXMLFile('A', self.options, order, payment)
        result = self.process(data, timeout=None)
        if result.proc_status == "0":
            if result.approval_status == '1':
                if self.options.check_cvv2:
                    # we check the cvv2 resp code:
                    if result.cvv2_resp_code != 'M':
                        if result.cvv2_resp_code in cvv2_codes:
                            return cvv2_codes[result.cvv2_resp_code]
                        else:
                            return "CVV number incorrect"
                annotation = IAnnotations(order)
                annotation[interfaces.keys.processor_txn_id] = result.trans_ref_num
                annotation[LAST_FOUR] = payment.credit_card[-4:]
                annotation[APPROVAL_KEY] = result.approval_status
                return interfaces.keys.results_success
        return result.status_msg

    def capture(self, order, amount):
        #AC - Authorization and Mark for Capture
        annotation = IAnnotations(order)
        trans_ref_num = annotation[interfaces.keys.processor_txn_id]
        data = createCaptureXMLFile(self.options, order, trans_ref_num, amount)
        
        result = self.process(data, timeout=None)
        
        if result.proc_status == "0":
            if annotation.get(interfaces.keys.capture_amount) is None:
                annotation[interfaces.keys.capture_amount] = amount
            else:
                annotation[interfaces.keys.capture_amount] += amount            
            return interfaces.keys.results_success
        else:
            return result.status_msg
    
    def refund(self, order, amount):
        """ XXX Not implemented
        """
        #R - Refund request
        #data = createAuthorizeXMLFile('R', options, order, payment)
        #
        #result = self.process(data, timeout=None)
        #
        #if result.proc_status == "0":
        #    annotation = IAnnotations(order)
        #    if annotation.get(interfaces.keys.capture_amount) is not None:
        #        annotation[interfaces.keys.capture_amount] -= amount                        
        #    return interfaces.keys.results_success
        #else:
        #    return result.status_msg
        return "Not implemented"

    def process(self, data, timeout):
        """
        creates a HTTPS request using SSL, sends the request
        and returns a response
        """
        conn = PaymentechConnection(data, self.server, self.options, timeout=None)
        response = conn.sendTransaction()
        return PaymentechResult(response)
