# romcomWeb.py 2/27/22 10:55 AM
""" Project to reuse Code Louisvillle Python data analysis class code for web delivery"""

import csv  # to import TSV files for movie and actor lists
import pickle

import re
import pandas as pd
from natsort import natsorted
from flask import Flask, render_template, request, jsonify


global tt_title, title_tt, tt_nm, tt_rating, nm_name, name_nm, nm_tt, title_rating, sp, ranked_titles
global cast_crew_info, movie_info, movie_cast_crew, leader_board, lacey_sp, no_pickle_file


# Initiate the Flask micro web framework
app = Flask(__name__)


@app.route('/')  # initialize program
def home():
    load_data()  # load data structures
    return render_template("home.html") # display the home page


@app.route('/actor_frm')  # user clicked on Actor in navbar
def actor_frm():
    return render_template('actor_frm.html')  # display the actor lookup form


@app.route('/actor_data/', methods=['POST', 'GET']) # user clicked on submit or typed in full path
def actor_data():
    if request.method == 'GET':  # display an error if user accessing results without search
        return f"The URL /data is accesed directly. Try going to '/form to submit form"
    if request.method == 'POST':  # otherwise let's process the name they sent in the form
        form_data = request.form
        actor_name = form_data['Actor']

        try:
            actor_nm = nm_lookup(actor_name)  # if we get results, we'll return them
            actor_movies = films_lookup(actor_nm)  # pull a list of this actor's movie title codes
            actor_titles = []
            for each in natsorted(actor_movies, reverse=True): # sort by one-up assigned tt numbers
                actor_titles.append(tt_title[each])  # lookup the code to get titles
            total_titles = len(actor_titles)
            shortest_path=lacey_sp[actor_name]
            separation=int(len(shortest_path)/2)
        except:  # otherwise well return a bunch of nulls so the handler page can notify the user
            return render_template('actor.html', actor=actor_name, actor_nm='', num_films=0, films=[], path=[], distance=0)

    return render_template('actor.html', actor=actor_name, actor_nm=actor_nm, num_films =total_titles, films=actor_titles, path=shortest_path, distance=separation)


@app.route('/movie_frm')  # user clicked on Movie in navbar
def movie_frm():
    return render_template('movie_frm.html')  # display the movie lookup form


@app.route('/movie_data/', methods=['POST', 'GET']) # same as actor_data process, but for movies
def movie_data():
    if request.method == 'GET':
        return f"The URL /data is accesed directly. Try going to '/form to submit form"
    if request.method == 'POST':
        form_data = request.form
        movie_name = form_data['Movie']

        try:
            movie_tt = tt_lookup(movie_name)
            movie_cast_codes = cast_lookup(movie_tt)  # create a list of actors from the dictionary lookup
            movie_cast_names = []
            for nm in movie_cast_codes:  # replace their codes with actual names
                name = name_lookup(nm)
                movie_cast_names.append(name)
        except:
            return render_template('movie.html', film='', movie_tt='', actors=[])  # allow error notification

    return render_template('movie.html', film=movie_name, movie_tt=movie_tt, actors=movie_cast_names)        


@app.route('/best/')  # top 20 actors based on centrality graph, and top 20 movies based on ratings
def best():
    top20 = leader_board[:20]
    top_actors=list(top20['Hall of Fame'])
    top_movies=ranked_titles[:20]  # create a top 20 list of movie titles
    return render_template("best.html", top_actors=top_actors, top_movies=top_movies) # display the Top 10 page


@app.route('/about/')  # user clicked on the About link in navbar
def about():  # about section
    return render_template("about.html")  # so redirect them to it, and Carry On!


###  Lookup utilities  ###
def nm_lookup(name):
    nm = name_nm[name]
    return nm

def name_lookup(nm):
    name = nm_name[nm]
    return name

def films_lookup(nm):
    films = nm_tt[nm]
    return films 

def rating_lookup(tt):  # used by API
    rating = tt_rating[tt]
    return rating

def tt_lookup(title):
    tt = title_tt[title]
    return tt

def title_lookup(tt):
    title = tt_title[tt]
    return title

def cast_lookup(tt):
    cast = tt_nm[tt]
    return cast


def load_data():  # read data from tab-delimited files to data structures

    global tt_title, title_tt, tt_nm, tt_rating, nm_name, name_nm, nm_tt, title_rating, sp, ranked_titles
    global cast_crew_info, movie_info, movie_cast_crew, leader_board, lacey_sp, no_pickle_file

    movie_info = pd.read_csv('movie_info.csv', sep='\t', index_col=None, \
                  dtype={'startYear': str, 'runtimeMinutes': str}, \
                  converters={'movieGenres': lambda x: re.split(',+', x)})  
    df = movie_info
    tt_title = dict(zip(df.tconst, df.primaryTitle))  # lookup title by movie ID
    title_tt = dict(zip(df.primaryTitle, df.tconst))  # lookup ID by movie title
    title_rating = dict(zip(df.primaryTitle, df.averageRating))  # lookup rating by movie title
    tt_rating = dict(zip(df.tconst, df.averageRating))  # used by api
    df = pd.DataFrame(list(title_rating.items()),columns = ['column1','column2']) # sort ratings
    df = df.sort_values(["column2", "column1"], ascending=False)  # get the highest ranking up top
    ranked_titles = df['column1'].tolist()  # convert results to a list

    cast_crew_info = pd.read_csv('cast_crew_info.csv', sep='\t', index_col=None)
    df = cast_crew_info 
    nm_name = dict(zip(df.nconst, df.primaryName))  # lookup name by cast ID
    name_nm = dict(zip(df.primaryName, df.nconst))  # lookup ID by cast name

    movie_cast_crew = pd.read_csv('movie_cast_crew.csv', sep='\t', \
      index_col=None)
    df = movie_cast_crew.groupby('nconst')['tconst'].apply(list).reset_index(name="movieList")
    nm_tt = dict(zip(df.nconst, df.movieList))  # lookup movie IDs by actor ID
    df = movie_cast_crew.groupby('tconst')['nconst'].apply(list).reset_index(name="actorList")
    tt_nm = dict(zip(df.tconst, df.actorList))  # lookup actor IDs by movie ID 

    leader_board = pd.read_csv('leader_board.csv', sep='\t', header=[0], index_col=None)
    try:
        lacey_sp = pickle.load(open("lacey_sp.pkl", "rb"))  # shortest path data, pickle 1/4 size of json
    except:
        no_pickle_file = True # allow most functions to run without romcom_prep using .csv and .db files
    return None


if __name__=='__main__': # Launch as a Flask app
    app.run(host="127.0.0.1", debug=True)
