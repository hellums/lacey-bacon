# **Import modules to handle downloading, compressed files, regular expressions, and dataframes.**

import requests #needs install
import gzip
import re
import pandas as pd #needs install
import unittest 
import matplotlib.pyplot as plt #needs install
import networkx as nx #needs install

def main():
#    """ Command-line menu of functions that process a curated IMDB list of Hallmark original movies (romcom, mystery, drama, western)"""
    
    global contender  # early prototyping, probably won't keep
    global watchlist, actor_list, role_list, movie_list, rating_list  # for processing imdb-related data
    global nm_name nm_tt nm_nm  # for actor/actress name lookup, filmography, and costar data
    global tt_title tt_nm  # for movie title lookup, cast/crew data
    global G degree_ity between_ity close_ity  # for NX graph, centrality, shortest_path data

    # Clear the screen
    clrscr()

    #download_uncompress_imdb_files()  # get imdb source files from web
    print('\nAll files downloaded and uncompressed!')
    load_dataframes_lists()  # load local files into data structures
    print('')

def download_uncompress_imdb_files():
    print('\nThis process could take a few minutes, depending on Internet speed...')
    remote_url ='https://datasets.imdbws.com/title.ratings.tsv.gz'
    local_file = 'movie_ratings.tsv.gz'  # ratings and number votes, for some movies (not all)
    download_file(remote_url, local_file)
    uncompress_file(local_file, 'movie_ratings.tsv')

    remote_url ='https://raw.githubusercontent.com/hellums/hallmarkish/root/watchlist.txt'  
    local_file = 'watchlist.txt' # export of imdb watchlist
    download_file(remote_url, local_file)

    remote_url ='https://datasets.imdbws.com/title.basics.tsv.gz'  
    local_file = 'movie_info.tsv.gz' # detail and metadata about all imdb movies (pare down!)
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

    return None

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

    watchlist = load_watchlist()
    assert len(watchlist) > 1100
    assert 'tt15943556' in watchlist

    actor_list = load_actor_list()

    role_list = load_role_list()

    movie_list = load_movie_list()

    rating_list = load_rating_list()

    return None

def load_watchlist():
    local_file = 'watchlist.txt'
    header_field = ['tconst']
    watchlist_info = pd.read_csv(local_file, names=header_field)
    return watchlist_info['tconst'].tolist() # refactor this to load direct to list, don't need a df

def load_actor_list():
    local_file = 'cast_crew_info.tsv'
    cast_crew_info = pd.read_csv(local_file, sep='\t', usecols=[0, 1, 2, 3]) # refactor to pare based on actor list
    actorlist = cast_crew_info['nconst'].tolist()
    actorlist = list(set(actorlist))
    cast_crew_info = cast_crew_info[cast_crew_info['nconst'].isin(actorlist) == True]  # drop people not in Hallmark movies
    return [cast_crew_info.tolist()]

def load_role_list():
    local_file = 'movie_cast_crew.tsv'
    movie_cast_crew = pd.read_csv(local_file, sep='\t', usecols=[0, 2, 3])
    movie_cast_crew = movie_cast_crew[movie_cast_crew['tconst'].isin(watchlist) == True]  # drop movies not on/by Hallmark
    unwantedValues = ['writer', 'producer', 'director', 'composer', 'cinematographer', 
                    'editor', 'production_designer', 'self']  # should only leave actor, actress categories
    movie_cast_crew = movie_cast_crew[movie_cast_crew['category'].isin(unwantedValues) == False] # keep actor, actress rows
    movielist = movie_cast_crew['tconst'].tolist()
    movielist = list(set(movielist))
    return ['']

def load_movie_list():
    local_file = 'movie_info.tsv'
    movie_info = pd.read_csv(local_file, sep='\t', usecols=[0, 1, 2, 5, 7, 8], 
        dtype={'startYear': str, 'runtimeMinutes': str}, 
        converters={'genres': lambda x: re.split(',+', x)})  # converting genre string to a list
    movie_info = movie_info[movie_info['tconst'].isin(watchlist) == True]  # drop movies not on/by Hallmark
    movie_info['runtimeMinutes'] = movie_info['runtimeMinutes'].replace(to_replace=r"\N", value='80')  # fix imdb format error
    return ['']

def load_rating_list():
    local_file = 'movie_ratings.tsv'  # only need this temporarily to add ratings and voters to movie_info df
    movie_ratings = pd.read_csv(local_file, sep='\t')
    return[movie_ratings[movie_ratings['tconst'].isin(watchlist) == True]  # drop ratings not associated w/Hallmark 

def stuff():  # just some rapid prototyping and experimentation, some will be moved to functions

    local_file = 'movie_crew.tsv'  # may not need separate director/writer associations, but better have than not
    movie_crew = pd.read_csv(local_file, sep='\t')
    movie_crew = movie_crew[movie_crew['tconst'].isin(watchlist) == True]  # drop people not associated w/Hallmark

    # # **Merge ratings into movie dataframe, and drop ratings df**
    movie_info = pd.merge(movie_info,
                        movie_ratings[['tconst', 'averageRating', 'numVotes']],
                        on='tconst', how='outer')  # adds the ratings and votes columns to the movie_info df
    movie_info = movie_info[:len(watchlist)]  # get rid of the NaN records from the merge, maybe refactor so not needed
    movie_info = movie_info.fillna(value={'averageRating':6.9,'numVotes':699})  # clean up <20 NaN values from csv import
    movie_info['runtimeMinutes'] = movie_info['runtimeMinutes'].astype(int)  # convert runtime to an int for proper processing
    movie_info['numVotes'] = movie_info['numVotes'].astype(int)  # convert column to an int for proper processing
    del movie_ratings # don't need it anymore, after outer join merge with movies


    # # **Validate import and data structures**
    get_ipython().magic('matplotlib inline')
    df = movie_info
    df.averageRating.plot(kind='hist',
                        title='Historgram of Ratings',
                        color='c',
                        bins=20);
    df.titleType.value_counts().plot(kind='bar',
                                    rot=0,
                                    title='Bar Graph of Titles',
                                    color='m');
    df.averageRating.plot(kind='box', title='Boxplot, duh!', color='b');
    df.runtimeMinutes.plot(kind='box', title='Boxplot, duh!', color='b');
    df.numVotes.plot(kind='box', title='Boxplot, duh!', color='b');
    null_counts = df.isnull().sum()
    null_counts[null_counts > 0].sort_values(ascending=False)
    pd.crosstab(df.startYear, df.titleType)
    df.groupby('titleType').averageRating.mean()
    df.groupby('titleType').runtimeMinutes.median()
    df.groupby(['titleType'])['runtimeMinutes'].median() # same as above
    df.groupby(['titleType']).agg({ 'numVotes': 'mean', 'runtimeMinutes': 'median' })
    df.to_json('./df.json', orient='records')
    df.to_csv('./df.csv', sep='\t', orient='records')
    'nm0000327' in actorlist
    movie_cast_crew.loc[movie_cast_crew.tconst == 'tt13831504',:]
    cast_crew_info.loc[cast_crew_info.nconst == 'nm0000327']
    movie_cast_crew.loc[movie_cast_crew.nconst == 'nm0000327',:]

    df3 = movie_cast_crew.groupby('nconst')['tconst'].apply(list).reset_index(name="movieList")
    nm_tt_Dict = dict(zip(df3.nconst, df3.movieList))
    nm_tt_Dict['nm4003706']
    nameDict = dict(zip(df3.nconst, df3.movieList))
    nameDict['nm0000327']  # much more useful, IMHO

    df2 = movie_cast_crew.groupby('tconst')['nconst'].apply(list).reset_index(name="actorList")
    tt_nm_Dict = dict(zip(df2.tconst, df2.actorList))
    list(tt_nm_Dict.items())[91:95]
    tt_nm_Dict['tt13831504']
    list(nm_tt_Dict.items())[91:95]
    nm_tt_Dict['nm4003706']

    df1 = cast_crew_info
    nm_Dict = dict(zip(df1.nconst, df1.primaryName))
    list(nm_Dict.items())[91:95]
    tt_nm_Dict['tt13831504']
    nm_tt_Dict['nm0000327']
    nm_Dict['nm4003706']

    df4 = movie_info
    tt_Dict = dict(zip(df4.tconst, df4.primaryTitle))
    tt_Dict['tt13831504']
    Name_nm_Dict = dict(zip(df1.primaryName, df1.nconst))
    Name_nm_Dict['Alison Sweeney']
    nm_tt_Dict['nm0842081']
    tt_nm_Dict['tt11068326']
    tt_Dict['tt11068326']
    title_tt_Dict = dict(zip(df4.primaryTitle, df4.tconst))
    title_tt_Dict['It Was Always You']
    Title_tt_Dict['Sarah, Plain and Tall']

    # # **Graph network plot and determine centrality** 
    titles = watchlist

    between_ity = nx.betweenness_centrality(G1)
    [(x, between_ity[x]) for x in sorted(between_ity, key=between_ity.get, reverse=True)[:20]]
    between_ity["Autumn Reeser"]

    degree_ity = nx.degree(G1)
    [(x, degree_ity[x]) for x in sorted(degree_ity, key=degree_ity.get, reverse=True)[:40]]
    degree_ity['Tyler Hynes']

    G1.edges()

    close_ity = nx.closeness_centrality(G1)  # not useful without removing titles from list
    [(x, close_ity[x]) for x in sorted(close_ity, key=close_ity.get, reverse=True)[:40]]

    nx.is_connected(G1)

    G1.neighbors('Lacey Chabert')
    int(nx.shortest_path_length(G1, 'Lacey Chabert', 'Tyler Hynes')/2)
    nx.shortest_path(G1, 'Lacey Chabert', 'Cindy Busby')

    lacey1 = nx.single_source_shortest_path(G1, 'Lacey Chabert', cutoff=1)
    lacey2 = nx.single_source_shortest_path(G1, 'Lacey Chabert', cutoff=2)
    lacey3 = nx.single_source_shortest_path(G1, 'Lacey Chabert', cutoff=3)
    lacey4 = nx.single_source_shortest_path(G1, 'Lacey Chabert', cutoff=4)
    lacey5 = nx.single_source_shortest_path(G1, 'Lacey Chabert', cutoff=5)
    lacey6 = nx.single_source_shortest_path(G1, 'Lacey Chabert', cutoff=6)
    lacey7 = nx.single_source_shortest_path(G1, 'Lacey Chabert', cutoff=7)
    lacey8 = nx.single_source_shortest_path(G1, 'Lacey Chabert', cutoff=8)

    path = nx.single_source_shortest_path(G1, 'Lacey Chabert')
    path['Autumn Reeser']

    sp=nx.all_pairs_shortest_path(G1)
    chabert_num = sp['Lacey Chabert']['Luke Macfarlane']
    chabert_num

    chabert_numbers = sp['Lacey Chabert'] 
    chabert_numbers
    len(chabert_numbers)

    centrality = nx.betweenness_centrality(G2)
    [(x, centrality[x]) for x in sorted(centrality, key=centrality.get, reverse=True)[:20]]
    centrality

    G2.number_of_nodes()
    G2.number_of_edges()
    G2.adj['nm0825555']
    G2.nodes()
    G2.edges()

    tt_Dict
    for titleID, title in tt_Dict.items():
        print (titleID, title)
    tt_Dict.head()
    print(tt_Dict.values())
    print(tt_Dict.items())

    L1 = list(tt_Dict.values())
    for i in L1:
        print (i)
    tt_Dict['tt1335977']
    df3.head()
    print(df3.head())
    tt_Dict['tt0217066']

    print(df1['primaryName'].where(df1['nconst'] == lacey).dropna())
    df1.loc[df1['nconst'] == lacey]
    df1.loc[df1['nconst'].isin(['nm0000327', 'nm0000001'])]
    df1.loc[(df1['birthYear'] == '1982') & (df1['deathYear'] > '2015')]

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

    tt_Dict['tt13831504']
    tt_Dict
    nm_Dict['nm4003706']
    Name_nm_Dict['Erin Krakow']
    tt_nm_Dict['tt13831504']
    tt_nm_Dict
    nm_Dict

    m = nx.Graph()
    edge_attribute_dict = {}
    for name_ID, titles in nm_tt_Dict.items():
        m.add_node(name_ID)
        for title in titles:
            for name_ID2, titles2 in nm_tt_Dict.items():
                if (title in titles2) and (titles2 != titles):
                    m.add_edge(name_ID, name_ID2)
                    name_ID_tuple = tuple(sorted((name_ID, name_ID2)))
                    if name_ID_tuple not in edge_attribute_dict:
                        edge_attribute_dict[name_ID_tuple] = 1
                    else:
                        edge_attribute_dict[name_ID_tuple] += 1
    len(m.edges())
    for k,v in edge_attribute_dict.items():
        edge_attribute_dict[k] = {'weight':v}
    edge_attribute_dict
    nx.set_edge_attributes(m, edge_attribute_dict)

    centrality = nx.betweenness_centrality(m)
    [(nm_Dict[x], centrality[x]) for x in sorted(centrality, key=centrality.get, reverse=True)[:30]]

    between_ity = nx.betweenness_centrality(m)
    [(nm_Dict[x], between_ity[x]) for x in sorted(between_ity, key=between_ity.get, reverse=True)[:30]]

    degree_ity = nx.degree(m)
    [(nm_Dict[x], degree_ity[x]) for x in sorted(degree_ity, key=degree_ity.get, reverse=True)[:30]]

    pos = nx.spring_layout(m,k=1,iterations=20)
    max_c = max(centrality.values())
    color_map = {x[0]:x[1]/max_c for x in centrality.items()}
    nx.draw(m, pos, node_color=list(color_map.values()), cmap=plt.cm.Blues)
    plt.show()

# Allow file to be used as function or program
if __name__=='__main__':
    main()