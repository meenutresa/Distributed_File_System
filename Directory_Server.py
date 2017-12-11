import web
import os
import shelve
import MyApplication
import requests as r
from cryptography.fernet import Fernet
import base64

urls = (
    '/(.*)','directory_server'
)

class directory_server:
    def encryption(self,message):
        #Method to encrypt the message using the session key
        client_session_key = web.config.client_session_key
        client_session_key32 = client_session_key+client_session_key
        client_cipher = Fernet(base64.urlsafe_b64encode(client_session_key32))
        encrypt_mesage = client_cipher.encrypt(message.encode())
        return encrypt_mesage

    def decrypt_sessionkey(self,arg_ticket):
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

    def decrypt_filename(self,File_name):
        #method to decrypt the file name
        print("File_name:",File_name)
        no_digits = int(File_name[0])
        filename_length = int(File_name[1:(no_digits+1)])
        print("filename_length",filename_length)
        encrypt_filename = File_name[(no_digits+1):(filename_length+no_digits+1)]
        print("encrypt_filename:",encrypt_filename)
        ticket = File_name[(filename_length+no_digits+1):]
        print("ticket: ",ticket)
        client_session_key = self.decrypt_sessionkey(ticket)
        web.config.update({"client_session_key":client_session_key})
        client_session_key32 = client_session_key+client_session_key
        client_cipher = Fernet(base64.urlsafe_b64encode(client_session_key32))
        filename = client_cipher.decrypt(encrypt_filename.encode())
        return filename

    def add_encrypt_port(self,port):
        encrypt_port = self.encryption(port)
        return encrypt_port

    #This gets the name of the file and returns the path of the file
    #if just '*' is passed, it displays all the files that the directory server handles
    def GET(self, File_name):
        print("inside directory server")
        File_name = self.decrypt_filename(File_name).decode()
        print("File_name: ",File_name)
        if not File_name:
            message = 'No input given'
            encrypt_message = self.encryption(message)
            encrypt_port = ""
            return str(len(str(len(encrypt_message))))+str(len(encrypt_message))+encrypt_message.decode()+encrypt_port
        else:
            if File_name == '*':
                try:
                    database = shelve.open("directory_names.dat")
                    file_keys = list(database.keys())
                    file_keys.sort()
                    list_of_files_available = ""
                    for i in range(len(file_keys)):
                        list_of_files_available = list_of_files_available + str((i+1)) + "   " + str(file_keys[i] + "\n")
                finally:
                    database.close()
                encrypt_list_of_files_available = self.encryption(list_of_files_available)
                encrypt_port = ""
                return str(len(str(len(encrypt_list_of_files_available))))+str(len(encrypt_list_of_files_available))+encrypt_list_of_files_available.decode()+encrypt_port
            else:
                try:
                    database = shelve.open("directory_names.dat")
                    (filepath_t,port) = database[File_name]
                    filepath = filepath_t+'/'+ File_name
                except KeyError as err:
                    filepath = "file not found"
                    encrypt_filepath = self.encryption(filepath)
                    encrypt_port = ""
                    return str(len(str(len(encrypt_filepath))))+str(len(encrypt_filepath))+encrypt_filepath.decode()+encrypt_port
                finally:
                    database.close()
                encrypt_filepath = self.encryption(filepath)
                encrypt_port = self.add_encrypt_port(port)
                return str(len(str(len(encrypt_filepath))))+str(len(encrypt_filepath))+encrypt_filepath.decode()+encrypt_port.decode()



if __name__ == "__main__":
    app = MyApplication.MyApplication(urls, globals())
    app.run(port=8081)
