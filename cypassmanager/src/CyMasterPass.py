import os
import re
import hashlib
import getpass
import src.Cydboperation as Cydboperation
import src.CyUi as CyUi


'''
CyMasterPass.py is a module containing everything about the master password
creating, validation, hashing, authentification.

'''



def create_masterpass():
    
    ''' this function is used to create the master password'''
    
    validation = False

    while not validation:

        # asking the user for the master password 
        crud_pass = getpass.getpass(prompt="\nChoose a Master password: ")
        # passing it to password_validator() to check for the contraint (Upper case letters, numbers ..)
        validation = password_validator(crud_pass)
    
    # generating the salt
    salt = os.urandom(32) 
    # calling password_hashing() to hash the (master password + salt)
    hashed_pass = _hashing(crud_pass,salt)
    db = Cydboperation.DataBaseOperation()
    db.insert_masterpass(salt,hashed_pass)



def password_validator(input):

    '''
    This function will check the master password contraints:
     - Having a len() >= 8
     - at least one Upper case char
     - at least one number
    '''

    if not (len(input) >= 8):
        print(CyUi.fail('\nYour master password is less than 8 character'))
        return False
    
    elif not re.findall('[A-Z]',input):
        print(CyUi.fail('\nYour master password does not contain upper case latters'))
        return False
    
    elif not re.findall('\d',input):
        print(CyUi.fail('\nYour master password does not contain any number'))
        return False

    else:
        return True



def _hashing(crud_pass,salt):
    
    '''
    _hashing() use the SHA-256 hashing function to hash (master password + salt)

    '''
    crud_salted = crud_pass.encode() + salt
    hashed_pass = hashlib.sha256(crud_salted)
    return hashed_pass.hexdigest()



def masterpass_auth():
    '''
    masterpass_auth() will do the authentification for master password, everytime the user enter it
    the function will retrieve the salt and the master password hash, once it entred it will be hashed
    using the salt to generate the full master password hash and compare it to the one retrieved from the database.

    '''
    not_authen = True
    
    # this while loop is for keeping asking the user for the master password
    while not_authen:

        # making a database object to call get_salt() and get_hash()
        db = Cydboperation.DataBaseOperation()
        salt = db.get_salt()
        hash = db.get_hash()

        # asking for the master password and hashing it using its salt
        masterpass = getpass.getpass(prompt='\nPlease enter your master password: ')
        masterpass_hashed = _hashing(masterpass,salt[0][0])

        # checking the generated hash with the one retrieved
        if masterpass_hashed == hash[0][0]:
            not_authen = False
        else:
            print(CyUi.fail('\nWrong master password try again !'))



