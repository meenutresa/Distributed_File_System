import shelve
from cryptography.fernet import Fernet


###File to generate and store server_encrypt_key

server_encrypt_key = Fernet.generate_key()
try:
    database = shelve.open('server_encrypt_key.dat')
    database['1'] = server_encrypt_key
finally:
    database.close()
