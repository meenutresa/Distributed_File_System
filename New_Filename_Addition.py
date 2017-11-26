import shelve

file_name = input("Enter the file name : ")
file_path = input("Enter the file path : ")

database = shelve.open('directory_names.dat')
#directory_path = "C:/MeenuNeenu/Study/ScalableComputing/python"
database[file_name] = file_path
database.close()

database = shelve.open('lock_files.dat')
#directory_path = "C:/MeenuNeenu/Study/ScalableComputing/python"
database[file_name] = "NoLock"
database.close()
