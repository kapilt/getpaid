import logging
from zc import ssl
from zope.component import adapts
from zope.interface import implements

from getpaid.pxpay import parser
from getpaid.pxpay.config import *
from getpaid.pxpay.interfaces import IPXPayWebInterfaceGateway, \
     IPXPayStandardOptions

log = logging.getLogger('getpaid.pxpay')

class PXPayWebInterfaceGateway( object ):

    implements(IPXPayWebInterfaceGateway)
    adapts(IPXPayStandardOptions)

    offline_testmode = False
    offline_testdata = {'returnresponse':'payment-accepted',
                        'initialresponse':'valid'}

    def __init__(self, context):
        self.context = context
        self.server_type = context.PxPayServerType

    def set_offline_testmode(self, value, data={}):
        self.offline_testmode = value
        self.offline_testdata.update(data)

    def send_message(self, message, timeout=None):
        """
        Creates the HTTPS/POST connection to the PaymentExpress PXPay
        server sends an xml message and returns the response body -
        which is usually another XML message.
        """
        if self.offline_testmode:
            # hand off to an offline test mode
            return self.send_message_offline_testmode(message)

        server = SERVER_DETAILS.get(self.server_type, {})
        server_name = server.get('host')
        server_path = server.get('path')
        conn = ssl.HTTPSConnection(server_name, timeout)

        # setup the HEADERS
        conn.putrequest('POST', server_path)
        conn.putheader('Content-Type', 'application/x-www-form-urlencoded')
        conn.putheader('Content-Length', len(message))
        conn.endheaders()

        log.info("About to send: %s" % message)
        conn.send(message.generateXML())
        return conn.getresponse().read()


    def send_message_offline_testmode(self, message):

        if isinstance(message, parser.InitialRequest):
            if self.offline_testdata['initialresponse'] == 'valid':
                return initialresponse_test_data
        if isinstance(message, parser.ReturnRequest):
            if self.offline_testdata['returnresponse'] == 'payment-accepted':
                return returnresponse_test_data_payment_accepted
            if self.offline_testdata['returnresponse'] == 'payment-declined':
                return returnresponse_test_data_payment_declined


initialresponse_test_data = """<Request valid="1"><URI>https://www.paymentexpress.com/pxpay/pxpay.aspx?userid=TestAccount&amp;request=e88cd9f2f6f301c712ae2106ab2b6137d86e954d2163d1042f73cce130b2c 88c06daaa226629644dc741b16deb77ca14ce4c59db84929eb0280837b92bd2ffec 2fae0b9173c066dab48a0b6d2c0f1006d4d26a8c75269196cc540451030958d257c1 86f587ad92cfa7472b101ef72e45cda3bf905862c2bf58fc214870292d6646f7c4ad 02a75e42fc64839fc50cea8c17f65c6a9b83b9c124e2f20844b63538e13a8cff17ec d8f165aee525632fd3661b591626f5fb77725ade21648fed94553f43bfa69acf3557 0ff8fdcbaf8a13a3fa7deb244017e41749e652a3549a5dbe20c6c3a7a66aa5901e3f 87150f7fc</URI></Request>"""


returnresponse_test_data_payment_accepted = """<Response valid="1"><Success>1</Success><TxnType>Purchase</TxnType><CurrencyInput>NZD</CurrencyInput><MerchantReference>Test Transaction</MerchantReference><TxnData1>28 Grange Rd</TxnData1><TxnData2>Auckland</TxnData2><TxnData3>NZ</TxnData3><AuthCode>053646</AuthCode><CardName>Visa</CardName><CurrencyName>NZD</CurrencyName><TxnId>123456789</TxnId><EmailAddress></EmailAddress><DpsTxnRef>000000040119429b</DpsTxnRef><BillingId></BillingId><DpsBillingId></DpsBillingId><CardHolderName>TEST</CardHolderName><AmountSettlement>2.06</AmountSettlement><CurrencySettlement>NZD</CurrencySettlement><ResponseText>APPROVED</ResponseText></Response>"""

returnresponse_test_data_payment_declined = """<Response valid="1"><Success>0</Success><TxnType>Purchase</TxnType><CurrencyInput>NZD</CurrencyInput><MerchantReference>None</MerchantReference><TxnData1 /><TxnData2 /><TxnData3 /><AuthCode /><CardName>Visa</CardName><CardHolderName>HFM TEST</CardHolderName><CardNumber>411111........11</CardNumber><DateExpiry>0908</DateExpiry><ClientInfo>125.238.25.95</ClientInfo><TxnId>234567891</TxnId><EmailAddress /><DpsTxnRef>0000000404c5bee6</DpsTxnRef><BillingId /><DpsBillingId /><AmountSettlement>4.76</AmountSettlement><CurrencySettlement>NZD</CurrencySettlement><TxnMac>BD43E619</TxnMac><ResponseText>DECLINED</ResponseText></Response>"""
