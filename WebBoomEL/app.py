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
panServoAngle = 90
tiltServoAngle = 90
panPin = 11
tiltPin = 7
@app.route("/",methods=['GET','POST'])
def main():
    return render_template('index.html')

@app.route("/")
def index():
    templateData = {
               'panServoAngle'  : panServoAngle,
               'tiltServoAngle' : tiltServoAngle
     }
    return render_template('index.html', **templateData)



@app.route("/<servo>/<angle>",methods=['GET'])
def move(servo, angle):
        global panServoAngle
        global tiltServoAngle
        if servo == 'pan':
            if angle == '+':
                   panServoAngle = panServoAngle + 10
            else:
                panServoAngle = panServoAngle - 10
            os.system("python3 angleServo.py " + str(panPin) + " " + str(panServoAngle))
        if servo == 'tilt':
               if angle == '+':
                        tiltServoAngle = tiltServoAngle + 10
               else:
                    tiltServoAngle = tiltServoAngle - 10
               os.system("python3 angleServo.py " + str(tiltPin) + " " + str(tiltServoAngle))
        templateData = {
               'panServoAngle'   : panServoAngle,
               'tiltServoAngle'  : tiltServoAngle
        }
        return render_template('index.html', **templateData)
@app.route("/takePic", methods=['GET','POST'])
def takePic():
     #connect to picture database
     try:
         db = sqlite3.connect('/home/pi/WebBoomEL/pics.db')
         cursor = db.cursor()
         currentTime=time.strftime('%x %X %Z')
	#take new photo
         camera = picamera.PiCamera()
         timeTaken = time.strftime("%Y%m%d-%H%M%S")
         pic = camera.capture('static/'+timeTaken+'.jpg')
         camera.close()
         picPath = timeTaken + ".jpg"
	#store new photo in database
         cursor.execute('''INSERT INTO pics(picPath, datetime)
		   VALUES(?,?)''', (picPath,curretnTime))
         db.commit()
     except Exception as e:
             db.rollback()
             raise e
     finally:
             db.close()
     return render_template('index.html')

#method to display all pictures take so far
@app.route("/showPics")
def showPics():
	#if request.method == 'POST':
	db = sqlite3.connect('/home/pi/WebBoomEL/pics.db')
	db.row_factory=sqlite3.Row
	cursor = db.cursor()
	cursor.execute('''SELECT * FROM pics''')
	rows = cursor.fetchall()
	db.close()
	return render_template('showPics.html',rows = rows)

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=8080, debug=True)
