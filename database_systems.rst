.. _dbs:

Database systems
=================

MySQL
-----

MySQL supports two UTF-8 variants:
* utf8mb4: This is the full UTF-8 character set supported since MySQL 5.5
* utf8: Also known as utf8mb3. This only supports the Basic Multilingual Plane of
Unicode 3.0 and doesn't support 4-byte characters.

.. seealso::
   https://dev.mysql.com/doc/refman/5.7/en/charset-unicode.html

In MySQL a character set is used on a per-column basis. A default characater set
for new columns is set on a table level. And the default for tables is set on
a database level.

.. todo:: Explain about setting defaults with ALTER DATABASE/TABLE/etc
.. todo:: Explain about conversions with MODIFY COLUMN / CONVERT TO..
.. todo:: Explain about connections (set unicode in connection string etc)


PostgreSQL
----------

Unicode support is set on database level. There is a cluster level default.

To create a database with UTF-8 support:
`createdb -E utf8`

To convert a non-unicode database to UTF-8 the recommended method is a dump/restore.

.. seealso::
   http://www.postgresql.org/docs/9.5/static/charset.html

SQLite
------

.. todo:: Add more databases: DB2, Oracle, SQL Server, etc.
