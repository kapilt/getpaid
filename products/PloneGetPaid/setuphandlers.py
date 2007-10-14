from StringIO import StringIO

from Products.PloneGetPaid.Extensions.install import install_dependencies
from Products.PloneGetPaid.Extensions.install import install_cart_portlet 
from Products.PloneGetPaid.Extensions.install import install_contentwidget_portlet
from Products.PloneGetPaid.Extensions.install import setup_site
from Products.PloneGetPaid.Extensions.install import setup_store
from Products.PloneGetPaid.Extensions.install import setup_order_manager
from Products.PloneGetPaid.Extensions.install import add_intids

def setupVarious(context):
    """Import steps that are not handled by GS import/export handlers can be
    defined in the setupVarious() function.
    See Products.GenericSetup.context.BaseContext to see what you can do with
    ``context`` (the function argument).
    For instance, it is possible to get the Plone Site object:
    ``site = context.getSite()``
    """
    if context.readDataFile('PloneGetPaid.setupVarious.txt') is None:
        return

    # Now do something useful
    site = context.getSite()

    logger = context.getLogger("PloneGetPaid")
    out = StringIO()

    print >> out, "Installing Dependencies"
    install_dependencies(site)

    print >> out, "Installing Cart Portlet"
    install_cart_portlet(site)

    print >> out, "Installing Content Widget Portlet"
    install_contentwidget_portlet(site)

    print >> out, "Installing Local Site"
    setup_site(site)

    print >> out, "Installing Store Marker Interface"
    setup_store(site)

    print >> out, "Installing Order Local Utility"
    setup_order_manager(site)

    print >> out, "Installing IntId Utility"
    add_intids(site)

    logger.info(out.getvalue())

    return "Setup various finished"

