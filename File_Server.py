import web
import os
import MyApplication
import requests as r
from cryptography.fernet import Fernet
import base64

urls = (
    '/(.*)','file_server'
)

class file_server:
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


    #This gets the file path and returns the file content
    def GET(self, File_name):
        File_name = self.decrypt_filename(File_name).decode()
        print("File_name: ",File_name)
        if not File_name:
            message = 'No file name given'
            encrypt_message = self.encryption(message)
            return encrypt_message
        else:
            if os.path.isfile(File_name) :
                with open(File_name) as f:
                    encrypt_message = self.encryption(f.read())
                    return encrypt_message
            else:
                message = "file doesnot exist"
                encrypt_message = self.encryption(message)
                return encrypt_message
            #File_size = os.path.getsize(File_name)
            #return File_size

    def POST(self, File_name):
        File_name = self.decrypt_filename(File_name).decode()
        print("File_name: ",File_name)
        if not File_name:
            message = 'No file name given'
            encrypt_message = self.encryption(message)
            return encrypt_message
        else:
            if os.path.isfile(File_name) :
                with open(File_name,'w') as f:
                    print("web.data():",web.data())
                    fcontent = self.decrypt_filename(web.data().decode()).decode()
                    print("fcontent: ",fcontent)
                    f.write(fcontent)
                    message = "Written successfully!"
                    encrypt_message = self.encryption(message)
                    return encrypt_message
            else:
                message = "file doesnot exist"
                encrypt_message = self.encryption(message)
                return encrypt_message
            #File_size = os.path.getsize(File_name)
            #return File_size


if __name__ == "__main__":
    app = MyApplication.MyApplication(urls, globals())
    app.run(port=8080)
