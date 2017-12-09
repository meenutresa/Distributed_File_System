import shelve


###File to store the user details into persistence dictionary
user_name = input("Enter the user name : ")
user_pass = input("Enter the password : ")

database = shelve.open('clientDetails.dat')
database[user_name] = user_pass
database.close()
