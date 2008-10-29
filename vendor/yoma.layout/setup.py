from setuptools import setup, find_packages

setup(
    name="yoma.layout",
    version="0.2.1",
    packages=find_packages('src'),
    package_dir= {'':'src'},
    namespace_packages=['yoma'],
    package_data = {
    '': ['*.txt', '*.zcml', '*.gif', '*.js', '*.pt'],
    },
    zip_safe=False,
    author='',
    author_email='',
    description="""\
Zope FormLib Extensions to add form layout capabilities.
""",
    license='ZPL',
    keywords="zope zope3",
    )
