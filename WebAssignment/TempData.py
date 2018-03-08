#!/usr/bin/env python
import sqlite3
import os
import time
import glob

dbname='/home/pi/temperture.db'

def log_Temp(temp):
	conn = splite3.connect(dbname)
	curs=conn.cursor()
	curs.execute("INSERT INTO temps valuesdatetime('now'),(?))",(temp,))
	conn.commit()
	conn.close()
def display_data():
	conn=sqlite3.connect(dbname)
	curs=conn.cursor()
	for row in curs.execute("SELECT * FROM temps"):
		print str(row[0]) +"     "+str(row[1])
	conn.close()

def get_temp(devicefile):
	try:
	   fileob = open(devicefile,'r')
	   lines = fileob.readlines()
	   fileob.close()
	except:
		return None
	status = lines[0][-4:-1]
	if status == "YES":
		print status
		tempstr = lines[1][-6:-1]
		tempval = float(tempstr)/1000
		print tempval
`		return tempval
	else:
		print "Error"
		return None
def main():
	#enable kernel modules
	os.system('sudo modprobe w1-gpio')
	os.system('sudomodprobe w1-therm')
	devicelist = glob.glob('/sys/bus/w1/devices/28*')
	if devicelist == '':
		return None
	else:
	w1devicefile = devicelist[0] + '/w1_slave'
	while True:
		temperature = get_temp(w1devicefile)
		if temperature != None:
			print "temperature="+str(temperature)
		else:
			temperature = get_temp(w1devicefile)
			print  "temperature=" + str(temperature)
		log_Temp(temperature)
		display_data()
if __name__=="__main__":
	main()
