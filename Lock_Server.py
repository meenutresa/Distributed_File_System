import web
import os
import shelve
import MyApplication

urls = (
    '/(.*)','lock_server'
    '/unlock/(.*)','lockserver_unlock'
)

class lock_server:
    #This gets the name of the file and check if it is locked or not
    #if * is passed, then it displays all the files that are not locked.
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
                        return 'The file is not locked'
                    else:
                        return 'The file is locked by other user'
                except KeyError as err:
                    error = "file not found"
                    return error
                finally:
                    database.close()

    def POST(self, File_name):
        #post accpets the file name and if it is not locked, it locks the file.
        if not File_name:
            File_size = 'No input given'
            return File_size
        else:
            try:
                database = shelve.open("lock_files.dat")
                lock = database[File_name]
                if "NoLock" in lock:
                    database[File_name] = 'Lock'
                    return str(File_name) + ' is locked now'
                else:
                    return 'The file ' + str(File_name) +' is locked by other user'
            except KeyError as err:
                error = "file not found"
                return error
            finally:
                database.close()

class lockserver_unlock:
    #class is created to handle unlock functionality
    def POST(self, File_name):
        #The method takes in the file name which should be unlocked.
        if not File_name:
            File_size = 'No input given'
            return File_size
        else:
            try:
                database = shelve.open("lock_files.dat")
                lock = database[File_name]
                if "Lock" == lock:
                    database[File_name] = 'NoLock'
                    return str(File_name) + ' is unlocked now'
                else:
                    return 'The file ' + str(File_name) +' is already unlocked'
            except KeyError as err:
                error = "file not found"
                return error
            finally:
                database.close()

if __name__ == "__main__":
    app = MyApplication.MyApplication(urls, globals())
    app.run(port=8082)
