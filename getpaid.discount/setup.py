from setuptools import setup, find_packages

setup(
    name="getpaid.discount",
    version="0.3",
    packages=find_packages('src'),
    package_dir={'':'src'},
    namespace_packages=['getpaid'],
    include_package_data=True,
    install_requires = ['setuptools'],
    zip_safe = False,
    )
