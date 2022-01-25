import unittest 
import romcom

def test_movies():
    test_list = []
    romcom.load_movies(test_list)
    assert 'tt2256703' in test_list[0].Id, "in load_movies, first movie ID in file should be tt2256703"

def test_actors():
    test_list = []
    romcom.load_actors(test_list)
    assert 'Bo Derek' in test_list[0].Name, "in load_actors, Bo Derek should be the first actress"
    assert int(test_list[0].Born) == 1956, "in load_actors, Bo Derek's birth year should be 1956"

def test_roles():
    test_list = []
    romcom.load_roles(test_list)
    assert 'nm0005129' in test_list[0].actorId, "in load_roles, first actor ID should be nm0005129"
    assert 'tt2256703' in test_list[0].movieId, "in load_roles, first movie ID should be nm0005129"    

def test_ratings():
    test_list = []
    romcom.load_ratings(test_list)
    assert '1996' in test_list[0].movieVotes
    assert int(test_list[0].movieVotes) == 1996, "in load_ratings, first rating in movie should have 1996 votes"

def main():
    test_actors()
    test_movies()    
    test_roles()
    test_ratings()    
    # should add a known count of records in each file, as additional test
    print('All tests passed') # files loaded properly into list of class objects

# Allow file to be used as function or program
if __name__=='__main__':
    main()
