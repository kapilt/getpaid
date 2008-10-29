from getpaid.ogone import _
from zope.schema import vocabulary

def serverUrlsChoices( context ):
    return vocabulary.SimpleVocabulary.fromItems(
        [
         (_(u"Test Server"),u"https://secure.ogone.com/ncol/test/orderstandard.asp"),
        (_("Production Server"), u"notification"),])

def currencyChoices( context ):
    return vocabulary.SimpleVocabulary.fromItems(
        [
         (_(u"Euro"), u"EUR"),
         (_(u"US DOLLAR"), u"USD")])
