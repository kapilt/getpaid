from setuptools import setup, find_packages

setup(
    name="yoma.batching",
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
Batching Tools
""",
    license='ZPL',
    keywords="zope zope3",
    )
