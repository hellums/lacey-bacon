# romcom_prep.py 2/12/22 9:06 PM
""" Downloads imdb-related files and watchlist, uncompresses and cleans/prunes them as necessary"""

import requests #needs install
import gzip
import csv  # to import TSV files for movie and actor lists
import pandas as pd #needs install
import networkx as nx #needs install

actorlist = []

def main():
    #download_uncompress_imdb_files()  #shipit
    load_dataframes()  # load local files into data structures
    graph_database()  # create a netwokx graph for analysis of centrality
    export_dataframes()  # write datasets to local json and csv files
    
def download_uncompress_imdb_files():
    print('\nThis process could take a few minutes, depending on Internet speed...')
    remote_url ='https://raw.githubusercontent.com/hellums/lacey-bacon/root/watchlist.txt'  
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

def download_file(remote, local):  #shipit
    print('\nDownloading', local)
    data = requests.get(remote)
    with open(local, 'wb') as file:
        file.write(data.content)
    return None

def uncompress_file(compressed, uncompressed):  #shipit
    print('\nUncompressing', uncompressed)
    with gzip.open(compressed, 'rb') as f:
        data = f.read()
    with open(uncompressed, 'wb') as f:
        f.write(data)
    return None

def load_dataframes():
    global watchlist
    watchlist = load_watchlist()
    assert len(watchlist) > 1100
    assert 'tt15943556' in watchlist
    movie_list = load_movie_list()  # also performs load_rating_list, prior to merge
    assert len(movie_list) > 1000
    assert len(movie_list) < 1500
    role_list = load_role_list()
    actor_list = load_actor_list()
    return None

def load_watchlist():  # shipit
    local_file = 'watchlist.txt'
    header_field = ['tconst']
    watchlist_info = pd.read_csv(local_file, names=header_field)
    return watchlist_info['tconst'].tolist() # refactor this to load direct to list, don't need a df?

def load_movie_list():  # load movies and ratings, merge and clean resulting dataset
    global watchlist, movie_info, tt_title, title_tt
    local_file = 'movie_info.tsv'
    movie_info = pd.read_csv(local_file, sep='\t', usecols=[0, 1, 2, 5, 7, 8], 
        dtype={'startYear': str, 'runtimeMinutes': str})  # converting genre string to a list
    movie_info = movie_info[movie_info['tconst'].isin(watchlist) == True]  # drop movies not on/by Hallmark    
    movie_info['runtimeMinutes'] = movie_info['runtimeMinutes'].replace(to_replace=r"\N", value='80')  # fix imdb format error
    local_file = 'movie_ratings.tsv'  # only need this temporarily to add ratings and voters to movie_info df
    movie_ratings = pd.read_csv(local_file, sep='\t')
    movie_ratings = movie_ratings[movie_ratings['tconst'].isin(watchlist) == True]
    movie_info = pd.merge(movie_info,
                        movie_ratings[['tconst', 'averageRating', 'numVotes']],
                        on='tconst', how='outer')  # adds the ratings and votes columns to the movie_info df
    movie_info = movie_info[:len(watchlist)]  # get rid of the NaN records from the merge, maybe refactor so not needed
    movie_info = movie_info.fillna(value={'averageRating':6.9,'numVotes':699})  # clean up <20 NaN values from csv import
    movie_info['runtimeMinutes'] = movie_info['runtimeMinutes'].astype(int)  # convert runtime to an int for proper processing
    movie_info['numVotes'] = movie_info['numVotes'].astype(int)  # convert column to an int for proper processing
    tt_title = dict(zip(movie_info.tconst, movie_info.primaryTitle))  # lookup title by movie ID
    title_tt = dict(zip(movie_info.primaryTitle, movie_info.tconst))  # lookup ID by movie title
    return movie_info.values.tolist()

def load_role_list():
    global actorlist, movie_cast_crew, nm_tt, tt_nm
    local_file = 'movie_cast_crew.tsv'
    movie_cast_crew = pd.read_csv(local_file, sep='\t', usecols=[0, 2, 3])
    movie_cast_crew = movie_cast_crew[movie_cast_crew['tconst'].isin(watchlist) == True]  # drop movies not on/by Hallmark
    unwantedValues = ['writer', 'producer', 'director', 'composer', 'cinematographer', 
                    'editor', 'production_designer', 'self']  # should only leave actor, actress categories
    movie_cast_crew = movie_cast_crew[movie_cast_crew['category'].isin(unwantedValues) == False] # keep actor, actress rows
    df = movie_cast_crew.groupby('nconst')['tconst'].apply(list).reset_index(name="movieList")
    nm_tt = dict(zip(df.nconst, df.movieList))  # lookup movie IDs by actor ID (coded filmography)
    df = movie_cast_crew.groupby('tconst')['nconst'].apply(list).reset_index(name="actorList")
    tt_nm = dict(zip(df.tconst, df.actorList))  # lookup actor IDs by movie ID (coded cast list)
    actorlist = list(set(movie_cast_crew['nconst'].tolist()))
    movielist = movie_cast_crew['tconst'].tolist()
    return list(set(movielist))

def load_actor_list():
    global cast_crew_info, actorlist, nm_name, name_nm
    local_file = 'cast_crew_info.tsv'
    cast_crew_info = pd.read_csv(local_file, sep='\t', usecols=[0, 1, 2, 3]) # refactor to pare based on actor list
    cast_crew_info = cast_crew_info[cast_crew_info['nconst'].isin(actorlist) == True]  # drop people not in Hallmark movies
    nm_name = dict(zip(cast_crew_info.nconst, cast_crew_info.primaryName))  # lookup name by cast ID
    name_nm = dict(zip(cast_crew_info.primaryName, cast_crew_info.nconst))  # lookup ID by cast name
    return cast_crew_info.values.tolist()

def graph_database():
    global G, leader_board, imdb_separation
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
    between_ity = nx.betweenness_centrality(G)  # calculate the candidates for "center of the Hallmark universe"
    imdb_separation = [[nm_name[x], between_ity[x]] for x in sorted(between_ity, key=between_ity.get, reverse=True)]
    leader_board = pd.DataFrame(imdb_separation, columns=('Hall of Famer', 'Hallmark-o-Meter'))
    return None

def export_dataframes():
    movie_info.to_json('./movie_info.json', orient='table', index=False)
    movie_info.to_csv('./movie_info.csv', sep='\t', index=False)
    movie_cast_crew.to_json('./movie_cast_crew.json', orient='table', index=False)
    movie_cast_crew.to_csv('./movie_cast_crew.csv', sep='\t', index=False)
    cast_crew_info.to_json('./cast_crew_info.json', orient='table', index=False)
    cast_crew_info.to_csv('./cast_crew_info.csv', sep='\t', index=False)
    leader_board.to_json('./leader_board.json', orient='table', index=False)
    leader_board.to_csv('./leader_board.csv', sep='\t', index=False)

# Allow file to be used as function or program
if __name__=='__main__':
    main()

# Everything below call to main() above is stash area and scratch work space

""" stash
def degree_separation():  # calculate all three for now
    global G
    #between_ity = nx.betweenness_centrality(G)
    #result_b = [(nm_name[x], between_ity[x]) for x in sorted(between_ity, key=between_ity.get, reverse=True)]
    imdb_separation = [[nm_name[x], int(between_ity[x]*1000+43)] for x in sorted(between_ity, key=between_ity.get, reverse=True)]
    df = pd.DataFrame(imdb_separation, columns=('Hall of Famer', 'Hallmark-o-Meter'))
    #degree_ity = nx.degree(G)
    #result_d = degree_ity
    #result_d = [(nm_name[x], degree_ity[x]) for x in sorted(degree_ity, key=degree_ity.get, reverse=True)]
    return None
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
