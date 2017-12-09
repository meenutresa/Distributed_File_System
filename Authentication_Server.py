import web
import re
import base64
import MyApplication
import shelve

urls = (
    '/','auth_index',
    '/login','auth_login'
)

class auth_index:
    def GET(self):
        if web.ctx.env.get('HTTP_AUTHORIZATION') is not None:
            #print(web.ctx.env.get('HTTP_AUTHORIZATION'))
            return 'HTTP authorization is done'
        else:
            raise web.seeother('/login')

class auth_login:
    def GET(self):
        auth = web.ctx.env.get('HTTP_AUTHORIZATION')
        authreq = False
        #print("reached get")
        if auth is None:
            #print("inside first if")
            authreq = True
        else:
            #print("inside fiest else")
            auth = re.sub('^Basic ','',auth)
            username,password = base64.decodestring(auth.encode()).decode().split(':')
            print(username)
            try:
                database = shelve.open('clientDetails.dat')
                print(username)
                passwd = database[username]
                if passwd == password:
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

if __name__=='__main__':
    app = MyApplication.MyApplication(urls, globals())
    app.run(port=8083)
