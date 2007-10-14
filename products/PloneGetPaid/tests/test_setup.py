from base import PloneGetPaidTestCase


class TestProductInstall(PloneGetPaidTestCase):

    def testNothing(self):
        pass
    

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestProductInstall))
    return suite
