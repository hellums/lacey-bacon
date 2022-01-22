# romcom.py
# Import os module for system calls to cls and clear (screen)
import os  # for system calls to clear screen
import csv  # to import TSV files for movie and actor lists

# Create classes, movie data courtesy of imdb.com (interface download)
class Movie:  # Curated list of romantic comedies, mysteries, and dramas, primarily Hallmark originals
  
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
  
  def __init__(self, actorId, actorName="", actorBorn=None, actorDied=None):      
    self.Id = actorId
    self.Name = actorName
    self.Born = actorBorn
    self.Died = actorDied

class Role:  # Curated list. all leading actors and actresses starring in Hallmark movie list
  
  def __init__(self, movieId, actorId, actorRole):      
    self.movieId = movieId
    self.actorId = actorId
    self.actorRole = actorRole

class Rating:  # Curated list, rating details on "Hallmark" movies in list
  
  def __init__(self, movieId, movieRating, movieVotes):      
    self.movieId = movieId
    self.movieRating = movieRating
    self.movieVotes = movieVotes

# Define function to clear screen in multiple os formats    
def clrscr():
    # Check if Operating System is Mac and Linux or Windows
    if os.name == 'posix':
      _ = os.system('clear')
    else:
        # Else Operating System is Windows (os.name = nt)
      _ = os.system('cls')

# Load records from each file as class instances to each list
def load_data():  

  global movie_list # title-basics-imdb.tsv
  movie_list = []  
  with open('data/title-basics-imdb.tsv', 'r', encoding='utf8') as f:
    data = csv.reader(f, delimiter='\t') #read tsv text file with csv
    for row in data:
      new_movie = Movie(row[0], row[1], row[2], row[3])
      movie_list.append(new_movie) #add the data from the text file to the list

  global rating_list  # title-ratings-imdb.tsv 
  rating_list = []  
  with open('data/title-ratings-imdb.tsv', 'r', encoding='utf8') as f:
    data = csv.reader(f, delimiter='\t') #read tsv text file with csv
    for row in data:
      new_rating = Rating(row[0], row[1], row[2])
      rating_list.append(new_rating) #add the data from the text file to the list

  global actor_list  # name-basics-imdb.tsv
  actor_list = []
  with open('data/name-basics-imdb.tsv', 'r', encoding='utf8') as f:
    data = csv.reader(f, delimiter='\t') #read tsv text file with csv
    for row in data:
      new_actor = Actor(row[0], row[1], row[2], row[3])
      actor_list.append(new_actor) #add the data from the text file to the list

  global role_list  # title-actors-imdb.tsv
  role_list = []
  with open('data/title-actors-imdb.tsv', 'r', encoding='utf8') as f:
    data = csv.reader(f, delimiter='\t') #read tsv text file with csv
    for row in data:
      new_role = Rating(row[0], row[1], row[2])
      role_list.append(new_role) #add the data from the text file to the list

# Define function to print a main menu to loop through
def print_menu():

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

# Define functions launched when chosen from main menu by user
def option1():
     print('\'Option 1\' selected.')

def option2():
     print('\'Option 2\' selected')

def option3():
     print('\'Option 3\' selected.')

def option9():  # for debug only, to be removed later
    # Validate records loaded from file and addressable
        print ( actor_list[0].Id, actor_list[1].Id, type(actor_list), "\n" )
        print ( "# actors: ", len(actor_list))
        print ( "# movies: ", len(movie_list))
        print ( "# ratings: ", len(rating_list))
        print ( "# roles: ", len(role_list))
        #print ( role_list.__sizeof__() )
        #print ( dir(Actor) )
        #next(item for item in movie_list if item["Id"] == "tt10921042", None)
        total = 0.0
        count = 0
        average = 0.0
        for line in rating_list:
            total = total + float(line.movieRating)
            count = count + 1
        average = total/count
        print("average rating:", format(average, '.1f') )

# Define main function to print menu and get user choice
def main():

    # Clear the screen
    clrscr()

    # Load data from files into list of class objects
    load_data()

    # Loop through main menu until user opts to exit
    while(True):

        # Print instructions and menu
        print('\nPlease enter a number between 1 and 4.\n')
        print_menu()

        # Get user's menu choice and verify entry of number, not other char or string
        option = ''
        try:
            option = int(input('\nEnter your choice (1-4): '))
        except:
            print('\nNumbers only, please...')

        # Launch whichever function the user selected from the main menu
        if option == 1:
            clrscr()
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
            print('\nDon\'t have a good day... Have a great day!\n')
            exit()
        else:
            pass

# Allow file to be used as function or program
if __name__=='__main__':
    main()
