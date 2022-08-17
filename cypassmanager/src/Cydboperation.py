from os.path import abspath, join
import sqlite3
import getpass
from prettytable import PrettyTable, from_db_cursor
import src.CyCrypt as CyCrypt
import src.CyUi as CyUi


'''
Cydboperation.py is a module containing DataBaseOperation class that is responsible for every database operation like:

- Connecting to the database (creating a database object)
- All of the inserting operation like inserting the master password or a new record
- Retrieving information from the database like getting a password, getting master pasword hash and salt for authentification, showing all the records

'''



class DataBaseOperation:

    def __init__(self):

        '''
        Here is the initialization of the object, in the db_path we get the full path of the database file 
        and in the db_uri we set the only read and write mode for our SQLite database connection cause the default one 
        is the 'rwc' which is read write create mode, to make sure that it will not create a new database each time a new
        object try to do a connection.
        '''
        try:
            db_path = abspath(join('data', 'cypass.db'))  
            db_uri = ('file:%s?mode=rw' % db_path)

            self.connect = sqlite3.connect(db_uri, uri=True)
            self.cur = self.connect.cursor()
            
        except sqlite3.Error as error:
            print(CyUi.fail(error))     



    def insert_masterpass(self, salt, hashed_pass):

        ''' This function responsible for inserting the master password into our Database '''

        Query = 'INSERT INTO cymasterpass(cysalt,cymasterpass) VALUES (?, ?)'
        
        try:
            self.cur.execute(Query,(salt,hashed_pass))
            self.connect.commit()
            print(CyUi.success('\nMaster password has been created successfully !'))
        except sqlite3.Error as error:
            print(CyUi.fail(error))



    def add_record(self):

        '''This function for adding new password record to the database'''

        #Here we prepare our encryption key to use it to encrypt the password before inserting it to our database
        encryption_key = CyCrypt.secret_key()

        # Is_empty as True to keep looping using while and asking for a value in case the user try to pass a blank 
        # if its a valid input we break
        Is_empty = True

        while Is_empty:

            app_name = input('\nName of the application: ')

            if not(app_name.strip()):
                print('\n' + CyUi.fail('Field required !'))
            else:
                break

        while Is_empty:

            url = input('\nApplication URL: ')

            if not(url.strip()):
                print('\n' + CyUi.fail('Field required !'))
            else:
                break

        while Is_empty:

            username = input('\nYour username: ')

            if not(username.strip()):
                print('\n' + CyUi.fail('Field required !'))
            else:
                break 

        while Is_empty:

            password = getpass.getpass(prompt='\nPassword: ') 

            if not (password.strip()):
                print('\n' + CyUi.fail('Field required !'))
            else:
                encrypted_password = CyCrypt.encrypt(password, encryption_key)
                break   

        comment = input('\nObservation: ')

        Query = 'INSERT INTO cyvault(app_name, url, username, password, comment) VALUES (?, ?, ?, ?, ?)'

        try:
            self.cur.execute(Query,(app_name.lower(), url, username, encrypted_password, comment))
            self.connect.commit()
            print(CyUi.success('\nYour record has been added successfully !'))

        except sqlite3.Error as error:
            print(CyUi.fail(error))



    def delete_record(self):
       
        ''' delete_record() allow to delete a record using it's 'id'  '''

        # we call show_all() to get all the records
        self.show_all()

        try:
           row_id = int(input("\nEnter the id record that you want to delete: "))
        
        # throwing an exception value error in case that the input value is not int
        except ValueError:
            print(CyUi.warnning("\nPlease enter a valid id"))
            return 0
        
        Query = 'DELETE FROM cyvault WHERE id=?'

        try:
            self.cur.execute(Query,(row_id,))
            self.connect.commit()
            print(CyUi.success("\nRecord has been deleted successfully"))
        
        except sqlite3.Error as error:
            print(CyUi.fail(error))



    def get_hash(self):

        ''' get_salt and get_hash are gonna retrieve the salt and the master password hash to use it in master password Authentification '''
       
        Query = 'SELECT cymasterpass FROM cymasterpass WHERE id=1'
        
        try:
            self.cur.execute(Query)
            hash = self.cur.fetchall()
            return hash

        except sqlite3.Error as error:
            print(CyUi.fail(error))



    def get_salt(self):
        
        ''' get_salt and get_hash are gonna retrieve the salt and the master password hash to use it in master password Authentification '''
       
        Query = 'SELECT cysalt FROM cymasterpass WHERE id=1'
        
        try:
            self.cur.execute(Query)
            salt = self.cur.fetchall()
            return salt

        except sqlite3.Error as error:
            print(CyUi.fail(error))



    def get_password_by(self, id):\

        '''get_password is a function responsible for selecting a password from the database to decrypt and copy it to clipboard '''

        Query = 'SELECT password FROM cyvault WHERE id=?'

        try:
            cur_result = self.cur.execute(Query,(id,))
            return cur_result.fetchall()

        except sqlite3.Error as error:
            print(CyUi.fail(error))



    def show_all(self):

        '''show_all() will select and show all of the records in our Database to allow the user to get information about accounts password he stored'''

        Query = 'SELECT id, app_name, url, username, comment FROM cyvault'

        try:
            self.cur.execute(Query)
            result = from_db_cursor(self.cur)
            print(result)

        except sqlite3.Error as error:
            print(CyUi.fail(error))



    def search_by_appname(self):

        '''search_byappname is a function that allow us to search a record by it's application name'''

        #Here getting the name of the app from the user
        app_name = input('Enter app name: ')
        Query = 'SELECT * FROM cyvault WHERE app_name=?'
        
        try:

            cur_result = self.cur.execute(Query,(app_name.lower(),))
            fetched_result = cur_result.fetchall()
            
            # We test the fetched result that is not empty 
            if len(fetched_result) != 0 :

                #If it's not empty we print the result in for of a table 
                # and we return the fetched result to use in copying the password to clipboard
                table = PrettyTable(["id","App name","username"])
                for r in fetched_result:
                  table.add_row([r[0],r[1],r[2]])
                
                print("\n",table)   
                return fetched_result
            else:
                print("\nNo result found for",app_name)
                return  None

        except sqlite3.Error as error:
            print(CyUi.fail(error)) 
            return None   
    




   