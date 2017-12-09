import requests as r
import json as j
from requests.auth import HTTPBasicAuth


url = "http://localhost:8083/login"
"""
file_name = input("Enter the file path : ")
url = url + str(file_name)
response = r.post(url)
"""

usename = input("Enter the username : ")
password = input("Enter the password : ")
response = r.get(url, auth=HTTPBasicAuth(usename, password))
#file_size = response.json()
print("Response : ", response.text)
