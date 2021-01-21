import cx_Oracle

conn = cx_Oracle.connect('proICT/TUITION@localhost:1521/xe')
print(conn.version)