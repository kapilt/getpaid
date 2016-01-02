# Configure Shipping #

## Configuring on a Content Object Basis ##

Any content object that is marked as Payable will also be able to be Shippable. See Setting Means of Delivery.

## Configuring Site-Wide ##

There will be a "shipping" tab in the Site Setup / GetPaid Configuration panel for setting up shipping settings. This is used when the site manager sets the site-wide shipping options to be used.

Note that most of this information is gleaned from Miva Merchant documentation. Some of this information may not be usable for implementation, but might be of use for end user documentation.
For the first iteration of this product, the following options are suggested for implementation:

## Weight Units ##
A dropdown box to choose units for weight in the site. Selecting "pounds (lbs)" or "kilograms (Kg)" will provide site-wide settings for interfaces.

### Base + Weight Shipping ###

  * Allows you to define a base charge, plus an amount to be charged per weight unit for the total weight of the order. It calculates shipping charges according to a configured Base charge PLUS a configured per unit-of-weight-measure charge, instead of charging a minimum OR per-unit amount. Site manager can edit the fields for "base charge" and "per weight charge".

### Flat Rate Shipping ###

  * Defines a flat rate that is to be charged for shipping. This most basic of all of the shipping modules may be given a list of methods that you can assign a name and flat amount for the shipping charge that will be added to the customer's order regardless of any weight data.

### Minimum or Weight Shipping ###

  * This shipping type allows you to establish a minimum charge for shipping. You configure a per/unit-of-weight charge and a minimum charge which MIVA Merchant will use to calculate the shipping charges for your customers orders. The weight unit set in the Settings of the Add Store page, and (based on that unit of measure) the weight specified in the product record of each product in your shoppers baskets are used to calculate the shipping charge.
  * Use the following procedure to set up minimum or weight shipping for your store. Enter the name of this Minimum or Weight Shipping Method. Enter the charge for each Unit of Measurement (Weight). Do not enter the currency symbol. (The Unit of Measurement is listed under Settings on the Edit Store page.) Enter the minimum charge for this shipping Module to charge if the total weight of items in a basket is less than the per-unit charge.

### Price Table Based Shipping ###

  * Fields include: Add Shipping Method (i.e. a country name), Add Handling Amount,  Add the Ceiling (the highest dollar amount that would be within the range for this price to be charged, i.e. from $0-$9.99, a person pays 7%. For $10.00-$29.99, they pay 17%, etc.), Add Charge Percentage.

### Quantity Based Shipping ###
This option allows the following modes of setting up your shipping charges: Standard, Progressive.

#### Standard - based on total number of items shipped ####

You can set up a standard fee that is to be charged for the total number of items ordered. For example, you can charge $3.00 per item if there is a minimum of 3 items per order. You can set the charge at $2.00 per item if the total order is up to 6 items, and $1.75 per item if the total order is over 6 items. You could have the series go as high as you wish.

|Minimum # of Items|Charge per Item|
|:-----------------|:--------------|
|3                 |$3.00          |
|6                 |$2.00          |
|+                 |$1.75          |

#### Progressive - based on defined ranges ####

You can set up a series of quantity ranges and charge shipping for the items that fall within the quantity range. For example, you can set up five ranges as follows: 1-3, 4-7, 8-15, +. This means that you can charge shipping progressively, the first 3 items are charged at the rate you set for that range, items 4 through 7 are charged at the rate for that range, etc. The last row has the highest range. This is the cost of items over the final range. Therefore, if you get a discount for quantity shipping, you can pass it on to your customers.

|Range of Items|Charge per Item in Range|
|:-------------|:-----------------------|
|1-3           |$3.00                   |
|4-7           |$2.00                   |
|8-15          |$1.50                   |
|+             |$1.00                   |


#### A comparison: ####

If you shipped 10 items using each method, the charges are shown below.

#### Standard Method ####
The charge for 10 items is $1.75 per item, or $17.50 total.

#### Progressive Method ####
Charge for the first three items is $3.00 per item, or $9.00 for this range of items.
Charge for next four items is $2.00 per item, or $8.00 for this range of items.
Charge for next three item (8, 9, 10) is $1.50 per item, or $4.50 for this range of items.
The total charge is the total of the three ranges: $9.00+$8.00+$4.50=$21.50.


### Weight Table Based Shipping ###
The Weight Table Based Shipping allows you to create pre–configured, custom Shipping Methods.

  * After configuring this shipping module, all your products will have the tab (link) Weight Table Shipping Charges. The charge field allows you to add or subtract an amount from the pre-configured table shipping rates for that product.
  * You can define a Handling charge for the shipping method. This charge is in addition to the amount specified in the weight table. This is handy when you are entering weight and rate information directly from a shipper 's rate table, but need to add a charge to cover the cost of packaging.
  * Each line in the table has a ceiling to define a top range for the weight.
  * The ceiling is the highest weight that qualifies for that row. For example, if you charge $4 shipping for orders up to 2 lbs., then the ceiling for the first row would be 2.

### Row Cost Ceiling ###

|Row|Cost|Ceiling|
|:--|:---|:------|
|1  |$4.00|2      |
|2  |$5.00|4      |
|3  |$6.00|+      |



  * Each line in the table has a rate for shipping a product that weighs less than the ceiling weight.
  * The last row should define the highest amount charged. Its ceiling is a +.
  * The rate is the amount you want to charge for shipping. This does not include the handling charge you may enter.


## Other shipping possibilities are: ##

### FedEx Shipping Cost Estimate: ###

Developer Documentation: http://www.fedex.com/us/solutions/shipapi/faq.html#1

The FedEx Shipping Cost Estimate module accesses FedEx to calculate the shipping cost. If you have an existing FedEx account, you can use that account number. If you do not presently have an a FedEx account, visit the FedEx website, http://www.fedex.com, and click the Open an Account link.

FedEx uses OpenSSL, which your host should already have installed. Contact your host if you see an error about not being able to load OpenSSL files.

The FedEx Shipping Cost Estimate module calculations are based on one package per order.

  1. Select Default Test, Default Production, or Other for the FedEx server you will be using. Choose Default Production when you go live. Remember, nothing is being charged, the module calculates the shipping cost estimate.
  1. Enter your **FedEx Account Number**.
  1. If you do not have a FedEx account, go to www.fedex.com.
  1. Enter the **Meter Number**. If you do not have one, MIVA Merchant will generate one for you.
  1. If you want to add a **Handling Charge**, choose one or more charges:
    * Base Handling: a fixed amount
    * Percent Handling: a percent of each order 's shipping cost that is shipped via FedEx
    * Minimum Handling: the minimum shipping amount for each order that is shipped via FedEx.
  1. Select the **Drop Off** type. These are the available selections:
    * Regular Pickup
    * Request Courier
    * Drop Box
    * Drop at BSC (a Ship Center)
    * Drop at Station (a FedEx World Service Center)
  1. Check the box next to **Signature required for home delivery**, as applicable.
  1. FedEx may charge an additional amount for this, so if you want the shipping cost estimate to include this amount, check the box.
  1. Check the boxes for the service you want and uncheck those you do not want to offer to your customers.
  1. Visit FedEx at http://www.fedex.com/us/services/waystoship/ for descriptions of these ways to ship.


### U.S.P.S. Online Rate Calculation (Domestic & International) ###

Developer documentation: http://www.usps.com/webtools/welcome.htm

This tool accesses U.S.P.S. Rates to calculate the shipping cost. The configuration for this module has default settings loaded into it for quick set up. GetPaid will take information for items in your shoppers baskets, and based on weight and service selected, will calculate shipping charges to be added to your customers orders.

See http://www.uspswebtools.com to register with U.S.P.S. and for additional information. After you register you will receive an e-mail from U.S.P.S. for their documentation locations and the testing URL.

When you are ready to go live, notify U.S.P.S., as indicated in the e-mail, and they will send you the production URL and provide access to it.

  * Enter your U.S.P.S. User ID and Password.

  * ote: Do not change the URL to USPS WebTools Server, unless directed to do so by USPS.

If you have not yet registered with USPS, visit http://www.uspswebtools.com to follow the click here to REGISTER link.

  1. Change the Source Zip Code for Calculations, if different from the zip/postal code in the Owner form of your store.
  1. Enter the Handling Charge, if any.
  1. Select the U.S.P.S. Shipping Method(s) you want to offer your customers. In your store only the applicable methods will display to your customers. If both you and your customer are in the United States, the global methods will not be shown.

#### U.S.P.S. Methods (within U.S.) ####

For additional information, see http://www.usps.com/consumers/domestic.htm. Also, at http://www.usps.com/businessmail101/classes/, you can find the classes of mail.

##### U.S.P.S. Priority Mail Service Standards #####

> Priority Mail is used for documents, gifts, and merchandise. Any mailable item may be sent as Priority Mail. You can request transit time standards for Priority Mail service between any two 5-digit ZIP Codes. You get an average delivery standard for two- or three-day service. Save your e–shoppers up to 65% by offering Priority Mail for their online purchases.
##### U.S.P.S. Express Mail Service Commitment #####

> Express Mail offers overnight service to many destinations and is guaranteed or your money is refunded. Express Mail is delivered to many locations 365 days a year including weekends and holidays — at no extra charge — and delivered next day by noon to select locations. Receive U.S.P.S. guaranteed commitment between any two 5-digit ZIP Codes. This API will tell you if delivery is guaranteed by noon the next day, by 3:00 p.m. or two-day including Saturday and Sunday commitments. All you need to do is mail by the scheduled acceptance time.
##### U.S.P.S. Bound Printed Matter #####

> One of the Package Services, Bound Printed Matter has content restrictions and specifications. In part, it must consist of Consist of advertising, promotional, directory, or editorial material (or any combination of such material).
##### U.S.P.S. Media Mail #####

> One of the Package Services, it is used for books, film, manuscripts, printed music, printed test materials, sound recordings, play scripts, printed educational charts, loose-leaf pages and binders consisting of medical information, videotapes, and computer recorded media such as CD-ROMs and diskettes. Media Mail cannot contain advertising.
##### U.S.P.S. First Class #####

> First-Class Mail is used for personal and business correspondence. Any mailable item may be sent as First-Class Mail. It includes postcards, letters, large envelopes, and small packages
##### U.S.P.S. Parcel Post #####

> One of the Package Services, it is used for mailing merchandise, books, circulars, catalogs, and other printed matter.
##### U.S.P.S. Library #####

> One of the Package Services, it is used by qualifying institutions like libraries, universities, zoos, and research institutions to mail educational and research material.

#### U.S.P.S. Methods (Global) ####

For International information, see http://pe.usps.gov/text/pub51/welcome.htm.

##### U.S.P.S. Global Express Guaranteed #####

> Global Express Guaranteed (GXG), formerly Priority Mail Global Guaranteed, is an expedited delivery service for both documents and non-documents (i.e., merchandise items) that is the product of a business alliance between the U.S. Postal Service and DHL Worldwide Express Inc. It provides senders with reliable, high-speed, time-definite service from designated U.S. ZIP Code areas to principal locations in more than 200 countries and territorial possessions. Service is guaranteed to meet destination-specific delivery standards or the requisite postage will be refunded.

##### U.S.P.S. Global Parcel Post (Airmail and Economy) #####

> Parcel post packages can be entered as either airmail or economy (surface) mail. Although both parcel post classifications are subject to the same regulatory requirements, the substantive differences between them relate primarily to the mode of transportation (i.e., air versus surface), speed of service, and price.

##### U.S.P.S. Global Priority Mail #####

> Global Priority Mail (GPM) is an accelerated airmail service that provides customers with a reliable and economical means of sending correspondence, business documents, printed matter, and light-weight merchandise items to Canada, Mexico, and specified destination countries in Western Europe, the Caribbean, Central and South America, the Pacific Rim, the Middle East, and Africa. GPM items receive priority handling within the U.S. Postal Service and the postal service of the destination country.


##### U.S.P.S. Global Express Mail #####

> Global Express Mail (formerly Express Mail International) is a reliable high-speed service for mailing time-sensitive items to more than 175 countries and territorial possessions. It provides customers with expeditious handling and delivery on an on demand basis.


#### UPS Domestic Shipping Calculator ####
Developer documentation: http://ups.com/content/us/en/bussol/offering/technology/automated_shipping/online_tools.html








