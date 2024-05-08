#!/usr/bin/env python

# execute with python 3!!
import csv
import sys
import os
from colorama import Fore, Back, Style, init
# Homebank
from csb43 import csb43, formats
from csb43.homebank import converter as hbk_converter
from csb43.csb43 import File

print("Starting csb43parser")

init()

if len(sys.argv) != 3:
	print (Style.RESET_ALL + Fore.RED + "Incorrect number of arguments:\nThe correct usage is csb43parser.py inputfilebankentries.txt outputfile.csv\noutputfile.csv will be created if it doesn't exist")
	exit()
if '.txt' in sys.argv[1]:
	csbFile = File(open(sys.argv[1],"rb"), strict=False, silent=True)
	linesBankEntries = hbk_converter.convertFromCsb(csbFile)
	o = formats.convertFromCsb(csbFile, 'csv')
	#y = formats.convertFromCsb(csbFile, 'yaml')
else:
	print (Style.RESET_ALL + Fore.RED + "Please enter a csb norma 43 formatted file as input for the bank entries (with extension .txt)")
	exit()
if '.csv' in sys.argv[2]:
	if os.path.exists(sys.argv[2]):
		os.remove(sys.argv[2])
	else:
		print(Style.RESET_ALL + Fore.BLUE + "The csv file does not exist and will be created")
else:
	print (Style.RESET_ALL + Fore.RED + "Please enter a csv formatted file as output (with extension .csv)\nIf it does not exist it will be created")
	exit()

#print(o.csv)
#print(o)
#print(y.yaml)

# create first row
data = [["Fecha Operacion", "Fecha Valor", "Descripcion", "Importe", "Saldo",]]
#print(data)

formattedRow = ["","","","",""]
# crop elements
for row in o[::-1]:
	if "04" in row[17]:
		transfText = "TRF. "
	else:
		transfText = ""
	formattedRow[0] = row[23]
	formattedRow[1] = row[24]
	formattedRow[2] = transfText+row[19]+" "+row[20]
	formattedRow[3] = float(row[25])
	formattedRow[4] = float(row[10])
	data.append(formattedRow)
	#reset extra array
	formattedRow = ["","","","",""]

# create csv file and write to it
with open(sys.argv[2], 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
	
    writer.writerows(data)

print("csb43parser done")