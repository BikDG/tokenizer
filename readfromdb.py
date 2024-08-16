import sqlite3
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import base64


def encrypt_data(data, secret_key):
    cipher = AES.new(secret_key, AES.MODE_CBC)
    iv = cipher.iv  # Generate a random IV
    ct_bytes = cipher.encrypt(pad(data.encode('utf-8'), AES.block_size))
    return base64.b64encode(iv + ct_bytes).decode('utf-8')

# Function to decrypt data
def decrypt_data(encrypted_data, secret_key):
    encrypted_data_bytes = base64.b64decode(encrypted_data)
    iv = encrypted_data_bytes[:AES.block_size]
    ct = encrypted_data_bytes[AES.block_size:]
#    print("iv: ", iv.decode('utf-8'), "ct: ", ct.decode('utf-8'))
    cipher = AES.new(secret_key, AES.MODE_CBC, iv)
    original_data = unpad(cipher.decrypt(ct), AES.block_size)
    return original_data.decode('utf-8')

#cursor_enc.execute('SELECT * FROM people')
#rows = cursor_enc.fetchall()
#for row in rows:
#    id, firstName, middleName, lastName, soundexFirstName, soundexMiddleName, soundexLastName, middleInitial, dob = row
#    encrypted_firstName = decrypt_data(firstName, secret_key)
#    encrypted_middleName = decrypt_data(middleName, secret_key)
#    encrypted_lastName = decrypt_data(lastName, secret_key)
#    encrypted_soundexFirstName = decrypt_data(soundexFirstName, secret_key)
#    encrypted_soundexMiddleName = decrypt_data(soundexMiddleName, secret_key)
#    encrypted_soundexLastName = decrypt_data(soundexLastName, secret_key)
#    encrypted_middleInitial = decrypt_data(middleInitial, secret_key)
#    encrypted_dob = decrypt_data(dob, secret_key)

def retrieve_data(secret_key, id=None, firstName=None, middleName=None, lastName=None, soundexFirstName=None, soundexMiddleName=None, soundexLastName=None, middleInitial=None, dob=None):
    conn_enc = sqlite3.connect('encryptedpeople.db')
    cursor_enc = conn_enc.cursor()
    
    query = "SELECT * FROM people WHERE 1=1"
    params = []

    if id is not None:
        query += " AND id = ?"
        params.append(id)
    if firstName is not None:
        query += " AND firstName = ?"
        params.append(encrypt_data(firstName, secret_key))
    if middleName is not None:
        query += " AND middleName = ?"
        params.append(encrypt_data(middleName, secret_key))
    if lastName is not None:
        query += " AND lastName = ?"
        params.append(encrypt_data(lastName, secret_key))
    if soundexFirstName is not None:
        query += " AND soundexFirstName = ?"
        params.append(encrypt_data(soundexFirstName, secret_key))
    if soundexMiddleName is not None:
        query += " AND soundexMiddleName = ?"
        params.append(encrypt_data(soundexMiddleName, secret_key))
    if soundexLastName is not None:
        query += " AND soundexLastName = ?"
        params.append(encrypt_data(soundexLastName, secret_key))
    if middleInitial is not None:
        query += " AND middleInitial = ?"
        params.append(encrypt_data(middleInitial, secret_key))
    if dob is not None:
        query += " AND dob = ?"
        params.append(encrypt_data(dob, secret_key))

    cursor_enc.execute(query, tuple(params))
    rows = cursor_enc.fetchall()

    decrypted_rows = []
    for row in rows:
        decrypted_row = {
            'id': row[0],
            'firstName': decrypt_data(row[1], secret_key),
            'middleName': decrypt_data(row[2], secret_key),
            'lastName': decrypt_data(row[3], secret_key),
            'soundexFirstName': decrypt_data(row[4], secret_key),
            'soundexMiddleName': decrypt_data(row[5], secret_key),
            'soundexLastName': decrypt_data(row[6], secret_key),
            'middleInitial': decrypt_data(row[7], secret_key),
            'dob': decrypt_data(row[8], secret_key),
        }
        decrypted_rows.append(decrypted_row)

    conn_enc.close()
    return decrypted_rows

with open('secret_key.txt', 'rb') as key_file:
    secret_key = key_file.read()
    print(secret_key)

conn_enc = sqlite3.connect('encryptedpeople.db')
cursor_enc = conn_enc.cursor()
query = "SELECT * FROM people WHERE 1=1"
cursor_enc.execute(query)
rows = cursor_enc.fetchall()
for row in rows:
    print(row[1])

print('MhB9vaCTHJoQbFdfVy2KFaV5BADvlkBzrz+Sn0s6FCU=')
print(decrypt_data('MhB9vaCTHJoQbFdfVy2KFaV5BADvlkBzrz+Sn0s6FCU=', secret_key))

results = retrieve_data(secret_key, id="999")#firstName="Janet") #, id="999")

for result in results:
    print(result)



