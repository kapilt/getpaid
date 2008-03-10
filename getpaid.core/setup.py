from setuptools import setup, find_packages

setup(
    name="getpaid.core",
    version="0.0.8",
    packages=find_packages('src'),
    package_dir={'':'src'},
    namespace_packages=['getpaid'],
    include_package_data=True,
    install_requires = [ 'setuptools',
                         ],
    zip_safe = False,
    )
