# execute with python 3!!
import csv
import sys
import os
import unidecode
from datetime import datetime
from pyexcel_ods3 import save_data

fuegos = ["Ana","Angel","Fanny y Adrián","Genny","Lide y Montxo","Lorena","Lurdes y Christian","Maria","Marta","Mauge","Miracles y Toni","Nadia","Silbia","Valen","Isa y Nahia","Alf","Jess y Tom","Stefania y Peppe"]
fuegos_lower = []
for index, s in enumerate(fuegos, start = 1):
	# Christian le pongo apellidos para que lo encuentre
	if "Lurdes y Christian" in s:
		s = "Lurdes y Cristian Gomez Marquina"
	# Tom es ahora Tomas Feeney
	if "Jess y Tom" in s:
		s = "Jess y Tomas Feeney"
	fuegos_lower.insert(index,unidecode.unidecode(s.casefold()))

if len(sys.argv) != 3:
	print ("Incorrect number of arguments:\nThe correct usage is csvparser.py inputfile.csv outputfile.ods\noutputfile.ods will be created if it doesn't exist")
	exit()
if '.csv' in sys.argv[1]:
	reader = csv.DictReader(open(sys.argv[1]))
	lines = [x for x in reader]
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
data = [["Fecha", "Caja", "Método", "Círculo/Área", "Persona", "Fuego", "Proyecto", "Concepto", "Entrada", "Salida"]]
for row in lines[::-1]:
	date = datetime.strptime(row['F. valor'],"%d/%m/%Y").date()
	# generate array
	array = [date, "", "Banco", "", "", "", "", row['Concepto'], "",""]
	# add amount either to input or output
	if float(row['Importe'].replace(',','.')) > 0:
		array[8] = float(row['Importe'].replace(',','.'))
	else:
		array[9] = abs(float(row['Importe'].replace(',','.')))
	# rule ab1.fuego.VmonthXXX.CmonthYYY.PmonthZZZ
	if "ab1" in row['Concepto'].casefold():
		parts = row['Concepto'].casefold().split('.')
		# find fuego in list
		name = parts[0].split()
		if any(name[2] in s for s in fuegos_lower):
			matching = [s for s in fuegos_lower if name[2] in s]
			array[5] = fuegos[fuegos_lower.index(matching[0])]
			array[1] = "Gasto"
			array[3] = "Alquiler vivienda"
	# rule fanny (Enero C/ Abajo 1,1o) and word alquiler or renta
	if "abajo 1,1o" in row['Concepto'].casefold() or "alquiler" in row['Concepto'].casefold() or "renta" in row['Concepto'].casefold() or "mensualidad" in row['Concepto'].casefold():
		array[1] = "Gasto"
		array[3] = "Alquiler vivienda"
		# TODO: add fuego 
	# rule caldera
	if "huesillo" in row['Concepto'].casefold():
		array[1] = "Gasto"
		array[3] = "Calefacción"
	# rule agua
	if "tasa de agua" in row['Concepto'].casefold():
		array[1] = "Gasto"
		array[3] = "Agua"
	# rule telefonia
	if "telefonica de espana" in row['Concepto'].casefold() or "sisnet" in row['Concepto'].casefold():
		array[1] = "Gasto"
		array[3] = "Internet y teléfono"
	# rule pedidos comedor
	if "gumiel y mendia" in row['Concepto'].casefold():
		array[1] = "Comedor"
		array[3] = "Pedidos"
	# rule electricidad
	if "som energia" in row['Concepto'].casefold():
		array[1] = "Gasto"
		array[3] = "Electricidad término fijo"
		# TODO: create additional line for variable term
	# rule pagos cuotas comedor
	if "comedor" in row['Concepto'].casefold():
		array[1] = "Comedor"
		array[3] = "Cuotas comedor"
	print(array)
	data.append(array)
dictionary.update({"Sheet 1": data})
save_data(sys.argv[2], dictionary)
print ('\nOds file has been generated.')
