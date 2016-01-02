# Introduction #

We started the DocComm sprint at Google June 25. This is an update of notes. Find us in #getpaid during the sprint and use the dev mailing list.

# Current Work #

On site sprinters:
  * Kapil: pay processor / workflow integration
  * Brian G: Product details portlet
  * David S:
  * DB: user order history
  * Eric S: Admin UI
  * Dave F: UPS (shipping utility) integration
  * Bill: GoogleCheckout, Paypal
  * Veda:
  * Donna:

Remote sprinters:
  * John L: order management UI
  * Ken W:

# Daily News #

## Day 5 ##

  * Kapil: Authorize.net can connect, authorize, and store order (though is not part of buildout because of dependency). Still pending is workflow/processor integration and exposing workflow management to admin. Also made a script to generate orders (for testing).
  * Db: User order history view and link integrated to UI.
  * Bill: GoogleCheckout has button and view (note: not in the buildout yet, will require Kapil updating products). Framed out PayPal processor integration (does html for button, but no view yet)
  * Dave: UPS communication, and now being parsed. All functionality there, needs to be put into utility, but is modular.
  * Eric: Admin UI work.
  * Brian: product details portlet.
  * John: Closed [issue 15](https://code.google.com/p/getpaid/issues/detail?id=15) (can now un-mark payable objects).
  * David S: More tests: workflow and order
  * Donna: Will be working to integrate wireframes with AdminUI next week.
  * Veda: Howto document structured on wiki

## Day 3 ##

  * Kapil: Now save orders! Workflow for orders is improved. Admin screen that shows you the orders placed on the system. (to use relational db, integrators can write a storage adapter for the order management).
  * Eric: Admin screens progress. All tabs done, most of form fields entered in forms (and being stored). Problem of having one Interface all the field, which will be split out into multiple ones (but still have a central way to query).
  * DaveF: UPS integration (choosing shipping rates with live lookup at UPS). Later would be internationalization. About half way - probably done Friday.
  * Brian: Working on shopping cart. Lots of learning! API for generating tables and . Working to convert quantity to text box. Working, but not saving/updating price. About another hour of work on that. Planning to work with Siebo tonight on integrating the view of payable info + "add to cart" button to the view of content.
  * Steve: GoogleCheckout will have to wait till we can get live data from Google. Sample messages don't parse with Gchecky. ie we need to know what Google gives back...need demo site.
  * Chris: dev.plonegetpaid.com now points to Kapil's server so we can do real testing. New issues being filed, see the tracker: http://code.google.com/p/getpaid/issues/list
  * Donna: All wireframes done and now being updated, cleaning up downloads area.
  * Bill: Authnet processor is loading and is connected to PGP, but the adapters have been changed, so PGP is not seeing Authorize.net in admin area. Need to get zcml to agree on how it is loaded. Close to being able to use it...but workflow not complete in places.

1:02pm: Doccom tag on flickr. [Issue #15](https://code.google.com/p/getpaid/issues/detail?id=#15) assigned to jlenton.

12:36pm
  * [Issue 14](https://code.google.com/p/getpaid/issues/detail?id=14) is closed! (by jlenton, aka Chipaca)
  * 21 people in #getpaid

12:06pm
Kapil: Now save orders! Workflow for orders is improved. Admin screen that shows you the orders placed on the system. (to use relational db, integrators can write a storage adapter for the order management).

## Day 2 ##

A day for many good things! Food was good :)

Day 2 Checkin:

  * Kapil set up workflow for finance and fulfillment, orders (now checked in) (integrating hurry.workflow, by backporting to Zope 3.2). Easy to hook into.
  * Kapil started experimenting with a checkout wizard, paired with Eric, and you can now collect user info to pass off to pay processor
  * Rudimentary zope 3 local utility set up to store and index the orders (to enable nice admin interfaces on top of that). Now part of install
  * Brian focused on donation today. Change made to make it like the other content. Now any item can be made "donateable" and can be added to a cart. Noted that it took 14 file changes to incorporate this; Kapil suggests considering consolidating the donation files in one place (separate from rest of product).  The old donation content object (addable from "add to folder") is still there...Next is UI! (and more unit tests)
  * Eric worked on Doctests, trying out interfaces to set as buyable, shippable and premium. Basic doctests now in place. Started functional test to make content type buyable and walk through the checkout process.
  * Veda and Donna: mockups of user interface in very general way. Tomorrow tackling the admin UI. Now available are review cart, product page, etc etc. Check out the download area and adapt to dev process.
  * Steve working on Google Checkout library...breaking so far. Note that we will need proxy for demo/testing site.
  * Bill: started looking on Gchecky and then went to Authorize.net. Decided processors are going to be **utilities**. Worked at some of workflow and now will have first pass at authnet processor tomorrow morning.
  * David S: tests written for marking objects and started some against getpaid.core (doctests).
  * Dave F: had first day of class today :)
  * Task (for testers): make notes on wiki about how to run the tests!


5:01pm
  * GetPaid team heads to sunny hill outside for checkin

3:06pm
  * 23 people in #getpaid!

2:36pm
  * Kapil set up workflow for finance and fulfillment, orders (now checked in) (integrating hurry.workflow, by backporting to Zope 3.2).
  * Brian made a checkin of the donation form changes. Now donation behaves like the other payable object options (ie you can make something "donateable".
  * Eric is nearly complete on a functional test of adding an object and making it payable.
  * Chris is ready to bash quills with a baseball bat (after learning that archived posts are not publicly accessible).

## Day 1 ##


9:30am
Google is open for DocComm sprinters! Breakfast begins, a huge spread of Guayaki yerba mate products are set out, along with Divine fair trade chocolates :)

11:05am
The mate is kicking in. Everyone has a gmail account and now the project has 12 members and 2 managers. We covered the architecture and philosophy of GetPaid and the user stories.

"...before I retreat to the doc [dark](dark.md) side." says Eric Rose, holding a glass of organic milk.

1:09pm: 19 people in #getpaid
5 people around a single table (mac laptops glowing), working on unit tests for GetPaid
Veda and Donna are refining the user stories and building css code for the UI
Bill and Steve are fixing the shopping cart portlet
Kapil is working on checkout wizard
The first blog post hits the net: Post w mate: http://advice.cio.com/esther_schindler/the_sprint_experience

1:54pm: 19 people in #getpaid
Jon Stahl drops in to let us know he is with us in spirit, if not in sprint :)

2:00pm: 20 people in #getpaid

3:00pm:
Google Snack Attack (ie more food shows up)

4:59pm : 18 people in #getpaid

GetPaid Day 1 Checkin

Unit tests:
- Now available for all major aspects of the code tests desired for
- Mostly stubs
- 5 people working on this used it as a chance to understand the product
- Some changes made to interfaces
- Tomorrow: advance unit tests more and then get to features!

Shopping cart:
- You can now add multiple items
- Price and link to item are shown
- Cart portlet is created in install
- Tomorrow: checkout wizard and workflow

GetPaid has an icon!

User interface:
- End user specs created and half way implemented in css/html (being uploaded at