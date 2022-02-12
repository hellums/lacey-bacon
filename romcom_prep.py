# romcom_prep.py 2/12/22 12:21 AM
""" Downloads imdb-related files and watchlist, uncompresses and cleans/prunes them as necessary"""

import requests #needs install
import gzip
import csv  # to import TSV files for movie and actor lists
import pandas as pd #needs install

actorlist = []

def main():
    #download_uncompress_imdb_files()  #shipit
    load_dataframes()  # load local files into data structures
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
    global watchlist, movie_info
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
    
    #del movie_ratings # don't need it anymore, after outer join merge with movies
    return movie_info.values.tolist()

def load_role_list():
    global actorlist, movie_cast_crew
    local_file = 'movie_cast_crew.tsv'
    movie_cast_crew = pd.read_csv(local_file, sep='\t', usecols=[0, 2, 3])
    movie_cast_crew = movie_cast_crew[movie_cast_crew['tconst'].isin(watchlist) == True]  # drop movies not on/by Hallmark
    unwantedValues = ['writer', 'producer', 'director', 'composer', 'cinematographer', 
                    'editor', 'production_designer', 'self']  # should only leave actor, actress categories
    movie_cast_crew = movie_cast_crew[movie_cast_crew['category'].isin(unwantedValues) == False] # keep actor, actress rows
    actorlist = list(set(movie_cast_crew['nconst'].tolist()))
    movielist = movie_cast_crew['tconst'].tolist()
    return list(set(movielist))

def load_actor_list():
    global cast_crew_info, actorlist
    local_file = 'cast_crew_info.tsv'
    cast_crew_info = pd.read_csv(local_file, sep='\t', usecols=[0, 1, 2, 3]) # refactor to pare based on actor list
    cast_crew_info = cast_crew_info[cast_crew_info['nconst'].isin(actorlist) == True]  # drop people not in Hallmark movies
    return cast_crew_info.values.tolist()

def export_dataframes():
    movie_info.to_json('./movie_info.json', orient='table', index=False)
    movie_info.to_csv('./movie_info.csv', sep='\t', index=False)
    movie_cast_crew.to_json('./movie_cast_crew.json', orient='table', index=False)
    movie_cast_crew.to_csv('./movie_cast_crew.csv', sep='\t', index=False)
    cast_crew_info.to_json('./cast_crew_info.json', orient='table', index=False)
    cast_crew_info.to_csv('./cast_crew_info.csv', sep='\t', index=False)

# Allow file to be used as function or program
if __name__=='__main__':
    main()
