import src.Cydboperation as Cydboperation 
import getpass
import src.CyMasterPass as CyMasterPass 
import hashlib
import src.CyUi as CyUi
from base64 import b64encode, b64decode
from Crypto.Cipher import AES



'''
CyCrypt.py is a module conataining all the necessary function to encrypt and decrypt the password stored by the user.

'''

def secret_key():
    
    '''
    secret_key() is the function responsible for returning the key that will be used to encrypt and decrypt passwords.

    We used the same piece of code as master password authentification but if the master password true 
    then we will generate a key from the combination of master password + its salt

    '''

    not_authen = True

    while not_authen:

        # creating database operation object to get salt and master pasword hash
        db = Cydboperation.DataBaseOperation()
        salt = db.get_salt()
        hash = db.get_hash()

        # getting the master password from the user and hashing it
        masterpass = getpass.getpass(prompt='\nEnter your master password: ')
        masterpass_hashed = CyMasterPass._hashing(masterpass,salt[0][0])
       
        # comparing the hash generated from the user input with the stored master password hash
        if masterpass_hashed == hash[0][0]:

            not_authen = False
            key = masterpass.encode() + salt[0][0]
            
            # generating the hashed key from combining master password hash with its salt
            hashed_key = hashlib.sha256(key).digest()
            return hashed_key

        else:
            print(CyUi.fail('\nWrong master password try again !'))


def encrypt(password, key):
    
    '''
    encrypt(password, key) function use AES.MODE_EAX to encrypt password using the key generated
    from the secret_key() function, returning a base64 hex composed from verification tag + cipher password + nonce
    '''

    cipher = AES.new(key, AES.MODE_EAX)
    nonce = cipher.nonce
    cipher_password, tag = cipher.encrypt_and_digest(password.encode('utf-8'))
   
    return b64encode(tag + cipher_password + nonce).decode('utf-8')
    

def decrypt(password, key):

    '''
    decrypt() responsible for decryption the stored password
    it convert to bytes the base64 composition (verification tag + cipher password + nonce) returned from the decrypt() function.

    '''

    # converting result of encrypt() to bytes
    bytes_cipher = b64decode(password)

    # extracting encrypted_password to decrypt it, nonce and tag for verification 
    nonce = bytes_cipher[-16:]
    encrypted_password = bytes_cipher[16:-16]
    tag = bytes_cipher[:16]
    
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    password = cipher.decrypt_and_verify(encrypted_password, tag)
    
    return password.decode('utf-8')

    