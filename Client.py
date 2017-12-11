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

    #Now we have to check the operation is read or write.
    if operation == "read":
        encrypt_fs_filepath = encryption(filepath)
        print("encrypt_fs_filepath:",encrypt_fs_filepath)
        file_server_url = "http://localhost:8080/"+str(len(str(len(encrypt_fs_filepath))))+str(len(encrypt_fs_filepath))+encrypt_fs_filepath.decode()+ticket.decode()
        file_server_response = r.get(file_server_url)
        encrypt_filecontent = file_server_response.text
        filecontent = decryption(encrypt_filecontent).decode()
        print("filecontent:",filecontent)
    else:
        encrypt_ls_filename = encryption(filename)
        print("encrypt_filename:",encrypt_ls_filename)
        lock_server_url = "http://localhost:8082/"+str(len(str(len(encrypt_ls_filename))))+str(len(encrypt_ls_filename))+encrypt_ls_filename.decode()+ticket.decode()
        lock_server_response = r.get(lock_server_url)
        encrypt_lock = lock_server_response.text
        islock = decryption(encrypt_lock).decode()
        print("islock:",islock)

        #unlock
        encrypt_ls_filename = encryption(filename)
        print("encrypt_filename:",encrypt_ls_filename)
        lock_server_unlock_url = "http://localhost:8082/unlock/"+str(len(str(len(encrypt_ls_filename))))+str(len(encrypt_ls_filename))+encrypt_ls_filename.decode()+ticket.decode()
        lock_server_response = r.post(lock_server_unlock_url)
        encrypt_lock = lock_server_response.text
        islock = decryption(encrypt_lock).decode()
        print("islock:",islock)



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
