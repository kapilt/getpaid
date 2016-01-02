# Introduction #

GetPaid remote sprints started in August and we decided to continue them every Friday. This is an organizing place for that. If you are interested to sprint, please check out the info below. We have a lot to do that ranges from project organization, cleanup, product packaging, new features, issue fixing and release creation.

### Sprint dates ###
  * Every Friday afternoon in #getpaid

# Topics & Interests #

See the list below and add your name next to anything you would be interested to work on:

## Distribution ##
  * Eggify components and get to pypi (everything in externals already there)
    * getpaid.warehouse
    * getpaid.report
  * Finish GetPaid recipe; Document usage
  * Buildouts:
    * Test and finish reorganization (base, 30, 25, currently on meteoroid-branch) and document buildouts (how to add getpaid)
      * Document and use in DevGettingStarted
      * Merge branch or copy files on existing buildout

## Bugs & Issues ##
  * fix issues
    * [Issue #209](https://code.google.com/p/getpaid/issues/detail?id=#209)
    * [Issue #202](https://code.google.com/p/getpaid/issues/detail?id=#202)
    * [Issue #117](https://code.google.com/p/getpaid/issues/detail?id=#117)
    * Improve paypal processor: make multi-item checkout possible, make/fix admin screen for processor

## i18n ##
  * update translations
    * Spanish: in progress (FranGM, Wu, cjj)
    * French (very close to done)
    * German
    * Italian
    * Chinese
    * Dutch

## Testing ##
  * add greater test coverage:
    * getpaid.report

## Documentation ##
  * gather/improve/update/add documentation (list specific here)
    * How to wire payment process to a workflow state change (ie create a piece of content, but pay before it is published)
    * How to get and use getpaid.formgen
      * First part drafted: HowToGetGetpaidDotFormgen
    * How to customize the checkout process (including using available slots, ie for comments)
    * Enabling components in buildouts
    * Using the new buildouts
    * Using the recipe
    * Review mailing list and document errors messages (on plone.org doc collection) and how to fix them
    * How to get and use getpaid.salesforce
  * ReorganizeIssueTracker (in progress; cjj, gabrielle)

## Release prep ##
  * 0.7.0 release (would support 2.5 and 3 together)
    * update changelog on plone.org/products/getpaid
    * branch code
  * make a branch to separate future 2.5 and 3 support (dennis)


## Features ##
  * implement flat rate tax calculation (6ftup, dennis, dixond)
  * improve Discount product (6ftup)
  * improve PloneFormGenAdapter and document (ifPeople, dennis)
  * finalize Paypal ipn (dennis)
  * document payable content use case (dennis, dixond, cjj)
  * improve getpaid.salesforce for general mapping (perrito666, duffyd)

DONE:
  * refactor svn repository (6ftup): see [svnrefactor](http://code.google.com/p/getpaid/wiki/svnrefactor) proposal and info
  * How to manage inventory
    * Review and improve [content type integration for devs doc](http://code.google.com/p/getpaid/source/browse/Products.PloneGetPaid/trunk/Products/PloneGetPaid/docs/development/make-content-types-buyable.txt)
    * How to show price (or other GetPaid properties) on a template in your site