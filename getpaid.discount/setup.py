from setuptools import setup, find_packages

setup(
    name="getpaid.discount",
    version="0.1",
    packages=find_packages('src'),
    package_dir={'':'src'},
    namespace_packages=['getpaid'],
    include_package_data=True,
    install_requires = [],
    zip_safe = False,
    )
