import web
import os
import shelve
import MyApplication
import requests as r
from cryptography.fernet import Fernet
import base64

urls = (
    '/unlock/(.*)','lockserver_unlock',
    '/(.*)','lock_server'
)

def encryption(message):
    #Method to encrypt the message using the session key
    client_session_key = web.config.client_session_key
    client_session_key32 = client_session_key+client_session_key
    client_cipher = Fernet(base64.urlsafe_b64encode(client_session_key32))
    encrypt_mesage = client_cipher.encrypt(message.encode())
    return encrypt_mesage

def decrypt_sessionkey(arg_ticket):
    #Method to get the session key decrypted in the ticket using the server encryption key
    auth_url = "http://localhost:8083/getKey"
    response = r.get(auth_url)
    server_encrypt_key_file = response.text
    server_encrypt_key = server_encrypt_key_file
    print("server_encrypt_key:",server_encrypt_key.encode())
    server_cipher = Fernet(server_encrypt_key.encode())
    #ticket_encoded = arg_ticket.encode()
    ticket_decrypted = server_cipher.decrypt(arg_ticket.encode())
    print("Session_key:",ticket_decrypted)
    return ticket_decrypted

def decrypt_filename(File_name):
    #method to decrypt the file name
    print("File_name:",File_name)
    no_digits = int(File_name[0])
    filename_length = int(File_name[1:(no_digits+1)])
    print("filename_length",filename_length)
    encrypt_filename = File_name[(no_digits+1):(filename_length+no_digits+1)]
    print("encrypt_filename:",encrypt_filename)
    ticket = File_name[(filename_length+no_digits+1):]
    print("ticket: ",ticket)
    client_session_key = decrypt_sessionkey(ticket)
    web.config.update({"client_session_key":client_session_key})
    client_session_key32 = client_session_key+client_session_key
    client_cipher = Fernet(base64.urlsafe_b64encode(client_session_key32))
    filename = client_cipher.decrypt(encrypt_filename.encode())
    return filename

class lock_server:
    #This gets the name of the file and check if it is locked or not
    #if * is passed, then it displays all the files that are not locked.
    def GET(self, File_name):
        File_name = decrypt_filename(File_name).decode()
        print("File_name: ",File_name)
        if not File_name:
            message = 'No input given'
            encrypt_message = encryption(message)
            return encrypt_message
        else:
            if File_name == '*':
                try:
                    database = shelve.open("lock_files.dat")
                    file_keys = list()
                    for name in database.keys():
                        if database[name] == 'NoLock':
                            file_keys.append(name)
                    file_keys.sort()
                    list_of_files_available = ""
                    for i in range(len(file_keys)):
                        list_of_files_available = list_of_files_available + str((i+1)) + "   " + str(file_keys[i] + "\n")
                finally:
                    database.close()
                encrypt_list_of_files_available = encryption(list_of_files_available)
                return encrypt_list_of_files_available
            else:
                try:
                    database = shelve.open("lock_files.dat")
                    lock = database[File_name]
                    if "NoLock" in lock:
                        message = 'The file is not locked'
                        encrypt_message = encryption(message)
                        return encrypt_message
                    else:
                        message = 'The file is locked by other user'
                        encrypt_message = encryption(message)
                        return encrypt_message
                except KeyError as err:
                    error = "file not found"
                    encrypt_message = encryption(error)
                    return encrypt_message
                finally:
                    database.close()

    def POST(self, File_name):
        #post accpets the file name and if it is not locked, it locks the file.
        File_name = decrypt_filename(File_name).decode()
        print("File_name: ",File_name)
        if not File_name:
            message = 'No input given'
            encrypt_message = encryption(message)
            return encrypt_message
        else:
            try:
                database = shelve.open("lock_files.dat")
                lock = database[File_name]
                if "NoLock" in lock:
                    database[File_name] = 'Lock'
                    message = str(File_name) + ' is locked now'
                    encrypt_message = encryption(message)
                    return encrypt_message
                else:
                    message = 'The file ' + str(File_name) +' is locked by other user'
                    encrypt_message = encryption(message)
                    return encrypt_message
            except KeyError as err:
                error = "file not found"
                encrypt_message = encryption(error)
                return encrypt_message
            finally:
                database.close()

class lockserver_unlock:
    #class is created to handle unlock functionality
    def POST(self, File_name):
        #The method takes in the file name which should be unlocked.
        print("inside unlock")
        File_name = decrypt_filename(File_name).decode()
        print("File_name: ",File_name)
        if not File_name:
            message = 'No input given'
            encrypt_message = encryption(message)
            return encrypt_message
        else:
            try:
                database = shelve.open("lock_files.dat")
                lock = database[File_name]
                if "Lock" == lock:
                    database[File_name] = 'NoLock'
                    message = str(File_name) + ' is unlocked now'
                    encrypt_message = encryption(message)
                    return encrypt_message
                else:
                    message = 'The file ' + str(File_name) +' is already unlocked'
                    encrypt_message = encryption(message)
                    return encrypt_message
            except KeyError as err:
                error = "file not found"
                encrypt_message = encryption(error)
                return encrypt_message
            finally:
                database.close()

if __name__ == "__main__":
    app = MyApplication.MyApplication(urls, globals())
    app.run(port=8082)
