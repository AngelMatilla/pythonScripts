# execute with python 3!!
import csv
import sys
import os
from datetime import datetime
from pyexcel_ods3 import save_data

if len(sys.argv) != 3:
	print ("Incorrect number of arguments:\nThe correct usage is csvparser.py inputfile.csv outputfile.ods\noutputfile.ods will be created if it doesn't exist")
	exit()
if '.csv' in sys.argv[1]:
	reader = csv.DictReader(open(sys.argv[1]))
else:
	print ("Please enter a csv formatted file as input (with extension .csv)")
	exit()
if '.ods' in sys.argv[2]:
	if os.path.exists(sys.argv[2]):
		os.remove(sys.argv[2])
	else:
		print("The ods file does not exist and will be created")
else:
	print ("Please enter a ods formatted file as output (with extension .ods)\nIf it does not exist it will be created")
	exit()

dictionary = dict()
data = [["Fecha", "Concepto", "Entrada", "Salida"]]
for row in reader:
	date = datetime.strptime(row['F. valor'],"%d/%m/%Y").date()
	if float(row['Importe'].replace(',','.')) > 0:
		array = [date, row['Concepto'], float(row['Importe'].replace(',','.')),""]
	else:
		array = [date, row['Concepto'], "",abs(float(row['Importe'].replace(',','.')))]
	print(array)
	data.append(array)
dictionary.update({"Sheet 1": data})
save_data(sys.argv[2], dictionary)
print ('\nOds file has been generated.')
