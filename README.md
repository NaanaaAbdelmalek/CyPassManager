# CyPassManager
 <br>     

![images](1.png)

CyPassManager is a simple CLI Password Manager tool that works locally (Offline). It allows to manage passwords and store it securely to a local SQLite database.


## Features

- Configure first time use (creating the database and setup a secure master password hashed using SHA-256 hashing function) 
- Add a new record (application name, url, user, password, a comment)
- Encrypt/Decrypt passwords using AES-256
- Show all the existing records
- Deleting a record
- Search for a record using application name and copy the password to clipboard 
<br>

## Cloning and usage

```
# Clone project
git clone https://github.com/Geekmalek/CyPassManager

# Accessing project folder
$ cd CyPassManager

# Installing dependencies
$ pip install -r requirements.txt

# Run
$ python cypassmanager
```
<br>

The database will be stored in data folder `data/cypass.db`, so each time we execute CyPassManager will check that location to verify the existance of the database.
If existe it will ask you to enter the master password if it's not CyPassManager will create the database file `cypass.db` that stored in `data` folder and it will ask you to setup the master password. 

<br>

> **Note**  
For copying the password to clipboard feature i used pyperclip python module, when using it in a linux system it may throw an error message saying "Pyperclip could not find a copy/paste mechanism for your system." <br />
> To fix this you need to install xclip or xsel via package manager. <br />
> 
> For example, in Debian:   
 sudo apt-get install xclip <br />
 sudo apt-get install xsel
<br>


## ToDo

- Add Update master password
- Add Update a stored record
- Import/Export as Json
- lock when inactivity
- Improving the CLI experience
- Writing tests
- Publishing CyPassManager to PyPi (Python Package Index)


## Licence

Copyright (c) 2022-2023 Naanaa Abdelmalek, <https://github.com/Geekmalek> <br />

[![license](https://img.shields.io/github/license/DAVFoundation/captain-n3m0.svg?style=flat-square)](https://github.com/DAVFoundation/captain-n3m0/blob/master/LICENSE)
