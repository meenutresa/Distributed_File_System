import web
import os
import shelve

urls = (
    '/(.*)','directory_server'
)

class directory_server:
    #This gets the name of the file and returns the path of the file
    #if just '*' is passed, it displays all the files that the directory server handles
    def GET(self, File_name):
        if not File_name:
            File_size = 'No input given'
            return File_size
        else:
            if File_name == '*':
                database = shelve.open("directory_names.dat")
                file_keys = list(database.keys())
                file_keys.sort()
                list_of_files_available = ""
                for i in range(len(file_keys)):
                    list_of_files_available = list_of_files_available + str((i+1)) + "   " + str(file_keys[i] + "\n")
                database.close()
                return list_of_files_available
            else:
                database = shelve.open("directory_names.dat")
                filepath = database[File_name]+'/'+ File_name
                database.close()
                return filepath

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
