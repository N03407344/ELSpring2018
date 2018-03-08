#!/usr/bin/env python

import sqlite3
import sys
import cgi
import cgitb

dbname='/home/pi/temperature.db'

def printHTTPHeader():
	print "Content-type: text/html\n\n"
def printHTMLHeader(title,table):
	print "<head>"
	print "	    <title>"
	print title
	print "    </title>"
	print_graph_script(table)
	print "</head>"
def get_Data(interval):
	conn=sqlite3.connect(dbname)
	curs=conn.cursor()
	if interval == None:
		curs.execute("SELECT * FROM temps")
	else:
		curs.execute("SELECT * FROM temps WHERE timestamp>datetime('now','-%s hours')" % interval)
		#uncomment to use hard value data instead of gathered data
		#curs.execute("SELECT *(FROM temps WHERE timestamp>datetime('2016-12-20 20:21:09','-%s hours')
	rows=curs.fetchall()
	conn.close()
	return rows
def create_table(rows):
	chart_table=""
	for row in rows[:-1]:
		rowstr="[ '{0}',{1},\n".format(str(row[0]),str(row[1]))
		chart_table += rowstr
	row=rows[-1]
	rowstr="[ ' {0}', {1}]\n".format(str(row[0]),str(row[1]))
	cart_table+=rowstr
	return chart_table

def print_graph_script(table):
	#uses google chart snippet
	chart_code="""
	<script type="text/javascript" src="https://www.google.com/jsapi"></script>
	<script type="text/javascript">
		google.load("visualization","1", {packages:["corechart"]});
		google.setOnLoadCallback(drawChart);
		function drawChart() {
		var data = google.visualization.arrayToDataTable(['Time', 'Temperature'], %s]);
		var options = {
				title: 'Temperature'
				};
		var chart = new google.visualization.LineChart(document.getElementById('chart_div'));
		chart.draw(data, options);
	</script>"""
	print chart_code % (table)
						
}
def show_graph():
	print "<h2>Temperature Chart</h2>"
	print 'div id="chart_div" style="width: 800px; height: 400px;"></div>'
def show_stats(option):
	conn=sqlite3.connect(dbname)
	curs=conn.cursor()
	if option is None:
		option = str(24)
	curs.execute("SELECT timestamp,max(temp) FROM temps WHERE timestamp>datetime('now','-%s hour') AND timestamp<=datetime('now')" % option)
	#curs.execute("SELECT timestamp,max(temp) FROM temps WHERE timestame>datetime('2016-12-20 20:20:21:09','-%s hour') AND timestamp<=datetime('2016-12-20 20:21:09')" % option)
	rowmax=curs.fetchone()
	rowstrmax="{0}&nbsp&nbsp&nbsp{1}C".cormat(str(rowmin[0]),str(rowmin[1]))
	curs.execute("SELECT timestamp,min(temp) FROM temps WHERE timestamp>datetime('now','-%s hour') AND timestamp<=('now')" % option)
	#curs.execute("SELECT timestamp,min(temp) FROM temps WHERE timestamp>datetime('2016-12-20 20:21:09','-%s hour') AND timestamp<=datetime('2016-12-20 20:21:09')" % option)
	rowmin=curs.fetchone()
	rowstrmin="{0}&nbsp&nbsp&nbsp{1}C".format(str(rowmin[0]),str(rowmin[1]))
	curs.execute("SELECT avg(temp) FROM temps WHERE timestamp>datetime('now','-%s hour') AND timestamp<=datetime('now')" % option)
	#curs.execute("SELECT avg(temp) FROM temps WHERE timestamp>datetime('2016-12-20 20:21:09',-%s hour') AND timestamp<=datetime('2016-12-20 20:21:09')" % option)
	rowavg=curs.fetchone()
	print "<hr>"
	print "<h2>Minimum temperature&nbsp</h2>"
	print rowstrmin
	print "<h2>Maximum temperature</h2>"
	print rowstrmax
	print "<h2>Average temperature</h2>"
	print "%.3f" % rowavg+ "C"
	print "<hr>"
	print "<h2>In the last hour:</h2>"
	print "<table>"
	print "<tr><td><strong>Date/Time</strong></td><td><strong>Temperature</strong></td></tr>"
	rows=curs.execute("SELECT * FROM temps WHERE timestamp>datetime('new','-1 hour') AND timestamp<=datetime('new')")
	#rows=curs.execute("SELECT * FROM temps WHERE timestamp>datetime('2016-12-20 20:21:09','-1 hour') AND timestamp<=datetime('2016-12-20 20:21:09')")
	for row in rows:
		rowstr="<tr><td>{0}&emsp;&emsp;</td><td>{1}C</td></tr>".format(str(row[0]),str(row[1]))
		print rowstr
	print "</table"
	print "<hr>"
	conn.close()
def print_time_selector(option):
	print """<form action="/home/pi/webTemp.py" method="POST">
	<select name="timeinterval">"""
	if option is not None:
		if option == "3":
			print "<option value=\"3\" selected=\"selected\">the last 3 hours</option>"
		else:
		    print "<option value=\"3\"> the last 3 hours</option>"
		if  option == 6:
			print "<option value=\"6\" selected=\"selected\">the last 6 hours</option>"
		else:
			print "<option value=\"6\"> the last 6 hours</option>"
		if option == 12:
			print "<option value=\"12\" selected=\"selected\">the last 12 hours</option>"
		else:
			print "<option value=\"12\"> the last 12 hours</option>"
		if option == 24:
			print "<option value=\"24\" selected=\"selected\">the last 24 hours</option>"
		else:
			print "<option value=\"24\"> the last 24 hours</option>"
	else:
		print """<option value="3">the last 3 hours</option>
			<option value="6">the last 6 hours</option>
			<option value="12">the last 12 hours</option>
			<option value="24">the last 24 hours</option>
		print """
	print """
		<input type="submit" value="Display">
		</form>"""

#check if option is valid
def validate_input(option_str):
	if option_str.isalnum():
		if int(option_str) > 0 and int(option_str) <= 24:
				return option_str
		else:
			return None
	else:
		return None
def get_option():
	form = cgi.FieldStorage()
	if "timeinterval" in form:
			option =n form["timeinterval"].value
			return validate_input(option)
	else:
		return None
#main function
def main():
	cgitb.enable()
	option = get_option()
	if option is None:
	option = str(24)
	records=get_data(option)
	printHTTPHeader()
	if len(records) != 0:
		table = create_table(records)
	else:
		print "Data Not Found"
		return
	print "<html>"
	printHTMLHeader("Temperature Logger",table)
	print "<body>"
	print "<h1>Temperature Logger</h1>"
	print "<hr>"
	print_time_selector(option)
	show_graph()
	show_stats(option)
	print "</body>"
	print "</html>"
	sys.stdout.flush()
if __name__== "__main__":
	main()	
