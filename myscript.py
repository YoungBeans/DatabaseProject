from __future__ import print_function

import cx_Oracle

connection = cx_Oracle.connect("test", "database", "localhost:1521/oracl")

cursor = connection.cursor()
cursor.execute("""
    SELECT empno, sal
    FROM emp
    """)

for empno, sal in cursor:
    print("Values", empno, sal)

cursor.close()
connection.close()