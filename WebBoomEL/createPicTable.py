import sqlite3

try:
	#creates or opens a file called pics with a SQLite3 DB
	db = sqlite3.connect('/home/pi/WebBoomEL/pics.db')
	cursor = db.cursor()
	#Check if table users does not exist and create it
	cursor.execute('''CREATE TABLE IF NOT EXISTS
	 pics(picPath varchar(255), datetime varchar(255))''')
	db.commit()
except Exception as e:
	#Roll back any change if something goes wrong
	db.rollback()
	raise e
finally:
	#close database connection
	db.close()
