import requests as r
import json as j
from requests.auth import HTTPBasicAuth
from cryptography.fernet import Fernet
import base64


url = "http://localhost:8083/login"
"""
file_name = input("Enter the file path : ")
url = url + str(file_name)
response = r.post(url)
"""

def encryption(message):
    #Method to encrypt the message using the session key
    encypt_session_key = session_key+session_key
    encrypt_cipher = Fernet(base64.urlsafe_b64encode(encypt_session_key))
    encrypt_message = encrypt_cipher.encrypt(message.encode())
    return encrypt_message

def decryption(encrypt_message):
    #Method to decrypt the message that is received from other servers using session key
    decrypt_session_key = session_key+session_key
    decrypt_cipher = Fernet(base64.urlsafe_b64encode(decrypt_session_key))
    message = decrypt_cipher.decrypt(encrypt_message.encode())
    return message


def client_proxy(filename,operation):
    #Client proxy handles teh flow to each of the servers for the operations that the client chooses
    #Call to the directory server.This is irrespective of the operation if it is write or wrong
    encrypt_filename = encryption(filename)
    print("encrypt_filename:",encrypt_filename)
    directory_server_url = "http://localhost:8081/"+str(len(str(len(encrypt_filename))))+str(len(encrypt_filename))+encrypt_filename.decode()+ticket.decode()
    print("directory_server_url:",directory_server_url)
    directory_server_response = r.get(directory_server_url)
    encrypt_filepath = directory_server_response.text
    filepath = decryption(encrypt_filepath).decode()
    print("filepath: ",filepath)
    lock_server_url = "http://localhost:8081/"+filename



usename = input("Enter the username : ")
password = input("Enter the password : ")
print("url :", url)
response = r.get(url, auth=HTTPBasicAuth(usename, password))
if response.text == 'Username or Password is wrong':
    print("Response :", response.text)
else:
    print("Response :", response.text)
    passwd_32bits = password
    passwd_32bits = passwd_32bits.zfill(32)
    passwd_32bits = passwd_32bits[:32]
    server_cipher = Fernet(base64.urlsafe_b64encode(passwd_32bits.encode()))
    token_decrypted = server_cipher.decrypt(response.text.encode())
    print("token_decrypted:",token_decrypted)
    #token_decoded = token_decrypted.decode()
    #file_size = response.json()
    session_key = token_decrypted[:16]
    ticket = token_decrypted[16:]
    print("session_key : ", session_key)
    print("ticket : ", ticket)

    filename = input("Enter the filename : ")
    operation = input("Enter the operation : ")
    client_proxy(filename,operation)
