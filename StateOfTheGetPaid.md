# State of the GetPaid #

## Review ##

Plone GetPaid has come along way over the last 8 months..


## Roadmap ##

Getting getpaid up to the point where its possible to add nice functionality soley contained
with a plugin, without modification of the core, and without resorting to zcml overrides.

There's a number of customization / feature / plugin issues that people have run into,
i think getpaid is best served by being made more pluggable, rather try to bake all our
features into the the existing components. most of this document tries to address issues
that people have had and propose refactoring for getpaid. some of these refactorings
where noted are already in progress.

### async processor integration ###

from a plugin perspective, customizing checkout via overrides for a new
component shouldn't be nesc. but this is definitely a trade off
because we'll have to have site integrators configuring persistent state
in components, and that has a maintenance cost.

the common case of async processors needs some additional support from
the checkout and cart views, for this plugin use case. the checkout system
needs to defer to payment processors which operate asynchronously to provide
their own checkoutbutton. async processors are queried for a checkoutbutton
view. which gets rendered in line with the form buttons and replaces the default
checkout action.

also another checkout button usage point is also optionally just
allowing users to checkout from the review shopping cart ui, controlled
via a setting allow direct checkout from cart, suggestions welcome.

### installation of persistent utilities as plugins ###

we need to accomodate plugins which have additional state and settings
to maintain, wiring them into the product is painful, and distribution
as python product packages, has shown itself to be too error prone.

instead we'll utilize a subscription adapter against a getpaid install
and uninstall event, and plugins can configure subscribers for the event
and handle their own state management, without any explicit/separate state
installation.

### utilities for settings ###

using adapters on the store was a mistake in hindsight, it creates a few
convulted code paths to carry or find context to get access to settings.

i propose that we change all settings to instead reside in utility settings,
and register backwards compatible adapters that defer to the utilities.

### ui customization ###

currently customizing either any of the content ui for getpaid, means replacing
view implementations, with the exception of the admin and cart ui, which are using
viewlets, and easy to plugin in additional ui components into...

but end user visible ui components need to be controlled and modified by the site
integrator, to allow for enabling components and ordering them. so i propose continuing
the viewletification of the end-user visible views ( content, checkout views ) and
allowing site administrators/integrators to manage them in the getpaid admin ui, utilizing
a persistent viewlet manager which delegates to store settings, and to additionally
allow viewlet appearance conditionally on zcml specified security checks.

one interesting feature of viewlets to keep in mind is that they, allow for arbitary class
fields to be specified in zcml, which can be processed by a viewlet.

### dropping plone 2.5 compatibility ###

getpaid pushes the edge on zope3 usage, and the support for this in plone 3 is greatly expanded,
as well being a more recent version of zope3, maintaining compatibility between these two is
non trivial as we add more and more features, as there are incompatibilities between the two
zope3 versions.

### refactoring checkout process ###

Currently the checkout process is a pain to customize, and has a number of issues

  * hard to customize without overrides
  * tightly coupled sequence of views.
  * schema validation and value extraction for the whole checkout is bound to each step.
  * hard to insert custom steps or remove defaults.

i'm hoping that viewlet conversion will address some of the ui concerns, but customizing
of the sequence of steps needs to be a bit easier as well. to that end i've setup refactoring
the checkout wizard into a separate package ( getpaid.wizard ), that abstracts out the
core concerns to view/viewlet sequence management our of the checkout code. Additional
Technical Details can be found here GetpaidWizard





