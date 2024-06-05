from flask import Flask, render_template, request, redirect,url_for, jsonify
import sqlite3
import json
import base64

import numpy as np
from numpy.linalg import inv
# key = get_random_bytes(16) 
app = Flask(__name__)
key = np.array([[6, 24, 1], [13, 16, 10], [20, 17, 15]])  # You can choose the desired key matrix

def encrypt_password(password, key):
    n = len(key)
    encrypted_password = ""
    for i in range(0, len(password), n):
        block = password[i:i + n]
        if len(block) < n:
            block += 'X' * (n - len(block))
        block_vector = np.array([ord(char.upper()) - ord('A') for char in block])
        encrypted_block = np.dot(key, block_vector) % 26
        encrypted_block_chars = [chr(val + ord('A')) for val in encrypted_block]
        encrypted_password += ''.join(encrypted_block_chars)
    return encrypted_password

def decrypt_password(encrypted_password, key):
    n = len(key)
    decrypted_password = ""
    inverse_key = inv(key)
    for i in range(0, len(encrypted_password), n):
        block = encrypted_password[i:i + n]
        block_vector = np.array([ord(char.upper()) - ord('A') for char in block])
        decrypted_block = np.dot(inverse_key, block_vector) % 26
        decrypted_block_chars = [chr(val % 26 + ord('A')) for val in decrypted_block]
        decrypted_password += ''.join(decrypted_block_chars)
    return decrypted_password
def create_table():
    conn = sqlite3.connect('user_data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                (id INTEGER PRIMARY KEY,
                 name TEXT,
                 password BLOB,
                 age INTEGER,
                 gender TEXT,
                 address TEXT,
                 contact INTEGER,
                 photo BLOB,
                 dec_pass TEXT)''')
    conn.commit()
    conn.close()
@app.route('/')
def index():
    error = request.args.get('error')  # Get the error parameter from the query string
    return render_template('login.html', show_signup_link=True, error=error)

@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    password = request.form['password']
    key = np.array([[6, 24, 1], [13, 16, 10], [20, 17, 15]])
    encrypted_password = encrypt_password(password, key)
    # print(encrypted_password)
    print(name)
    # Assuming you have the encrypted password and the key matrix
    decrypted_password = decrypt_password(encrypted_password, key)
    # print(decrypted_password)
    age = request.form['age']

    gender = request.form['gender']
    address = request.form['address']
    contact = request.form['contact']

    photo = request.files['photo'].read()

    conn = sqlite3.connect('user_data.db')
    c = conn.cursor()
    c.execute('INSERT INTO users (name, age, password, gender, address, contact, photo, dec_pass) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (name, age, encrypted_password, gender, address, contact, photo, decrypted_password))
    conn.commit()
    conn.close()

    return redirect(url_for('get_user', name=name))
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        error_message = None  # No error message initially for GET requests
        show_signup_link = True  # Show signup link on the login page
        return render_template('login.html', show_signup_link=show_signup_link, error=error_message)

    elif request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        print(name)
        conn = sqlite3.connect('user_data.db')
        c = conn.cursor()

        # Execute a SELECT query to retrieve the encrypted password for the given username
        c.execute('SELECT password FROM users WHERE name = ?', (name,))
        result = c.fetchone()  # Fetch the first row from the query result

        if result is not None:
            encrypted_password = result[0]
            print(encrypted_password)
            print(name)
            # Decrypt the stored encrypted password
            decrypted_password = decrypt_password(encrypted_password, key)  # Use the appropriate key

            # Compare the entered password with the decrypted password
            if password == decrypted_password:
                # Redirect to the user's profile page if login is successful
                return redirect(url_for('get_user', name=name))

        # Display an error message for wrong credentials
        error_message = 'Invalid login credentials. Please try again.'
        show_signup_link = True  # Show signup link on the login page

        # Render the login page and pass the error message and signup link parameter
        return render_template('login.html', show_signup_link=show_signup_link, error=error_message)

@app.route('/users/<name>', methods=['GET', 'POST'])
def get_user(name):
    if request.method == 'POST':
        return redirect(url_for('login'))  # Redirect to the login page

    conn = sqlite3.connect('user_data.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE name=?", (name,))
    user_data = c.fetchone()
    conn.close()

    if user_data:
        user_dict = {
            'id': user_data[0],
            'name': user_data[1],
            'age': user_data[3],
            'gender': user_data[4],
            'contact': user_data[6],
            'address': user_data[5],
            'photo': base64.b64encode(user_data[7]).decode('utf-8')
        }
        return render_template('user.html', user=user_dict, kk=name)
    else:
        return render_template('signup.html', error='User not found')
           
if __name__ == '__main__':
    create_table()
    app.run(port=3000, debug=True)
    
