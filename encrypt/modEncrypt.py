""" """
from __future__ import print_function
from cryptography.fernet import Fernet
import traceback
import pdb

def encrypt(cipher, message):
    """ encrypt(message) : return en encrypted content of the message in parameter"""
    encrypted = '' 
    try :
        encrypted = cipher.encrypt(message)
    except:
        traceback.print_exc()
    return encrypted

def decrypt(cipher, encoded_text):
    """ decrypt(message) : return the decrypted content of the message in parameter"""
    decrypted= ''
    try:
        decrypted = cipher.decrypt(encoded_text)
    except:
        traceback.print_exc()
    return decrypted

if __name__ == "__main__":
    key = Fernet.generate_key()
    print("Key:", key)
    f = Fernet(key)
    message = "Hello World"
    encrypted = encrypt(f, message)
    print(message, encrypted)
    decrypted = decrypt(f, encrypted)
    print(message, decrypted)
    #------------------
    newKey=''
    newKey = raw_input("Please give us the key again :")
    f1 = Fernet(newKey)
    decrypted = decrypt(f1, encrypted)
    print(message, decrypted)
