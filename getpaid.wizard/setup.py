from setuptools import setup, find_packages

setup(
    name="getpaid.wizard",
    version="0.2",
    install_requires=['setuptools'], # use in plone means bad requires spec
    dependency_links=['http://download.zope.org/distribution/',],
    packages=find_packages('src', exclude=["*.tests", "*.ftests"]),
    package_dir= {'':'src'},
    namespace_packages=['getpaid'],
    package_data = {
    '': ['*.txt', '*.zcml', '*.pt'],
    },
    zip_safe=False,
    author='Kapil Thangavelu',
    author_email='kapil.foss@gmail.com',
    description="""Sequence composition of views, viewlets, forms.""",
    license='X11',
    keywords="zope zope3",
    )
