import pyfiglet
from termcolor import colored
import colorama
from prettytable import PrettyTable


''' CyUi.py is a module containing all the function responsible for CLI like displaying the logo, colors, menu '''

# to fix some termcolor issues with windows prompt
colorama.init(autoreset=True)

# generating the logo
def logo():
    result = pyfiglet.figlet_format("CyPassManager", font = "doom")
    print('\n',colored(result,"blue"))

# Creating the main menu
fields = ['Menu']
functionality = [['(A)dd'],['(S)how all'],['(D)elete'],['(R)eveal password'],['(E)xit']]

# fields = ['(A)dd', '(S)how all','(D)elete','(r)eveal password','(E)xit' ]

def menu():
    
    ''' 
    this function create a table that showing the choice and the functionality gotten from fields and 
    functionality lists.
    '''
    
    table = PrettyTable()
    table.title = success('Welcome to CyPassManager :)')
    table.field_names = fields

    for f in functionality:
        table.add_row(f)
    print(table)

# Messages coloring functions
def success(message):
    return colored (message,'green')

def warnning(message):
    return colored (message,'yellow')

def fail(message):
    return colored (message,'red')