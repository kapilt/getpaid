getpaid.report
--------------

a one way synchronization of getpaid data structures to a rdbms for
the purpose of constructing reports.

setup
-----

setup the database schema
=========================

installing this getpaid.warehouse also creates a script, in a buildout
its installed to $(buildout-directory)/bin/setup-report-db

the script is invoked with the sqlalchemy database url. for example,
to setup a postgres database:
  
  # createdb is the standard postgres tool for creating databases
  $ createdb getpaid  
  $ ./bin/setup-report-db postgres://localhost/getpaid
  ... output of database creation script


setting up the zope database connection
======================================= 

you must configure the database url ... currently done in python from
an existing product.

 >> from getpaid.report import schema
 >> from sqlalchemy import create_engine

create a database connection to the database we're using

 >> db = create_engine('postgres://localhost/getpaid')

bind it to the metadata

 >> schema.metadata.bind = db

