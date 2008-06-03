from elementtree import ElementTree as ET

class FieldModel(object):
    def __init__(self, xmlrepr):
        self.basemodel = ET.XML(xmlrepr)

    def validate(self, element, model=None, errors=None):
        """Ok, we check for:
           1) Correct tagname
           2) Correct datatype
           3) Within datalength constraint
           5) Tag present if required
           6) Tag empty or not as required
           7) Attributes present if defined and with valid data
        """
        if errors is None:
            errors = []
        if model is None:
            model = self.basemodel
        else:
            try:
                model = model.getroot()
                if model is None:
                    return [{'RootNode' : 'There must be a root node to be a valid XML document'}]
            except AttributeError, e:
                pass
        errors.append({})
        err = errors[-1]
        if model.tag != element.tag:
            err['tag'] = "Element tag '%s' does not match model tag '%s'" \
                         % (element.tag, model.tag)
        if model.get('data', False) == "required":
            if not element.text:
                err['data'] = "Element tag '%s' requires data" % element.tag
        maxdata = model.get('maxdata', False)
        if maxdata is not False:
            maxdata = int(maxdata)
            if element.text is not None and len(element.text.strip()) > maxdata:
                err['maxdata'] = "Element tag '%s' has too much data: %d, when the maximum allowed is: %d)" % (element.tag, len(element.text), maxdata)
        if model.get('datavalues', False):
            datavalues = model.get('datavalues').split()
            if element.text not in datavalues:
                err['datavalues'] = "Element tag '%s' requires its data to be only one of '%s'" % (element.tag, datavalues)
        if model.get('datatype', False):
            datatype = model.get('datatype')
            if datatype == 'str':
                # no-op (it's XML, duh!)
                pass
            elif datatype == 'int':
                try:
                    int(element.text)
                    if model.get('maxval', False):
                        if int(maxval) < int(element.tex):
                            err['maxval'] = "Element tag '%s' only allows a maximum value of '%d'" % (element.tag, model.get('maxval'))
                except ValueError, e:
                    err['datatype'] = "Element tag '%s' requires its data to be an integer" % element.tag
            elif datatype == 'float':
                try:
                    float(element.text)
                    maxval =  model.get('maxval', False)
                    if maxval:
                        if float(maxval) < float(element.text):
                            err['maxval'] = "Element tag '%s' only allows a maximum value of '%f'" % (element.tag, model.get('maxval'))
                except ValueError, e:
                    err['datatype'] = "Element tag '%s' requires its data to be a float" % element.tag
        if model.get('attributes', False):
            attrs = model.get('attributes').split(';')
            for attr in attrs:
                attrname, attrvals = attr.split()
                attrvals = attrvals.split('|')
                if element.get(attrname, False):
                    if element.get(attrname) not in attrvals:
                        err.setdefault('attributes', []).append("Element tag '%s' requires an attribute named '%s' with a value of only one of '%s'" % (element.tag, attrname, attrvals))
                else:
                        err.setdefault('attributes', []).append("Element tag '%s' requires an attribute named '%s' with a value of only one of '%s'" % (element.tag, attrname, attrvals))
        children = model.getchildren()
        for child in children:
            elementchild = element.find(child.tag)
            if child.get('required', False) == 'required':
                if elementchild is None:
                    err.setdefault('required', []).append("Element tag '%s' requires a child with tag '%s'" % (element.tag, child.tag))
            if elementchild is not None:
                state_validate, errors = self.validate(elementchild, child, errors)
        all_errors = [error for error in errors if error]
        return all_errors and (False, all_errors) or (True, all_errors)

class BaseMessage:

    def __init__(self, xmlstate=None, validstate=True):
        self._model = FieldModel(self.modeltext)
        if xmlstate is not None:
            self._state = ET.ElementTree(ET.XML(xmlstate))
            # If state is being pre-supplied, then it ought to validate,
            # unless the caller has specifically asserted that it does not:
            if validstate:
                self.state_validate()
        else:
            # No root node!
            self._state = ET.ElementTree()

    def state_validate(self):
        return self._model.validate(self._state.getroot())

    def setRoot(self, node_name, node_attrs={}, clear_all=False):
        # Total Wart.
        try:
            root = self._findElement('/')
        except AssertionError, e:
            # ElementTree.py #647 asserts that _root is not None
            root = None
        newroot = ET.Element(node_name, node_attrs)
        children = []
        if not clear_all and root:
            children = root.getchildren()
        for child in children:
            newroot.append(child)
        self._state = ET.ElementTree(newroot)

    def getRoot(self):
        return self.getNode('', '')

    def addNode(self, node_path, node_name, node_attrs={}, node_data=''):
        parent = self._findElement(node_path)
        # MUSTMUSTMUST specifically test against 'None':
        if parent is not None:
            sub = ET.SubElement(parent, node_name, node_attrs)
            sub.text = unicode(node_data)
            return sub
        else:
            return None

    def delNode(self, node_path, node_name):
        # No, you may not delete the root node. Set a new
        # one with self.setRoot(), instead.
        parent = self._findElement(node_path)
        if parent:
            return parent.remove(parent.find(node_name))
        else:
            return False

    def getNode(self, node_path, node_name):
        return self._findElement('/'.join((node_path, node_name)))

    def _findElement(self, path):
        return self._state.find(path)

    def generateXML(self):
        return ET.tostring(self.getRoot())

    def __str__(self):
        return self.generateXML()

    def __repr__(self):
        return """%s(\"\"\"%s\"\"\")""" % (self.__class__, self.__str__())

    def __len__(self):
        return len(self.__str__())

class InitialRequest(BaseMessage):
    """The initial transaction setup request
    """
    modeltext = """
<GenerateRequest required="required" maxdata="0">
    <PxPayUserId datatype="str" maxdata="32" required="required" />
    <PxPayKey datatype="str" maxdata="64" required="required" />
    <AmountInput datatype="float" maxdata="13" maxval="99999.99" required="required" />
    <BillingId datatype="str" maxdata="32" />
    <CurrencyInput datatype="str" maxdata="4" datavalues="CAD CHF EUR FRF GBP HKD JPY NZD SGD USD ZAR AUD WST VUV TOP SBD PNG MYR KWD FJD" required="required" />
    <DpsBillingId datatype="str" maxdata="16" />
    <DpsTxnRef datatype="str" maxdata="16" />
    <EmailAddress datatype="str" maxdata="255" />
    <EnableAddBillCard datatype="int" datavalues="0 1" maxdata="1" />
    <MerchantReference datatype="str" maxdata="64" required="required" />
    <TxnData1 datatype="str" maxdata="255" />
    <TxnData2 datatype="str" maxdata="255" />
    <TxnData3 datatype="str" maxdata="255" />
    <TxnType datatype="str" datavalues="Auth Complete Purchase" />
    <TxnId datatype="str" maxdata="16" />
    <UrlFail datatype="str" maxdata="255" required="required" />
    <UrlSuccess datatype="str" maxdata="255" required="required" />
</GenerateRequest>
"""


class InitialResponse(BaseMessage):
    """The response from the inital transaction setup request
    see: http://www.dps.co.nz/technical_resources/ecommerce_hosted/pxpay.html#Request
    """
    modeltext = """
<Request required="required" maxdata="0" attributes="valid 0|1" valid="1">
    <URI required="required" datatype="str" />
</Request>
"""
    @property
    def is_valid_response(self):
        """
        Does the current data indicate the pxpay Request to be valid?
        """
        return self.getRoot().get('valid') == '1'

    @property
    def request_url(self):
        """
        Return the uri we need to redirect the user to
        """
        return self.getNode('/', 'URI').text

class ReturnRequest(BaseMessage):
    """
    When the user is redirected back to our site after they have
    entered payment details, we receive a 'request' parameter that has
    an encrypted response that we use to ask pxpay for details about
    the success or failure of the users payment submission.

    see http://www.dps.co.nz/technical_resources/ecommerce_hosted/pxpay.html#ProcessResponse
    """
    modeltext = """
<ProcessResponse required="required" maxdata="0">
    <PxPayUserId datatype="str" maxdata="32" required="required" />
    <PxPayKey datatype="str" maxdata="64" required="required" />
    <Response required="required" datatype="str" />
</ProcessResponse>
"""
class ReturnResponse(BaseMessage):
    """The response from DPS from submitting a
       ReturnRequest(ProcessResponse in pxpay speak) indicating
       whether the transaction was successful or not
    """
    modeltext = """
<Response required="required" maxdata="0" attributes="valid 0|1" valid="1">
    <Success required="required" datatype="int" maxdata="1" datavalues="0 1" />
    <TxnType required="required" datatype="str" datavalues="Auth Complete Purchase" />
    <CurrencyInput datatype="str" maxdata="4" datavalues="CAD CHF EUR FRF GBP HKD JPY NZD SGD USD ZAR AUD WST VUV TOP SBD PNG MYR KWD FJD" required="required" />
    <MerchantReference datatype="str" maxdata="64" required="required" />
    <TxnData1 required="required" datatype="str" maxdata="255" />
    <TxnData2 required="required" datatype="str" maxdata="255" />
    <TxnData3 required="required" datatype="str" maxdata="255" />
    <AuthCode required="required" datatype="str" maxdata="22" />
    <CardName required="required" datatype="str" maxdata="16" />
    <TxnId datatype="str" maxdata="16" />
    <EmailAddress datatype="str" maxdata="255" />
    <DpsTxnRef datatype="str" maxdata="16" />
    <BillingId datatype="str" maxdata="32" />
    <DpsBillingId datatype="str" maxdata="16" />
    <CardHolderName datatype="str" maxdata="64" />
    <AmountSettlement datatype="float" maxdata="13" maxval="99999.99" required="required" />
    <CurrencySettlement datatype="str" maxdata="4" datavalues="CAD CHF EUR FRF GBP HKD JPY NZD SGD USD ZAR AUD WST VUV TOP SBD PNG MYR KWD FJD" required="required" />
    <ResponseText datatype="str" maxdata="32" />
</Response>
"""

    @property
    def is_valid_response(self):
        """
        Does the current data indicate the pxpay Request to be valid?
        """
        return self.getRoot().get('valid') == '1'

    @property
    def transaction_successful(self):
        return self.getNode('/', 'Success').text == '1'

    @property
    def transaction_type(self):
        return self.getNode('/', 'TxnType').text

    @property
    def transaction_currencyinput(self):
        return self.getNode('/', 'CurrencyInput').text

    @property
    def transaction_merchantreference(self):
        return self.getNode('/', 'MerchantReference').text

    @property
    def transaction_txn_data_1(self):
        return self.getNode('/', 'TxnData1').text

    @property
    def transaction_txn_data_2(self):
        return self.getNode('/', 'TxnData2').text

    @property
    def transaction_txn_data_3(self):
        return self.getNode('/', 'TxnData3').text

    @property
    def transaction_authcode(self):
        return self.getNode('/', 'AuthCode').text

    @property
    def transaction_cardname(self):
        return self.getNode('/', 'CardName').text

    @property
    def transaction_currencyname(self):
        return self.getNode('/', 'CurrencyName').text

    @property
    def transaction_id(self):
        return self.getNode('/', 'TxnId').text

    @property
    def transaction_email_address(self):
        return self.getNode('/', 'EmailAddress').text

    @property
    def transaction_dps_reference(self):
        return self.getNode('/', 'DpsTxnRef').text

    @property
    def transaction_billing_id(self):
        return self.getNode('/', 'BillingId').text

    @property
    def transaction_dps_billing_id(self):
        return self.getNode('/', 'DpsBillingId').text

    @property
    def transaction_cardholder_name(self):
        return self.getNode('/', 'CardHolderName').text

    @property
    def transaction_amountsettlement(self):
        return float(self.getNode('/', 'AmountSettlement').text)

    @property
    def transaction_currency_settlement(self):
        return self.getNode('/', 'CurrencySettlement').text

    @property
    def transaction_response_text(self):
        return self.getNode('/', 'ResponseText').text

if __name__ == '__main__':
    # Do selftest of embedded datamodel:
    InitialRequest()
    InitialResponse()
    ReturnRequest()
    x = ReturnResponse()
    x.setRoot('Response', {'valid' : '1'})
    x.addNode('/', 'Success', node_data='1')
    x.state_validate()
    x.delNode('/', 'Success')
    x.addNode('/', 'Success', node_data='2')
    print x.state_validate()
