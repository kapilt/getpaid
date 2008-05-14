from setuptools import setup, find_packages

setup(
    name="getpaid.pxpay",
    version="0.1",
    packages=find_packages('src'),
    package_dir={'':'src'},
    description = "PXPay payment plugin",
    license = "GPL",
    keywords = "getpaid pxpay payment",
    namespace_packages=['getpaid'],
    classifiers = [
        'Development Status :: 3 - Alpha',
        "License :: OSI Approved"],
    include_package_data=True,
    install_requires = [ 'setuptools',
                         'getpaid.core',
                         'zope.interface',
                         'zope.component',
                         'zc.ssl',
                         ],
    zip_safe = False,
    )
