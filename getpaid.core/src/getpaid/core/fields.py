from zope import schema
from zope.schema.interfaces import ValidationError

from zope.i18nmessageid import MessageFactory
_ = MessageFactory('getpaid')

class InvalidPhoneNumber(ValidationError):
    __doc__ = _(u"Only digit character allowed.")

class InvalidCreditCardNumber(ValidationError):
    __doc__ = _(u"Invalid Credit Card Number.")

def creditCardValid(card_number):
    """ checks to make sure that the card passes a luhn mod-10 checksum """
    # strip any whitespace
    card_number = card_number.replace(' ', '').strip()
    
    if isinstance( card_number, unicode ) and not card_number.isnumeric():
        return False
    
    elif isinstance( card_number, str) and not card_number.isdigit():
        return False

    sum = 0
    num_digits = len(card_number)
    oddeven = num_digits & 1
    for count in range( 0, num_digits):
        digit = int(card_number[count])
        if not (( count & 1 ) ^ oddeven ):
            digit = digit * 2
        if digit > 9:
            digit = digit - 9
        sum = sum + digit
    return ( (sum % 10) == 0 )

class PhoneNumber( schema.TextLine):

    def _validate(self, value):
        super(PhoneNumber, self)._validate(value)
        if value and not value.isdigit():
            raise InvalidPhoneNumber(value)

class CreditCardNumber( schema.TextLine ):

    def _validate(self, value):
        super(CreditCardNumber, self)._validate(value)
        if not creditCardValid( value ):
            raise InvalidCreditCardNumber(value)
