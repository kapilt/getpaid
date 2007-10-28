from zope import component
from zope.interface import implements
from zope.schema import vocabulary
import interfaces


def CreditCardTypes(context):
    adapter = component.getAdapter(context, interfaces.ICreditCardTypeEnumerator)
    return vocabulary.SimpleVocabulary.fromValues(adapter.allCreditCardTypes())


def AcceptedCreditCardTypes(context):
    adapter = component.getAdapter(context, interfaces.ICreditCardTypeEnumerator)
    return vocabulary.SimpleVocabulary.fromValues(adapter.acceptedCreditCardTypes())
