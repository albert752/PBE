from Crypto.Cipher import XOR
import base64
from pprint import pprint as pp
import json

def encrypt_message(message, key):
    cipher = XOR.new(key)
    return base64.b64encode(cipher.encrypt(message))


def decrypt_message(criptogram, key):
    cipher = XOR.new(key)
    return cipher.decrypt(base64.b64decode(criptogram))


def decrypt_data(data, key):
    for row in data:
        for elem in row:
            row[elem] = decrypt_message(row[elem], key)
            row[elem] = row[elem].decode('UTF-8')
    return data


def encrypt_data(data, key):
    for row in data:
        for elem in row:
            row[elem] = encrypt_message(row[elem], key)
    return data


if __name__ == '__main__':
    path = input("Enter JSONs file path to encrypt: ")
	with open('filename.txt', 'r') as f:
    	array = json.load(f)
pp(array)
