from exceptions import Exception

from zope.component import getUtility

from getpaid.core.interfaces import IOrderManager, IShoppingCartUtility, ILineContainerTotals
from getpaid.pxpay.config import *
from getpaid.pxpay.interfaces import IPXPayStandardOptions
from getpaid.pxpay.parser import InitialRequest, InitialResponse, ReturnRequest, ReturnResponse
import zc.ssl

from Products.CMFCore.interfaces import IURLTool, IMembershipTool
from Products.CMFPlone.utils import getToolByName
from Products.Five import BrowserView
from Products.PloneGetPaid.interfaces import IGetPaidManagementOptions
from Products.PloneGetPaid.browser.checkout import OrderIdManagerMixin

import zLOG

class InvalidResponseMessageException(Exception):
    pass

class InvalidRequestMessageException(Exception):
    pass

class PXPayCheckoutPayment(OrderIdManagerMixin, BrowserView):
    """
    This is substantially different from the normal GetPaid CheckoutWizard.
    Our checkout steps:
    1) Setup the transaction with PXPay server (XML conversation)
    2) Send the user offsite to the URL that PXPay server supplies
    3) Wait for the user to return with auth key
    4) Talk to PXPay server to get auth key validated and transaction result returned
    TODO: step 5 ------>
    5) Put returned data into all the usual format / places that GetPaid expects
    """

    def __call__( self ):
        options = IPXPayStandardOptions(self.context)
        if not self.checkShoppingCart():
            # Do we really want to return None here??
            return
        if not self.checkAuthenticated():
            # Or here??
            return
        if self.request.get('result', False):
            # The user is returning from a transaction validation
            success, errors = self.finaliseTransaction()
            #TODO: At this point we need to stuff data into the correct places
            #      that GetPaid expects... For now, just stub it out :)
            if success:
                # Hooray, they paid :)
                return "Thanks for paying"
            else:
                return "Darn, no $$"
        else:
            success, redir = self.setupTransaction()
            if success:
                self.request.RESPONSE.redirect(redir)
            else:
                # Meh. Need to wire this up to some sort of custom error screen.
                # Probably there's something, somewhere in GetPaid already that
                # fits the bill... Any takers?
                raise "CrappyError"

    def checkShoppingCart(self):
        cart = getUtility(IShoppingCartUtility).get(self.context)
        if cart is None or not len(cart):
            self.request.response.redirect('@@empty-cart')
            return False
        return True

    def checkAuthenticated(self):
        membership = getToolByName(self.context, 'portal_membership')
        if membership.isAnonymousUser():
            portal = getToolByName(self.context, 'portal_url').getPortalObject()
            if IGetPaidManagementOptions(portal).allow_anonymous_checkout:
                return True
            self.request.response.redirect('login_form?came_from=@@getpaid-checkout-wizard')
            return False
        return True

    def setupTransaction(self, retry=True):
        options = IPXPayStandardOptions(self.context)
        cart = getUtility(IShoppingCartUtility).get(self.context)
        initialRequest = InitialRequest()
        initialRequest.setRoot('GenerateRequest')
        initialRequest.addNode('/', 'PxPayUserId', node_data=options.PxPayUserId)
        initialRequest.addNode('/', 'PxPayKey', node_data=options.PxPayKey)
        initialRequest.addNode('/', 'AmountInput', node_data=ILineContainerTotals(cart).getTotalPrice())
        initialRequest.addNode('/', 'CurrencyInput', node_data=options.PxPaySiteCurrency)
        initialRequest.addNode('/', 'MerchantReference', node_data="Test Transaction")
        initialRequest.addNode('/', 'TxnType', node_data="Purchase")
        initialRequest.addNode('/', 'TxnId', node_data=self.getOrderId())
        initialRequest.addNode('/', 'UrlFail', node_data=self.context.portal_url()+'/@@getpaid-checkout-wizard')
        initialRequest.addNode('/', 'UrlSuccess', node_data=self.context.portal_url()+'/@@getpaid-checkout-wizard')
        state_valid, errors =  initialRequest.state_validate()
        if state_valid:
            webresponse = sendMessage(options.PxPayServerType, initialRequest.generateXML())
            zLOG.LOG("setupTransaction", zLOG.INFO, webresponse.reason)
            data = webresponse.read()
            zLOG.LOG("setupTransaction", zLOG.INFO, data)
            if webresponse.reason == 'OK':
                # 200 OK
                initialResponse = InitialResponse(data)
                state_valid, errors = initialResponse.state_validate()
                zLOG.LOG("setupTransaction", zLOG.INFO, "Errors: %s" % errors)
                if state_valid:
                    zLOG.LOG("setupTransaction", zLOG.INFO, "State valid")
                    # Find out if our setup request was accepted, and then return the redirect URI: 
                    valid = initialResponse.getRoot().get('valid', '0')
                    # No, we're not doing any clever marshalling at this stage:
                    if valid == '1':
                        return (True, initialResponse.getNode('/', 'URI').text)
                else:
                    zLOG.LOG("setupTransaction", zLOG.INFO, "State of return message wasn't valid? %s" % errors)
        # Policy: retry once if we make it here?
        if retry:
            return self.setupTransaction(retry=False)
        else:
            return (False, '')

    def finaliseTransaction(self, retry=True):
        options = IPXPayStandardOptions(self.context)
        cart = getUtility(IShoppingCartUtility).get(self.context)
        returnRequest = ReturnRequest()
        returnRequest.setRoot('ProcessResponse')
        returnRequest.addNode('/', 'PxPayUserId', node_data=options.PxPayUserId)
        returnRequest.addNode('/', 'PxPayKey', node_data=options.PxPayKey)
        returnRequest.addNode('/', 'Response',  node_data=self.request.get('result', ''))
        state_valid, errors = returnRequest.state_validate()
        if state_valid:
            webresponse = sendMessage(options.PxPayServerType, returnRequest.generateXML())
            zLOG.LOG("finaliseTransaction", zLOG.INFO, webresponse.reason)
            data = webresponse.read()
            zLOG.LOG("finaliseTransaction", zLOG.INFO, data)
            if webresponse.reason == 'OK':
                # 200 OK
                returnResponse = ReturnResponse(data)
                state_valid, errors = returnResponse.state_validate()
                if state_valid:
                    valid = returnResponse.getRoot().get('valid', '0')
                    if valid == '1':
                        # Ok, so the server <3 our message, but did the payment go through?
                        if returnResponse.getNode('/', 'Success').text == '0':
                            # FAILURE, suck.
                            return (False, returnResponse)
                        else:
                            # Apparently all successful.
                            # One last check. This protects us from one type of fraud, which the
                            # the PXPay interface effectively exposes us to, otherwise...
                            if returnResponse.getNode('/', 'CardNumber').text == RETURNED_TEST_CARD_NUMBER:
                                # Someone has used the Test CC number...
                                if options.PxPayServerType != TEST_SERVER_TYPE:
                                    # ...and has attempted to defraud us.
                                    zLOG.LOG("finaliseTransaction", zLOG.INFO, "FRAUD attempt - use of Test CC number in non-test environment: '%s'" % returnResponse)
                                    return (False, returnResponse)
                            # Hooray, they paid! :-D
                            return (True, returnResponse)
                else:
                    zLOG.LOG("finaliseTransaction", zLOG.INFO, "State of return message wasn't valid? %s" % errors)
        # Policy: retry once if we make it here?
        if retry:
            return self.finaliseTransaction(retry=False)
        else:
            return (False, '')

class ValidatePaymentParameters(object):

    def getTransactionResult(self):
        """
        Take the 'Request' parameter value from self.REQUEST and then go
        talk to PaymentExpress about whether the transaction succeeded or not.
        """
        options = IPXPayStandardOptions(self.context)
        requestParam = self.request.get('Request', False)
        if requestParam is False:
            return requestParam
        return dir(self.getCart())
        requestQuery = ReturnRequest()
        requestQuery.setRoot('ProcessResponse')
        requestQuery.addNode('/', 'PxPayUserId', node_data=options.PxPayUserId)
        requestQuery.addNode('/', 'PxPayKey', node_data=options.PxPayKey)
        requestQuery.addNode('/', 'Response', node_data=requestParam)
        state_valid, errors =  requestQuery.state_validate()
        if state_valid:
            response = sendMessage(server_url, requestQuery.generateXML())
            return response
            requestResponse = ReturnResponse(response)
            state_valid, errors = requestResponse.state_validate()
            if state_valid:
                # Extract the actual data now.
                pass
            else:
                # More serious pukage - retry?
                raise InvalidResponseMessageException("Received invalid response message, the errors were: %s" % errors)
        else:
            # Serious pukage
            raise InvalidRequestMessageException("Generated an invalid request message, the errors were: %s" % errors)


    def extractSuccessFail(self, responsemessage):
        state_valid, errors = responsemessage.state_validate()
        if not state_valid:
            # No Mercy:
            raise InvalidResponseMessageException("Received an invalid response message, the errors were: %s" % errors)
        valid = responsemessage.getRoot().get('valid')
        if valid == '1':
            valid = True
        else:
            valid = False
        success = responsemessage.getNode('/', 'Success').text
        if success == '0':
            success = True
        else:
            success = False

def sendMessage(server_type, message, timeout=None):
    """
    Creates the HTTPS/POST connection to the PaymentExpress PXPay server
    """
    this_server = SERVER_DETAILS.get(server_type, {})
    server_name = this_server.get('host', 'localhost')
    server_path = this_server.get('path', '/@@getpaid-checkout-wizard')
    conn = zc.ssl.HTTPSConnection(server_name, timeout)

    # setup the HEADERS
    conn.putrequest('POST', server_path)
    conn.putheader('Content-Type', 'application/x-www-form-urlencoded')
    conn.putheader('Content-Length', len(message))
    conn.endheaders()

    zLOG.LOG("sendMessage", zLOG.INFO, "About to send: %s" % message)
    conn.send(message)
    return conn.getresponse()
