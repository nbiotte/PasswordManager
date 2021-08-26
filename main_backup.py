import json
import os
import base64
import uuid
from tkinter import *

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from getpass import getpass


# This is a sample Python script.

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

def encrypt(key, data):
    f = Fernet(key)
    token = f.encrypt(data)
    return token


def decrypt(key, data):
    f = Fernet(key)
    decrypt = f.decrypt(data)
    return decrypt


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print(encrypt('test'))

    # password = str.encode(getpass('Entrer le mot de passe principal: '))
    # # salt = os.urandom(16)
    # salt = b'Dul3pMczSLGZXDBjQ9EN3Q=='
    # kdf = PBKDF2HMAC(
    #     algorithm=hashes.SHA256(),
    #     length=32,
    #     salt=salt,
    #     iterations=100000,
    # )
    # key = base64.urlsafe_b64encode(kdf.derive(password))
    # print(key)
    # encryptedKey = encrypt(key, key)
    #
    # print('')

    # encryptedData = encrypt(key, b'toto')
    # print(encryptedData)
    # decryptedData = decrypt(key, encryptedData)
    # print(decryptedData)


    # with open('mdp.json') as file:
    #     data_dict = json.load(file)
    #     print(data_dict)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
