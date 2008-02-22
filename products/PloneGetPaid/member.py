from getpaid.core import options, interfaces
from Products.PloneGetPaid.i18n import _
from Products.CMFPlone.utils import getSiteEncoding


class ContactInfo( options.PropertyBag ):
    title = _("Contact Information")

ContactInfo.initclass( interfaces.IUserContactInformation )

class ShipAddressInfo( options.PropertyBag ):
    title = "Shipping Information"

ShipAddressInfo.initclass( interfaces.IShippingAddress )

class BillAddressInfo( options.PropertyBag ):
    title = "Payment Information"

BillAddressInfo.initclass( interfaces.IBillingAddress )

def memberContactInformation( user ):
    """
    adapt a member to contact information, based on thier settings
    we assume a default user from a plone site
    """
    # go from the user to the site via a user containment acquisition
    # ( user, userfolder, container)
    store = user.aq_inner.aq_parent.aq_parent
    if not interfaces.IStore.providedBy( store ):
        return None

    # get a member which will properly wrap up a user in a member object
    member = store.portal_membership.getMemberById( user.getId() )

    # get contact information for default members from settings
    email = member.getProperty('email')
    name = member.getProperty('fullname')

    # get the site encoding
    encoding = getSiteEncoding(store)

    info = ContactInfo()
    info.email = unicode(email, encoding)
    info.name = unicode(name, encoding)
    return info

def memberBillAddressInfo( user ):
    return memberBillAndShipAddressInfo( user, BillAddressInfo, 'bill' )

def memberShipAddressInfo( user ):
    return memberBillAndShipAddressInfo( user, ShipAddressInfo, 'ship'  )


def memberBillAndShipAddressInfo( user, BillOrShipAddressInfo, objectName ):
    """
    adapt a member to billing and shipping address information, based on thier settings
    we assume a default user from a plone site
    """
    # go from the user to the site via a user containment acquisition
    # ( user, userfolder, container)
    store = user.aq_inner.aq_parent.aq_parent
    if not interfaces.IStore.providedBy( store ):
        return None

    # get a member which will properly wrap up a user in a member object
    member = store.portal_membership.getMemberById( user.getId() )

    # get contact information for default members from settings
    address = member.getProperty('location')

    # get the site encoding
    encoding = getSiteEncoding(store)

    AddressInfo = BillOrShipAddressInfo()
    AddressInfo.__setattr__('%s_first_line' % objectName, unicode(address, encoding))

    return AddressInfo


