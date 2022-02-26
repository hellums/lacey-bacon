# romcomWeb.py 2/25/22 4:53 PM
""" Project to reuse Code Louisvillle Python data analysis class code for web delivery"""

from importlib.resources import path
import csv  # to import TSV files for movie and actor lists
import re
import pandas as pd  # needs install
import pickle
import sqlite3
import matplotlib.pyplot as plt  # needs install
import networkx as nx #needs install
from flask import Flask, render_template, request, jsonify # needs install

# Initiate the Flask micro web framework
app = Flask(__name__)

@app.route('/')  # initialize program
def home():
    load_data()  # load data structures
    return render_template("home.html") # display the home page

@app.route('/best/')  # top 20 actors based on centrality graph, and top 20 movies based on ratings
def best():
    top20 = leader_board[:20]
    top_actors=list(top20['Hall of Fame'])
    top_movies=ranked_titles[:20]  # create a top 20 list of movie titles
    return render_template("best.html", top_actors=top_actors, top_movies=top_movies) # display the Top 10 page

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
            for k, v in enumerate(actor_movies):
                actor_titles.append(tt_title[v])  # lookup the code to get titles
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

@app.route('/about/')  # user clicked on the About link in navbar
def about():  # about section
    return render_template("about.html")  # so redirect them to it, and Carry On!

def graphs():  # show BA plots on ratings, production, etc.
    df = movie_info
    df = df.groupby(['startYear']).agg({'averageRating': 'median'})[-14:-1]
    df.index.names = ['Year']
    df.plot(kind='line')
    plt.legend(['Average Rating'])
    plt.title('Ratings Increase\n')
    plt.show()

    df = movie_info
    df = pd.crosstab(df.startYear, df.titleType)[-14:-2]
    df.index.names = ['Year']
    df.plot(kind='line')
    plt.legend(['Movie', 'TV Episode', 'TV Mini-Series', 'TV Movie', 'TV Series'])
    plt.title('Production Increase\n')    
    plt.show()
    return None

@app.route('/actors/', methods=['GET'])  # api to return top 10 actors
def api_actors():
    leader_board = pd.read_csv('leader_board.csv', sep='\t', header=[0], index_col=None)
    top10 = leader_board[:10]  # create a top 10 list of actor names
    try:
        top_actors=list(top10['Hall of Fame'])
    except:
        top_actors = list
        return('Something went wrong, or the Hall of Fame is empty. Try returning to the main page first, and try again.')
    return jsonify(top_actors)

@app.route('/movies/', methods=['GET'])  # api to return top 10 movies
def api_movies():
    try:
        top_movies=list(ranked_titles[:10])  # create a top 10 list of movie titles
    except:
        top_movies = list
        return('Something went wrong, or the Hall of Fame is empty. Try returning to the main page first, and try again.')
    return jsonify(top_movies)

@app.route('/rating/', methods=['GET'])  # api to return a specific movie rating
def api_tt():
    # Check if a title code (tt) was provided as part of the URL.
    # If tt is provided, assign it to a variable.
    # If no tt is provided, display an error in the browser.
    if 'tt' in request.args:
        tt = str(request.args['tt'])
    else:
        return "Error: No tt field provided. Please specify a title code (tt)."

    # Create an empty list for our results
    results = []

    # Lookup the rating and return it
    try:
        results.append(rating_lookup(tt))
    except:
        results = list
        return('Something went wrong, or that movies is not in the database. Try returning to the main page first, lookup the movie to find its code (in the movie\'s IMDB link), and try again.')

    # Use the jsonify function from Flask to convert dictionary to JSON format
    return jsonify(results)

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
    # Read data from an external file, such as text, JSON, CSV, etc, and use that data in your
    # application. Code Louisville requirement.
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

# Launch as a Flask app
if __name__=='__main__':
    app.run(debug=True)
