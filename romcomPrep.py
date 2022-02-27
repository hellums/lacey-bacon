# romcom_prep.py dbh 2/27/22 10:55 AM
""" Downloads imdb-related files and watchlist, uncompresses and cleans/prunes them as necessary"""

import re
import requests  # needs install
import gzip
import re
import csv  # to import TSV files for movie and actor lists
import pandas as pd  #needs install
import networkx as nx  #needs install
import pickle
import sqlite3  # to export records to flatfile database
from pathlib import Path

def main():
    download_uncompress_imdb_files()  #shipit
    load_dataframes()  # load local files into data structures
    graph_database()  # create a netwokx graph for analysis of centrality
    graph_all_as_nodes()
    export_dataframes()  # write datasets to local json and csv files
    export_sqlite()
    
def download_uncompress_imdb_files():  # shipit
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
    print('Downloading', local)
    data = requests.get(remote)
    with open(local, 'wb') as file:
        file.write(data.content)
    return None

def uncompress_file(compressed, uncompressed):  #shipit
    print('Uncompressing', uncompressed)
    with gzip.open(compressed, 'rb') as f:
        data = f.read()
    with open(uncompressed, 'wb') as f:
        f.write(data)
    return None

def load_dataframes():  # shipit
    global watchlist
    print('Loading dataframes...')
    # Create a dictionary or list, populate it with several values, retrieve at least one value, 
    # and use it in your program. Code Louisville requirement.
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
    print('Loading watchlist...')
    local_file = 'watchlist.txt'
    header_field = ['tconst']
    watchlist_info = pd.read_csv(local_file, names=header_field)
    return watchlist_info['tconst'].tolist() # refactor this to load direct to list, don't need a df?

def load_movie_list():  # shipit - load movies and ratings, merge and clean resulting dataset
    global watchlist, movie_info, tt_title, title_tt, title_rating
    print('Loading movies...')
    local_file = 'movie_info.tsv'
    movie_info = pd.read_csv(local_file, sep='\t', usecols=[0, 1, 2, 5, 7, 8], 
                        dtype={'startYear': str, 'runtimeMinutes': str}, \
                        converters={'movieGenres': lambda x: re.split(',+', x)})  # convert genres to a list
    movie_info = movie_info[movie_info['tconst'].isin(watchlist) == True]  # drop movies not on/by Hallmark    
    movie_info['runtimeMinutes'] = movie_info['runtimeMinutes'].replace(to_replace=r"\N", value='80')  # fix imdb format error
    local_file = 'movie_ratings.tsv'  # only need this temporarily to add ratings and voters to movie_info df
    print('Loading ratings...')
    # Use pandas, matplotlib, and/or numpy to perform a data analysis project. Ingest 2 or more pieces of data, 
    # analyze that data in some manner, and display a new result to a graph, chart, or other display. 
    # Code Louisville requirement (pandas, ingest multiple data sets)
    movie_ratings = pd.read_csv(local_file, sep='\t')
    movie_ratings = movie_ratings[movie_ratings['tconst'].isin(watchlist) == True]
    print('Merging movies and ratings...')
    movie_info = pd.merge(movie_info,
                        movie_ratings[['tconst', 'averageRating', 'numVotes']],
                        on='tconst', how='outer')  # adds the ratings and votes columns to the movie_info df
    movie_info = movie_info[:len(watchlist)]  # get rid of the NaN records from the merge, maybe refactor so not needed
    movie_info = movie_info.fillna(value={'averageRating':6.9,'numVotes':699})  # clean up <20 NaN values from csv import
    movie_info['runtimeMinutes'] = movie_info['runtimeMinutes'].astype(int)  # convert runtime to an int for proper processing
    movie_info['numVotes'] = movie_info['numVotes'].astype(int)  # convert column to an int for proper processing
    tt_title = dict(zip(movie_info.tconst, movie_info.primaryTitle))  # lookup title by movie ID
    title_tt = dict(zip(movie_info.primaryTitle, movie_info.tconst))  # lookup ID by movie title
    title_rating = dict(zip(movie_info.primaryTitle, movie_info.averageRating))  # lookup rating by movie title
    return movie_info.values.tolist()

def load_role_list():  # shipit
    global actorlist, movie_cast_crew, nm_tt, tt_nm
    print('Loading cast and crew...')
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

def load_actor_list():  # shipit
    global cast_crew_info, actorlist, nm_name, name_nm
    print('Loading actors and actresses...')
    local_file = 'cast_crew_info.tsv'
    cast_crew_info = pd.read_csv(local_file, sep='\t', usecols=[0, 1, 2, 3]) # refactor to pare based on actor list
    cast_crew_info = cast_crew_info[cast_crew_info['nconst'].isin(actorlist) == True]  # drop people not in Hallmark movies
    nm_name = dict(zip(cast_crew_info.nconst, cast_crew_info.primaryName))  # lookup name by cast ID
    name_nm = dict(zip(cast_crew_info.primaryName, cast_crew_info.nconst))  # lookup ID by cast name
    return cast_crew_info.values.tolist()

def graph_database():  # shipit
    global G, sp, leader_board, imdb_separation
    G = nx.Graph()
    print('Graphing movies and cast...')
    edge_attribute_dict = {}  # store weight of movie edges between costaring actors
    # Use pandas, matplotlib, and/or numpy to perform a data analysis project. Ingest 2 or more pieces of data, 
    # analyze that data in some manner, and display a new result to a graph, chart, or other display. 
    # Code Louisville requirement (use NX graph, analyze that data, display a new reult to graph/table).
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
    
    print('Creating connectivity graphs...')
    between_ity = nx.betweenness_centrality(G)  # calculate the candidates for "center of the Hallmark universe"
    imdb_separation = [[nm_name[x], format(between_ity[x]*1000+40, ".2f")] for x in sorted(between_ity,
                     key=between_ity.get, reverse=True)]  # magic number shapes scores to "out of 100" range

    leader_board = pd.DataFrame(imdb_separation, columns=('Hall of Fame', 'Fame-O-Meter'))
    return None

def graph_all_as_nodes():  # shipit - for text-based presentation of actor degrees of separation
    global sp, sp1, sp2
    G1 = nx.Graph()
    print('Creating degree separation graph...')
    names = {}
    for n, star in enumerate(movie_cast_crew.nconst.unique()):
        name = nm_name[star]
        names[star] = name
        G1.add_node(name)
    for n, movie in enumerate(movie_cast_crew.tconst.unique()):
        name = tt_title[movie]
        names[movie] = name
        G1.add_node(name)    
    for row in movie_cast_crew.index:
        star = movie_cast_crew['nconst'][row]
        s_name = names[star]
        movie = movie_cast_crew['tconst'][row]
        m_name = names[movie]
        G1.add_edge(s_name, m_name)
    sp = nx.all_pairs_shortest_path(G1)  # create list of shortest paths
    sp1 = dict(sp)  # convert to dictionary for export and import
    sp = nx.single_source_shortest_path(G1, 'Lacey Chabert', cutoff=7)
    sp2 = dict(sp)  # convert the Lacey only shortest path info
    return None

def export_dataframes():  # shipit - save all four tables in csv format
    print('Exporting movies...')
    movie_info.to_csv('./movie_info.csv', sep='\t', index=False)

    print('Exporting cast...')
    movie_cast_crew.to_csv('./movie_cast_crew.csv', sep='\t', index=False)
    
    print('Exporting actors and actresses...')
    cast_crew_info.to_csv('./cast_crew_info.csv', sep='\t', index=False)

    print('Exporting leaderboard...')
    leader_board.to_csv('./leader_board.csv', sep='\t', index=False)

    print('Exporting shortest path graph...')  # export shortest path for import in main and web
    with open('./shortest_path.pkl', 'wb') as fp:
        pickle.dump(sp1, fp)  #file is .5 GB, more suitable to task than JSON
    with open('./lacey_sp.pkl', 'wb') as fp:
        pickle.dump(sp2, fp)  #file is much smaller, for Lacey-only analysis and lookups

def export_sqlite():  # shipit - add all four main dataframes to database as tables
    print('Exporting database records...')
    
    #create_tables()  # comment out as necessary, works fine 1st time, but fails on 2nd

    conn=sqlite3.connect('movies.db')
    
    movie_info.to_sql('movie_info', conn, if_exists = 'replace', index = False)
    movie_cast_crew.to_sql('movie_cast_crew', conn, if_exists = 'replace', index = False)
    cast_crew_info.to_sql('cast_crew_info', conn, if_exists = 'replace', index = False)
    leader_board.to_sql('leader_board', conn, if_exists = 'replace', index = False)

    conn.close()
    return None

def create_tables():  # pandas to_sql doesn't support PRIMARY KEY or IF EXISTS IGNORE, so...

    conn=sqlite3.connect('movies.db')

    sql_query = ('''CREATE TABLE IF NOT EXISTS movie_info (
    "tconst" TEXT PRIMARY KEY, 
    "titleType" TEXT,
    "primaryTitle" TEXT,
    "startYear" TEXT, 
    "runtimeMinutes" INTEGER,
    "genres" TEXT,
    "averageRating" REAL,
    "numVotes" INTEGER
    );''')
    cursor=conn.cursor()
    cursor.execute(sql_query)

    sql_query = ('''CREATE TABLE IF NOT EXISTS "movie_cast_crew" (
    "tconst" TEXT,
    "nconst" TEXT,
    "category" TEXT,
    PRIMARY KEY("tconst","nconst")
    );''')
    cursor=conn.cursor()
    cursor.execute(sql_query)

    sql_query = ('''CREATE TABLE IF NOT EXISTS "leader_board" (
    "Hall of Fame" TEXT PRIMARY KEY,
    "Fame-O-Meter" TEXT
    );''')
    cursor=conn.cursor()
    cursor.execute(sql_query)

    sql_query = ('''CREATE TABLE IF NOT EXISTS "cast_crew_info" (
    "nconst" TEXT PRIMARY KEY,
    "primaryName" TEXT,
    "birthYear" TEXT,
    "deathYear" TEXT
    );''')
    cursor=conn.cursor()
    cursor.execute(sql_query)

    conn.close()
    return None

# Allow file to be used as function or program
if __name__=='__main__':
    main()