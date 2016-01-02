# Sprint Report for October 2008 Plone Conference #

# Sprinters #
  * Christopher Johnson (cjj)
  * Antonio
  * Bruno
  * B?
  * Ken Wasetis (ctxlken)
  * Adam Hutton (AdamAtNCPC)
  * Lee
  * Aleksi Korvenranta (lexi)


# Details #

New buildout 316.cfg pinned to Plone 3.1.6 for more consistent sprinting among dev team

Fixed Bugs:

  * We now persist and present (to admin) the Name on Card and Phone on Card onto the getpaid order
(see:  http://code.google.com/p/getpaid/source/detail?r=2074)

  * We now persist and present (to admin) the Last4 CC digits and Processor Transaction ID
( see: http://code.google.com/p/getpaid/source/detail?r=2073 and
http://code.google.com/p/getpaid/source/detail?r=2072)

  * Added missing Italian translations (fixed [bug #151](https://code.google.com/p/getpaid/issues/detail?id=151))
( see: http://code.google.com/p/getpaid/source/detail?r=2071 and
http://code.google.com/p/getpaid/source/detail?r=2068 and
http://code.google.com/p/getpaid/source/detail?r=2067 and
http://code.google.com/p/getpaid/source/detail?r=2065)

  * Added missing Japanese translations
( see: http://code.google.com/p/getpaid/source/detail?r=2070)

  * Added notes to README.txt to deal with two new potential dependencies
(see: http://code.google.com/p/getpaid/source/detail?r=2069)

  * Fixed dist.plone.org find-links value in buildout
( see: http://code.google.com/p/getpaid/source/detail?r=2066 )

  * Fixed buildout tests that broke anonymous checkout test due to browser logoff issue
( see: http://code.google.com/p/getpaid/source/detail?r=2064)

  * Fixed getpaid.recipe release 0.1

  * Clean-up of buildout/setup/readme and added flexibility to specify getpaid packages desired for install
( see: http://code.google.com/p/getpaid/source/detail?r=2057 and
http://code.google.com/p/getpaid/source/detail?r=2059)

  * Updated version number and changes.txt and updated on pypi

  * Tagged getpaid.discount for 0.6 release

  * Added documentation for using new buildout and for integrating getpaid with custom content type