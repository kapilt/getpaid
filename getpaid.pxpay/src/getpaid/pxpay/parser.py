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



class BaseMessage(object):
    """
    A base class for pxpay xml messages

    >>> from getpaid.pxpay import parser
    >>> from elementtree import ElementTree as ET
    >>> message = parser.BaseMessage()
    >>> print message.generateXML()
    <none />
    >>> message.setRoot('top', {'a':'1','b':'2'})
    >>> print message.generateXML()
    <top a="1" b="2" />
    >>> message.addNode('/','bling')
    <Element bling at ...>
    >>> print message.generateXML()
    <top a="1" b="2"><bling /></top>
    >>> message.setRoot('newtop')
    >>> print message.generateXML()
    <newtop a="1" b="2"><bling /></newtop>
    >>> print message.getRoot().tag
    newtop
    """

    modeltext = "<none/>"

    def __init__(self, xmlstate=None, validatestate=True):
        self._model = FieldModel(self.modeltext)
        if xmlstate is not None:
            self._state = ET.ElementTree(ET.XML(xmlstate))
            # If state is being pre-supplied, then it ought to validate,
            # unless the caller has specifically asserted that it does not:
            if validatestate:
                self.state_validate()
        else:
            self._state = ET.ElementTree(ET.Element('none'))

    def state_validate(self):
        return self._model.validate(self._state.getroot())

    def setRoot(self, node_name, node_attrs=None):
        root = self._state.getroot()
        root.tag = node_name
        if node_attrs:
            root.attrib.update(node_attrs)

    def getRoot(self):
        return self._state.getroot()

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

def to_float(value):
    return float(value)

class MessageProperty(object):
    """
    Computed attributes that access or set the underlying values in
    the message xml model.

    We can do this since all messages are flat, i.e. they have only
    one depth of children and all values are text nodes.

    >>> from getpaid.pxpay import parser
    >>> class MessageModel(parser.BaseMessage):
    ...
    ...     p1 = parser.MessageProperty('bling')
    ...     p2 = parser.MessageProperty('blong')
    ...     p3 = parser.MessageProperty('number',
    ...                                 transform=parser.to_float)
    >>> message = MessageModel()
    >>> message.setRoot('top')
    >>> print message.generateXML()
    <top />
    >>> message.p1 = 'hello'
    >>> message.p2 = 'there'
    >>> message.generateXML()
    '<top><bling>hello</bling><blong>there</blong></top>'
    >>> print message.p1
    hello
    >>> print message.p2
    there
    >>> message.p1 = 'over'
    >>> print message.p1
    over
    >>> message.p3 = '1'
    >>> message.generateXML()
    '<top><bling>over</bling><blong>there</blong><number>1</number></top>'
    >>> print message.p3
    1.0
    >>> type(message.p3)
    <type 'float'>
    """
    def __init__(self, nodename, parentpath='/', transform=None):
        self._nodename = nodename
        self._parentpath = parentpath
        self._transform = transform

    def __get__(self, inst, klass):
        if inst is None:
            return self
        value = inst.getNode(self._parentpath, self._nodename).text
        if self._transform:
            return self._transform(value)
        else:
            return value

    def __set__(self, inst, value):
        node = inst.getNode(self._parentpath, self._nodename)
        if node is not None:
            node.text = unicode(value)
            return
        else:
            inst.addNode(self._parentpath, self._nodename, node_data=value)



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
    pxpay_user_id = MessageProperty('PxPayUserId')
    pxpay_key = MessageProperty('PxPayKey')
    amount_input = MessageProperty('AmountInput')
    currency_input = MessageProperty('CurrencyInput')
    dps_billing_id =  MessageProperty('DpsBillingId')
    dps_transaction_reference = MessageProperty('DpsTxnRef')
    email_address = MessageProperty('EmailAddress')
    enable_add_bill_card = MessageProperty('EnableAddBillCard')
    merchant_reference = MessageProperty('MerchantReference')
    transaction_data_1 = MessageProperty('TxnData1')
    transaction_data_2 = MessageProperty('TxnData2')
    transaction_data_3 = MessageProperty('TxnData3')
    transaction_type = MessageProperty('TxnType')
    transaction_id = MessageProperty('TxnId')
    url_failure = MessageProperty('UrlFail')
    url_success = MessageProperty('UrlSuccess')

    def __init__(self, data=None):
        super(InitialRequest, self).__init__(data)
        if not data:
            self.setRoot('GenerateRequest')



class InitialResponse(BaseMessage):
    """The response from the inital transaction setup request
    see: http://www.dps.co.nz/technical_resources/ecommerce_hosted/pxpay.html#Request
    """
    modeltext = """
<Request required="required" maxdata="0" attributes="valid 0|1" valid="1">
    <URI required="required" datatype="str" />
</Request>
"""

    uri = MessageProperty('URI')

    def __init__(self, data=None):
        super(InitialResponse, self).__init__(data)
        if not data:
            self.setRoot('Request')

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
        return self.uri

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

    pxpay_user_id = MessageProperty('PxPayUserId')
    pxpay_key = MessageProperty('PxPayKey')
    response = MessageProperty('Response')

    def __init__(self, data=None):
        super(ReturnRequest, self).__init__(data)
        if not data:
            self.setRoot('ProcessResponse')


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
    <CardNumber datatype="str" maxdata="20" />
    <AmountSettlement datatype="float" maxdata="13" maxval="99999.99" required="required" />
    <CurrencySettlement datatype="str" maxdata="4" datavalues="CAD CHF EUR FRF GBP HKD JPY NZD SGD USD ZAR AUD WST VUV TOP SBD PNG MYR KWD FJD" required="required" />
    <ResponseText datatype="str" maxdata="32" />
</Response>
"""
    success = MessageProperty('Success')
    transaction_type = MessageProperty('TxnType')
    transaction_currencyinput = MessageProperty('CurrencyInput')
    transaction_merchantreference = MessageProperty('MerchantReference')
    transaction_txn_data_1 = MessageProperty('TxnData1')
    transaction_txn_data_2 = MessageProperty('TxnData2')
    transaction_txn_data_3 = MessageProperty('TxnData3')
    transaction_authcode = MessageProperty('AuthCode')
    transaction_cardname = MessageProperty('CardName')
    transaction_currencyname = MessageProperty('CurrencyName')
    transaction_id = MessageProperty('TxnId')
    transaction_email_address = MessageProperty('EmailAddress')
    transaction_dps_reference = MessageProperty('DpsTxnRef')
    transaction_billing_id = MessageProperty('BillingId')
    transaction_dps_billing_id = MessageProperty('DpsBillingId')
    transaction_cardholder_name = MessageProperty('CardHolderName')
    transaction_card_number = MessageProperty('CardNumber')
    transaction_amountsettlement = MessageProperty('AmountSettlement',
                                                   transform=to_float)
    transaction_currency_settlement = MessageProperty('CurrencySettlement')
    transaction_response_text = MessageProperty('ResponseText')

    def __init__(self, data=None):
        super(ReturnResponse, self).__init__(data)
        if not data:
            self.setRoot('Response')

    @property
    def is_valid_response(self):
        """
        Does the current data indicate the pxpay Request to be valid?
        """
        return self.getRoot().get('valid') == '1'

    @property
    def transaction_successful(self):
        """
        Returns whether DPS authorised this transaction.
        Beware users using the Test CC number against your Production site!
        """
        return self.success == '1'


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
