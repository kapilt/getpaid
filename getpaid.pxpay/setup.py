from setuptools import setup, find_packages

setup(
    name="getpaid.pxpay",
    version="0.1",
    classifiers=[
        "Framework :: Plone",
        "Framework :: Zope2",
        "Framework :: Zope3",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
    long_description=open("src/getpaid/pxpay/README.txt").read(),
    packages=find_packages('src'),
    package_dir={'':'src'},
    description = "PXPay payment plugin",
    license = "GPL",
    keywords = "getpaid pxpay payment",
    namespace_packages=['getpaid'],
    include_package_data=True,
    install_requires = [ 'setuptools',
                         'getpaid.core',
                         'zope.interface',
                         'zope.component',
                         'zc.ssl',
                         'elementtree',
                         ],
    zip_safe = False,
    )
