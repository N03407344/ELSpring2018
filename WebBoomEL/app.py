#!usr/bin/env python3



import os
import time
import datetime
import picamera
import sqlite3
import atexit
from flask import Flask, render_template, request, Response, url_for


app = Flask(__name__)
global panServoAngle
global tiltServoAngle
panServoAngle = 90 #starting position for pan servo
tiltServoAngle = 90 #starting position for tilt servo
panPin = 17 #pin number for connecting pan servo to gpio board
tiltPin = 4 #pin number for connecting tilt servo
#renders the main template for viewing
@app.route("/",methods=['GET','POST'])
def main():
    return render_template('index.html')

#move the servos
@app.route("/<servo>/<angle>")
def move(servo, angle):
        global panServoAngle
        global tiltServoAngle
        if servo == 'pan':
            if angle == '+':
                     panServoAngle = panServoAngle + 10
                     os.system("python3 angleServo.py " + str(panPin))
            else:
                panServoAngle = panServoAngle - 10
                os.system("python3 angleServo2.py " + str(panPin))
        if servo == 'tilt':
              if angle == '+':
                     tiltServoAngle = tiltServoAngle + 10
                     os.system("python3 angleServo.py " + str(tiltPin))
              else:
                  tiltServoAngle = tiltServoAngle - 10
                  os.system("python3 angleServo2.py " + str(tiltPin))
        templateData = {
                    'panServoAngle' : panServoAngle,
                    'tiltServoAngle' : tiltServoAngle
        }
        return render_template('index.html',**templateData)
#connects to picture database and takes the pictures
@app.route("/takePic", methods=['GET','POST'])
def takePic():
     #connect to picture database
     try:
         db = sqlite3.connect('/home/pi/WebBoomEL/pics.db')
         cursor = db.cursor()
         currentTime=time.strftime('%x %X %Z')
	#take new photo
         camera = picamera.PiCamera() #uses the pi camera
         timeTaken = time.strftime("%Y%m%d-%H%M%S") #stores time of picture taken
         pic = camera.capture('static/'+timeTaken+'.jpg') #takes the picture
         camera.close() #close the camera connection
         picPath = timeTaken + ".jpg"
	#store new photo in database
         cursor.execute('''INSERT INTO pics(picPath, datetime)
		   VALUES(?,?)''', (picPath,curretnTime))
         db.commit()
     except Exception as e:
             db.rollback()
             raise e
     finally:
             db.close() #close database connection
     return render_template('index.html')

#method to display all pictures take so far
@app.route("/showPics")
def showPics():
	#if request.method == 'POST':
	db = sqlite3.connect('/home/pi/WebBoomEL/pics.db')
	db.row_factory=sqlite3.Row #creates rows for pictures taken
	cursor = db.cursor()
	cursor.execute('''SELECT * FROM pics''')
	rows = cursor.fetchall() #fetches all rows of the query result 
	db.close()
	return render_template('showPics.html',rows = rows)

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=8080, debug=True)
