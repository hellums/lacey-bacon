# test_romcom.py 2/25/22 3:38 PM
import unittest 
import romcom
import romcomSQL  
import romcomPrep

class TestSqlRecords(unittest.TestCase):  

    # Create 3 or more unit tests for your application. Code Louisville requirement.

    def test_table1_loaded(self):
        print('Checking movie table...')
        table_name = 'movie_info'
        results = romcomSQL.count_records(table_name)
        for var in results:
            actual = var[0]
        expected = 1000
        self.assertLess(expected, actual, "movie_info < 1000 records")

    def test_table2_loaded(self):
        print('Checking movie_cast table...')
        table_name = 'movie_cast_crew'
        results = romcomSQL.count_records(table_name)
        for var in results:
            actual = var[0]
        expected = 4500  # should be 4702 or so
        self.assertLess(expected, actual, "movie_cast_crew < 4500 records")

    def test_table3_loaded(self):
        print('Checking cast_crew table...')
        table_name = 'cast_crew_info'
        results = romcomSQL.count_records(table_name)
        for var in results:
            actual = var[0]
        expected = 2300  # should be 2463 or so
        self.assertLess(expected, actual, "cast_crew_info < 2300 records")

    def test_table4_loaded(self):
        print('Checking leader_board table...')
        table_name = 'leader_board'
        results = romcomSQL.count_records(table_name)
        for var in results:
            actual = var[0]
        expected = 2300  # should be 2463 or so
        self.assertLess(expected, actual, "leader_board < 2300 records")
    
    def test_watch_list(self):
        results = list(romcomPrep.load_watchlist())
        actual = len(results)  # should be 1141-ish
        expected = 1000 
        self.assertLess(expected, actual, "Less than 1000 movies in list?")

if __name__=='__main__': # use testrunner for unittest
    unittest.main()