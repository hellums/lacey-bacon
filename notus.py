# Import os module for system calls to cls and clear (screen)
import os

# Function to print a main menu to loop through
def print_menu():

    # Dictionary for user menu item selection
    menu_options = {
        1: 'Option 1',
        2: 'Option 2',
        3: 'Option 3',
        4: 'Exit',
}

    # Loop for main menu until user selects to exit program
    for key in menu_options.keys():
        print (key, '--', menu_options[key] )

# Function #1, launched when chosed from main menu by user
def option1():
     print('\'Option 1\' selected.')

# Function #2, launched when chosed from main menu by user
def option2():
     print('\'Option 2\' selected')

# Function #3, launched when chosed from main menu by user
def option3():
     print('\'Option 3\' selected.')

# Function to clear the screen using os.system
def clrscr():
    # Check if Operating System is Mac and Linux or Windows
    if os.name == 'posix':
      _ = os.system('clear')
    else:
        # Else Operating System is Windows (os.name = nt)
      _ = os.system('cls')

def main():
    # Clear the screen
    clrscr()

    # Loop through main menu until user opts to exit
    while(True):

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
