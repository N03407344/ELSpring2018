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
panServoAngle = 90 #starting postion for pan servo
tiltServoAngle = 90 #starting postion for tilt servo
panPin = 17
tiltPin = 7
@app.route("/")
def main():
   templateData = {
                    'panServoAngle' : panServoAngle,
                    'tiltServoAngle' : tiltServoAngle
        }
   return render_template('main.html', **templateData)

#move the servos
@app.route("/",methods=['POST'])
def move_post():
     global panServoAngle
     global tiltServoAngle
     panNewAngle = int(request.form['panServoAngle'])
     if (panNewAngle != panServoAngle):
               panServoAngle = panNewAngle
               os.system("python3 angleServo.py " + str(panPin) + " " + str(panServoAngle))
     tiltNewAngle = int(request.form['panServoAngle'])
     if (tiltNewAngle != tiltServoAngle):
               tiltServoAngle = tiltNewAngle
               os.system("python3 angleServo.py " + str(tiltPin) + " " + str(tiltServoAngle))
     templateData = {
           'panServoAngle'  : panServoAngle,
           'tiltServoAngle' : tiltServoAngle
      }
     return render_template('main.html', **templateData)
@app.route("/takePic", methods=['GET','POST'])
def takePic():
    try:
       db = sqlite3.connect('/home/pi/WebBoomEL/pics.db')
       cursor = db.cursor()
       currentTime = time.srtftime('%x %X %Z')
       camera = picamera.Picamera()
       timeTaken = time.strftime("%Y%m%d-%H%M%S")
       pic = camera.capture('static/'+timeTaken+'.jpg')
       camera.close()
       picPath = timeTaken + ".jpg"
       cursor.execute('''INSERT INTO pics(picPath, datetime)
                            VALUES(?,?)''', (picPath,currentTime))
       db.commit()
    except Exception as e:
          db.rollback()
          raise e
    finally:
         db.close()
    return render_template('main.html')

@app.route("/showPics")
def showPics():
    db = sqlite3.connect('/home/pi/WebBoomEL/pics.db')
    db.row_factory=sqlite3.Row
    cursor = db.cursor()
    cursor.execute('''SELECT * FROM pics''')
    rows.cursor.fetchall()
    db.close()
    return render_template('showPics.html',rows = rows)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
