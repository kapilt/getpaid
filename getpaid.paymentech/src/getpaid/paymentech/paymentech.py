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

def createXMLFile(message_type, options, payment, order):
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
    amount = str(order.getTotalPrice() * 100) # $50.00 should be sent as 5000
    xml_text = """\
<Request xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="Request_PTI42.xsd">
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
    return data


def createConnection(data_len, server, options, timeout=None):
    """
    Creates the HTTPS/POST connection to the Paymentech server
    """
    conn = zc.ssl.HTTPSConnection(server, timeout)
        
    # setup the MIME HEADERS
    conn.putrequest('POST', '/authorize')
    conn.putheader('content-type', 'application/PTI41')
    conn.putheader('content-length', data_len)
    conn.putheader('content-transfer-encoding', 'text')
    conn.putheader('request-number', '1')
    conn.putheader('document-type', 'request')
    conn.putheader('merchant-id', options.merchant_id)
    conn.endheaders()
    return conn

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
        # create the XML file
        data = createXMLFile('A', self.options, payment, order) # A – Authorization request
        
        # create an HTTPS request using SSL
        data_len = len(data)
        conn = createConnection(data_len, self.server, self.options, timeout=None)
        
        # send the request
        conn.send(data)
        
        # take the results
        response = conn.getresponse()
        result = xml.dom.minidom.parseString(response.read())
        
        # ProcStatus is the only element that is returned in all response scenarios
        proc_status_node = result.getElementsByTagName('ProcStatus')[0]
        proc_status_child = proc_status_node.childNodes[0]
        proc_status = proc_status_child.nodeValue
        
        if proc_status == "0":
            approval_status_node = result.getElementsByTagName('ApprovalStatus')[0]
            approval_status_child = approval_status_node.childNodes[0]
            approval_status = approval_status_child.nodeValue

            trans_node = result.getElementsByTagName('TxRefNum')[0]
            trans_child = trans_node.childNodes[0]
            trans_ref_num = trans_child.nodeValue
            
            annotation = IAnnotations(order)
            annotation[interfaces.keys.processor_txn_id] = trans_ref_num
            annotation[LAST_FOUR] = payment.credit_card[-4:]
            annotation[APPROVAL_KEY] = approval_status
            return interfaces.keys.results_success
        else:
            status_node = result.getElementsByTagName('StatusMsg')[0]
            status_child = status_node.childNodes[0]
            status_msg = status_child.nodeValue
            return status_msg

    def capture(self, order, amount):
        data = createXMLFile('AC', self.options, payment, order) #AC – Authorization and Mark for Capture
    
    def refund(self, order, amount):
        data = createXMLFile('R', self.options, payment, order) #R – Refund request

