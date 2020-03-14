# execute with python 3!!
import csv
import sys
import os
import unidecode
from datetime import datetime
from pyexcel_ods3 import save_data

if len(sys.argv) != 3:
	print ("Incorrect number of arguments:\nThe correct usage is csvparser.py inputfile.csv outputfile.txt\noutputfile.txt will be created if it doesn't exist")
	exit()
if '.csv' in sys.argv[1]:
	reader = csv.DictReader(open(sys.argv[1]))
	lines = [x for x in reader]
else:
	print ("Please enter a csv formatted file as input (with extension .csv)")
	exit()
if '.txt' in sys.argv[2]:
	if os.path.exists(sys.argv[2]):
		os.remove(sys.argv[2])
	else:
		print("The txt file does not exist and will be created")
else:
	print ("Please enter a ods formatted file as output (with extension .txt)\nIf it does not exist it will be created")
	exit()

f= open(sys.argv[2],"w+")

for row in lines:
	name = row['name']
	lat = float(row['latitude'])
	lon = float(row['longitude'])
	link = row['href']
	# generate new line
	line = "[leaflet-marker lat=" +str(lat)+" lng="+str(lon)+" iconUrl=\"https://raw.githack.com/GEN-Europe/gen-web/master/map/leaf.gif\" iconSize=\"28,35\"] <a href=\""+str(link)+"\" target=\"_blank\" rel=\"noopener noreferrer\">"+str(name)+"</a> [/leaflet-marker]"
	line = line + "\n"
	print(line)
	f.write(line)
f.close()
