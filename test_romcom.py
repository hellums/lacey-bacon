# test_romcom.py 2/15/22 11:14 PM
import unittest 
import romcom
import romcom_sql  
import romcom_prep

class TestSqlRecords(unittest.TestCase):  

    # Create 3 or more unit tests for your application. Code Louisville requirement.

    def test_table1_loaded(self):
        print('Checking movie table...')
        table_name = 'movie_info'
        results = romcom_sql.count_records(table_name)
        for var in results:
            actual = var[0]
        expected = 1000
        self.assertLess(expected, actual, "movie_info < 1000 records")

    def test_table2_loaded(self):
        print('Checking movie_cast table...')
        table_name = 'movie_cast_crew'
        results = romcom_sql.count_records(table_name)
        for var in results:
            actual = var[0]
        expected = 4500  # should be 4702 or so
        self.assertLess(expected, actual, "movie_cast_crew < 4500 records")

    def test_table3_loaded(self):
        print('Checking cast_crew table...')
        table_name = 'cast_crew_info'
        results = romcom_sql.count_records(table_name)
        for var in results:
            actual = var[0]
        expected = 2300  # should be 2463 or so
        self.assertLess(expected, actual, "cast_crew_info < 2300 records")

    def test_table4_loaded(self):
        print('Checking leader_board table...')
        table_name = 'leader_board'
        results = romcom_sql.count_records(table_name)
        for var in results:
            actual = var[0]
        expected = 2300  # should be 2463 or so
        self.assertLess(expected, actual, "leader_board < 2300 records")
    
    def test_watch_list(self):
        results = list(romcom_prep.load_watchlist())
        actual = len(results)  # should be 1141
        expected = 1000 
        self.assertLess(expected, actual, "Less than 1000 movies in list?")

# use testrunner for unittest
if __name__=='__main__':
    unittest.main()

''' stash a few class-related tests, although superceded by functions in refactoring process    

    def test_actors_loaded(self):
        testlist=[]
        actual = romcom.load_actors(testlist)
        expected = romcom.Actor  # of class type Actor
        self.assertIsInstance(actual[0], expected)

    def test_actors_first(self):
        testlist=[]
        actual = romcom.load_actors(testlist)
        expected = '1956'  # birth year of first actress stored in database
        self.assertEqual(actual[0].Born, expected)

    def test_actors_total(self):
        testlist=[]
        actual = romcom.load_actors(testlist)
        expected = 3463  # number of actor records currently in database
        self.assertEqual(len(actual), expected)
'''

# wc -l *imdb.tsv for record count
# actors   3463 src/data/name-basics-imdb.tsv
# roles    4707 src/data/title-actors-imdb.tsv
# movies    2566 src/data/title-basics-imdb.tsv
# ratings    1126 src/data/title-ratings-imdb.tsv

# head -1 *imdb.tsv for first records
#==> actors = src/data/name-basics-imdb.tsv <==
#nm0000137       Bo Derek        1956    NAN
#==> roles = src/data/title-actors-imdb.tsv <==
#tt2256703       nm0005129       actor
#==> movies = src/data/title-basics-imdb.tsv <==
#tt2256703       tvMovie Hitched for the Holidays        2012    87      Drama,Romance
#==> ratings = src/data/title-ratings-imdb.tsv <==
#tt2256703       6.6     1996

# available unittest methods
# Method	            Assertion
# assertEqual(a, b)     a == b
# assertNotEqual(a, b)	a != b
# assertTrue(a)	        bool(a) is True
# assertFalse(a)	    bool(a) is False
# assertIsNone(a)	    a is None
# assertIsNotNone(a)	a is not None
# assertIn(a, b)	    a in b
# assertNotIn(a, b)	    a not in b
