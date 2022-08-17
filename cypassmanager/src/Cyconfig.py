from os.path import abspath, join
import sqlite3
import src.CyMasterPass as CyMasterPass
import src.CyUi as CyUi

''' 

Cyconfig.py is the module containing the intial configuration for CyPassManager (Database creation and existing
as well as the Master password) when first time use and checking every time the app start.
 
'''



def create_db():

    ''' create_db() function responsible for creating the database at the first use of CyPassManager'''
    
    # abspath will get the absolute path of CyPassManager while join wil generate the right path to db file 
    # (depending on the os that CyPassManager will be executed on to avoid back and forward slash problems) 
    db_path = abspath(join('data', 'cypass.db')) 
    connect = sqlite3.connect(db_path)
    cur = connect.cursor()

    # executing table creation Querys
    try:
        cur.execute(
            ''' CREATE TABLE cymasterpass (
                id int NOT NULL DEFAULT 1,
                cysalt varchar(256),
                cymasterpass varchar(256),
                PRIMARY KEY (id),
                CHECK (id = 1) ) '''
        )
        cur.execute(
            ''' CREATE TABLE cyvault (
                id INTEGER PRIMARY KEY,
                app_name varchar(256) NOT NULL,
                url text NOT NULL,
                username varchar(256) NOT NULL,
                password varchar(256) NOT NULL,
                comment text) '''
        )
        connect.commit()
        print(CyUi.success('\nDatabase has been created successfully !'))
    
    except sqlite3.Error as error:
        print(CyUi.fail(error))

        

def check_config():

    ''' 

    check_config() is a function responsible for checking the existance of the Database
    every time CyPassManager start, in case nothing found it asks the user if he/she want to configure by
    calling create_db() to create a new database and a create_masterpass() for setting up the master password.

    '''

    # We connect to the database using uri set to read write mode to check the existance of the data base
    db_path = abspath(join('data', 'cypass.db')) 
    db_uri = ('file:%s?mode=rw' % db_path)
    
    try:
       conn = sqlite3.connect(db_uri, uri=True)
       print(CyUi.success('[i] Database started'))
       print(CyUi.success('[i] CyPassManager already configured'))
       return True
    
    # In case no database has found we call create_db() and create_masterpass to configure CyPassManager 
    except sqlite3.Error as error:
        
        print(CyUi.fail('CyPassManager is not configured'))
        print(CyUi.fail('No Database has been found !'))
        
        answer = input('\nWould you like to configure a new Database and a Matser password y/n: ')
        
        if answer.lower() == 'y':
            create_db()
            CyMasterPass.create_masterpass()
            return True
        else:
            print(CyUi.warnning('\nSorry you need to configure both Database and Master password to use CyPassManager !'))
            return False
    
       

    

