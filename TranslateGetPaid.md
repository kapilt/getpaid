# Introduction #

Like Plone, GetPaid incorporates internationalization (i18n) as part of the product. Translation of a product consists of two parts:

  * Developers identifying text and phrases in the product that need translations
  * Translators creating a translation file for each language (translating each of the phrases identified in the above step).

Thus it is necessary that both developers and those adapting the product for a new language (be they translators, developers, or integrators) participate in maintaining the internationalization.


# Details #

**For Developers**

  * Implemented for Zope 3 technologies, the fields and texts for all of the templates, zcml files, and python files that present text in the interface have been given i18n tags.

  * We are using two domains: "plonegetpaid" (for all Plone-specific templates) and "getpaid" (for non-Plone, ie Zope-specific, templates)

  * We are using the Plone Guidelines for Translators "Guide to Prefixes" to choose IDs for the tagged areas of the templates. See [Guidelines for Translators](http://plone.org/development/teams/i18n/translators-guidelines)

  * For more on i18n for developers, see: [Plone i18n for developers](http://plone.org/documentation/how-to/i18n-for-developers/) or [this short course](http://plone.org/products/archgenxml/documentation/how-to/handling-i18n-translation-files-with-archgenxml-and-i18ndude/)

**For Translators**

GetPaid is implemented in 2 main products (PloneGetPaid and getpaid.core), and thus has two separate areas where translations are created/maintained: **PloneGetPaid/i18n/** (two files) and **getpaid.core/src/getpaid/core/locales/** (one file).

  * Updating translations: GetPaid continues in development, and thus new items that need translation will be created as new parts of the interface are added. Please be sure to update the appropriate .po files located at PloneGetPaid/i18n/ and getpaid.core/src/getpaid/core/locales/ .

  * Creating a new translation: For translating to a new language, translate each of the fields in the .po file to the language corresponding to the file (see more below). In order to get the .po file into the product, it needs to be committed to the product. To get commit access to GetPaid, send an email via www.plonegetpaid.com/contact requesting access. If you already have a file and need it added to the product, you can send it to the [getpaid-dev](http://groups.google.com/group/getpaid-dev) mailing list.

  * For more on i18n translation maintenance, see [How to update language files - Plone translation files](http://plone.org/documentation/how-to/how-to-update-languague-files-plone-translation-files)