#!/usr/bin/env python3

# from __future__ import annotations

import os
import sys
import time
import apsw

# Note: this code uses Python's optional typing annotations.  You can
# ignore them and do not need to use them
from typing import Optional, Iterator, Tuple

###
### Check we have the expected version of apsw and sqlite
###

print("      Using APSW file", apsw.__file__)  # from the extension module
print("         APSW version", apsw.apswversion())  # from the extension module
print("   SQLite lib version", apsw.sqlitelibversion())  # from the sqlite library code
print("SQLite header version", apsw.SQLITE_VERSION_NUMBER)  # from the sqlite header file at compile time

connection = apsw.Connection("dbfile.sqlite")

cursor = connection.cursor()
cursor.execute("create table foo(x,y,z)")

connection.execute("insert into foo values(?,?,?)", (1, 1.1, None))  # integer, float/real, Null
connection.execute("insert into foo(x) values(?)", ("abc", ))  # string (note trailing comma to ensure tuple!)
connection.execute(
    "insert into foo(x) values(?)",  # a blob (binary data)
    (b"abc\xff\xfe", ))