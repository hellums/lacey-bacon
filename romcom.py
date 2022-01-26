# romcom.py

# Import os module for system calls to cls and clear (screen)
import os  # for system calls to clear screen
import csv  # to import TSV files for movie and actor lists

# Define global variables
contender = ""    # Id number of actor/actress in question
role_list = []    # list of actor/actresses that played in each movie
actor_list = []   # curated list of actor/actresses in Hallmark romcoms
movie_list = []   # curated list of Hallmark romcom movies
rating_list = []  # list of ratings for each movie, and total votes

# Create classes, movie data courtesy of imdb.com (interface download)
class Movie:  
  """create Movie class"""
  
  def __init__(self, movieId, movieTitle="", movieRating=None, movieGenres="", movieRuntime=None, movieType="", movieYear=None, movieDirector="", movieActors=""):      
    self.Id = movieId
    self.Title = movieTitle
    self.Rating = movieRating
    self.Genres = movieGenres 
    self.Runtime = movieRuntime
    self.Type = movieType       
    self.Year = movieYear 
    self.Director = movieDirector
    self.Actors = movieActors

class Actor:  # Curated list, details of "Hallmark" leading actor and actress
  """create Actor class"""
  
  def __init__(self, actorId, actorName="", actorBorn=None, actorDied=None):      
    self.Id = actorId
    self.Name = actorName
    self.Born = actorBorn
    self.Died = actorDied

class Role:  # Curated list. all leading actors and actresses starring in Hallmark movie list
  """create Role class"""
  
  def __init__(self, movieId, actorId, actorRole):      
    self.movieId = movieId
    self.actorId = actorId
    self.actorRole = actorRole

class Rating:  # Curated list, rating details on "Hallmark" movies in list
  """create Rating class"""
  
  def __init__(self, movieId, movieRating, movieVotes):      
    self.movieId = movieId
    self.movieRating = movieRating
    self.movieVotes = movieVotes

def clrscr():
  """clears screen in Mac, Linux, or Windows"""
  # Check if Operating System is Mac and Linux or Windows
  if os.name == 'posix':
    _ = os.system('clear')
  else:
      # Else Operating System is Windows (os.name = nt)
    _ = os.system('cls')

def load_movies(movie_list):  
  """takes in an empty list, loads records from file, returns a list of Movie class ojects"""
  with open('src/data/title-basics-imdb.tsv', 'r', encoding='utf8') as f:
    data = csv.reader(f, delimiter='\t') #read tsv text file with csv
    for row in data:
      new_movie = Movie(row[0], row[1], row[2], row[3])
      movie_list.append(new_movie) #add the data from the text file to the list
  return(movie_list)

def load_ratings(rating_list):  
  """takes in an empty list, loads records from file, returns a list of Rating class ojects"""
  with open('src/data/title-ratings-imdb.tsv', 'r', encoding='utf8') as f:
    data = csv.reader(f, delimiter='\t') #read tsv text file with csv
    for row in data:
      new_rating = Rating(row[0], row[1], row[2])
      rating_list.append(new_rating) #add the data from the text file to the list
    return(rating_list)

def load_actors(actor_list):  
  """takes in an empty list, loads records from file, returns a list of Actor class ojects"""
  with open('src/data/name-basics-imdb.tsv', 'r', encoding='utf8') as f:
    data = csv.reader(f, delimiter='\t') #read tsv text file with csv
    for row in data:
      new_actor = Actor(row[0], row[1], row[2], row[3])
      actor_list.append(new_actor) #add the data from the text file to the list
    return(actor_list)

def load_roles(role_list):  
  """takes in an empty list, loads records from file, returns a list of Role class ojects"""
  with open('src/data/title-actors-imdb.tsv', 'r', encoding='utf8') as f:
    data = csv.reader(f, delimiter='\t')  # read tsv text file with csv
    for row in data:
      new_role = Role(row[0], row[1], row[2])
      role_list.append(new_role)  # add the data from the text file to the list
  return(role_list)

# Define function to print a main menu to loop through
def print_menu():
    """prints a main menu for user to input a choice for program flow"""

    # Create dictionary for user menu and item selections
    menu_options = {
        1: 'Option 1',
        2: 'Option 2',
        3: 'Option 3',
        4: 'Exit',
}

    # Loop for main menu until user selects to exit program
    for key in menu_options.keys():
        print (key, '--', menu_options[key] )

def getContenderMovies():
 
  global contender
  contenderMovies = [index for index, item in enumerate(role_list) if item.actorId == contender]
  print(contenderMovies)

# Define functions launched when chosen from main menu by user
def option1():
 
  global contender
  print('\'Option 1\' selected.')
  getContenderMovies()

def option2():
 
  print('\'Option 2\' selected')

def option3():
 
  print('\'Option 3\' selected.')

def option9():  # for debug only, to be removed later
  """(for testing purposes only) validate records loaded from file and addressable"""
  
  global actor_list
  global role_list
  global movie_list
  global rating_list  
  
  total = 0.0
  count = 0
  average = 0.0
  for line in rating_list:
      total = total + float(line.movieRating)
      count = count + 1
  average = total/count

  print ( "actor records: \t", len(actor_list))
  print ( "movie records: \t", len(movie_list))
  print ( "role records: \t", len(role_list))
  print ( "rating records: ", len(rating_list))
  print("average rating: ", format(average, '.1f') )  

# Define main function to print menu and get user choice
def main():
    """command-line menu of functions that process a curated IMDB list of Hallmark original movies (romcom, mystery, drama, western)"""
    
    global contender
    global actor_list
    global role_list
    global movie_list
    global rating_list

    # Clear the screen
    clrscr()

    # Load data from files into list of class objects
    load_movies(movie_list)
    load_actors(actor_list)
    load_roles(role_list)
    load_ratings(rating_list)
    
    # Loop through main menu until user opts to exit
    while(True):

        # Print instructions and menu
        print('\nPlease enter a number between 1 and 4.\n')
        print_menu()

        # Get user's menu choice and verify entry of number, not other char or string
        option = ''
        try:
            option = int(input('\nEnter your choice (1-4) and RETURN: '))
        except:
            print('\nNumbers only, please...')

        # Launch whichever function the user selected from the main menu
        if option == 1:
            clrscr()
            contender = 'nm0000327'  # Lacey Chabert's actorId
            option1()
        elif option == 2:
            clrscr()
            option2()
        elif option == 3:
            clrscr()
            option3()
        elif option == 9:  # for debug only, to be removed later
            clrscr()
            option9()
        elif option == 4:
            clrscr()
            print('\'Option 4\' selected, our work is done here.')
            print("\nDon\'t have a good day... Have a great day!\n")
            exit()
        else:
            pass

# Allow file to be used as function or program
if __name__=='__main__':
    main()
