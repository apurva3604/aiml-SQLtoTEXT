import sqlite3
##connect to sqlite3
connection=sqlite3.connect("student.db")
##create a cursor object to insert record,create table,retrieve data
cursor=connection.cursor()
##create the table
table_info="""
create TABLE STUDENT(NAME VARCHAR(25),CLASS VARCHAR(25),SECTION VARCHAR(25),MARKS INT);
"""

cursor.execute(table_info)

##insert more records
cursor.execute('''insert into STUDENT values('apurva','biology','A','100')''')
cursor.execute('''insert into STUDENT values('hardika','math','B','80')''')
cursor.execute('''insert into STUDENT values('kratika','math','A','75')''')
cursor.execute('''insert into STUDENT values('hiral','biology','B','50')''')
cursor.execute('''insert into STUDENT values('janhavi','biology','A','60')''')

#display the inserted records
print("The inserted records are")
data=cursor.execute('''Select * From STUDENT''')
for row in data:
    print(row)

#close the connection
connection.commit()
connection.close()
