import requests as r
import json as j

url = "http://localhost:8081/"
file_name = input("Enter the file path : ")
url = url + str(file_name)
response = r.get(url)
#file_size = response.json()
print("Response : ", response.text)
