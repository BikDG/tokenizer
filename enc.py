import sqlite3
from faker import Faker
from soundex import getInstance
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import base64

# Initialize Faker
fake = Faker()

# Connect to (or create) a SQLite database
conn = sqlite3.connect('people.db')
cursor = conn.cursor()

# Create a table if it doesn't exist already
cursor.execute('''
    CREATE TABLE IF NOT EXISTS people (
        id INTEGER PRIMARY KEY,
        firstName TEXT,
        middleName TEXT,
        lastName TEXT,
        soundexFirstName TEXT,
        soundexMiddleName TEXT,
        soundexLastName TEXT,
        middleInitial TEXT,
        dob TEXT
    )
''')

# Function to encrypt data
def encrypt_data(data, secret_key):
    cipher = AES.new(secret_key, AES.MODE_CBC)
    iv = cipher.iv  # Generate a random IV
    ct_bytes = cipher.encrypt(pad(data.encode('utf-8'), AES.block_size))
    if data=="Janet":
        print("iv: ", iv, " ct: ", ct_bytes, "\n")
    return base64.b64encode(iv + ct_bytes).decode('utf-8')

# Generate secret key and save it to a file
secret_key = get_random_bytes(32)
with open('secret_key.txt', 'wb') as key_file:
    key_file.write(secret_key)
    print(secret_key)
# Connect to (or create) the encrypted database
conn_enc = sqlite3.connect('encryptedpeople.db')
cursor_enc = conn_enc.cursor()

# Create an encrypted table with the same schema
cursor_enc.execute('''
    CREATE TABLE IF NOT EXISTS people (
        id INTEGER PRIMARY KEY,
        firstName TEXT,
        middleName TEXT,
        lastName TEXT,
        soundexFirstName TEXT,
        soundexMiddleName TEXT,
        soundexLastName TEXT,
        middleInitial TEXT,
        dob TEXT
    )
''')

# Read from the original database, tokenize the data, and insert into the encrypted database
cursor.execute('SELECT * FROM people')
rows = cursor.fetchall()
for row in rows:
    id, firstName, middleName, lastName, soundexFirstName, soundexMiddleName, soundexLastName, middleInitial, dob = row
    encrypted_firstName = encrypt_data(firstName, secret_key)
    encrypted_middleName = encrypt_data(middleName, secret_key)
    encrypted_lastName = encrypt_data(lastName, secret_key)
    encrypted_soundexFirstName = encrypt_data(soundexFirstName, secret_key)
    encrypted_soundexMiddleName = encrypt_data(soundexMiddleName, secret_key)
    encrypted_soundexLastName = encrypt_data(soundexLastName, secret_key)
    encrypted_middleInitial = encrypt_data(middleInitial, secret_key)
    encrypted_dob = encrypt_data(dob, secret_key)
    
    cursor_enc.execute('''
        INSERT INTO people (id, firstName, middleName, lastName, soundexFirstName, soundexMiddleName, soundexLastName, middleInitial, dob)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (id, encrypted_firstName, encrypted_middleName, encrypted_lastName, encrypted_soundexFirstName, encrypted_soundexMiddleName, encrypted_soundexLastName, encrypted_middleInitial, encrypted_dob))

# Commit the transactions and close connections
conn_enc.commit()
conn.commit()
conn.close()
conn_enc.close()

print("Database encrypted and saved to encryptedpeople.db. Secret key saved to secret_key.txt.")
