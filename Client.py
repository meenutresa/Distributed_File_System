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

usename = input("Enter the username : ")
password = input("Enter the password : ")
response = r.get(url, auth=HTTPBasicAuth(usename, password))
if response.text == 'Username or Password is wrong':
    print("Response :", response.text)
else:
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
