import sqlite3
import win32crypt
import os

def chromePasswdRecover(username =""):
	#input Chrome db location
	# i.e. "C:\Users\<username>\AppData\Local\Google\Chrome\User Data\Default"
	location = "C:\\Users\\" + username + "\\AppData\\Local\\Google\\Chrome\\User Data\\Default"

	#check the folder
	if os.path.exists(location):
		dbconn = sqlite3.connect(location + "\\Login Data")
		cursor = dbconn.cursor()
		# Read the DB
		cursor.execute('SELECT action_url, username_value, password_value FROM logins')
		for result in cursor.fetchall():
		  # Decrypt the Password
			password = win32crypt.CryptUnprotectData(result[2], None, None, None, 0)[1]

			#Print site, username and password in readable form
			if password:
				print('Site: ' + result[0])
				print('Username: ' + result[1])
				print('Password: ' + str(password))
				print()
	else:
		print("Unable to find the DB file...")

def main():
	username = input("Give your Windows username:")
	chromePasswdRecover(username)
	input("press enter to exit")




main()