import unittest 
import romcom

class TestFileInput(unittest.TestCase):
    '''Provides set of test cases for unittest to run against romcom app functions and methods'''
    
    def test_movies_loaded(self):
        testlist=[]
        actual = romcom.load_movies(testlist)
        expected = romcom.Movie  # of class type Movie
        self.assertIsInstance(actual[0], expected)

    def test_movies_first(self):
        testlist=[]
        actual = romcom.load_movies(testlist)
        expected = 'tt225670300'  # imdb ID number of first movie stored in database
        self.assertEqual(actual[0].Id, expected)

    def test_movies_total(self):
        testlist=[]
        actual = romcom.load_movies(testlist)
        expected = 2566  # number of movie records currently in database
        self.assertEqual(len(actual), expected)

    def test_ratings_loaded(self):
        testlist=[]
        actual = romcom.load_ratings(testlist)
        expected = romcom.Rating # of class type Rating
        self.assertIsInstance(actual[0], expected)

    def test_ratings_first(self):
        testlist=[]
        actual = romcom.load_ratings(testlist)
        expected = '1996' # number of votes in first rating record currently in database
        self.assertEqual(actual[0].movieVotes, expected)

    def test_ratings_total(self):
        testlist=[]
        actual = romcom.load_ratings(testlist)
        expected = 1126  # number of rating records currently in database
        self.assertEqual(len(actual), expected)

    def test_roles_loaded(self):
        testlist=[]
        actual = romcom.load_roles(testlist)
        expected = romcom.Role  # of class type Role
        self.assertIsInstance(actual[0], expected)

    def test_roles_first(self):
        testlist=[]
        actual = romcom.load_roles(testlist)
        expected = 'tt2256703'  # imdb ID number of first movie stored in database
        self.assertEqual(actual[0].movieId, expected)

    def test_roles_total(self):
        testlist=[]
        actual = romcom.load_roles(testlist)
        expected = 4707  # number of role records currently in database
        self.assertEqual(len(actual), expected)
    
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

# use testrunner for unittest
if __name__=='__main__':
    unittest.main()

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
