# romcomWeb.py 2/25/22 9:29 AM
""" Project to reuse Code Louisvillle Python data analysis class code for web delivery"""

from importlib.resources import path
import csv  # to import TSV files for movie and actor lists
import re
import pandas as pd  # needs install
import pickle
import sqlite3
import matplotlib.pyplot as plt  # needs install
import networkx as nx #needs install
from flask import Flask, render_template, request  # needs install

# Initiate the Flask micro web framework
app = Flask(__name__)

@app.route('/')  # initialize program
def home():
    load_data()  # load data structures
    return render_template("home.html") # display the home page

@app.route('/leaders/')  # top 10 actors based on centrality graph, and top 10 movies based on ratings
def leaderboard():  # leaderboard
    leader_board_headers=['"Hall of Fame"', "Fame-O-Meter\u2081"]
    df = sorted(title_rating.items(), key = lambda kv: kv[1], reverse=True)
    top_movie_headers=['Top 20 Movies', "Average Rating"]
    tab_print(df[:20], top_movie_headers)
    return (tab_print(df[:20], top_movie_headers))

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
            return render_template('movie.html', film=movie_name, actors=[])  # allow error notification
    return render_template('movie.html', film=movie_name, actors=movie_cast_names)        

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
    global tt_title, title_tt, tt_nm, nm_name, name_nm, nm_tt, title_rating, sp
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

    leader_board = pd.read_csv('leader_board.csv', sep='\t', index_col=None)
    try:
        lacey_sp = pickle.load(open("lacey_sp.pkl", "rb"))  # shortest path data, pickle 1/4 size of json
    except:
        no_pickle_file = True # allow most functions to run without romcom_prep using .csv and .db files
    return None

# Launch as a Flask app
if __name__=='__main__':
    app.run(debug=True)

# stash code here in case needed later
'''
@app.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response

@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/data/', methods=['POST', 'GET'])
def data():
    if request.method == 'GET':
        return f"The URL /data is accesed directly. Try going to '/form to submit form"
    if request.method == 'POST':
        form_data = request.form
    return render_template('data.html', form_data = form_data)

@app.route('/actor')
def actor():  # filmography for a person
    actor_name = 'Cindy Busby'
    actor_nm = ""
    #actor_nm = nm_lookup(actor_name)
    actor_nm = name_nm[actor_name]    
    actor_movies = nm_tt[actor_nm]  # pull a list of this actor's movie title codes
    actor_titles = []
    for k, v in enumerate(actor_movies):
        actor_titles.append(tt_title[v])  # lookup the code to get titles
    total_titles = len(actor_titles)
    shortest_path=lacey_sp[actor_name]
    separation=int(len(shortest_path)/2)
    return render_template('actor.html', actor=actor_name, num_films =total_titles, films=actor_titles, path=shortest_path, distance=separation)

@app.route('/movie')
def movie():  # a movie's top actors and actresses
    #movie_name = input('Please enter a movie title (Date with Love, for example) and press enter: ')
    movie_name = "It Was Always You"
    movie_tt = tt_lookup(movie_name)
    try:
        movie_tt = tt_lookup(movie_name)
        if not movie_name:  # handle case of an empty string from ENTER/RETURN input
            print("A movie with that exact title is not in the database.") 
            return None
    except:
        if not movie_name:  # handle case of an empty string from ENTER/RETURN input
            print("A movie with that exact title is not in the database.") 
            return None
        print("A movie with that exact title is not in the database.") 
        try:
            movie_name = movie_name.rsplit(' ', 1)  # split up the title
            stripped  = [word for word in movie_name if word.lower() not in ['christmas']]
            movie_name = [' '.join(stripped)]  # exlude the word Christmas
            movie_name = max(movie_name, key=len)  # to find a suitable keyword for search
            #movie_name = movie_name.lower()  # normalize it somewhat, in case of bad input
            #movie_name = movie_name.title() # caused problem with McKellar. Clean up later.
        except:  # bail if input was single word, or numbers
            return None
        possible_match = movie_fuzzy_search(movie_name)  # see if there's any movie with keyword
        if possible_match:
            print('\nPossible title match:')
            for item in possible_match:  # print out the list of possible alternative titles
                print(item[0])  
            print('\nNOTE: titles are punctuation and case sensitive. For example,')
            print('"Good Morning Christmas!" and "Date with Love"')
        input('\nPress ENTER/RETURN to return to main menu: ')
        return None

    movie_cast_codes = cast_lookup(movie_tt)  # create a list of movies from the dictionary lookup
    movie_cast_names = []
    for nm in movie_cast_codes:
        name = name_lookup(nm)
        movie_cast_names.append(name)
    #movie_info_headers=["IMDB #","Category ","Title  ","Year","Runtime","Genres   ","Rating","Votes"]  # note: bug in tab api
    #tab_print(movie_info.head(10), movie_info_headers)  # "pretty" print result
    #print(movie_name, 'had', total_actors, 'main actors and actresses in it:')
    #tab_print(df, '')
    return render_template('movie.html', film=movie_name, actors=movie_cast_names)
'''