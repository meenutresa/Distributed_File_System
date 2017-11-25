import web
import os
import MyApplication

urls = (
    '/(.*)','file_server'
)

class file_server:
    #This gets the file path and returns the file size
    def GET(self, File_name):
        if not File_name:
            File_size = 'No file name given'
            return File_size
        else:
            if os.path.isfile(File_name) :
                with open(File_name) as f:
                    return f.read()
            else:
                return "file doesnot exist"
            #File_size = os.path.getsize(File_name)
            #return File_size


if __name__ == "__main__":
    app = MyApplication.MyApplication(urls, globals())
    app.run(port=8080)
