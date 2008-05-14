from getpaid.pxpay import _
from getpaid.pxpay.config import *
from zope.schema import vocabulary

def serverUrlsChoices( context ):
    return vocabulary.SimpleVocabulary.fromItems(
        [
         (_(u"Test Server"), TEST_SERVER_TYPE),
         (_(u"Production Server"), PRODUCTION_SERVER_TYPE),
        ]
       )

def currencyChoices( context ):
    return vocabulary.SimpleVocabulary.fromItems(
        [
         (_(u"Canadian Dollar"), u"CAD"),
         (_(u"Swiss Franc"), u"CHF"),
         (_(u"Euro"), u"EUR"),
         (_(u"French Franc"), u"FRF"),
         (_(u"United Kingdom Pound"), u"GBP"),
         (_(u"Hong Kong Dollar"), u"HKD"),
         (_(u"Japanese Yen"), u"JPY"),
         (_(u"New Zealand Dollar"), u"NZD"),
         (_(u"Singapore Dollar"), u"SGD"),
         (_(u"United States Dollar"), u"USD"),
         (_(u"Rand"), u"ZAR"),
         (_(u"Australian Dollar"), u"AUD"),
         (_(u"Samoan Tala"), u"WST"),
         (_(u"Vanuatu Vatu"), u"VUV"),
         (_(u"Tongan Pa'anga"), u"TOP"),
         (_(u"Solomon Islands Dollar"), u"SBD"),
         (_(u"Papua New Guinea Kina"), u"PNG"),
         (_(u"Malaysian Ringgit"), u"MYR"),
         (_(u"Kuwaiti Dinar"), u"KWD"),
         (_(u"Fiji Dollar"), u"FJD"),
        ]
       )
