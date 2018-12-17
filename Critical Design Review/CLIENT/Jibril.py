from Crypto.Cipher import XOR
import base64


def encrypt_message(message, key):
    cipher = XOR.new(key)
    return base64.b64encode(cipher.encrypt(message))


def decrypt_message(criptogram, key):
    cipher = XOR.new(key)
    return cipher.decrypt(base64.b64decode(criptogram))


def get_hash():
    pass


if __name__ == '__main__':
    for i in range(10):
        print(hash("this is a fuckfyujing test motherfuckernn"))
    if input("Do you want to Code or Decode: ") == 'C':
        key = input("Enter the key: ")
        message = input("Enter the message to encrypt: ")
        criptogram = encrypt_message(message, key)
        print("The cryptogram is " + str(criptogram))
    else:
        key = input("Enter the key: ")
        criptogram = input("Enter the message to dencrypt: ")
        print("The decrypted message is " + str(decrypt_message(criptogram, key)))


