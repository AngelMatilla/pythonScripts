# execute with python 3!!
import csv
import sys
import os
import unidecode
import re
import logging
from datetime import datetime
from pyexcel_ods3 import save_data

fuegos = ["Ana","Angel","Fanny y Adrián","Genny","Lide y Montxo","Lorena","Lurdes y Christian","Maria","Marta","Mauge","Miracles y Toni","Nadia","Silbia","Valen","Isa y Nahia","Alf","Jess y Tom","Stefania y Peppe"]
personas = ["Ana","Angel","Fanny","Genny","Lide","Lorena","Lurdes","Maria","Marta","Mauge","Miracles","Nadia","Silbia","Valen","Isa","Alf","Jess","Stefania"]
months = ["ene" , "feb" , "mar", "abr", "may", "jun" , "jul" , "ago" , "sep" , "oct" , "nov" , "dic"]
fuegos_lower = []
personas_lower = []
for index, s in enumerate(fuegos, start = 1):
	# Christian le pongo apellidos para que lo encuentre
	if "Lurdes y Christian" in s:
		s = "Lurdes y Cristian Gomez Marquina"
	# Tom es ahora Tomas Feeney
	if "Jess y Tom" in s:
		s = "Jess y Tomas Feeney"
	# Peppe es ahora Giuseppe
	if "Stefania y Peppe" in s:
		s = "Stefania y Giuseppe"
	# Valen es ahora Valentin
	if "Valen" in s:
		s = "Juan Valentin Ruiz Lopez"
	fuegos_lower.insert(index,unidecode.unidecode(s.casefold()))
for index, s in enumerate(personas, start = 1):
	personas_lower.insert(index,unidecode.unidecode(s.casefold()))

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
	extra_array = []
	# add amount either to input or output
	if float(row['Importe'].replace(',','.')) > 0:
		array[8] = float(row['Importe'].replace(',','.'))
	else:
		array[9] = abs(float(row['Importe'].replace(',','.')))
	# rule ab1.fuego.VmonthXXX.CmonthYYY.PmonthZZZ
	if "ab1" in row['Concepto'].casefold():
		try:
			parts = row['Concepto'].casefold().split('.')
			#print(parts)
			if (len(parts) < 3):
				raise Exception('badly formatted string. Not using point separation:  {}'.format(parts))
			elif len(parts[2].lstrip()) < 3:
				raise Exception('badly formatted string. Not enough info in first quantity element:  {}'.format(parts))

			# check if sum of quantity elements is correct
			total_sum = 0
			for x in parts[2::]:
				numbers = re.findall(r"[-]?[\d]+[\.,]?\d*",x)
				for i in numbers:
					total_sum += float(i.replace(',','.'))
			if (total_sum != float(row['Importe'].replace(',','.'))):
				raise Exception('Total sum of quantity elements is not correctly calculated:  {}'.format(parts))

			# find fuego in list
			name = parts[0].split()
			if any(name[2] in s for s in fuegos_lower):
				matching = [s for s in fuegos_lower if name[2] in s]
				index = fuegos_lower.index(matching[0])
				array[5] = fuegos[index]
			# allocate first quantity element {parts[2]}
			# vivienda
			if (parts[2].lstrip())[0] == "v" :
				array[1] = "Gasto"
				array[3] = "Alquiler vivienda"
			# proyecto
			elif (parts[2].lstrip())[0] == "p":
				array[1] = "Gasto"
				array[3] = "Alquiler proyectos"
				if "global ecovillage network of europe" in row['Concepto'].casefold() or "GLOBAL ECOV.NETW.EUROPE".casefold() in row['Concepto'].casefold():
					array[6] = "GEN"
				elif "ecohabitar" in row['Concepto'].casefold():
					array[6] = "Ecohabitar"
				elif "ana lucia" in row['Concepto'].casefold():
					array[6] = "Oficina Oeste"
			# comedor
			elif (parts[2].lstrip())[0] == "c":
				array[1] = "Comedor"
				array[3] = "Cuotas comedor"
				if 'index' in locals():
					array[4] = personas[index]
					array[5] = ""
			else:
				raise Exception('badly formatted string. First letter of first quantity element wrong:  {}'.format(parts))
			
			# read number in first quantity element
			if (parts[2].lstrip())[1] == ":":
				numbers = re.findall(r"[-]?[\d]+[\.,]?\d*",(parts[2].lstrip())[2:len(parts[2].lstrip())])
				#print(numbers)
				if float(numbers[0].replace(',','.')) > 0:
					array[8] = float(numbers[0].replace(',','.'))
				else: 
					array[9] = abs(float(numbers[0].replace(',','.')))
			elif any((parts[2].lstrip())[1:4] in r for r in months):
				numbers = re.findall(r"[-]?[\d]+[\.,]?\d*",(parts[2].lstrip())[4:len(parts[2].lstrip())])
				#print(numbers)
				if float(numbers[0].replace(',','.')) > 0:
					array[8] = float(numbers[0].replace(',','.'))
				else: 
					array[9] = abs(float(numbers[0].replace(',','.')))
			else: 
				raise Exception('badly formatted string:  {}'.format(parts))
			
			# allocate other quantity elements beyond parts[2]. Need to create another row for each
			if len(parts) > 3:
				for q, x in enumerate(parts[3::], start=0):
					extra_array.append(array.copy())
					# vivienda
					if x[0] == "v":
						extra_array[q][1] = "Gasto"
						extra_array[q][3] = "Alquiler vivienda"
						extra_array[q][4] = ""
						extra_array[q][5] = fuegos[index]
					# proyecto
					elif x[0] == "p":
						extra_array[q][1] = "Gasto"
						extra_array[q][3] = "Alquiler proyectos"
						if "global ecovillage network of europe" in row['Concepto'].casefold() or "GLOBAL ECOV.NETW.EUROPE".casefold() in row['Concepto'].casefold():
							extra_array[q][6] = "GEN"
						elif "ecohabitar" in row['Concepto'].casefold():
							extra_array[q][6] = "Ecohabitar"
						elif "ana lucia" in row['Concepto'].casefold():
							extra_array[q][6] = "Oficina Oeste"
							
					# comedor
					elif x[0] == "c":
						extra_array[q][1] = "Comedor"
						extra_array[q][3] = "Cuotas comedor"
						extra_array[q][4] = personas[index]
						extra_array[q][5] = ""
					else:
						raise Exception('badly formatted string. First letter of a quantity element wrong:  {}'.format(parts))
					
					# read number in other quantity element
					if (x.lstrip())[1] == ":":
						numbers = re.findall(r"[-]?[\d]+[\.,]?\d*",(x.lstrip())[2:len(x.lstrip())])
						#print(numbers)
						if float(numbers[0].replace(',','.')) > 0:
							extra_array[q][8] = float(numbers[0].replace(',','.'))
						else: 
							extra_array[q][9] = abs(float(numbers[0].replace(',','.')))
					elif any((x.lstrip())[1:4] in r for r in months):
						numbers = re.findall(r"[-]?[\d]+[\.,]?\d*",(x.lstrip())[4:len(x.lstrip())])
						#print(numbers)
						if float(numbers[0].replace(',','.')) > 0:
							extra_array[q][8] = float(numbers[0].replace(',','.'))
						else: 
							extra_array[q][9] = abs(float(numbers[0].replace(',','.')))
					else: 
						raise Exception('badly formatted string:  {}'.format(parts))

		except Exception as exception:
			print("***********************")
			logging.error(exception)
			print("***********************")
	# rule fanny (Enero C/ Abajo 1,1o) and word alquiler or renta
	if "abajo 1,1o" in row['Concepto'].casefold() or "alquiler" in row['Concepto'].casefold() or "renta" in row['Concepto'].casefold() or "mensualidad" in row['Concepto'].casefold():
		array[1] = "Gasto"
		array[3] = "Alquiler vivienda"
		# find fuego in list
		parts = row['Concepto'].casefold().split('.')
		name = parts[0].split()
		if any(name[2] in s for s in fuegos_lower):
			matching = [s for s in fuegos_lower if name[2] in s]
			array[5] = fuegos[fuegos_lower.index(matching[0])]
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
	# rule garbileku
	if "garbileku" in row['Concepto'].casefold():
		array[1] = "Gasto"
		array[3] = "Aterpe"
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
	# rule Contenedor
	# TODO: implement as part of ab1
	if "david.p" in row['Concepto'].casefold():
		array[1] = "Gasto"
		array[3] = "Alquiler proyectos"
		array[6] = "Contenedor de Ruido"
	print(array)
	data.append(array)
	if len(extra_array) > 0:
		for row in extra_array:
			print(row)
			data.append(row)
	#reset extra array
	extra_array = []
dictionary.update({"Sheet 1": data})
save_data(sys.argv[2], dictionary)
print ('\nOds file has been generated.')
