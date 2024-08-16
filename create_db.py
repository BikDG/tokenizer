import sqlite3
from faker import Faker
from soundex import getInstance

# Initialize Faker
fake = Faker()

# Connect to (or create) a SQLite database
conn = sqlite3.connect('people.db')
cursor = conn.cursor()

# Create a table
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
s = getInstance()
# Insert randomly generated data into the table
for _ in range(1000):  # Adjust the range for more or fewer entries
    firstName = fake.first_name()
    middleName = fake.first_name()
    lastName = fake.last_name()
    middleInitial = middleName[0]
    dob = fake.date_of_birth()
    soundexFirstName = s.soundex(firstName)
    soundexMiddleName = s.soundex(middleName)
    soundexLastName = s.soundex(lastName)
    cursor.execute('''
        INSERT INTO people (firstName, middleName, lastName, soundexFirstName, soundexMiddleName, soundexLastName, middleInitial, dob) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (firstName, middleName, lastName, soundexFirstName, soundexMiddleName, soundexLastName, middleInitial, dob))

# Commit the transaction
conn.commit()

# Close the connection
conn.close()

print("Database and table created with random data.")
