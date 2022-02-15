# romcom-sql.py
# Import flat file ORM database module
import sqlite3
      
# Create sqlite3 database for Hallmark imdb movie database tables
conn=sqlite3.connect('movie_info.db')

# create movie table
cur=conn.cursor()
""" don't need to create these anymore, done during romcom_prep
  cur.execute('''CREATE TABLE IF NOT EXISTS movie
  (movieId TEXT PRIMARY KEY,
  title TEXT,
  rating REAL,
  genres TEXT,
  runtime INTEGER,
  type TEXT,
  year INTEGER,
  director TEXT, 
  actors TEXT);''')

# create actor table
cur=conn.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS actor
  (actorId TEXT,
  name TEXT,
  born TEXT,
  died TEXT);''')
  
# create role table
cur=conn.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS role
  (movieId TEXT,
  actorId TEXT,
  role TEXT);''')

# create rating table
cur=conn.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS rating
  (movieId TEXT,
  rating REAL,
  votes INT);''')
  
# Close database connection
conn.close()"""

# Validate that all tables were created in the movie database
try:
  # Method 1 - Query sqlite_master
  sqliteConnection = sqlite3.connect('movie_info.db')
  print('Connected to SQLite movie_info.db')
  sql_query = ('''SELECT name FROM sqlite_master  
WHERE type='table';''')
  cursor=sqliteConnection.cursor()
  cursor.execute(sql_query)
  print(cursor.fetchall())

  # Method 2 - Query sqlite_schema. Didn't work on Mac initially (odd)
  sql_query = ('''
  SELECT name FROM sqlite_schema
    WHERE type='table'
    ORDER BY name;
    ''')
  cursor=sqliteConnection.cursor()
  cursor.execute(sql_query)
  print(cursor.fetchall())

  # Close database connection
  sqliteConnection.close()

except sqlite3.Error as error:
  print('Failed to execute the above query', error)        

finally:
  if sqliteConnection:
    sqliteConnection.close()
    print('the SQLite3 connection is closed')

sqliteConnection = sqlite3.connect('movie_info.db')
print('Connected to SQLite movie_info.db')
sql_query = ('''SELECT * FROM movie_info  
  WHERE tconst='tt13831504';''')
cursor=sqliteConnection.cursor()
cursor.execute(sql_query)
print(cursor.fetchall())
sqliteConnection.close()

# Validation output:
  # Connected to SQLite movie.db
  # [('movie',), ('actor',), ('role',), ('rating',)]
  # the SQLite3 connection is closed
