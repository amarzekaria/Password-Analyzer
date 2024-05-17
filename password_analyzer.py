''' The point of this project is to store the key to see the password into a file using base64-encoded bytes. once its encrypted there would be a decryption key stored, the user would have to enter the decryption key to see the stored password'''
#Made in September of 2023
#Published in May 2024 due to school setback and continuous learning

import os
import random
import string
from cryptography.fernet import Fernet


#Func for generating a valid password and characters
def valid_password(length=14):
    characters = string.ascii_letters + string.digits + string.punctuation 
    
    password = '' .join(random.choice(characters) for _ in range(length))
    return password

#Func for generating and saving encrypt. key as a file
def generate_key():
    key = Fernet.generate_key()
    with open('secret.key', 'wb') as key_file:
        key_file.write(key)
    return key

#Func for loading the encryp. when open so it is readable to user
def load_key():
    return open('secret.key', 'rb').read()

#Func for encrypting a message
def encrypt_message(message, key):
    f = Fernet(key)
    encrypted_message = f.encrypt(message.encode())
    return encrypted_message

#Func for decrypting a message
def decrypt_message(encrypted_message, key):
    f = Fernet(key)
    decrypted_message = f.decrypt(encrypted_message).decode()
    return decrypted_message

#Saving the encrypting password
def save_encrypted_password(encrypted_password, filename):
    with open(filename, 'wb') as file:
        file.write(encrypted_password)


'''This is where the "magic" happens.... the user will question on whether they would like to generate a new password to encrypt or decrept and existing passowrd
Using simple conditionals loops and input validation, calling the function the user has a choice to choose what to do but make no errors'''
def main():
    while True:
        choice = input("Do you want to (g)enerate a new password or (r)etrieve an existing password or (q)uit? ")

        if choice == 'g':
            password_length = int(input('Enter the desired length of your password:'))
            if password_length < 2:
                print('Your password must be at least 2 characters long.')
            else:
                password = valid_password(password_length)
                print('Your valid password:', password)

                # Generate and save encryption key
                key = generate_key()
                key_path = os.path.abspath("encryption.key")
                print(f'Encryption key has been generated and saved at {key_path}.')

                # Encrypt the password
                encrypted_password = encrypt_message(password, key)

                # Ask for a filename to save the encrypted password
                filename = input("Enter the filename to save the encrypted password (e.g., 'password1.txt'): ")
                save_encrypted_password(encrypted_password, filename)
                password_path = os.path.abspath(filename)
                print(f'Your encrypted password has been saved at {password_path}.')

        elif choice == 'r':
            try:
                # Ask for the filename of the encrypted password
                filename = input("Enter the filename of the encrypted password (example: 'password1.txt'): ")
                
                # Load the encrypted password
                with open(filename, "rb") as file:
                    encrypted_password = file.read()

                # Ask the user for the decryption key
                decryption_key = input('Enter the decryption key: ').encode()

                try:
                    # Decrypt the password
                    decrypted_password = decrypt_message(encrypted_password, decryption_key)
                    print('Your decrypted password:', decrypted_password)
                except Exception as e:
                    print('Invalid decryption key or corrupted data.', str(e))
            except FileNotFoundError:
                print(f'No encrypted password found with the filename {filename}. Please check the filename and try again.')

        elif choice == 'q':
            print('Exiting...')
            break

        else:
            print("Invalid choice. Please enter 'g' to generate a new password, 'r' to retrieve an existing password, or 'q' to quit.")

if __name__ == '__main__':
    main()