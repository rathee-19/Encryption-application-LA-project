# Secure User Data Storage and Authentication Using  AES Encryption and HIll Cipher in Flask

This project demonstrates how to securely store and manage user data using Flask, SQLite, and AES encryption. The application supports user signup, login, and profile viewing functionalities, ensuring that sensitive information, such as passwords, is encrypted before storage.

## Features

- **User Signup**: Users can sign up by providing their name, password, age, gender, address, contact details, and photo.
- **User Login**: Users can log in with their credentials, and the application will authenticate them by decrypting and verifying their password.
- **Profile Viewing**: After logging in, users can view their profile information.

## Technologies Used

- **Flask**: A lightweight WSGI web application framework in Python.
- **SQLite**: A C-language library that provides a relational database management system.
- **AES Encryption**: Used to securely encrypt and decrypt user passwords.
- **Hill Cipher**: An alternative encryption method demonstrated in the code.

## Installation

1. **Clone the repository**:
   ```sh
   git clone https://github.com/your-repo/flask-aes-encryption.git
   cd flask-aes-encryption
   ```

2. **Install the required Python packages**:
 ```sh
   pip install flask pycryptodome numpy
```
## Run the application
Run the Flask application using the following command:
```sh
python app.py
```
**Open your web browser and navigate to http://localhost:3000**.

## Project Structure

- `app.py`: Main application file containing routes, encryption functions, and database interaction logic.
- `templates/`: Directory containing HTML templates for signup, login, and user profile pages.
- `static/`: Directory for static files (CSS, JavaScript, images).

## Encryption Details
### AES Encryption
AES (Advanced Encryption Standard) is used to encrypt and decrypt user passwords before storing them in the database. This ensures that even if the database is compromised, the actual passwords remain secure.

#### Functions:

- **encrypt_password(password, key)**:
  Encrypts a password using AES encryption with a specified key.

```python

def encrypt_password(password, key):
    cipher = AES.new(key, AES.MODE_ECB)
    encrypted_password = cipher.encrypt(pad(password.encode('utf-8'), AES.block_size))
    return encrypted_password
decrypt_password(encrypted_password, key):
Decrypts an encrypted password using AES decryption with the specified key.
```
```python

def decrypt_password(encrypted_password, key):
    cipher = AES.new(key, AES.MODE_ECB)
    decrypted_password = unpad(cipher.decrypt(encrypted_password), AES.block_size)
    return decrypted_password.decode('utf-8')
```
## Hill Cipher
The Hill cipher is demonstrated as an alternative encryption method, primarily for educational purposes. It encrypts passwords using matrix multiplication over a specified key matrix.

### Functions:
encrypt_password1(password, key):
Encrypts a password using the Hill cipher with the specified key matrix.

```python
def encrypt_password1(password, key):
    n = len(key)
    encrypted_password = ""
    for i in range(0, len(password), n):
        block = password[i:i + n]
        if len(block) < n:
            block += 'X' * (n - len(block))
        block_vector = np.array([ord(char) - ord('A') for char in block])
        encrypted_block = np.dot(key, block_vector) % 26
        encrypted_block_chars = [chr(val + ord('A')) for val in encrypted_block]
        encrypted_password += ''.join(encrypted_block_chars)
    return encrypted_password
decrypt_password1(encrypted_password, key):
Decrypts an encrypted password using the Hill cipher with the specified key matrix.
```

```python
def decrypt_password1(encrypted_password, key):
    n = len(key)
    decrypted_password = ""
    inverse_key = inv(key)
    for i in range(0, len(encrypted_password), n):
        block = encrypted_password[i:i + n]
        block_vector = np.array([ord(char) - ord('A') for char in block])
        decrypted_block = np.dot(inverse_key, block_vector) % 26
        decrypted_block = np.round(decrypted_block).astype(int)
        decrypted_block_chars = [chr(val + ord('A')) for val in decrypted_block]
        decrypted_password += ''.join(decrypted_block_chars)
    return decrypted_password
```
## Database Schema
The user data is stored in an SQLite database with the following schema:

```python
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT,
    password BLOB,
    age INTEGER,
    gender TEXT,
    address TEXT,
    contact TEXT,
    photo BLOB,
    dec_pass TEXT,
    password_hill TEXT
)

```

## Usage
#### Signup
- Navigate to the signup page: http://localhost:3000/signup
- Fill in the required fields and submit the form.
#### Login
- Navigate to the login page: http://localhost:3000/login
- Enter your username and password to log in.
#### Profile
- After logging in, you will be redirected to your profile page where you can view your details.
## Notes
AES encryption is used for secure storage of passwords.
The Hill cipher encryption is included as an additional demonstration and is not recommended for real-world use due to its vulnerability to cryptographic attacks.
This project is intended for educational purposes to demonstrate secure password storage techniques.
