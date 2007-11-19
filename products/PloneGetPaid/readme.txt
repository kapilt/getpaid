**GetPaid for Plone**

*Product Description: Version 0.3 (Red Ochre Release)*

Congratulations - you have installed GetPaid for Plone! GetPaid provides you basic commerce functionality (donations, shopping cart, checkout) and order management out of the box while providing a flexible framework for creating custom ecommerce applications. 

You can find more information about this project at

- "www.plonegetpaid.com":http://www.plonegetpaid.com (public web site, general information, sponsorship opportunities, blog)

- "Google Code":http://code.google.com/p/getpaid (issue tracker, wiki, browse and checkout source code)

- "Plone Products":http://plone.org/products/getpaid (release plans, official documentation, release code tarballs)

How to Start Using GetPaid:

  GetPaid allows you to make any existing content in your site "buyable" (ie can be added to a cart and then purchased in the checkout). For a full explanation of setting up GetPaid, please see "GetPaid Setup":http://plone.org/products/getpaid/documentation/tutorial/setting-up-getpaid . The following is an abbreviated version of how to get started (bare essentials).

 - Install:  From the Plone Quick Installer, install PloneGetPaid. This will also add other tools that GetPaid needs. 

 - Setup: From the Plone Setup area, scroll down to the area for configuration of custom products and click on GetPaid. This will take you to the administrative screens for GetPaid. At a minimum, you will need to set what content types will be buyable (on the "Content Types" screen) and the payment processor (setting to Testing Processor will allow you to test the product). If you do not have a mailhost set on your server, you will need to disable the email notifications. Also, if you want to receive email notifications, be sure to enter an email address in the "Site Profile" part in the GetPaid Setup. We recommend that you fill out information in all the screens applicable to your store to provide the best user experience. 

 - Content: Go to the content of your site. When you click on the "action" menu while viewing a type of content you selected in the "content types" configuration, you will see options to make the content "buyable", a "donation", "shippable", etc. Select the option you want and then fill in the required fields (ie price). 

Payment Processors:

  GetPaid currently has two working payment processors: Authorize.net and a Test Processor (so you can experience the features before setting up/activating your account). Authorize.net requires you to have a US-based merchant account. Other payment processors are also being integrated (Ogone - which allows European-based merchant accounts, Paymentech, PayPal, GoogleCheckout). It is not the intent of this document to answer all your questions about payment processors, payment gateways, and merchant accounts. We suggest you ask on the development mailing list (see below) for more questions if you are unfamiliar with these. 

How to Customize Functionality:

  Most functionality and features of GetPaid can be easily customized. To do so, you should be familiar with the Zope 3 Component Architecture. By writing your own adapters for GetPaid, you use a custom way of storing member data (ie a relational database), handling pricing (to implement specific discounting options, for example), introducing new payment processors, and much more. Documentation on GetPaid customization best practices is available here: http://plone.org/products/getpaid/documentation/how-to/best-practices-for-customizing-getpaid

Where to Find More Information:

  In addition to the links above, you can also join our development mailing list to contact others, find collaborators or discuss issues of the product, and get help: http://groups.google.com/group/getpaid-dev

  The project community uses the irc channel #getpaid (irc.freenode.net) for real-time interaction. 

Where to Find Support: 

  Support options, including commercial support, are listed at: "GetPaid Support":http://www.plonegetpaid.com/support

  If you find this product beneficial, please consider making a contribution: "Contribute to GetPaid":http://www.plonegetpaid.com/sponsor

License:

  This product is licensed under the Zope Public License (ZPL), available at "Zope Public License":http://www.zope.org/Resources/ZPL

Credits:

  Project leaders: Kapil Thangavelu is the chief architect and author of the product. Christopher Johnson is the project organizer. Jon Stahl is the project's NGO Liason.

  Lots of people have contributed to this project through our sprints. Thanks to all those who participated in the BBQSprint, Google DocComm Sprint, and i18n Sprint. For more complete list of credits, please see "GetPaid Credits":http://plonegetpaid.com/about/credits/

  Special thanks to our sponsors that helped us "social source" this project!

  "ObjectRealms":http://objectrealms.net | "ifPeople":http://www.ifpeople.net | "One/Northwest":http://onenw.org | "Contextual Corporation":http://contextualcorp.com | "Trees for Life":http://treesforlife.org | "Totsie.com":http://totsie.com




