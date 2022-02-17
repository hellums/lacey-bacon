# romcom.py 2/15/22 11:13 PM
""" Provides a menu screen where user can select various IMDB movie functions"""

# Import os module for system calls to cls and clear (screen)
import os  # for system calls to clear screen
import csv  # to import TSV files for movie and actor lists
import unittest 
import re
import pandas as pd #needs install
import pickle
import json
import sqlite3
import matplotlib.pyplot as plt #needs install
import networkx as nx #needs install
from tabulate import tabulate

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
            option1(option)
        elif option == 2:
            clrscr()
            option2(option)
        elif option == 3:
            clrscr()
            option3(option)
        elif option == 4:
            clrscr()
            option4(option)
        elif option == 5:
            clrscr()
            option5(option)
        elif option == 6:
            clrscr()
            option6(option)
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
        3: 'Costars - See any movie(s) two select people starred in',
        4: 'Leaderboard - ("Hallmark" TV RomComDram Hall of Fame)',
        5: 'About - See more about this project',
        6: 'Graphs - See data analysis charts of ratings, production, etc.',
        7: 'Exit',
    }
    # Loop for main menu until user selects to exit program
    for key in menu_options.keys():
        print (str(key) + '. ', menu_options[key] )
    return None

# Define functions launched when chosen from main menu by user

def option1(option):  # filmography for a person
    option = option  # premature optimization
    actor_name = input('Please enter an actor\'s name (Alison Sweeney, for example) and press enter: ')
    actor_name = actor_name.lower()
    actor_name = actor_name.title()
    try:
        actor_nm = nm_lookup(actor_name)
    except:
        print("\nThat actor is not in the database.")
        try:
            last_name = actor_name.rsplit(' ', 1)[1]  # grab the last name
        except:  # bail if input was single word, or numbers
            return None
        possible_match = actor_fuzzy_search(last_name)  # see if there's anyone with that last name
        if possible_match:
            print('\nPossible last name match:')
            for item in possible_match:
                print(item[0])
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

def option2(option):  # a movie's top actors and actresses
    option = option  # premature optimization
    movie_name = input('Please enter a movie title (Date With Love, for example) and press enter: ')
    try:
        movie_tt = tt_lookup(movie_name)
    except:
        print("\nA movie with that exact title is not in the database.") 
        #input('\nPress ENTER/RETURN to return to main menu: ')
        #return None
        try:
            movie_name = movie_name.rsplit(' ', 1)  # split up the title
            stripped  = [word for word in movie_name if word.lower() not in ['christmas']]
            movie_name = [' '.join(stripped)]  # exlude the word Christmas
            movie_name = max(movie_name, key=len)  # to find a suitable keyword for search
            movie_name = movie_name.lower()  # normalize it somewhat, in case of bad input
            movie_name = movie_name.title()
        except:  # bail if input was single word, or numbers
            return None
        possible_match = movie_fuzzy_search(movie_name)  # see if there's any movie with keyword
        if possible_match:
            print('\nPossible title match:')
            for item in possible_match:  # print out the list of possible alternative titles
                print(item[0])  
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

def option3(option):  # movies where two specific people acted in
    option = option  # premature optimization
    actor1 = 'Lacey Chabert'
    actor2 = 'Luke Macfarlane'
    separation = (sp[actor1][actor2])
    df = pd.DataFrame(separation)
    distance = int(len(separation)/2)
    header_string = (str(distance) + " Degrees Separation - " + str(actor1) + " and " + str(actor2))
    separation_headers = [header_string]
    tab_print(df, separation_headers)
    return None

def option4(option):  # leaderboard
    option = option  # premature optimization
    leader_board_headers=['"Hall of Fame"', "Fame-O-Meter\u2081"]
    tab_print(leader_board[:10], leader_board_headers)
    print('\nNote 1. Calculated using graph analysis and centrality.')
    return None

def option5(option):  # about section
    option = option  # premature optimization
    about_header = 'SIX DEGREES OF LACEY CHABERT\n' + '--------------------------------------------------------------------------------'
    about = ['This initiative includes a GitHub repository, which includes more information',
            'as well as a Wiki page and Kanban project schedule.',
            '\nLacey Chabert is widely regarded as the "queen" of Hallmark movies, having', 
            'starred in over 30 Hallmark original romantic comedies, dramas, and mysteries.', 
            'Six Degrees of Kevin Bacon is a meme that cast him as "center of the universe"',
            'in Hollywood. Based on how many movies he\'s starred and costarred in with top',
            'actors and actresses in Hollywood, analysts joked that nobody in Hollywood was',
            'more than six degrees of separation from Kevin. And they backed it up with',
            'research and analyis. Other studies have proven several people are more likely',
            'candidates as the center of the Hollywood metaverse.',
            '\nThis neophyte Python program performs similar analysis on Lacey Chabert within',
            'Hallmark movies. This initiative is associated with a Code Louisville bootcamp',
            'on Python programming and data analysis. It uses a public dataset provided by',
            'IMDB, and provides a command-line program that provides the capability to query',
            'the database to learn more about an actor or actress or the movies they\'ve',
            'costarred in. Any external analysis from Jupyter Notebook will also be displayed.']
    print(about_header)
    for lines in about:
        print(lines)
    return None

def option6(option):  # show BA plots on ratings, production, etc.
    option = option  # premature optimization 
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

    #df = movie_info
    #plt.show()

    #notImplementedYet()
    return None

def option7(option):  
    option = option  # premature optimization
    return None

def option0(option):  # for debug only, to be replaced later with 'easter egg'
    option = option  # premature optimization
    notImplementedYet()
    return None

def load_data():  # read data from tab-delimited files to data structures
    global tt_title, title_tt, tt_nm, nm_name, name_nm, nm_tt
    global cast_crew_info, movie_info, movie_cast_crew, leader_board, sp 
    # Read data from an external file, such as text, JSON, CSV, etc, and use that data in your
    # application. Code Louisville requirement.
    print('Loading data, please wait (15-20 seconds)...')
    movie_info = pd.read_csv('movie_info.csv', sep='\t', index_col=None, \
                  dtype={'startYear': str, 'runtimeMinutes': str}, \
                  converters={'movieGenres': lambda x: re.split(',+', x)})  
    df = movie_info
    tt_title = dict(zip(df.tconst, df.primaryTitle))  # match title by movie ID
    title_tt = dict(zip(df.primaryTitle, df.tconst))  # match ID by movie title

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
    sp = pickle.load(open("shortest_path.pkl", "rb"))  # shortest path data, pickle 1/4 size of json
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

# Allow file to be used as function or program
if __name__=='__main__':
    main()