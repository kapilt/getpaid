getpaid.report
--------------

a one way synchronization of getpaid data structures to a rdbms for
the purpose of constructing reports.

setup
-----

you must configure the database url ... currently done in python..

 >> from getpaid.report import schema
 >> from sqlalchemy import create_engine

create a database connection

 >> db = create_engine('postgres://localhost/getpaid')

bind it to the metadata

 >> schema.metadata.bind = db

create the database tables

 >> schema.metadata.create_all()


reports
-------

report data is synchronized
