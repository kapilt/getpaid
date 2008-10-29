from setuptools import setup, find_packages

setup(
    name="hurry.workflow",
    version="0.9.1",
    packages=find_packages('src'),
    
    package_dir= {'':'src'},
    
    namespace_packages=['hurry'],
    package_data = {
    '': ['*.txt', '*.zcml'],
    },

    zip_safe=False,
    author='Infrae',
    author_email='faassen@infrae.com',
    description="""\
hurry.workflow is a simple workflow system. It can be used to
implement stateful multi-version workflows for Zope 3 applications.
""",
    license='BSD',
    keywords="zope zope3",
    classifiers = ['Framework :: Zope3'],
    install_requires=['setuptools'],
    )
