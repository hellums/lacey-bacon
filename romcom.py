# romcom.py 2/22/22 8:35 PM
""" Project for Code Louisvillle python class, provides a menu of IMDB movie functions"""

# Import os module for system calls to cls and clear (screen)
import os  # for system calls to clear screen
import csv  # to import TSV files for movie and actor lists
import unittest 
import re
import pandas as pd  # needs install
import pickle
#import json  # not used at this time
import sqlite3
import matplotlib.pyplot as plt  # needs install
import networkx as nx #needs install
from tabulate import tabulate  # needs install

# Define main function to print menu and get user choice
def main():
    """ Command-line menu of functions Hallmark original movies """
    
    # Clear the screen
    clrscr()

    # Load the data structures
    load_data()

    # Implement a “master loop” console application where the user can repeatedly enter commands,
    # perform actions, including choosing to exit the program. Code Louisville requirement.

    while(True):

        # Print instructions and menu
        print('\nPlease enter a number between 1 and 7.\n')
        print_menu()

        # Get user's menu choice and verify entry data type
        option = ''
        try:
            option = int(input('\nEnter your choice (1-7) and ENTER/RETURN: '))
        except:
            print('\nNumbers only, please...')

        # Launch whichever function the user selected from the main menu
        if option == 0:  # for debug only, to be removed later
            clrscr()
            option0(option)
        elif option == 1:
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
    # Loop for main menu until user selects to exit program
    for key in menu_options.keys():
        print (str(key) + '. ', menu_options[key] )
    return None

# Define functions launched when chosen from main menu by user

def filmography():  # filmography for a person
    actor_name = input('Please enter an actor\'s name (Alison Sweeney, for example) and press enter: ')
    clrscr()
    #actor_name = actor_name.lower()  # normalize it somewhat, in case of poor input formatting
    #actor_name = actor_name.title()  # caused problem with McKellar. Clean up later.
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
    for k, v in enumerate(actor_movies):
        actor_titles.append(tt_title[v])  # lookup the code to get titles
    df = pd.DataFrame(actor_titles)  # prep for pretty print
    total_titles = len(actor_titles)
    #filmography_headers = actor_name + ' Movies'
    print(actor_name, ': ', total_titles, 'Hallmark movies')
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
    df = pd.DataFrame(movie_cast_names)
    total_actors = len(movie_cast_names)
    #movie_info_headers=["IMDB #","Category ","Title  ","Year","Runtime","Genres   ","Rating","Votes"]  # note: bug in tab api
    #tab_print(movie_info.head(10), movie_info_headers)  # "pretty" print result
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
        if no_pickle_file:
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
    about = ['This initiative includes a GitHub repository, which includes more information',
            'as well as a Wiki page and Kanban project schedule.',
            '\nLacey Chabert is widely regarded as the "queen" of Hallmark movies, having', 
            'starred in over 30 Hallmark original romantic comedies, dramas, and mysteries.', 
            'Six Degrees of Kevin Bacon is a meme that cast him as "center of the universe"',
            'in Hollywood.',
            '\nBased on how many movies he\'s starred and costarred in with top actors',
            'and actresses in Hollywood, analysts joked that nobody in Hollywood was',
            'more than six degrees of separation from Kevin. And they backed it up with',
            'research and analyis. Other studies have proven several people are more likely',
            'candidates as the center of the Hollywood metaverse.',
            '\nThis neophyte Python program performs similar analysis on Lacey Chabert within',
            'Hallmark movies. This initiative is associated with a Code Louisville bootcamp',
            'on Python programming and data analysis. It uses a public dataset provided by',
            'IMDB, and provides a command-line program that provides the capability to query',
            'the database to learn more about an actor or actress or the movies they\'ve',
            'costarred in.',
            '\nThis program also includes SQL functions using SQLite3, using the same data.',
            'A few graphs prototyped in Jupyter Notebook will also be displayed.']
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

def option7(option):  
    option = option  # premature optimization
    return None

def option0(option):  # for debug only, to be replaced later with 'easter egg'
    option = option  # premature optimization
    notImplementedYet()
    return None

###  General purpose utilities  ###
def clrscr():  # clears screen in Mac, Linux, or Windows
    # Check if Operating System is Mac and Linux or Windows
    if os.name == 'posix':
        _ = os.system('clear')
    else:
          # Else Operating System is Windows (os.name = nt)
        _ = os.system('cls')
    return None

def notImplementedYet(option):  # stub for drivers and testing
    separator = '\n******************************************************\n'
    print(separator)
    print("'Option", str(option) + "' selected. Section not implemented yet.")
    print(separator)
    return None

def tab_print(df, header_name):  # "pretty" print for a dataframe slice
    print(tabulate(df, headers=header_name, showindex=False, numalign='center'))
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

###  Fuzzy search utilities  ###
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

def load_data():  # read data from tab-delimited files to data structures
    global tt_title, title_tt, tt_nm, nm_name, name_nm, nm_tt, title_rating
    global cast_crew_info, movie_info, movie_cast_crew, leader_board, sp, no_pickle_file
    # Read data from an external file, such as text, JSON, CSV, etc, and use that data in your
    # application. Code Louisville requirement.
    print('Loading data, please wait (15-20 seconds)...')
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
        sp = pickle.load(open("shortest_path.pkl", "rb"))  # shortest path data, pickle 1/4 size of json
    except:
        no_pickle_file = True # allow most functions to run without romcom_prep using .csv and .db files
    return None

# Allow file to be used as function or program
if __name__=='__main__':
    main()
