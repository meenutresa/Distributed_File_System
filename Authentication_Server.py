import web
import re
import base64
import MyApplication
import shelve
import os
from cryptography.fernet import Fernet

# Authetication Server

urls = (
    '/','auth_index',
    '/login','auth_login',
    '/getKey','auth_getKey'
)

def Encript_Ticket(arg_ticket):
    ##The function is ued to encrypt the ticket which contains session_key with Serverencryption key
    #Server encryption Key is taken from the file
    try:
        server_encrypt_key_file = shelve.open('server_encrypt_key.dat')
        server_encrypt_key = server_encrypt_key_file['1']
        server_cipher = Fernet(server_encrypt_key)
        print("server_encrypt_key: ",server_encrypt_key)
        #ticket_encoded = arg_ticket.encode()
        ticket_encrypted = server_cipher.encrypt(arg_ticket)
    finally:
        server_encrypt_key_file.close()
    return ticket_encrypted


class auth_index:
    def GET(self):
        if web.ctx.env.get('HTTP_AUTHORIZATION') is not None:
            #print(web.ctx.env.get('HTTP_AUTHORIZATION'))
            return web.config.return_token
            #return 'HTTP authorization is done'
        else:
            raise web.seeother('/login')

class auth_login:
    def GET(self):
        # Authenticate username and passwordand generate token
        auth = web.ctx.env.get('HTTP_AUTHORIZATION')
        authreq = False
        #print("reached get")
        if auth is None:
            #print("inside first if")
            authreq = True
        else:
            print("inside fiest else")
            auth = re.sub('^Basic ','',auth)
            username,password = base64.decodestring(auth.encode()).decode().split(':')
            print(username)
            try:
                database = shelve.open('clientDetails.dat')
                print(username)
                passwd = database[username]
                if passwd == password:
                    session_key = os.urandom(16)
                    print("session_key",session_key)
                    ticket = session_key
                    encripted_ticket = Encript_Ticket(ticket)
                    print("encripted_ticket",encripted_ticket)
                    token = session_key + encripted_ticket
                    passwd_32bits = password
                    passwd_32bits = passwd_32bits.zfill(32)
                    passwd_32bits = passwd_32bits[:32]
                    server_cipher = Fernet(base64.urlsafe_b64encode(passwd_32bits.encode()))
                    #token_encoded = token.encode()
                    token_encrypted = server_cipher.encrypt(token)
                    web.config.update({"return_token":token_encrypted})
                    raise web.seeother('/')
                else:
                    authreq = True
                    return "Username or Password is wrong"
            except KeyError as err:
                #authreq = True
                return "Username or Password is wrong"
            finally:
                database.close()

        if authreq:
            web.header('WWW-Authenticate','Basic realm="Client Authentication"')
            web.ctx.status = '401 Unauthorized'
            return

class auth_getKey:
    def GET(self):
        #This is used by the other servers which are part of distributed system to get the server encrypt key. This is shared between the Authentication server and other servers.
        try:
            print("inside inside auth_getkey")
            server_encrypt_key_file = shelve.open('server_encrypt_key.dat')
            server_encrypt_key = server_encrypt_key_file['1']
        finally:
            server_encrypt_key_file.close()
        return server_encrypt_key

if __name__=='__main__':
    app = MyApplication.MyApplication(urls, globals())
    app.run(port=8083)
