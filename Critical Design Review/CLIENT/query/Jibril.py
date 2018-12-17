from Crypto.Cipher import XOR
import base64
from pprint import pprint as pp


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
    '''
    if input("Do you want to Code or Decode: ") == 'C':
        key = input("Enter the key: ")
        message = input("Enter the message to encrypt: ")
        criptogram = encrypt_message(message, key)
        print("The cryptogram is " + str(criptogram))
    else:
        key = input("Enter the key: ")
        criptogram = input("Enter the message to dencrypt: ")
        print("The decrypted message is " + str(decrypt_message(criptogram, key)))
    '''
    response = [{'uid': 'A6F8A8B7', 'Subject': 'DSBM', 'Mark': '8.5'}, {'uid': 'A6F8A8B7', 'Subject': 'PBE', 'Mark': '9'}]
    key = input("Enter the key: ")
    pp(response)
    data = encrypt_data(response, key)
    pp(response)
    data = decrypt_data(response, key)
    pp(response)