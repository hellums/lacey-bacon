# romcomWeb.py 2/26/22 5:45 PM
""" Project to reuse Code Louisvillle Python data analysis class code for API delivery"""

import csv  # to import TSV files for movie and actor lists
import re
import pandas as pd  # needs install
from flask import Flask, render_template, request, jsonify # needs install

# Initiate the Flask micro web framework for API delivery on port (:8080)
api = Flask(__name__)

@api.route('/')  # initialize program, load data structures
def starting_url():
    load_data()   # load data structures
    status_code = "201"  # won't take Flask.Response(status=201) for some reason, continue to debug
    return status_code

@api.route('/actors/', methods=['GET'])  # endpoint to return top 10 actors, http://localhost:8080/actors
def api_actors():
    leader_board = pd.read_csv('leader_board.csv', sep='\t', header=[0], index_col=None)
    top10 = leader_board[:10]  # create a top 10 list of actor names
    try:
        top_actors=list(top10['Hall of Fame'])
    except:
        top_actors = list
        return('Something went wrong, or the Hall of Fame is empty. Try returning to the main page first, and try again.')
    return jsonify(top_actors)

@api.route('/movies/', methods=['GET'])  # endpoint to return top 10 movies, http://localhost:8080/movies
def api_movies():
    try:
        top_movies=list(ranked_titles[:10])  # create a top 10 list of movie titles
    except:
        top_movies = list
        return('Something went wrong, or the Hall of Fame is empty. Try returning to the main page first, and try again.')
    return jsonify(top_movies)

@api.route('/rating/', methods=['GET'])  # endpoint to return a specific movie rating, e.g. /rating/?tt=tt13831504
def api_tt():
    
    if 'tt' in request.args: # Check if a title code (tt) was provided as part of the URL.
        tt = str(request.args['tt']) # If tt is provided, assign it to a variable.
    else:   # Display an error in the browser.
        return "Error: No tt field provided. Please specify a title code (tt)."

    
    results = [] # Create an empty list for our results

    try:
        results.append(rating_lookup(tt)) # Lookup the rating and return it
    except:
        results = list
        return('Something went wrong, or that movies is not in the database. Try returning to the main page first, lookup the movie to find its code (in the movie\'s IMDB link), and try again.')    

    return jsonify(results) # Use the jsonify function from Flask to convert dictionary to JSON format

def rating_lookup(tt):  # used by API
    rating = tt_rating[tt]
    return rating

def load_data():  # read data from tab-delimited files to data structures
    global tt_rating, title_rating, ranked_titles, movie_info, leader_board
    # Read data from an external file, such as text, JSON, CSV, etc, and use that data in your
    # application. Code Louisville requirement.

    movie_info = pd.read_csv('movie_info.csv', sep='\t', index_col=None, \
                  dtype={'startYear': str, 'runtimeMinutes': str}, \
                  converters={'movieGenres': lambda x: re.split(',+', x)})  
    df = movie_info
    title_rating = dict(zip(df.primaryTitle, df.averageRating))  # lookup rating by movie title
    tt_rating = dict(zip(df.tconst, df.averageRating))  # used by api
    df = pd.DataFrame(list(title_rating.items()),columns = ['column1','column2']) # sort ratings
    df = df.sort_values(["column2", "column1"], ascending=False)  # get the highest ranking up top
    ranked_titles = df['column1'].tolist()  # convert results to a list

    leader_board = pd.read_csv('leader_board.csv', sep='\t', header=[0], index_col=None)
    return None

if __name__=='__main__': # Launch as a Flask app
    api.run(host="127.0.0.1", port=8080, debug=True)