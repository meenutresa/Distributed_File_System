import web
import os
import shelve
import MyApplication

urls = (
    '/(.*)','lock_server'
)

class lock_server:
    #This gets the name of the file and check if it is locked or not
    #if not locked, it locks the file
    def GET(self, File_name):
        if not File_name:
            File_size = 'No input given'
            return File_size
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
                return list_of_files_available
            else:
                try:
                    database = shelve.open("lock_files.dat")
                    lock = database[File_name]
                    if "NoLock" in lock:
                        database[File_name] = 'Lock'
                        return 'Locked the file given'
                    else:
                        return 'The file is already locked by other user'
                except KeyError as err:
                    error = "file not found"
                    return error
                finally:
                    database.close()

if __name__ == "__main__":
    app = MyApplication.MyApplication(urls, globals())
    app.run(port=8082)
