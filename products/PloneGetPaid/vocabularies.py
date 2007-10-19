"""
$Id$

vocabularies for getpaid
"""

from zope import component
from zope.interface import implements
from zope.app import zapi
from os import path

from zope.schema import vocabulary
from getpaid.core import interfaces

from iso3166 import CountriesStatesParser
from Products.PloneGetPaid.interfaces import ICountriesStates, IMonthsAndYears

from Products.CMFCore.utils import getToolByName

from Products.PloneGetPaid.i18n import _

def PaymentMethods( context ):
    # context is the portal config options, whose context is the portal
    adapters = component.getAdapters( (context.context,), interfaces.IPaymentProcessor )
    payment_names = set( map(unicode, [ n for n,a in adapters]) )
    return vocabulary.SimpleVocabulary.fromValues( payment_names )

def ContentTypes( context ):
    # context is actually a preferences object, dig another level to get to the adapted context
    # which is acq wrapped.
    portal_types = getToolByName( context.context, 'portal_types' )
    terms = []
    # hmmm..
    types = filter( lambda x: x.global_allow, portal_types.objectValues() )

    properties = getToolByName( context.context, 'portal_properties')
    types_not_searched = set( properties.site_properties.types_not_searched )

    for type in portal_types.objectValues():
        if type.getId() in types_not_searched:
            continue
        terms.append(
            vocabulary.SimpleTerm( unicode(type.getId()), title=unicode(type.title_or_id()) )
            )

    terms.sort( lambda x,y: cmp( x.title, y.title ) )

    return vocabulary.SimpleVocabulary( terms )

def TaxMethods( context ):
    return vocabulary.SimpleVocabulary.fromValues( (u"None",) )

def ShippingMethods( context ):
    return vocabulary.SimpleVocabulary.fromValues( (u"None", _(u"Flat Rate Shipping")))

def CreditCards( context ):
    return vocabulary.SimpleVocabulary.fromValues( (u"Visa", u"Mastercard", u"Discover", u"American Express") )

def WeightUnits( context ):
    return vocabulary.SimpleVocabulary.fromValues( (_(u"Pounds"),) )

def Currencies( context ):
    return vocabulary.SimpleVocabulary.fromValues( (_(u"US Dollars"),) )

def MerchantNotificationChoices( context ):
    return vocabulary.SimpleVocabulary.fromItems(
        [
        (_(u"Do not send merchant email notification of a completed transaction") ,u"no_notification"),
        (_(u"Send merchant email notification when a transaction happens"), u"notification"),
        #("Send merchant encrypted email notification when a transaction happens", u"encrypted_notification")]
        ]
        )

def CustomerNotificationChoices( context ):
    return vocabulary.SimpleVocabulary.fromItems(
        [
        (_(u"Do not send customer email notification of a completed transaction"), u"no_notification"),
        (_(u"Send customer email notification of a completed transaction"), u"notification")
        ]
        )

class TitledVocabulary(vocabulary.SimpleVocabulary):
    def fromTitles(cls, items, *interfaces):
        """Construct a vocabulary from a list of (value,title) pairs.

        The order of the items is preserved as the order of the terms
        in the vocabulary.  Terms are created by calling the class
        method createTerm() with the pair (value, title).

        One or more interfaces may also be provided so that alternate
        widgets may be bound without subclassing.
        """
        terms = [cls.createTerm(value,value,title) for (value,title) in items]
        return cls(terms, *interfaces)
    fromTitles = classmethod(fromTitles)

class CountriesStatesFromFile(object):
    """Countries utility that reads data from a file
    """
    implements(ICountriesStates)

    _noValues = [(u'(no values)',u'(no values)')]

    def __init__(self):
        iso3166_path = path.join(path.dirname(__file__), 'iso3166')
        self.csparser = CountriesStatesParser(iso3166_path)
        self.csparser.parse()
        self.loaded_countries = []

    def countries(self):
        if self.loaded_countries:
            return self.loaded_countries
        names =  self.csparser.getCountriesNameOrdered()
        res = []
        for n in names:
            if len(n[1]) < 18:
                res.append( n )
            elif ',' in n:
                res.append( ( n[0], n[1].split(',')[0] ) )

        # need to pick this up some list of strings property in the admin interface
        def sorter( x, y, order=['UNITED STATES', 'UNITED KINGDOM', 'CANADA']):
            if x[1] in order and y[1] in order:
                return cmp( order.index(x[1]), order.index(y[1]) )
            if x[1] in order:
                return -1
            if y[1] in order:
                return 1
            return cmp( x[1], y[1] )

        res.sort( sorter )
        self.loaded_countries = res
        return res

    countries = property(countries)

    def states(self, country=None):
        if country is None:
            return [n for n in self.allStates() if len(n[1]) < 20]

        states = self.csparser.getStatesOf(country)

        if len(states) == 0:
            return self._noValues

        return [n for n in states if len(n[1]) < 20 ]

    def allStates(self):
        return self.csparser.getStatesOfAllCountries() + self._noValues

def Countries( context ):
    utility = zapi.getUtility(ICountriesStates)
    return TitledVocabulary.fromTitles(utility.countries)

def States( context ):
    utility = zapi.getUtility(ICountriesStates)
    return TitledVocabulary.fromTitles(utility.states())

class MonthsAndYears(object):
    """Months-Years utility"""
    implements(IMonthsAndYears)

    def tuple_unicode_range(self,begin,end):
        return tuple([unicode('%02i' % i) for i in range(begin,end)])

    def months(self):
        return self.tuple_unicode_range(1,13)
    months = property(months)

    def years(self):
        return self.tuple_unicode_range(2007,2030)
    years = property(years)


#def Months( context ):
    #utility = zapi.getUtility(IMonthsAndYears)
    #return vocabulary.SimpleVocabulary.fromValues(utility.months)

#def Years( context ):
    #utility = zapi.getUtility(IMonthsAndYears)
    #return vocabulary.SimpleVocabulary.fromValues(utility.years)
