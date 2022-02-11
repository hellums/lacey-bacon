

from ast import NameConstant


NameConstant
NameConstant

actor(s)
  nconst (nameID)
  primaryName
  birthYear
  deathYear
  knownForTitles []

Dictionaries
  nconst-primaryName
  primaryName-nconst
  nconst-knownForTitles

movie(s)
  tconst (titleID)
  titleType
  primaryTitle
  startYear
  runtimeMinutes
  genres
  averageRating
  numVotes

Dictionaries
  tconst-primaryTitle
  primaryTitle-tconst

principal(s)
  tconst
  nconst []
  category

def actor_filmIDs(actor_ID)
def actor_filmnames(actor_filmIDs)

_nconst 
_primaryName
_birthYear
_deathYear
_nameID 
nconst-primaryName {}
primaryName-nconst {}
nconst-knownForTitles {}

_tconst  
_primaryTitle
_titleType
_titleID
_startYear
_runtimeMinutes
_genres
_averageRating
_numVotes
tconst-primaryTitle
primaryTitle-tconst

principal(s)
_tconst
_nconst
_category
tconst-nconst 
tconst-nconst-category


def actor_movies(actor):

    _name = actor
    _ID = _name_to_ID(actor_name)
    if (_ID == None): return (error)
    title_IDs = actor_filmIDs(_ID)
    _filmography = actor_titles(_titleIDs)
    hallmark_actor = actor_in_df(actor_ID)


    if hallmark_actor == None:
        print(error)
    else:
        actor_ID = actor_name_to_ID(actor_name)
    
