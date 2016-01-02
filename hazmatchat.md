#notes from chat with hazmat on checkout wizard refactoring questions...

```
(07:18:41 PM) cjj: hazmat: we are ready to start refactoring. and the guys say product catalog is doable and understood
(07:19:01 PM) cjj: but they don't get the vision of what was wanted for the checkout wizard refactoring (or why refactor the working one befre release)
(07:19:27 PM) Kapil: because right now its pretty hard wired
(07:19:30 PM) Kapil: its hard to customize
(07:19:54 PM) Kapil: its silly to ask for shipping address on orders without deliverables
(07:19:54 PM) Kapil: etc
(07:20:33 PM) cjj: hazmat: jfroche said he was able to customize fairly easily for hte sites he did
(07:20:54 PM) cjj: i think we could get around the shipping address issue just adding a link to use same as billing...
(07:22:59 PM) cjj: hazmat: but they didn't know the exact use case for customization or how it should be done, so that is kinda  amystery at this point
(07:23:13 PM) cjj: otherwise, we have over 40 tests in PGP (up from 3)
(07:23:23 PM) cjj: GenericSetup transition is done
(07:23:26 PM) cjj: 2 issues fixed
(07:24:44 PM) Kapil: sweet!
(07:24:46 PM) Kapil: re tests
(07:24:51 PM) cjj: :)
(07:24:59 PM) cjj: yeap, they say ready for refactoring...
(07:25:00 PM) Kapil: is that including the getpaid.core* and getpaid.io tests?
(07:25:06 PM) cjj: nope!
(07:25:28 PM) cjj: it is basically all the admin functions - setup and content integration
(07:25:38 PM) Kapil: hmm
(07:25:48 PM) cjj: but the tests aren't there for the checkout since it is slated for refactoring...
(07:25:51 PM) Kapil: the part that needs tests the most is the checkout wizard
(07:26:00 PM) Kapil: right
(07:26:12 PM) cjj: sure, but we don't get the vision :(
(07:26:27 PM) ***Kapil goes to reread the task list
(07:27:48 PM) Kapil: the only one that i see as definitely nesc. is the duplicate processing protection
(07:28:09 PM) Kapil: basically have the order id generated early in checkout wizard, and passed around through the process
(07:28:32 PM) cjj: ah ha
(07:28:35 PM) Kapil: and then at the end before creating a new order we check to see if the order has already been created, and handle appropriately
(07:28:48 PM) rsantos left the room (quit: ).
(07:29:19 PM) cjj: hazmat: is the issue that getpaid passes it to the pay processor twice? 
(07:29:26 PM) cjj: or that we generate two orders in the system? 
(07:29:31 PM) cjj: (or both)
(07:29:34 PM) Kapil: no, its protection against duplicates
(07:29:48 PM) Kapil: which would could result in two orders, two payments, etc
(07:29:51 PM) Kapil: if you hit submit twice
(07:29:59 PM) Kapil: on the final page
(07:30:03 PM) Kapil: of the checkout
(07:30:19 PM) Kapil: or you go back in your browser, etc
(07:30:53 PM) cjj: hazmat: so, that makes sense, i think. but the team is in the checkin meeting now. 
(07:31:00 PM) Kapil: authorize.net has duplicate protection that can be configured in its control panel to prevent, but i want this built in to the checkou
(07:31:09 PM) Kapil: checkin meeting?
(07:31:23 PM) cjj: hazmat: we are about to get kicked out...so if you could hang around for a few minutes more i can make sure they understand
(07:31:39 PM) cjj: hazmat: yes, end of day 60+ sprinter checkin...
(07:31:50 PM) Kapil: right on
(07:31:59 PM) Kapil: i want to hear bout the plonegov/sqlalchemy folks
(07:32:15 PM) Kapil: could you find out whose working on sqlalchemy?
(07:32:20 PM) cjj: yes...they had it streaming on a p4a channel...
(07:32:35 PM) cjj: i think roche is...maybe gotcha also
(07:32:39 PM) Kapil: if you have a chance, i really want to touch base with those folks
(07:32:45 PM) cjj: (they are doing a sql / zope content testing)
(07:33:55 PM) Emanuel left the room (quit: "Konversation terminated!").
(07:34:02 PM) cjj: btw, i think issue 95 needs to be done for the release: http://code.google.com/p/getpaid/issues/detail?id=95
(07:34:29 PM) cjj: hazmat: and the other thing, i wonder if we need to get the donation dropdown price selector done for this release (given it is meant for ngos...)
(07:36:53 PM) cjj: hazmat: also, traffic nicely spiking on the site this week...
(07:37:13 PM) Kapil: cool
(07:37:40 PM) Kapil: and yes.. i gotta run.. more apt/condo showings
(07:39:25 PM) cjj: hazmat: ok, we will get an email to list with any questions
(07:39:35 PM) cjj: please try to respond today so we can get first thing tomorrow
(07:39:38 PM) cjj: thanks!
(07:40:10 PM) Kapil: sounds good, cheers
(07:41:04 PM) cjj: ciao!
(07:45:18 PM) Kapil left the room (quit: "This computer has gone to sleep").
```