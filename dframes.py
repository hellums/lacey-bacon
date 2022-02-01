from pickletools import read_stringnl_noescape
import pandas as pd
import re
import imdb

header_fields = ['movieId', 'actorId', 'roleId']
roles = pd.read_csv('data/title-actors-imdb.tsv', sep='\t', header=None, names=header_fields)
#print('\nROLES\n', roles.tail(2))

header_fields = ['movieId', 'movieRating', 'movieVotes']
ratings = pd.read_csv('data/title-ratings-imdb.tsv', sep='\t', header=None, names=header_fields)
#print('\nRATINGS', ratings.tail(2))

header_fields = ['actorId', 'actorName', 'actorBirthYr', 'actorDeathYr']
actors = pd.read_csv('data/name-basics-imdb.tsv', sep='\t', header=None, names=header_fields)
#print('\nACTORS\n', actors.tail(2))

header_fields = ['movieId', 'movieType', 'movieTitle', 'movieYear', 'movieMinutes', "movieGenres"]
movies = pd.read_csv('data/title-basics-imdb.tsv', sep='\t', header=None, names=header_fields, \
    converters={'movieGenres': lambda x: re.split(',+', x)})
#movies = pd.read_csv('data/title-basics-imdb.tsv', sep='\t', header=None, names=header_fields)
#print('\nMOVIES\n', movies.tail(30))
#print('\n', movies.iloc[2555])
#print(type(movies.iloc[2555]['movieGenres']))
#print('\n', movies.iloc[2555]['movieGenres'])

#print('\n', roles.dtypes)
#print('\n', ratings.dtypes)
#print('\n', actors.dtypes)
#print('\n', movies.dtypes)

