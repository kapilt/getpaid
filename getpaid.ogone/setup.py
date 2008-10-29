from setuptools import setup, find_packages

setup(
    name="getpaid.ogone",
    version="0.1",
    packages=find_packages('src'),
    package_dir={'':'src'},
    description = "Ogone payment plugin",
    license = "GPL",
    keywords = "getpaid ogone payment",
    namespace_packages=['getpaid'],
    classifiers = [
        'Development Status :: 3 - Alpha',
        "License :: OSI Approved"],
    include_package_data=True,
    install_requires = [ 'setuptools',
                         'getpaid.core',
                         'zope.interface',
                         'zope.component',
                         ],
    zip_safe = False,
    )
