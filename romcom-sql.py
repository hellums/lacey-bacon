# romcom-sql.py dbh 2/15/22 12:40 PM
# Import flat file ORM database module
import sqlite3
      
# Connect to sqlite3 database for Hallmark imdb movie database and tables
conn=sqlite3.connect('romcom.db')

# Connect to database and validate that all tables were properly created
try:
  # Method 1 - Query sqlite_master
  conn = sqlite3.connect('romcom.db')
  print('Connected to SQLite romcom.db')
  sql_query = ('''SELECT name FROM sqlite_master  
            WHERE type='table';''')
  cursor=conn.cursor()
  cursor.execute(sql_query)
  print(cursor.fetchall())

  # Method 2 - Query sqlite_schema. Didn't work on Mac initially (odd)
  sql_query = ('''
  SELECT name FROM sqlite_schema
    WHERE type='table'
    ORDER BY name;
    ''')
  cursor=conn.cursor()
  cursor.execute(sql_query)
  print(cursor.fetchall())

  # Close database connection
  conn.close()

except sqlite3.Error as error:
  print('Failed to execute the above query', error)        

finally:
  if conn:
    conn.close()
    print('the SQLite3 connection is closed')

conn = sqlite3.connect('romcom.db')
print('Connected to SQLite romcom.db')
sql_query = ('''SELECT * FROM movie_info
  WHERE tconst='tt13831504';''')
cursor=conn.cursor()
cursor.execute(sql_query)
print(cursor.fetchall())
conn.close()