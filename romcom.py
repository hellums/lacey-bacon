# romcom.py 2/12/22 3:15 PM
""" Provides a menu screen where user can select various IMDB movie functions"""

# Import os module for system calls to cls and clear (screen)
import os  # for system calls to clear screen
import csv  # to import TSV files for movie and actor lists
import unittest 
import re
import pandas as pd #needs install
import matplotlib.pyplot as plt #needs install
import networkx as nx #needs install
from tabulate import tabulate 

# Define global variables
contender = 'nm0000327'  # Lacy Chabert ID for early prototyping, probably won't keep
#movie_list, actor_list, role_list, rating_list = [], [], [], [] # for processing Hallmark/imdb data
nm_name, name_nm = {}, {} # actor ID and name lookup (1:1)
tt_title, title_tt = {}, {} # movie ID and name lookup (1:1)
tt_nm, nm_tt = {}, {}  # lookups for movie cast (1:M) and actor filmography (1:M)
#imdb_graph, degree_ity, between_ity, close_ity = [], [], [], [] # for NX graph, centrality, shortest_path data
df, cast_crew_info, movie_info, movie_cast_crew = pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
imdb_sp = {}

# Define main function to print menu and get user choice
def main():
    """ Command-line menu of functions that process a curated IMDB list of Hallmark original movies (romcom, mystery, drama, western)"""
    
    # Clear the screen
    clrscr()

    # Load the data structures
    load_data()

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
  #notImplementedYet(option)  # driver, eventually replaced by validated features
  #graph_database()
  #imdb_graph = graph_database()
  #imdb_separation = degree_separation()
  #print(leaders for leaders in imdb_separation)
  leader_board_headers=["Hall of Famer", "Hallmark-o-Meter"]
  print(tabulate(leader_board[:20], headers=leader_board_headers, showindex=False, numalign='center'), '\n')
  #df = pd.DataFrame(imdb_separation, columns=('Hall of Famer', 'Hallmark-o-Meter'))
  #print(df.head())
  return None

def option5(option):
  notImplementedYet(option)  # driver, eventually replaced by validated features

def option6(option): 
  notImplementedYet(option)  # driver, eventually replaced by validated features

def option0(option):  # for debug only, to be replaced later with 'easter egg'
    option = option  # space holder, unknown what parameter will be passed yet, or how used
    #print(lacey_bacon['nm0000327']) 
    imdb_sp = shortest_path()
    #print('imdb_sp is a:',type(imdb_sp))
    #print('\npath to Erin Krakow', imdb_sp['nm4003706'])
    #print('\nconverted path', nm_name[x] for x in imdb_sp['nm4003706'])
    #print(tabulate(imdb_sp))
    #print([imdb_sp['Lacey Chabert']['Luke Macfarlane']])
    #chabert_numbers = imdb_sp['Lacey Chabert']
    #print(chabert_numbers,)
    #print(len(chabert_numbers),)
    #imdb_separation = degree_separation(imdb_graph)
    print('')
    return None

def load_data():  # read data from tab-delimited files to data structures for module
    global cast_crew_info, movie_info, movie_cast_crew, leader_board
    global nm_name, name_nm, tt_title, title_tt, nm_tt, tt_nm
    
    movie_info = pd.read_csv('movie_info.csv', sep='\t', index_col=None) 
    df = movie_info
    tt_title = dict(zip(df.tconst, df.primaryTitle))  # lookup title by movie ID
    title_tt = dict(zip(df.primaryTitle, df.tconst))  # lookup ID by movie title

    cast_crew_info = pd.read_csv('cast_crew_info.csv', sep='\t', index_col=None)
    df = cast_crew_info 
    nm_name = dict(zip(df.nconst, df.primaryName))  # lookup name by cast ID
    name_nm = dict(zip(df.primaryName, df.nconst))  # lookup ID by cast name

    movie_cast_crew = pd.read_csv('movie_cast_crew.csv', sep='\t', index_col=None)
    df = movie_cast_crew.groupby('nconst')['tconst'].apply(list).reset_index(name="movieList")
    nm_tt = dict(zip(df.nconst, df.movieList))  # lookup movie IDs by actor ID (coded filmography)
    df = movie_cast_crew.groupby('tconst')['nconst'].apply(list).reset_index(name="actorList")
    tt_nm = dict(zip(df.tconst, df.actorList))  # lookup actor IDs by movie ID (coded cast list)

    leader_board = pd.read_csv('leader_board.csv', sep='\t', index_col=None)

    return None

""" # stash, moved this processing to romcom_prep, will just read in leader_board now
def graph_database():
    global G
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

def degree_separation():  # calculate all three for now
    global G
    between_ity = nx.betweenness_centrality(G)
    #result_b = [(nm_name[x], between_ity[x]) for x in sorted(between_ity, key=between_ity.get, reverse=True)]
    result_b = [[nm_name[x], int(between_ity[x]*1000+43)] for x in sorted(between_ity, key=between_ity.get, reverse=True)]
    close_ity = nx.closeness_centrality(G)
    result_c = [(nm_name[x], close_ity[x]) for x in sorted(close_ity, key=close_ity.get, reverse=True)]
    #print(result_c)
    #print(type(result_c))
    degree_ity = nx.degree(G)
    result_d = degree_ity
    #print([(x, degree_ity[x]) for x in sorted(degree_ity, key=degree_ity.get, reverse=True)[:40]])
    #print(result_b)
    return(result_b)  # but only return most accurate for this dataset    
"""

def shortest_path(): # add this to menu item that needs it
    global G
    #print('\n\n\n\n\n\n\n\n\n', G['nm0000327'])
    print('\ncurrent: ', G['nm0000327']['nm0018271'])
    my_sp = dict(nx.all_pairs_shortest_path(G))
    my_list = list(my_sp)
    #print(p in my_list)
    #print(my_sp['nm0000327']['nm0000327'])
    #for pairs in my_sp:
    #  print(pairs)
    #print(my_sp['nm1674903'])
    #print(type(my_sp))
    #chabert = my_sp['nm0000327']['nm1674903']
    #print(type(chabert))
    #print('\nHello World \n')
    #print(chabert)
    return my_sp

def stash():
    movie_info_headers=["IMDB #", "Category", "Title", "Year", "Runtime", "Genres", "Rating", "Votes"]
    cast_crew_info_headers=["IMDB #", "Name", "Yr Birth", "Yr Death"]
    movie_cast_crew_headers=["Movie IMDB #", "Actor IMDB #", "Role"]
    print(tabulate(movie_info[5:10], headers=movie_info_headers, showindex=False, numalign='center'), '\n')
    print(tabulate(movie_cast_crew[5:10], headers=movie_cast_crew_headers, showindex=False, stralign='center'), '\n')
    print(tabulate(cast_crew_info[5:10], headers=cast_crew_info_headers, showindex=False, numalign='center'), '\n')
    #assert len(watchlist) > 1100
    #assert 'tt15943556' in watchlist
    #actor_list = load_actor_list()
    #print (actor_list[:5])
    #role_list = load_role_list()
    #actorlist = cast_crew_info['nconst'].tolist()
    #actorlist = list(set(actorlist))
    #return cast_crew_info[cast_crew_info['tconst'].isin(watchlist) == True].values.tolist()  # drop people not in Hallmark movies
    #movielist = movie_cast_crew['tconst'].tolist()
    return None
    
# Allow file to be used as function or program
if __name__=='__main__':
    main()

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

""" stashing early rapid prototyping code for hidden menu item
def option0(option):

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

  # some exploration of functional commands
  print ( '\n'+actor_list[0].Id, actor_list[1].Id, type(actor_list), "\n" )
  print ( role_list.__sizeof__(), '\n' )
  print ( dir(Actor) )
  #next(item for item in movie_list if item["Id"] == "tt10921042", None)
  #help(print_menu)
"""

""" stashing functions related to early prototyping with classes
def getContenderMovieIds(contenderMoviesIndex):
  global role_list
  contenderMovieIds = []
  for item in contenderMoviesIndex:
    contenderMovieIds.append(role_list[item].movieId)
  return(contenderMovieIds)

def getContenderMoviesIndex():
  global contender
  contenderMoviesIndex = [index for index, item in enumerate(role_list) if item.actorId == contender]
  return(contenderMoviesIndex)

def load_movies(movie_list):  
  with open('src/data/title-basics-imdb.tsv', 'r', encoding='utf8') as f:
    data = csv.reader(f, delimiter='\t') #read tsv text file with csv
    for row in data:
      new_movie = Movie(row[0], row[1], row[2], row[3])
      movie_list.append(new_movie) #add the data from the text file to the list
  return(movie_list)

def load_ratings(rating_list):  
  with open('src/data/title-ratings-imdb.tsv', 'r', encoding='utf8') as f:
    data = csv.reader(f, delimiter='\t') #read tsv text file with csv
    for row in data:
      new_rating = Rating(row[0], row[1], row[2])
      rating_list.append(new_rating) #add the data from the text file to the list
    return(rating_list)

def load_actors(actor_list):  
  with open('src/data/name-basics-imdb.tsv', 'r', encoding='utf8') as f:
    data = csv.reader(f, delimiter='\t') #read tsv text file with csv
    for row in data:
      new_actor = Actor(row[0], row[1], row[2], row[3])
      actor_list.append(new_actor) #add the data from the text file to the list
    return(actor_list)

def load_roles(role_list):  
  with open('src/data/title-actors-imdb.tsv', 'r', encoding='utf8') as f:
    data = csv.reader(f, delimiter='\t')  # read tsv text file with csv
    for row in data:
      new_role = Role(row[0], row[1], row[2])
      role_list.append(new_role)  # add the data from the text file to the list
  return(role_list)
"""

""" stashing the classes for now, proceeding with py primitives and pandas 
# Create classes, movie data courtesy of imdb.com (interface download)
class Movie:  
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
  def __init__(self, actorId, actorName="", actorBorn=None, actorDied=None):      
    self.Id = actorId
    self.Name = actorName
    self.Born = actorBorn
    self.Died = actorDied

class Role:  # Curated list. all leading actors and actresses starring in Hallmark movie list
  def __init__(self, movieId, actorId, actorRole):      
    self.movieId = movieId
    self.actorId = actorId
    self.actorRole = actorRole

class Rating:  # Curated list, rating details on "Hallmark" movies in list
  def __init__(self, movieId, movieRating, movieVotes):      
    self.movieId = movieId
    self.movieRating = movieRating
    self.movieVotes = movieVotes
"""
