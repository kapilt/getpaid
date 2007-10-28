"""
$Id$
"""

from zope.interface import Interface, Attribute, classImplements
from zope import schema
try:
    from zope.component.interfaces import IObjectEvent
except ImportError:
    # BBB for Zope 2.9
    from zope.app.event.interfaces import IObjectEvent
from zope.app.container.interfaces import IContainer
from zope.schema.interfaces import ITextLine
from zope.schema.vocabulary import SimpleVocabulary
from fields import PhoneNumber, CreditCardNumber
from zope.i18nmessageid import MessageFactory
_ = MessageFactory('getpaid')


#################################
# Where to Buy Stuff

class IStore( Interface ):
    """ represents a getpaid installation, should be a local site w/ getpaid local components installed
    """

class IPersistentOptions( Interface ):
    """
    a base interface that our persistent option annotation settings,
    can adapt to. specific schemas that want to have context stored
    annotation values should subclass from this interface, so they
    use adapation to get access to persistent settings. for example,
    settings = IMySettings(context)
    """

class IStoreSettings( IPersistentOptions ):
    """ minimum configuration schema for a store, pgp product has examples of many more
    """
    shipping_method = schema.Choice( title = _(u"Shipping Method"),
                                     required = True,
                                     source = "getpaid.shipping_methods" )

    store_name = schema.TextLine( title = _(u"Store/Organization Name"),
                                  required = True,
                                  default = u""
                                )
    

#################################
# Stuff To Buy

class IPayable( Interface ):
    """
    An object which can be paid for. Payables are typically gotten via adapation between
    a context and the request, to allow for pricing / display customization on a user
    basis.
    """
    
    made_payable_by = schema.TextLine(
        title = _(u"Made Payable By"),
        readonly = True,
        required = False
        )
    
    product_code = schema.TextLine( title = _(u"Product Code"),
                        description=_(u"An organization's unique product identifier (not required since shopping cart uses content UID internally)"),
                        required=False
                        )
    price = schema.Float( title = _(u"Price"), required=True)

class IDonationContent( IPayable ):
    """ Donation
    """
    donation_text = schema.TextLine( title = _(u"Donation Description"),
                        description=_(u"Very brief 50 character text (that shows up in portlet)"),
                        required=True,
                        max_length=50)

class ISubscription( IPayable ):
    """ Subscription
    """

class IBuyableContent( IPayable ):
    """ Purchasable Content Delivered Virtually
    """
    
class IPremiumContent( Interface ):
    """ Premium Content for Subscriptions
    """

class IPhysicalPayable( IPayable ):
    """
    """

class IShippableContent( IPayable ):
    """ Shippable Content
    """
    dimensions = schema.TextLine( title = _(u"Dimensions"))
    sku = schema.TextLine( title = _(u"Product SKU"))
    
    def getShipWeight( self ):
        """ Shipping Weight
        """

#################################
# Events

class IPayableCreationEvent( IObjectEvent ):
    """ sent out when a payable is created
    """

    payable = Attribute("object implementing payable interface")    
    payable_interface = Attribute("payable interface the object implements")


class IPayableAuditLog( Interface ):
    """ ordered container of changes, most recent first, hook on events.
    """


#################################
# Stuff to Process Payments

class IPaymentProcessor( Interface ):
    """ A Payment Processor

    a processor can keep processor specific information on an orders
    annotations.
    """ 

    def authorize( order, payment_information ):
        """
        authorize an order, using payment information.
        """

    def capture( order, amount ):
        """
        capture amount from order.
        """

    def refund( order, amount ):
        """
        reset
        """
    
class IRecurringPaymentProcessor( IPaymentProcessor ):
    """ a payment processor that can handle recurring line items
    """
    
class IPaymentProcessorOptions( Interface ):
    """ Options for a Processor

    """

class IWorkflowPaymentProcessorIntegration( Interface ):
    """
    integrates an order's workflow with a payment processor
    """

    def __call__( order_workflow_event ):
        """
        process a workflow event
        """
    
#################################
# Info needed for payment processing

    
class ILineItem( Interface ):
    """
    An Item in a Cart
    """
    item_id = schema.TextLine( title = _(u"Unique Item Id"))
    name = schema.TextLine(title = _(u"Name"))
    description = schema.TextLine( title = _(u"Description"))
    cost = schema.Float( title = _(u"Cost"))
    quantity = schema.Int( title = _(u"Quantity"))


class ILineItemFactory( Interface ):
    """ encapsulation of creating and adding a line item to a line item container
    from a payable. sort of like an adding view
    """
    
    def create( payable ):
        """
        create a payable from a line item
        """

class ILineItemContainer( IContainer ):
    """ A container for line items
    """
    
class IPayableLineItem( ILineItem ):
    """
    A line item linked to a payable
    """

    uid = schema.ASCIILine( title = _(u"Integer Id for a Product") )

    def resolve( ):
        """ return the payable object, or None if can't be found.
        """

class IRecurringLineItem( IPayableLineItem ):

    period = schema.Int( title = _(u"Period as a timedelta"))
    

class IGiftCertificate( ILineItem ):
    """ A Gift Certificate
    """

#################################
# Shopping Cart Stuff

class IShoppingCartUtility( Interface ):

    def get( create=False ):
        """
        return the user's shopping cart or none if not found.
        if create is passed then create a new one if one isn't found
        """

    def destroy( ):
        """
        remove the current's users cart from the session if it exists
        """
        
class IShoppingCart( ILineItemContainer ):
    """ A Shopping Cart 
    """
    def size( ):
        """
        Count the number of items in the cart (*not* the number of line
        items)
        """


#################################
# Shipping

class IShipmentContainer(  IContainer ):
    """ a container for shipments
    """

class IShipment( ILineItemContainer ):
    """ a (partial|complete) shipment of ishippable line items of an order
    """

class IShippingMethod( Interface ):

    def getCost( order ):
        """ get the shipping cost for an order
        """

#################################
# Tax Utility

class ITaxUtility( Interface ):

    def getCost( order ):
        """ return the tax amount for an order
        """
        

#################################
# Payment Information Details

class IAddress( Interface ):
    """ a physical address
    """
    first_line = schema.TextLine( title = _(u"First Line"), description=_(u"Please Enter Your Address"))
    second_line = schema.TextLine( title = _(u"Second Line"), required=False )
    city = schema.TextLine( title = _(u"City") )
    country = schema.Choice( title = _(u"Country"),
                               vocabulary = "getpaid.countries")    
    state = schema.Choice( title = _(u"State"),
                             vocabulary="getpaid.states")
    postal_code = schema.TextLine( title = _(u"Zip/Postal Code"))

class IShippingAddress( Interface ):
    """ where to send goods
    """
    ship_first_line = schema.TextLine( title = _(u"First Line"))
    ship_second_line = schema.TextLine( title = _(u"Second Line"), required=False )
    ship_city = schema.TextLine( title = _(u"City") )
    ship_country = schema.Choice( title = _(u"Country"),
                                    vocabulary = "getpaid.countries")
    ship_state = schema.Choice( title = _(u"State"),
                                  vocabulary="getpaid.states" )
    ship_postal_code = schema.TextLine( title = _(u"Zip Code"))

class IBillingAddress( Interface ):
    """ where to bill 
    """
    bill_first_line = schema.TextLine( title = _(u"First Line"))
    bill_second_line = schema.TextLine( title = _(u"Second Line"), required=False )
    bill_city = schema.TextLine( title = _(u"City") )
    bill_country = schema.Choice( title = _(u"Country"),
                                    vocabulary = "getpaid.countries")
    bill_state = schema.Choice( title = _(u"State"),
                                  vocabulary="getpaid.states" )
    bill_postal_code = schema.TextLine( title = _(u"Zip Code"))

MarketingPreferenceVocabulary = SimpleVocabulary( 
                                   map(SimpleVocabulary.createTerm, 
                                       ( (True, "Yes", _(u"Yes")), (False, "No", _(u"No") ) )
                                       )
                                )
                                
EmailFormatPreferenceVocabulary = SimpleVocabulary( 
                                   map( lambda x: SimpleVocabulary.createTerm(*x), 
                                       ( (True, "Yes", _(u"HTML")), (False, "No", _(u"Plain Text") ) )
                                       )
                                  )                                

class IUserContactInformation( Interface ):
    """docstring for IUserContactInformation"""
    
    name = schema.TextLine( title = _(u"Your Name"))
    
    phone_number = PhoneNumber( title = _(u"Phone Number"),
                                description = _(u"Only digits allowed - e.g. 3334445555 and not 333-444-5555 "))
                                
    email = schema.TextLine( 
                        title=_(u"Email"),
                        description = _(u"Contact Information") 
                        )
        
    marketing_preference = schema.Bool(
                                        title=_(u"Can we contact you with offers"), 
                                        description=_(u"Can we contact you regarding new offers?"),                            
                                        ) 
    
    email_html_format = schema.Choice( 
                                        title=_(u"Email Format"), 
                                        description=_(u"Would you prefer to receive rich html emails or only plain text"),
                                        vocabulary = EmailFormatPreferenceVocabulary
                                        )

                                
class IUserPaymentInformation( Interface ):
    """ A User's payment information to be optionally collected by the
    payment processor view.
    """

    name_on_card = schema.TextLine( title = _(u"Card Holder Name"),
                                description = _(u"Enter the full name, as it appears on the card. "))

    phone_number = PhoneNumber( title = _(u"Phone Number"),
                                description = _(u"Only digits allowed - e.g. 3334445555 and not 333-444-5555 "))

    # DONT STORED PERSISTENTLY
    credit_card_type = schema.Choice( title = _(u"Credit Card Type"),
                                      source = "getpaid.core.accepted_credit_card_types",)

    credit_card = CreditCardNumber( title = _(u"Credit Card Number"),
                                    description = _(u"Only digits allowed - e.g. 4444555566667777 and not 4444-5555-6666-7777 "))

    cc_expiration = schema.Date( title = _(u"Credit Card Expiration Date"),
                                    description = _(u"Select month and year"))

    cc_cvc = schema.TextLine(title = _(u"Credit Card Verfication Number"),
                             description = _(u"For MC, Visa, and DC, this is a 3-digit number on back of the card.  For AmEx, this is a 4-digit code on front of card. "))


class IPaymentTransaction( ILineItemContainer ):
    """  A Payment that's been applied
    """

    status = schema.Choice( title = _(u"Payment Status"),
                            values = ( _(u"Accepted"),
                                       _(u"Declined"),
                                       _(u"Refunded") ) )
    
#################################
#
class IProductCatalog( Interface ):
    
    def query( **kw ):
        """ query products """
    def __setitem__( product_id, product ):
        """ """
#################################
# Orders

class IOrderManager( Interface ):
    """ persistent utility for storage and query of orders
    """

    def query( **kw ):
        """ query the orders, XXX extract order query interface
        """

    def get( order_id ):
        """ retrieve an order
        """

# future interface
#    def __setitem__( order_id, order ):
#               """ save an order
#        """

    def store( order ):
         """ save an order
         """
class IDefaultFinanceWorkflow( Interface ):
    """ marker interface for workflow / processor integration on the default ootb workflow """

class IOrder( Interface ):
    """ captures information, and is a container to multiple workflows
    """
    user_id = schema.ASCIILine( title = _(u"Customer Id"), readonly=True )
    shipping_address = schema.Object( IShippingAddress, required=False)
    billing_address  = schema.Object( IBillingAddress )
    # only shown on anonymous checkouts?
    contact_information = schema.Object( IUserContactInformation, required=False )
    shopping_cart = schema.Object( IShoppingCart )
    finance_state = schema.TextLine( title = _(u"Finance State"), readonly=True)
    fulfillment_state = schema.TextLine( title = _(u"Fufillment State"), readonly=True)
    processor_order_id = schema.ASCIILine( title = _(u"Processor Order Id") )
    processor_id = schema.ASCIILine( readonly=True )


# Various Order Classification Markers..
# a shippable order for exmaple contains something an ishippable,
# virtual order contains only ttw deliverables
# donation orders contain donations
# recurrence for not yet implement contains recurring line items
# the only mutual exclusive we have at the moment we these is shippable/virtual


class IShippableOrder( Interface ):
    """ marker interface for orders which need shipping """

class IRecurringOrder( Interface ):
    """ marker interface for orders containing recurring line items """

class IVirtualOrder( Interface ):
    """ marker inteface for orders which are delivered virtually """

class IDonationOrder( Interface ):
    """ marker interface for orders which contain donations"""

class IOrderSetReport( Interface ):
    """ store adapters that can serialize a set of orders into a report"""
    
    title = schema.TextLine()
    mime_type = schema.ASCIILine()

    def __call__( orders ):
        """ 
        return a rendered report string from the given ordrs
        """
    
class IOrderWorkflowLog( Interface ):
    """ an event log based history of an order's workflow
    """
    def __iter__( ):
        """ iterate through records of the order's history, latest to oldest.
        """

    def last( ):
        """ get the last change to the order
        """

class IOrderWorkflowEntry( Interface ):
    """ a record describing a change in an order's workflow history
    """
    changed_by = schema.ASCIILine( title = _(u"Changed By"), readonly = True )
    change_date = schema.Date( title = _(u"Change Date"), readonly = True)
    change_kind = schema.TextLine( title=_(u"Change Kind"), readonly=True) 
    comment = schema.ASCIILine( title = _(u"Comment"), readonly = True, required=False )
    new_state = schema.ASCIILine( title = _(u"New State"), readonly = True)
    previous_state = schema.ASCIILine( title = _(u"Previous State"), readonly = True )
    transition = schema.ASCIILine( title = u"", readonly = True)
    # change type?? (workflow, user


class IPhoneNumber(ITextLine):
    """A Text line field that handles phone number input."""
classImplements(PhoneNumber,IPhoneNumber)


class ICreditCardNumber(ITextLine):
    """A Text line field that handles credit card input."""
classImplements(CreditCardNumber,ICreditCardNumber)

class ICreditCardTypeEnumerator(Interface):
    """Responsible for listing credit card types. """

    def acceptedCreditCardTypes(self):
        """ Lists the accepted credit card types. """

    def allCreditCardTypes(self):
        """ List al credit card types. """

class keys:
    """ public annotation keys and static variables
    """

    # how much of the order have we charged
    capture_amount= 'getpaid.capture_amount'
    
    # processor specific txn id for an order
    processor_txn_id = 'getpaid.processor.uid'
    
    # name of processor adapter
    processor_name = 'getpaid.processor.name'

    # sucessful call to a processor
    results_success = 1
    results_async = 2
    
class workflow_states:

    class order:
        # order workflows are executed in parallel

        class finance:
            # name of parallel workflow            
            name = "order.finance"

            REVIEWING = 'REVIEWING'
            CHARGEABLE = 'CHARGEABLE'
            CHARGING = 'CHARGING'
            CHARGED = 'CHARGED'
            REFUNDED = 'REFUNDED'
            PAYMENT_DECLINED = 'PAYMENT_DECLINED'
            CANCELLED = 'CANCELLED'
            CANCELLED_BY_PROCESSOR = 'CANCELLED_BY_PROCESSOR'
            
        class fulfillment:
            # name of parallel workflow
            name = "order.fulfillment"            

            NEW = 'NEW'
            PROCESSING = 'PROCESSING'
            DELIVERED = 'DELIVERED'
            WILL_NOT_DELIVER = 'WILL_NOT_DELIVER'
            
    class item:
        NEW = 'NEW'
        PROCESSING = 'PROCESSING'
        DELIVER_VIRTUAL = 'DELIVERVIRTUAL'
        CANCELLED = 'CANCELLED'
        SHIPPED = 'SHIPPED'
        #RETURNING = 'RETURNING'
        #RETURNED = 'RETURNED'
        REFUNDING = 'REFUNDING'
        REFUNDED = 'REFUNDED'

    class shipment:
        NEW = 'NEW'
        CHARGING = 'CHARGING'
        DECLINED = 'DECLINED'
        DELIVERED = 'DELIVERED'
        SHIPPED = 'SHIPPED'
        SHIPPABLE = 'SHIPPABLE'
        CHARGED = 'CHARGED'
            
