from zope.app.component.interfaces import ISite
from zope.app.intid.interfaces import IIntIds
from zope.component import getUtility

from getpaid.core.interfaces import IOrderManager, IStore
from Products.PloneGetPaid import _GETPAID_DEPENDENCIES_

from base import PloneGetPaidTestCase



class TestProductInstall(PloneGetPaidTestCase):
    # XXX need test for teardown_store (and all uninstallers)

    def testNothing(self):
        pass #is this test useful? [chipaca, 2007-10-14]

    def test_portal_is_a_site(self):
        self.assert_(ISite.providedBy(self.portal))

    def test_portal_is_a_store(self):
        self.assert_(IStore.providedBy(self.portal))

    def test_order_manager_is_setup(self):
        sm = self.portal.getSiteManager()
        self.assert_(list(sm.getUtilitiesFor(IOrderManager)))

    def test_intid_is_setup(self):
        self.assert_(getUtility(IIntIds, context=self.portal) is not None)

    def test_dependencies_are_installed(self):
        qi = self.portal.portal_quickinstaller
        installed = dict.fromkeys([i['id']
                                   for i in qi.listInstalledProducts()])
        for dep in _GETPAID_DEPENDENCIES_:
            self.assert_(dep in installed)

    def test_portlets_are_installed(self):
        right_slots = self.portal.getProperty('right_slots')
        if not isinstance( right_slots, str):
            right_slots = "\n".join(list(right_slots))
        self.assert_('portlet-shopping-cart' in right_slots)
        self.assert_('portlet-contentwidget' in right_slots)
        
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestProductInstall))
    return suite
