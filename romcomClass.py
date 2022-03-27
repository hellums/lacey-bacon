import networkx as nx  #needs install
import pandas as pd  # needs install
import matplotlib.pyplot as plt  # needs install


global movies, actors  # dictionaries of class objects < IMDB files


class actor: 

    def __init__(self, ident, name, yrBorn, yrDied):
        self.ident = ident
        self.name = name
        self.yrBorn = yrBorn
        self.yrDied = yrDied
        self.movies = set()
        self.rating = str

    def __repr__(self):
        return "Class object for cast member of a Hallmark movie \
listed in private IMDB watchlist"

    def __str__(self):
        print("Name:", self.name)
        print("IMDB#:", self.ident)
        print("Avg Rating:", self.rating)
        print("Year born:", self.yrBorn)
        print("Year died:", end=" ")
        return self.yrDied

    def add_movie (self, movie):
        self.movies.add(movie)
        return(None)
    
    def avg_rating (self):
        total = 0.0
        for val in self.movies:
            try:
                total += float(movies[val].rating)
            except:
                pass
        try:
            rating = total / len(self.movies)
            self.rating = str("{:.1f}".format(rating))
        except:
            pass  # zero division case where no movies are associated
        return (self.rating)

    def num_movies(self):
        return(None)

    def movie_list(self):
        filmography = set()
        for val in self.movies:
            filmography.add(movies[val].name)
        return (filmography)


class movie:
    def __init__(self, ident, category, name, released, minutes,
                genres, rating, votes):
        self.ident = ident
        self.category = category
        self.name = name
        self.released = released
        self.minutes = minutes 
        self.genres = genres
        self.rating = rating
        self.votes = votes
        self.cast = set()

    def __repr__(self):
        return "Class object for a Hallmark movie listed in a private \
IMDB watchlist"

    def __str__(self):
        print("Title:", self.name)
        print("IMDB #:", self.ident)
        print("Type:", self.category)
        print("Release Year:", self.released)
        print("Runtime:", self.minutes, "minutes")
        print("Genres:", self.genres)
        print("Avg Rating:", self.rating)
        print("Number of votes:", end=" ")
        return (self.votes)

    def add_cast (self, cast):
        self.cast.add(cast)
        return None

    def cast_list(self):
        for val in self.cast:
            print(actors[val].name)
        return None

def createActorRecords():
    global actors
    actors = dict()
    file = 'cast_crew_info.csv'
    row = list()
    try:
        data = open(file,"r")
        next(data)  # skip header row  
        for line in data:
            row = line.split("\t")  # read "tsv" file
            new_actor = actor(row[0], row[1], row[2], row[3])
            actors[row[0]] = new_actor  # add record to dictionary
    except:
        pass
    data.close()
    return None


def createMovieRecords():
    global movies
    movies = dict()
    file = 'movie_info.csv'
    row = list()
    try:
        data = open(file,"r")
        next(data)  # skip header row
        for line in data:
            row = line.split("\t")  # read "tsv" file
            new_movie = movie(row[0], row[1], row[2], row[3], 
                            row[4], row[5], row[6], row[7])
            movies[row[0]] = new_movie  # add record to dictionary
    except:
        pass
    data.close()
    return None

def linkMoviesToActors():
    file = 'movie_cast_crew.csv'
    row = list()
    try:
        data = open(file,"r")
        next(data)  # skip header row
        for line in data:
            row = line.split("\t")  # read "tsv" file
            actors[row[1]].add_movie(row[0]) # update filmography 
            movies[row[0]].add_cast(row[1]) # update cast list
    except:
        pass
    data.close()
    return None

def printActorInfo(name):
    try:
        k = next((row for row in actors 
            if actors[row].name == name), None)
    except:
        pass
    if k != None:    
        print("\n------------\n BASIC INFO\n------------\n")
        print(actors[k])
#        print("Average movie rating:", \
#            "{:.2f}".format(actors[k].rating))
        h_line = "----------------------\n"
        print(h_line, "HALLMARK FILMOGRAPHY\n" + h_line)
        movieList = actors[k].movie_list()
        for movie in movieList:
            print(movie)
    else:
        print("\nThat name was not found in the database.")
    return(None)

def lookupActorByName(name):
    k = next((row for row in movies 
        if movies[row].name == name), None)
    return(k)

def printMovieInfo(name):
    try:
        k = next((row for row in movies 
        if movies[row].name == name), None)
    except:
        pass  # case of actor name not in dictionary
    if k != None:
        print("\n------------\n BASIC INFO\n------------\n")
        print(movies[k])
        h_line = "--------------------------\n"
        print(h_line, "PRIMARY ACTORS/ACTRESSES\n" + h_line)
        movies[k].cast_list()
        print()
    else:
        print("\nThat title was not found in the database. Titles are \
case-sensitive, including puncturation. For example: Good Morning, \
Christmas!")
    return(None)

def printDegreeSeparation(name):
    try:  # see if there is a link from name entered and Lacey Chabert
        connection = sp[name]
    except:
        print('\nThis actor has no known connections to Lacey. Are \
you sure you spelled the name correctly? Some actors use middle names \
or initials in IMDB lists. For example: Andrew W. Walker')
        return None
    distance = int(len(connection)/2)  # count of movies between actors
    print("\n" + str(distance) + " Degree(s) of Separation")
    print(*connection, sep=' -> ', end='\n')
    return None

def createNetworkGraph():  # for text-based representing Lacey distance
    global sp
    G = nx.Graph()
    for k in actors:
        G.add_node(actors[k].name)
    for k in movies:
        G.add_node(movies[k].name)
    for k in actors:
        for role in actors[k].movies:
            G.add_edge(actors[k].name, movies[role].name)
    sp = dict(nx.single_source_shortest_path(G, 'Lacey Chabert',
        cutoff=7))
    return None

def printTopRatedActors():  # Top 10 avg movie ratings by actor
    print("\n--------\n TOP 10\n--------\n")
    for k, v in sorted(actors.items(), key=lambda item: item[1].rating,
                    reverse=True)[:10]:
        print(f'{actors[k].rating:<5}' + "| ", actors[k].name)
    return None

def printTopRatedMovies():  # Top 10 avg movie ratings by actor
    print("\n--------\n TOP 10\n--------\n")
    for k, v in sorted(movies.items(), key=lambda item: item[1].rating,
                    reverse=True)[:10]:
        print(f'{movies[k].rating:<5}' + "| ", movies[k].name)
    return None

def menuPrompt(option):
    prompts = list()
    prompts.append('\nFull name of Hallmark actor/actress (for \
example, Alison Sweeney, Ryan Paevey): ')
    prompts.append('\nTitle of Hallmark movie (case-sensitive, \
for example, Date with Love, It Was Always You): ')
    prompts.append('\nFull name of Hallmark actor/actress (for \
example, Tyler Hynes, Wes Brown): ')
    prompts.append('\nMenu 4: ')
    prompts.append('\nMenu 5: ')
    prompts.append('\nMenu 6: ')
    prompts.append('\n\'Option 7\' selected, our work is done here.\n\
\nDon\'t have a good day... Have a great day!\n')
    return prompts[option-1]

def addActorRating():
    for k in actors:
        actors[k].avg_rating()

def showPlots():

    myList = list()
    for k, v in sorted(movies.items(), key=lambda item: item[1].released):
        myList.append(movies[k].__dict__)  # store sorted records in list

    df = pd.DataFrame.from_records(myList)  # import list to dataframe
    df = df.groupby('released').agg({'rating': 'median'})[-14:-1]  # last 14 years
    df.index.names = ['Year']  # ratings by year
    df.plot(kind='line')
    plt.legend(['Average Rating'])
    plt.title('Ratings Increase\n')
    plt.show()

    df = pd.DataFrame.from_records(myList)  # reload dataframe from list
    df = pd.crosstab(df.released, df.category)[-14:-2]
    df.index.names = ['Year']  # movie categories by year
    df.plot(kind='line')
    plt.legend(['Movie', 'TV Episode', 'TV Mini-Series', 'TV Movie', 'TV Series'])
    plt.title('Production Increase\n')    
    plt.show()

def main():

    createActorRecords()
    createMovieRecords()
    linkMoviesToActors()
    addActorRating()
    createNetworkGraph()

    option = ''  # Get user's menu choice and verify entry data type
    menu_options = {  # dictionary of menu options
        1: 'Actor Info Search',
        2: 'Movie Info Search',
        3: 'Lacey # - "Distance" from Lacey in the "Hallmark Universe"',
        4: 'Top 10 Rated Actors',
        5: 'Top 10 Rated Movies',
        6: 'Various Data Plots',
        7: 'Exit',
    }

    while(True):
        print("\n---- MAIN MENU ----\n")
        for key in menu_options.keys():  # loop main menu until quit
            print (str(key) + '. ', menu_options[key] )
        try:
            option = int(input('\nEnter your choice (1-7) and \
ENTER/RETURN: '))
        except:
            print('\nNumbers only, please...')

        if option == 1:  # launch functions user selected from menu
            name = input(menuPrompt(option))
            printActorInfo(name)
        elif option == 2:
            name = input(menuPrompt(option))
            printMovieInfo(name)
        elif option == 3:
            name = input(menuPrompt(option))
            printDegreeSeparation(name)
        elif option == 4:
            printTopRatedActors()
        elif option == 5:
            printTopRatedMovies()
        elif option == 6:
#            print(movies['tt13831504'])
#            print(movies['tt13831504'].__dict__)
            showPlots()
        elif option == 7:
            print(menuPrompt(option))
            exit()
        else:
            pass  # continue looping
    return None

if __name__=='__main__':  # Allow use as function or program
    main()

