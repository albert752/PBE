from Crypto.Cipher import XOR
import base64
from pprint import pprint as pp
import json
import hashlib

def encrypt_message(message, key):
    cipher = XOR.new(key)
    return base64.b64encode(cipher.encrypt(message)).decode('UTF-8')


def decrypt_message(criptogram, key):
    cipher = XOR.new(key)
    return cipher.decrypt(base64.b64decode(criptogram))


def decrypt_data(data, key):
    pp(data)
    for row in data:
        for elem in row:
            print(elem)
            if elem == "mark":
                row[elem] = decrypt_message(row[elem], key)
                row[elem] = row[elem].decode('UTF-8')
                row[elem] = float(row[elem])
            elif elem == "user_name":
                row[elem] = decrypt_message(row[elem], key)
                row[elem] = row[elem].decode('UTF-8')
                
    return data

def encrypt_data(data, key):
    for row in data:
        for elem in row:
            row[elem] = encrypt_message(row[elem], key)
    return data

def decrypt_dict_values(data, key):
    for elem in data:
        print("key" + elem)
        data[elem] = decrypt_message(data[elem], key)
        data[elem] = data[elem].decode('UTF-8')
    pp(data)
    return data

def encrypt_dict_values(data, key):
    for elem in data:
        if elem != "_id":
            if elem == "uid":
                data[elem] = hashlib.sha256(data[elem].encode("UTF-8")).hexdigest()
            elif elem == "mark":
                data[elem] = encrypt_message(str(data[elem]), key)
    return data

if __name__ == '__main__':
    print("Welcome to Jibrils Secure file creator v1.0!")
    path = input("Enter JSONs file path to encrypt: ")
    with open(path, 'r') as f:
        with open("Secure_"+path, 'w') as outfile:  
            for line in f:
                loaded_line = json.loads(line)
                cypher = encrypt_dict_values(loaded_line, loaded_line['uid'])
                pp(cypher)
                json.dump(cypher, outfile)
                outfile.write('\n')







