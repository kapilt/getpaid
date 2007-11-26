from setuptools import setup, find_packages

setup(
    name="getpaid.paymentech",
    version="0.1",
    packages=find_packages('src'),
    package_dir={'':'src'},
    namespace_packages=['getpaid'],
    include_package_data=True,
    install_requires = [ 'setuptools',
                         'getpaid.core',
                         'zc.ssl'
                         ],
    zip_safe = False,
    )
