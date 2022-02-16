# romcom-sql.py dbh 2/15/22 1:32 PM
# Import flat file ORM database module
import sqlite3

def main():

  # Connect to sqlite3 database for Hallmark imdb movie database and tables
  conn=sqlite3.connect('romcom.db')

  # Connect to database and validate that all tables were properly created
  try:
    
    # Method 1 - Query sqlite_master
    #conn = sqlite3.connect('romcom.db')
    #print('Connected to SQLite romcom.db')
    sql_query = ('''SELECT name FROM sqlite_master  
              WHERE type='table';''')
    cursor=conn.cursor()
    cursor.execute(sql_query)
    print('\n', cursor.fetchall())

    """
    Method 2 - Query sqlite_schema. Didn't work on Mac initially (odd)
    sql_query = ('''
    SELECT name FROM sqlite_schema
      WHERE type='table'
      ORDER BY name;
      ''')
    cursor=conn.cursor()
    cursor.execute(sql_query)
    print(cursor.fetchall())
    """

  except sqlite3.Error as error:
    print('Failed to execute the above query', error)        

  #finally:
   # if conn:
    #  conn.close()
     # print('the SQLite3 connection is closed')

  # Connect to a database and read data using SQL - Code Louisville requirement
  #conn = sqlite3.connect('romcom.db')
  #print('Connected to SQLite romcom.db')
  sql_query = ('''SELECT * FROM movie_info
    WHERE tconst='tt13831504';''')
  cursor=conn.cursor()
  cursor.execute(sql_query)
  print(cursor.fetchall(), '\n')

  sql_query = ('''SELECT tconst, primaryTitle, runtimeMinutes FROM movie_info 
    WHERE startYear=2022;''')
  cursor=conn.cursor()
  cursor.execute(sql_query)
  print(cursor.fetchall(), '\n')

  sql_query = ('''SELECT sql FROM sqlite_schema
    ORDER BY tbl_name, type DESC, name''')
  cursor=conn.cursor()
  cursor.execute(sql_query)
  print(cursor.fetchall(), '\n')

  for table_name in ['leader_board', 'movie_cast_crew', 'cast_crew_info', 'movie_info']:
    results = count_records(table_name)
    for var in results:
      total = var[0]
    print(table_name, 'has', total, 'records')

  # Close database connection
  conn.close()
  return None

def count_records(table_name):
  conn = sqlite3.connect('romcom.db')
  #conn = sqlite3.connect('romcom.db')
  sql_query = "SELECT COUNT(*) FROM "+table_name
  cursor=conn.cursor()
  cursor.execute(sql_query)
  results = cursor.fetchall()
  return results
  
# Allow file to be used as function or program
if __name__=='__main__':
    main()

#[('tt13831504', 'tvMovie', 'It Was Always You', '2021', 86, 'Comedy,Drama,Romance', 7.1, 1452), 
# ('tt13831504', 'tvMovie', 'It Was Always You', '2021', 86, 'Comedy,Drama,Romance', 7.1, 1452)] 


'''
CREATE TABLE IF NOT EXISTS "movie_info" (
"tconst" TEXT,
  "titleType" TEXT,
  "primaryTitle" TEXT,
  "startYear" TEXT,
  "runtimeMinutes" INTEGER,
  "genres" TEXT,
  "averageRating" REAL,
  "numVotes" INTEGER
);
CREATE TABLE IF NOT EXISTS "movie_cast_crew" (
"tconst" TEXT,
  "nconst" TEXT,
  "category" TEXT
);
CREATE TABLE IF NOT EXISTS "cast_crew_info" (
"nconst" TEXT,
  "primaryName" TEXT,
  "birthYear" TEXT,
  "deathYear" TEXT
);
CREATE TABLE IF NOT EXISTS "leader_board" (
"Hall of Famer" TEXT,
  "Hallmark-o-Meter" TEXT
);
'''