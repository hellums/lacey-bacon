# romcom.py 2/11/22 12:20 PM
""" Provides a menu screen where user can select various IMDB movie functions"""

# Import os module for system calls to cls and clear (screen)
import os  # for system calls to clear screen
import csv  # to import TSV files for movie and actor lists
import unittest 
import requests #needs install
import gzip
import re
import pandas as pd #needs install
import matplotlib.pyplot as plt #needs install
import networkx as nx #needs install

# Define global variables
contender = 'nm0000327'  # Lacy Chabert ID for early prototyping, probably won't keep
watchlist, movie_list, actor_list, role_list, rating_list = [] # for processing Hallmark_imdb-related data
nm_name, nm_tt, nm_nm = {} # for actor/actress name lookup, filmography, and costar data
tt_title, tt_nm = {} # for movie title lookup, cast/crew data
imdb_graph, degree_ity, between_ity, close_ity = [] # for NX graph, centrality, shortest_path data

# Define main function to print menu and get user choice
def main():
    """ Command-line menu of functions that process a curated IMDB list of Hallmark original movies (romcom, mystery, drama, western)"""
    
    # Clear the screen
    clrscr()

    # Load data from files into list of class objects
    #download_uncompress_imdb_files()  # get imdb source files from web
    print('\nAll files downloaded and uncompressed!')
    load_dataframes_lists()  # load local files into data structures
    export_dataframes()  # write datasets to local json and csv files
    imdb_graph = graph_database()
    imdb_sp = shortest_path(imdb_graph)
    imdb_separation = degree_separation(imdb_graph)
    print('')
    
    # Loop through main menu until user opts to exit
    while(True):

        # Print instructions and menu
        print('\nPlease enter a number between 1 and 6.\n')
        print_menu()

        # Get user's menu choice and verify entry of number, not other char or string
        option = ''
        try:
            option = int(input('\nEnter your choice (1-6) and the ENTER/RETURN key: '))
        except:
            print('\nNumbers only, please...')

        # Launch whichever function the user selected from the main menu
        if option == 0:  # for debug only, to be removed later
            clrscr()
            option0(option)
        elif option == 1:
            clrscr()
            option1(option)
        elif option == 2:
            clrscr()
            option2(option)
        elif option == 3:
            clrscr()
            option3(option)
        elif option == 4:
            clrscr()
            option4(option)
        elif option == 5:
            clrscr()
            option5(option)
        elif option == 6:
            clrscr()
            print('\'Option 6\' selected, our work is done here.')
            print("\nDon\'t have a good day... Have a great day!\n")
            exit()
        else:
            pass

def clrscr():  # clears screen in Mac, Linux, or Windows
  # Check if Operating System is Mac and Linux or Windows
  if os.name == 'posix':
    _ = os.system('clear')
  else:
      # Else Operating System is Windows (os.name = nt)
    _ = os.system('cls')

def notImplementedYet(option):  # stub for drivers and testing
  separator = '\n******************************************************\n'
  print(separator)
  print("'Option", str(option) + "' selected. This section not implemented yet.")
  print(separator)

def print_menu():  # builds a basic menu screen for user to select program feature sets
    menu_options = {  # dictionary of menu options
        1: 'Filmography - See what movies a select person starred in',
        2: 'Cast - See who starred in a select movie',
        3: 'Costars - See any movie(s) two select people starred in',
        4: 'Leaderboard - ("Hallmark" TV RomComDram Hall of Fame)',
        5: 'About - See more about this project',
        6: 'Exit',
}
    # Loop for main menu until user selects to exit program
    for key in menu_options.keys():
        print (str(key) + '. ', menu_options[key] )

# Define functions launched when chosen from main menu by user

def option1(option):  
  notImplementedYet(option)  # driver, eventually replaced by validated features
  
def option2(option):
 
  notImplementedYet(option)  # driver, eventually replaced by validated features

def option3(option):
 
  notImplementedYet(option)  # driver, eventually replaced by validated features

def option4(option):
 
  notImplementedYet(option)  # driver, eventually replaced by validated features

def option5(option):

  notImplementedYet(option)  # driver, eventually replaced by validated features

def option6(option):
 
  notImplementedYet(option)  # driver, eventually replaced by validated features

def option0(option):  # for debug only, to be replaced later with 'easter egg'
  """ (for testing purposes only) Validate records loaded from file and addressable"""
  
  global contender, movie_list, actor_list, role_list, rating_list

  contenderMoviesIndex = getContenderMoviesIndex()
  print("\ncontenderMovieIndex", contenderMoviesIndex)
  contenderMovieIds = getContenderMovieIds(contenderMoviesIndex)
  print('\ncontenderMovieIds\n', contenderMovieIds) 
  
  total = 0.0
  count = 0
  average = 0.0
  for line in rating_list:
      total = total + float(line.movieRating)
      count = count + 1
  average = total/count

  print ( "\nactor records: \t", len(actor_list))
  print ( "movie records: \t", len(movie_list))
  print ( "role records: \t", len(role_list))
  print ( "rating records: ", len(rating_list))
  print ( "average rating: ", format(average, '.1f') )  

    #a few preliminary experimentation of functional commands
  print ( '\n'+actor_list[0].Id, actor_list[1].Id, type(actor_list), "\n" )
  print ( role_list.__sizeof__(), '\n' )
  print ( dir(Actor) )
  #next(item for item in movie_list if item["Id"] == "tt10921042", None)
  #help(print_menu)

def getContenderMovieIds(contenderMoviesIndex):
  """ Returns a list of movie IDs selected actor has starred in"""
  global role_list
  contenderMovieIds = []
  for item in contenderMoviesIndex:
    contenderMovieIds.append(role_list[item].movieId)
  return(contenderMovieIds)

def getContenderMoviesIndex():
  """ Returns a list of movie ID numbers for a selected actor's ID """ 
  global contender
  contenderMoviesIndex = [index for index, item in enumerate(role_list) if item.actorId == contender]
  return(contenderMoviesIndex)

def load_movies(movie_list):  
  """ Takes in an empty list, loads records from file, returns a list of Movie class ojects"""
  with open('src/data/title-basics-imdb.tsv', 'r', encoding='utf8') as f:
    data = csv.reader(f, delimiter='\t') #read tsv text file with csv
    for row in data:
      new_movie = Movie(row[0], row[1], row[2], row[3])
      movie_list.append(new_movie) #add the data from the text file to the list
  return(movie_list)

def load_ratings(rating_list):  
  """ Takes in an empty list, loads records from file, returns a list of Rating class ojects"""
  with open('src/data/title-ratings-imdb.tsv', 'r', encoding='utf8') as f:
    data = csv.reader(f, delimiter='\t') #read tsv text file with csv
    for row in data:
      new_rating = Rating(row[0], row[1], row[2])
      rating_list.append(new_rating) #add the data from the text file to the list
    return(rating_list)

def load_actors(actor_list):  
  """ Takes in an empty list, loads records from file, returns a list of Actor class ojects"""
  with open('src/data/name-basics-imdb.tsv', 'r', encoding='utf8') as f:
    data = csv.reader(f, delimiter='\t') #read tsv text file with csv
    for row in data:
      new_actor = Actor(row[0], row[1], row[2], row[3])
      actor_list.append(new_actor) #add the data from the text file to the list
    return(actor_list)

def load_roles(role_list):  
  """ Takes in an empty list, loads records from file, returns a list of Role class ojects"""
  with open('src/data/title-actors-imdb.tsv', 'r', encoding='utf8') as f:
    data = csv.reader(f, delimiter='\t')  # read tsv text file with csv
    for row in data:
      new_role = Role(row[0], row[1], row[2])
      role_list.append(new_role)  # add the data from the text file to the list
  return(role_list)

# Create classes, movie data courtesy of imdb.com (interface download)
class Movie:  
  """Creates Movie class for IMDB Hallmark/romcom movie records"""  
  def __init__(self, movieId, movieTitle="", movieRating=None, movieGenres="", movieRuntime=None, movieType="", movieYear=None, movieDirector="", movieActors=""):      
    self.Id = movieId
    self.Title = movieTitle
    self.Rating = movieRating
    self.Genres = movieGenres 
    self.Runtime = movieRuntime
    self.Type = movieType       
    self.Year = movieYear 
    self.Director = movieDirector
    self.Actors = movieActors

class Actor:  # Curated list, details of "Hallmark" leading actor and actress
  """ Creates Actor class: Id, Name, Born, Died"""
  def __init__(self, actorId, actorName="", actorBorn=None, actorDied=None):      
    self.Id = actorId
    self.Name = actorName
    self.Born = actorBorn
    self.Died = actorDied

class Role:  # Curated list. all leading actors and actresses starring in Hallmark movie list
  """ Creates Role class: movieId, actorId, actorRole"""  
  def __init__(self, movieId, actorId, actorRole):      
    self.movieId = movieId
    self.actorId = actorId
    self.actorRole = actorRole

class Rating:  # Curated list, rating details on "Hallmark" movies in list
  """ Creates Rating class: movieId, movieRating, movieVotes"""  
  def __init__(self, movieId, movieRating, movieVotes):      
    self.movieId = movieId
    self.movieRating = movieRating
    self.movieVotes = movieVotes

def download_uncompress_imdb_files():    
    print('\nThis process could take a few minutes, depending on Internet speed...')
    remote_url ='https://raw.githubusercontent.com/hellums/hallmarkish/root/watchlist.txt'  
    local_file = 'watchlist.txt'  # export of imdb watchlist
    download_file(remote_url, local_file)
    remote_url ='https://datasets.imdbws.com/title.ratings.tsv.gz'
    local_file = 'movie_ratings.tsv.gz'  # ratings and number votes, for some movies (not all)
    download_file(remote_url, local_file)
    uncompress_file(local_file, 'movie_ratings.tsv')
    remote_url ='https://datasets.imdbws.com/title.basics.tsv.gz'  
    local_file = 'movie_info.tsv.gz'  # detail and metadata about all imdb movies (pare down!)
    download_file(remote_url, local_file)
    uncompress_file(local_file, 'movie_info.tsv')
    remote_url ='https://datasets.imdbws.com/name.basics.tsv.gz'
    local_file = 'cast_crew_info.tsv.gz'  # personal details of cast and crew
    download_file(remote_url, local_file)
    uncompress_file(local_file, 'cast_crew_info.tsv')
    remote_url ='https://datasets.imdbws.com/title.principals.tsv.gz'
    local_file = 'movie_cast_crew.tsv.gz'  # list of major cast and crew for all movies (pare down!)
    download_file(remote_url, local_file)
    uncompress_file(local_file, 'movie_cast_crew.tsv')
    remote_url ='https://datasets.imdbws.com/title.crew.tsv.gz'
    local_file = 'movie_crew.tsv.gz'  # list of director and writers for all movies
    download_file(remote_url, local_file)
    uncompress_file(local_file, 'movie_crew.tsv')
    return None  # results of download_uncompress_imdb_files

def download_file(remote, local):
    print('\nDownloading', local)
    data = requests.get(remote)
    with open(local, 'wb') as file:
        file.write(data.content)
    return None

def uncompress_file(compressed, uncompressed):
    print('\nUncompressing', uncompressed)
    with gzip.open(compressed, 'rb') as f:
        data = f.read()
    with open(uncompressed, 'wb') as f:
        f.write(data)
    return None

def load_dataframes_lists():
    global watchlist = load_watchlist()
    assert len(watchlist) > 1100
    assert 'tt15943556' in watchlist
    global actor_list = load_actor_list()
    global role_list = load_role_list()
    global movie_list = load_movie_list()
    global rating_list = load_rating_list()
    return None

def load_watchlist():
    local_file = 'watchlist.txt'
    header_field = ['tconst']
    watchlist_info = pd.read_csv(local_file, names=header_field)
    return watchlist_info['tconst'].tolist() # refactor this to load direct to list, don't need a df?

def load_actor_list():
    local_file = 'cast_crew_info.tsv'
    cast_crew_info = pd.read_csv(local_file, sep='\t', usecols=[0, 1, 2, 3]) # refactor to pare based on actor list
    actorlist = cast_crew_info['nconst'].tolist()
    actorlist = list(set(actorlist))
    cast_crew_info = cast_crew_info[cast_crew_info['nconst'].isin(actorlist) == True]  # drop people not in Hallmark movies
    return cast_crew_info.tolist()

def load_role_list():
    local_file = 'movie_cast_crew.tsv'
    movie_cast_crew = pd.read_csv(local_file, sep='\t', usecols=[0, 2, 3])
    movie_cast_crew = movie_cast_crew[movie_cast_crew['tconst'].isin(watchlist) == True]  # drop movies not on/by Hallmark
    unwantedValues = ['writer', 'producer', 'director', 'composer', 'cinematographer', 
                    'editor', 'production_designer', 'self']  # should only leave actor, actress categories
    movie_cast_crew = movie_cast_crew[movie_cast_crew['category'].isin(unwantedValues) == False] # keep actor, actress rows
    movielist = movie_cast_crew['tconst'].tolist()
    return list(set(movielist))

def load_movie_list():  # load movies and ratings, merge and clean resulting dataset
    local_file = 'movie_info.tsv'
    movie_info = pd.read_csv(local_file, sep='\t', usecols=[0, 1, 2, 5, 7, 8], 
        dtype={'startYear': str, 'runtimeMinutes': str}, 
        converters={'genres': lambda x: re.split(',+', x)})  # converting genre string to a list
    movie_info = movie_info[movie_info['tconst'].isin(watchlist) == True]  # drop movies not on/by Hallmark
    movie_info['runtimeMinutes'] = movie_info['runtimeMinutes'].replace(to_replace=r"\N", value='80')  # fix imdb format error
    local_file = 'movie_ratings.tsv'  # only need this temporarily to add ratings and voters to movie_info df
    movie_ratings = pd.read_csv(local_file, sep='\t')
    movie_info = pd.merge(movie_info,
                        movie_ratings[['tconst', 'averageRating', 'numVotes']],
                        on='tconst', how='outer')  # adds the ratings and votes columns to the movie_info df
    movie_info = movie_info[:len(watchlist)]  # get rid of the NaN records from the merge, maybe refactor so not needed
    movie_info = movie_info.fillna(value={'averageRating':6.9,'numVotes':699})  # clean up <20 NaN values from csv import
    movie_info['runtimeMinutes'] = movie_info['runtimeMinutes'].astype(int)  # convert runtime to an int for proper processing
    movie_info['numVotes'] = movie_info['numVotes'].astype(int)  # convert column to an int for proper processing
    del movie_ratings # don't need it anymore, after outer join merge with movies
    return [set(movie_info)]

def export_dataframes():
    movie_info.to_json('./movie_info.json', orient='records')
    movie_info.to_csv('./movie_info.csv', sep='\t', orient='records')
    movie_cast_crew.to_json('./movie_info.json', orient='records')
    movie_cast_crew.to_csv('./movie_info.csv', sep='\t', orient='records')
    cast_crew_info.to_json('./movie_info.json', orient='records')
    cast_crew_info.to_csv('./movie_info.csv', sep='\t', orient='records')
    cast_crew_info.to_json('./movie_info.json', orient='records')
    cast_crew_info.to_csv('./movie_info.csv', sep='\t', orient='records')

def graph_database(nm_tt):
    G = nx.Graph()
    edge_attribute_dict = {}  # store weight of movie edges between costaring actors
    for name_ID, titles in nm_tt.items():
        G.add_node(name_ID)  # create a node for each movie title in the database
        for title in titles:  # for every one of those movies...
            for name_ID2, titles2 in nm_tt.items():  # and for each costar...
                if (title in titles2) and (titles2 != titles):  # if they aren't already matched
                    G.add_edge(name_ID, name_ID2)  # add an edge
                    name_ID_tuple = tuple(sorted((name_ID, name_ID2)))
                    if name_ID_tuple not in edge_attribute_dict:  # if they weren't already tagged as costars 
                        edge_attribute_dict[name_ID_tuple] = 1  # this is the first movie they were both in
                    else:
                        edge_attribute_dict[name_ID_tuple] += 1  # increase the weight of their connection
    for k,v in edge_attribute_dict.items():  # load and format the costar weights
        edge_attribute_dict[k] = {'weight':v}
    nx.set_edge_attributes(G, edge_attribute_dict)  # add the weighting factor to the graph edges
    return(G) 

def degree_separation(G):  # calculate all three for now
    between_ity = nx.betweenness_centrality(G)
    result_b = [(x, between_ity[x]) for x in sorted(between_ity, key=between_ity.get, reverse=True)]
    close_ity = nx.closeness_centrality(G)
    result_c = [(nm_Dict[x], close_ity[x]) for x in sorted(close_ity, key=close_ity.get, reverse=True)]
    degree_ity = nx.degree(G)
    result_d = [(nm_Dict[x], degree_ity[x]) for x in sorted(degree_ity, key=degree_ity.get, reverse=True)]
    return(result_b)  # but only return most accurate for this dataset    

def shortest_path(graph): # add this to menu item that needs it
    return nx.all_pairs_shortest_path(graph)

"""  # discard, early prototype approach, people and movies all as nodes, not as effective
def graph_database(nm_tt):
    G10 = nx.Graph()  
    names = {}
    node_color = []
    for n, star in enumerate(movie_cast_crew.nconst.unique()):
        name = nm_Dict[star]
        names[star] = name
        G10.add_node(name, {'type':'Star', 'color':'green'})
        #G1.add_node(name)
        #node_color.append('cyan')
    for n, movie in enumerate(movie_cast_crew.tconst.unique()):
        name = tt_Dict[movie]
        names[movie] = name
        G10.add_node(name, {'type': 'Movie', 'color':'blue'})    
    for row in movie_cast_crew.index:
        star = movie_cast_crew['nconst'][row]
        s_name = names[star]
        movie = movie_cast_crew['tconst'][row]
        m_name = names[movie]
        G10.add_edge(s_name, m_name)
"""

# Allow file to be used as function or program
if __name__=='__main__':
    main()