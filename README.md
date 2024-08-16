# Set up virtual env
Windows:
```
python -m venv .venv 
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Linux:
```
python -m venv .venv 
source .\.venv\bin\activate
pip install -r requirements.txt
```
# Generate SQL database with fake information
Windows:
```
python .\create_db.py
```
Linux:
```
python ./create_db.py
```
This will create a database with 1000 entries and fill in the following fields:
```
        id INTEGER PRIMARY KEY,
        firstName TEXT,
        middleName TEXT,
        lastName TEXT,
        soundexFirstName TEXT,
        soundexMiddleName TEXT,
        soundexLastName TEXT,
        middleInitial TEXT,
        dob TEXT
```

# Parse through unencrypted db, encrypt information, and save into encrypted db
Windows:
```
python .\enc.py
```
Linux:
```
python ./enc.py
```
This will create the encrypted db (encryptedperople.db) and the secret key (secret_key.txt) that is used to create a new AES cypher.

#
