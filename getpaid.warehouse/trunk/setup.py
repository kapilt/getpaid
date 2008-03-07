from setuptools import setup, find_packages

setup(
    name="getpaid.warehouse",
    version="0.2",
    packages=find_packages('src'),
    package_dir={'':'src'},
    namespace_packages=['getpaid'],
    include_package_data=True,
    install_requires = [ 'setuptools',
                         'getpaid.core',
                         ],
    zip_safe = False,
    )
