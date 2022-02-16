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