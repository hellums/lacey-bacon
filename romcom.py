# romcom.py 2/28/22 10:07 PM
""" Project for Code Louisvillle python class, provides a menu of IMDB movie functions"""


import os  # for system calls to clear screen
import csv  # to import TSV files for movie and actor lists
import unittest 
import pickle
import gzip
import sqlite3

import pandas as pd  # needs install
import matplotlib.pyplot as plt  # needs install
import networkx as nx #needs install
import re
from tabulate import tabulate  # needs install
from natsort import natsorted

global tt_title, title_tt, tt_nm, nm_name, name_nm, nm_tt, title_rating, lacey_sp
global cast_crew_info, movie_info, movie_cast_crew, leader_board, sp, one_sp_pkl, all_sp_pkl


###  Main Menu  ###
def main():
    """ Command-line menu of functions Hallmark original movies """
    
    clrscr() # Clear the screen
    print('Loading data, please wait (15-20 seconds)...')  # Load the data structures
    load_data()

    # Implement a “master loop” console application where the user can repeatedly enter commands,
    # perform actions, including choosing to exit the program. Code Louisville requirement.

    while(True):
        
        print('\nPlease enter a number between 1 and 7.\n')  # warn user of short delay
        print_menu()  # Print instructions and menu
        
        option = ''  # Get user's menu choice and verify entry data type
        try:
            option = int(input('\nEnter your choice (1-7) and ENTER/RETURN: '))
        except:
            print('\nNumbers only, please...')

        # Launch whichever function the user selected from the main menu
        if option == 1:
            clrscr()
            filmography()
        elif option == 2:
            clrscr()
            cast()
        elif option == 3:
            clrscr()
            deg_separation()
        elif option == 4:
            clrscr()
            leaderboard()
        elif option == 5:
            clrscr()
            graphs()
        elif option == 6:
            clrscr()
            about()
        elif option == 7:
            #clrscr()
            print('\n\'Option 7\' selected, our work is done here.')
            print("\nDon\'t have a good day... Have a great day!\n")
            exit()
        else:
            pass
    return None

def print_menu():  # basic menu screen for user to select program feature sets
    menu_options = {  # dictionary of menu options
        1: 'Filmography - See what movies a select person starred in',
        2: 'Cast - See who starred in a select movie',
        3: 'Degree Separation - Distance between people in the "Hallmark Universe"',
        4: 'Leaderboard - "Hallmark" TV RomComDram Hall of Fame',
        5: 'Graphs - See data analysis charts of ratings, production, etc.',
        6: 'About - See more about this project',
        7: 'Exit',
    }

    for key in menu_options.keys():  # loop main menu until user selects quit
        print (str(key) + '. ', menu_options[key] )
    return None

###  Menu Functions  ###


def filmography():  # filmography for a person
    actor_name = input('Please enter an actor\'s name (Alison Sweeney, for example) and press enter: ')
    clrscr()

    try:
        actor_nm = nm_lookup(actor_name)
    except:
        print("That actor is not in the database.")

        try:
            last_name = actor_name.rsplit(' ', 1)[1]  # grab the last name
        except:  # bail if input was single word, or numbers
            return None

        possible_match = actor_fuzzy_search(last_name)  # see if there's anyone with that last name
        if possible_match:
            print('\nPossible last name match:')
            for item in possible_match:
                print(item[0])
            print('\nNOTE: names are case sensitive.') 
        input('\nPress ENTER/RETURN to return to main menu: ')
        return None

    # Create and call at least 3 functions or methods, at least one of which must return a value
    # that is used somewhere else in your code. Code Louisville requirement.
    actor_movies = nm_tt[actor_nm]  # pull a list of this actor's movie title codes
    actor_titles = []
    for each in natsorted(actor_movies, reverse=True): # sort by one-up assigned tt numbers
        actor_titles.append(tt_title[each])  # lookup the code to get titles
    df = pd.DataFrame(actor_titles)  # prep for pretty print
    total_titles = len(actor_titles)
    separation = list(lacey_sp[actor_name])
    print(actor_name, 'is', int((len(separation)/2)), 'Degrees of Separation from Lacey Chabert:\n')
    print(*separation, sep = " <-> ")
    print('\n')
    print(total_titles, 'Hallmark movies')
    tab_print(df, '')
    return None


def cast():  # a movie's top actors and actresses
    movie_name = input('Please enter a movie title (Date with Love, for example) and press enter: ')
    clrscr()

    try:
        movie_tt = tt_lookup(movie_name)
        if not movie_name:  # handle case of an empty string from ENTER/RETURN input
            print("A movie with that exact title is not in the database.") 
            return None
    except:
        print("A movie with that exact title is not in the database.") 

        try:
            if movie_name.lower() == 'christmas' or movie_name.lower() == ' christmas':
                movie_name = 'bazinga Christmas'  # workaround, "Christmas" only fails next line
            movie_name = movie_name.rsplit(' ', 1)  # split up the title
            stripped  = [word for word in movie_name if word.lower() not in ['christmas']]
            movie_name = [' '.join(stripped)]  # exlude the word Christmas
            movie_name = max(movie_name, key=len)  # to find a suitable keyword for search
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
    df = pd.DataFrame(movie_cast_names)
    total_actors = len(movie_cast_names)
    print(movie_name, 'had', total_actors, 'main actors and actresses in it:')
    tab_print(df, '')
    return None


def deg_separation():  # connectivity between two actors based on who they starred with in other movies
    clrscr()
    print('Please enter two actor or actress first and last names.')
    actor1 = input('First person? ')
    actor2 = input('Second person? ')
    clrscr()

    try:  # see if they ran _prep first, and allow most program functions to work without crash on load
        separation = (sp[actor1][actor2])  # lookup any movie connection shortest path between actors
    except:  # can't do degree separation without the SP file, so gracefully warn, instruct, and exit
        if all_sp_pkl == False:
            print('One or more files were not installed using the prep program. Please run that before main program.')
            return None
        else:
            print('One or more of those two names were not in the database. Try looking them up in menu item 1.')
        input('\nPress ENTER/RETURN to return to main menu: ')
        return None

    try:
        df = pd.DataFrame(separation)  # prepare for pretty print
        distance = int(len(separation)/2)  # count of movies between actors
        header_string = (str(distance) + " Degree(s) Separation - " + str(actor1) + " and " + str(actor2))
        separation_headers = [header_string]
        tab_print(df, separation_headers)
    except:
        print('There are no connections between the two people, or something else went wrong.')
    return None


def leaderboard():  # leaderboard
    clrscr()
    leader_board_headers=['"Hall of Fame"', "Fame-O-Meter\u2081"]
    tab_print(leader_board[:10], leader_board_headers)
    print('\nNote 1. Calculated using graph analysis and centrality.\n')
    df = sorted(title_rating.items(), key = lambda kv: kv[1], reverse=True)
    top_movie_headers=['Top 20 Movies', "Average Rating"]
    tab_print(df[:20], top_movie_headers)
    input('\nPress ENTER/RETURN to return to main menu: ')
    clrscr()
    return None


def about():  # about section
    clrscr()
    about_header = 'SIX DEGREES OF LACEY CHABERT\n' + '--------------------------------------------------------------------------------'
    about = ['This initiative includes a GitHub repository, which contains more information',
            'as well as a Wiki page and Kanban project schedule.',
            '\nThis Python program performs a "Kevin Bacon"-esque analysis of Lacey Chabert and',
            'Hallmark movies. This effort is associated with a Code Louisville bootcamp',
            'on Python programming and data analysis.',
            '\nIt uses a public dataset provided by IMDB, and includes a command-line program',
            'with general-purpose search utilities, Jupyter Notebook analysis, a Flask-based',
            'web interface, and a basic Flask API module.']
    print(about_header)
    for lines in about:
        print(lines)
    return None


def graphs():  # show BA plots on ratings, production, etc.
    clrscr()
    print('INSTRUCTIONS:')
    print('This page allows you to see several popup graphs, one at a time. You')
    print('will need to close each one out after viewing it, to see the next.')
    print('Once you have closed the last graph, you can continue with this')
    print('program. Press ENTER/RETURN to see the charts now...')
    _ = input()

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

    clrscr()
    return None

###  General purpose utilities  ###


def clrscr():  # clears screen in Mac, Linux, or Windows
    
    if os.name == 'posix':  # Operating System is Mac and Linux ?
        _ = os.system('clear')
    else:          
        _ = os.system('cls')  # Operating System is Windows (os.name = nt)
    return None


def tab_print(df, header_name):  # "pretty" print for a dataframe slice
    print(tabulate(df, headers=header_name, showindex=False, numalign='center'))
    return None


def load_data():  # read data from tab-delimited files to data structures
    global tt_title, title_tt, tt_nm, nm_name, name_nm, nm_tt, title_rating, lacey_sp
    global cast_crew_info, movie_info, movie_cast_crew, leader_board, sp, one_sp_pkl, all_sp_pkl
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

    all_sp_pkl = one_sp_pkl = True
    try:
        with gzip.open('shortest_path.pkl.gz', 'rb') as f:  # unpack the actor shortest path routes
            data = f.read()
        with open('shortest_path.pkl', 'wb') as f:
            f.write(data)
        sp = pickle.load(open("shortest_path.pkl", "rb"))
    except:
        all_sp_pkl = False # allow most functions to run without romcom_prep using .csv and .db files

    try:
        lacey_sp = pickle.load(open("lacey_sp.pkl", "rb"))  # shortest path data for just Lacey
    except:
        one_sp_pkl = False # allow most functions to run without romcom_prep using .csv and .db files

    return None

###  Lookup utilities  ###


def nm_lookup(name):
    nm = name_nm[name]
    return nm


def name_lookup(nm):
    name = nm_name[nm]
    return name


def tt_lookup(title):
    tt = title_tt[title]
    return tt


def title_lookup(tt):
    title = tt_title[tt]
    return title


def cast_lookup(tt):
    cast = tt_nm[tt]
    return cast


def actor_fuzzy_search(name):  # find anyone with unexpected initials, St., full middle name, etc. 
    conn = sqlite3.connect('movies.db')
    sql_query = "SELECT primaryName FROM cast_crew_info WHERE primaryName LIKE '%"+name+"'"
    cursor=conn.cursor()
    cursor.execute(sql_query)
    results = cursor.fetchall()
    conn.close()
    return results


def movie_fuzzy_search(title):  # find any movie with prominent word in title
    conn = sqlite3.connect('movies.db')
    sql_query = "SELECT primaryTitle FROM movie_info WHERE primaryTitle LIKE '%"+title+"%'"
    cursor=conn.cursor()
    cursor.execute(sql_query)
    results = cursor.fetchall()
    conn.close()
    return results


if __name__=='__main__':  # Allow file to be used as function or program
    main()
