import pyperclip
import src.Cydboperation as Cydboperation 
import src.CyCrypt as CyCrypt 
import src.CyUi as CyUi

'''

CyClipboard.py containing to_clipboard() that allow the user to search for a record and copy
it's password to the clipboard

'''

def to_clipboard():
    
    # Creating database object and calling search_by_appname()
    # to allow the user to search for a record using its app name
    db = Cydboperation.DataBaseOperation()
    search_result = db.search_by_appname()
     
    # in case no search result found
    if search_result == None:
        return 0 
    
    # in case one search result found
    # that allow to copy it directly to the clipboard in case the user wanted 
    elif len(search_result) == 1:
        
        answer = input('\nWould you like to copy that password (Y)es/(N)o: ')
        
        if answer.lower() == 'y':
            
            password_id = search_result[0][0]
            # preparing decryption key 
            decryption_key = CyCrypt.secret_key()
            # getting the password from the database
            _password = db.get_password_by(password_id)
            # decrypting the password
            decrypted_password = CyCrypt.decrypt(_password[0][0], decryption_key)
            
            # copying the decrypted password to the clipboard 
            pyperclip.copy(decrypted_password)
            print(CyUi.success("\nYour password has been copied to your clipboard"))

        elif answer.lower() == 'n':
            return 0
        else:
            print(CyUi.warnning('\nAnswer with Y for Yes or N for No !'))

    # here in case there is a multiple search result found
    else:
        
        answer = input('\nWould you like to copy a password (Y)es/(N)o: ')
        if answer.lower() == 'y':
            
            # creating a list of record id's found in search result
            # to use it in checking id user input
            search_result_ids = [x[0] for x in search_result]
            password_id = int(input("\nEnter the id of the desired password:"))
            
            # checking if the id entred by the user exist in id's list (search result)
            if password_id in search_result_ids:
                # retrieve the password and decrypt it
                _password = db.get_password_by(password_id)
                # preparing the decryption key
                decryption_key = CyCrypt.secret_key()
                decrypted_password = CyCrypt.decrypt(_password[0][0], decryption_key) 
                
                # copying the password to user clipboard
                pyperclip.copy(decrypted_password)
                print(CyUi.success("\nYour password has been copied to your clipboard"))
            else:
                print("\nEnter one of the available id !")
        
        elif answer.lower() == 'n':
            return 0
        else:
            print(CyUi.warnning('\nAnswer with Y for Yes or N for No !'))