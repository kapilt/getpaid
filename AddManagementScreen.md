# Introduction #

If you want something to be controlled by the GetPaid administrative controls, there's some good news and bad news. The bad news is, it may be difficult to make something in the GetPaid code dependent on the IGetPaidManagementOptions. The good news is, it's really easy to add a new management screen and put control there.


# Details #

## The link itself ##

  1. Open /browser/settings.zcml
    * Several stanzas are commented out
    * The rest correlate pretty closely to the links so...
  1. Copy/paste a stanza and tweak it.
    * I based mine on "Legal Disclaimers"
  1. This change begets a class...

## The python file part (the class attribute) ##

In my case, .admin.CheckoutOptions

  1. Copy/paste class and tweak it.
    * I based mine on "class LegalDisclaimers( BaseSettingsForm )"
  1. This change begets an interface...

## The form\_fields part (interface) ##

  1. In my case, interfaces.IGetPaidManagementCheckoutOptions
  1. Also, add new interface to IGetPaidManagementOptions list

## Test it ##

  1. After saving settings.zcml, admin.py, and interfaces.py, restart the instance (no reinstall necessary).
  1. There should now be a new management screen with the expected control on it.

But, of course, setting that control doesn't have any real effect.

## Change the code to check for the config value ##

As mentioned in the Introduction, this is the tricky part. Good luck!