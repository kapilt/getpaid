GetPaid Paymentech Interface
=======================================

Store Specific Processor Setting Tests
This is only for Authorization and Mark for Capture
We are doing the tests of Section A and C of 
the Orbital Certification Guidelines
--------------------------------------
STORE CREATION:
      
      >>> from getpaid.core import interfaces
      >>> from zope.app.annotation import IAttributeAnnotatable
      >>> from zope.interface import implements
      >>> class Store:
      ...    implements(interfaces.IStore, IAttributeAnnotatable)
      >>> store = Store()

LINE ITEM CREATION:
      
      >>> from getpaid.core import order, cart, item
      >>> from cPickle import loads, dumps
      >>> order_ids = []
      >>> abc = item.LineItem()
      >>> abc.name = 'abc'
      >>> abc.quantity = 1
      
      >>> def createOrderId():
      ...     order_id = str(random.randint( 2**10, 2**30 ))
      ...     while order_id in order_ids:
      ...         order_id = str(random.randint( 2**10, 2**30 ))
      ...     order_ids.append(order_id)
      ...     return order_id

PAYMENT PROCESSOR CREATION:

      >>> from getpaid.paymentech.paymentech import PaymentechAdapter
      >>> processor = PaymentechAdapter(store)
      >>> processor.options.merchant_id = "700000007587"
      >>> processor.options.terminal_id = "001"
      >>> processor.server = processor._sites['Test1']

=======================================
SECTION A: Authorization only transactions
=======================================
Generic function to test the Authorization:

      >>> from getpaid.paymentech.paymentech import createAuthorizeXMLFile
      >>> from getpaid.paymentech.paymentech import getElement
      >>> import random
      >>> from Products.PloneGetPaid.browser.checkout import BillingInfo
      >>> from datetime import date
      >>> def test_authorize(credit_card_type, credit_card_number, cc_cvc, amount, my_order):
      ...     my_cart = cart.ShoppingCart()
      ...     abc.cost = amount 
      ...     my_cart['abc'] = abc
      ...     my_order.shopping_cart = loads(dumps(my_cart))
      ...     payment_infos = BillingInfo(my_order)
      ...     payment_infos.name_on_card = "Test Cardholder"
      ...     payment_infos.phone_number = "1234567890"
      ...     payment_infos.cc_expiration = date(2009, 2, 1)
      ...     payment_infos.credit_card_type = credit_card_type
      ...     payment_infos.credit_card = credit_card_number
      ...     payment_infos.cc_cvc = cc_cvc
      ...     data = createAuthorizeXMLFile('A', processor.options, my_order, payment_infos)
      ...     return processor.process(data, timeout=None)

TEST 1:
      >>> credit_card_type = "Visa"
      >>> credit_card_number = "4788250000028291"
      >>> cc_cvc = "111"
      >>> amount = 30.00
      >>> order1 = order.Order()
      >>> order1.order_id = order_id = createOrderId()
      >>> result = test_authorize(credit_card_type, credit_card_number, cc_cvc, amount, order1)
      >>> res_order_id = getElement(result.result_resp, 'OrderID')
      >>> order_id == res_order_id
      True
      >>> res_resp_code = getElement(result.result_resp, 'RespCode')
      >>> res_resp_code == "00"
      True
      >>> res_trans_ref_num1 = result.trans_ref_num
      
TEST 2:
      >>> credit_card_type = "Visa"
      >>> credit_card_number = "4788250000028291"
      >>> cc_cvc = "222"
      >>> amount = 38.01
      >>> order2 = order.Order()
      >>> order2.order_id = order_id = createOrderId()
      >>> result = test_authorize(credit_card_type, credit_card_number, cc_cvc, amount, order2)
      >>> res_order_id = getElement(result.result_resp, 'OrderID')
      >>> order_id == res_order_id
      True
      >>> res_resp_code = getElement(result.result_resp, 'RespCode')
      >>> res_resp_code == "05"
      True
      >>> res_trans_ref_num2 = result.trans_ref_num

TEST 3:
      >>> credit_card_type = "Mastercard"
      >>> credit_card_number = "5454545454545454"
      >>> cc_cvc = "333"
      >>> amount = 41.00
      >>> order3 = order.Order()
      >>> order3.order_id = order_id = createOrderId()
      >>> result = test_authorize(credit_card_type, credit_card_number, cc_cvc, amount, order3)
      >>> res_order_id = getElement(result.result_resp, 'OrderID')
      >>> order_id == res_order_id
      True
      >>> res_resp_code = getElement(result.result_resp, 'RespCode')
      >>> res_resp_code == "00"
      True
      >>> res_trans_ref_num3 = result.trans_ref_num

TEST 4:
      >>> credit_card_type = "Mastercard"
      >>> credit_card_number = "5454545454545454"
      >>> cc_cvc = "666"
      >>> amount = 11.02
      >>> order4 = order.Order()
      >>> order4.order_id = order_id = createOrderId()
      >>> result = test_authorize(credit_card_type, credit_card_number, cc_cvc, amount, order4)
      >>> res_order_id = getElement(result.result_resp, 'OrderID')
      >>> order_id == res_order_id
      True
      >>> res_resp_code = getElement(result.result_resp, 'RespCode')
      >>> res_resp_code == "01"
      True
      >>> res_trans_ref_num4 = result.trans_ref_num

TEST 5:
      >>> credit_card_type = "American Express"
      >>> credit_card_number = "371449635398431"
      >>> cc_cvc = "1111"
      >>> amount = 1055.00
      >>> order5 = order.Order()
      >>> order5.order_id = order_id = createOrderId()
      >>> result = test_authorize(credit_card_type, credit_card_number, cc_cvc, amount, order5)
      >>> res_order_id = getElement(result.result_resp, 'OrderID')
      >>> order_id == res_order_id
      True
      >>> res_resp_code = getElement(result.result_resp, 'RespCode')
      >>> res_resp_code == "00"
      True
      >>> res_trans_ref_num5 = result.trans_ref_num
      
TEST 6:
      >>> credit_card_type = "American Express"
      >>> credit_card_number = "371449635398431"
      >>> cc_cvc = "555"
      >>> amount = 75.00
      >>> order6 = order.Order()
      >>> order6.order_id = order_id = createOrderId()
      >>> result = test_authorize(credit_card_type, credit_card_number, cc_cvc, amount, order6)
      >>> res_order_id = getElement(result.result_resp, 'OrderID')
      >>> order_id == res_order_id
      True
      >>> res_resp_code = getElement(result.result_resp, 'RespCode')
      >>> res_resp_code == "00"
      True
      >>> res_trans_ref_num6 = result.trans_ref_num
      
TEST 7:
      >>> credit_card_type = "Discover"
      >>> credit_card_number = "6011000995500000"
      >>> cc_cvc = "666"
      >>> amount = 10.00
      >>> order7 = order.Order()
      >>> order7.order_id = order_id = createOrderId()
      >>> result = test_authorize(credit_card_type, credit_card_number, cc_cvc, amount, order7)
      >>> res_order_id = getElement(result.result_resp, 'OrderID')
      >>> order_id == res_order_id
      True
      >>> res_resp_code = getElement(result.result_resp, 'RespCode')
      >>> res_resp_code == "00"
      True
      >>> res_trans_ref_num7 = result.trans_ref_num
      
TEST 8:
      >>> credit_card_type = "Discover"
      >>> credit_card_number = "6011000995500000"
      >>> cc_cvc = "444"
      >>> amount = 63.03
      >>> order8 = order.Order()
      >>> order8.order_id = order_id = createOrderId()
      >>> result = test_authorize(credit_card_type, credit_card_number, cc_cvc, amount, order8)
      >>> res_order_id = getElement(result.result_resp, 'OrderID')
      >>> order_id == res_order_id
      True
      >>> res_resp_code = getElement(result.result_resp, 'RespCode')
      >>> res_resp_code == "04"
      True
      >>> res_trans_ref_num8 = result.trans_ref_num
      
=======================================
SECTION C: Mark for Capture
=======================================
Generic function to test the Capture:

      >>> from getpaid.paymentech.paymentech import createCaptureXMLFile
      >>> def test_capture(order, trans_ref_num, amount):
      ...     data = createCaptureXMLFile(processor.options, order, trans_ref_num, amount)
      ...     return processor.process(data, timeout=None)
      
TEST A-1:
      >>> amount = 30.00
      >>> result = test_capture(order1, res_trans_ref_num1, amount)
      >>> res_resp_code = getElement(result.result_resp, 'ProcStatus')
      >>> res_resp_code == "0"
      True
      >>> res_trans_ref_num = result.trans_ref_num

TEST A-3:
      >>> amount = 41.00
      >>> result = test_capture(order3, res_trans_ref_num3, amount)
      >>> res_resp_code = getElement(result.result_resp, 'ProcStatus')
      >>> res_resp_code == "0"
      True
      >>> res_trans_ref_num = result.trans_ref_num

TEST A-5:
      >>> amount = 1055.00
      >>> result = test_capture(order5, res_trans_ref_num5, amount)
      >>> res_resp_code = getElement(result.result_resp, 'ProcStatus')
      >>> res_resp_code == "0"
      True
      >>> res_trans_ref_num = result.trans_ref_num

TEST A-7:
      >>> amount = 10.00
      >>> result = test_capture(order7, res_trans_ref_num7, amount)
      >>> res_resp_code = getElement(result.result_resp, 'ProcStatus')
      >>> res_resp_code == "0"
      True
      >>> res_trans_ref_num = result.trans_ref_num






