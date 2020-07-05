# execute with python 3!!
import csv
import sys
import os
import unidecode
import re
import logging
from datetime import datetime
from pyexcel_ods3 import save_data

fuegos = ["Ana","Angel","Fanny y Adrián","Genny","Lide y Montxo","Lorena","Lurdes y Christian","Maria","Marta","Mauge","Miracles y Toni","Nadia","Silbia","Valen","Isa y Nahia","Alf","Jess y Tom","Stefania y Peppe","Carlos","Monica y Franco","Ibai","Iñigo"]
personas = ["Adrián","Alf","Ametz","Ana","Angel","Aratz","Chester","Christian","Eki","Fanny","Genny","Ibrahim","Isa","Jess","Lide","Lluch","Lorena","Lurdes","Manuel","Maria","Mariona","Marta","Mauge","Miracles","Montxo","Nadia","Nahia","Noa","Peppe","Salma","Selba","Silbia","Stefania","Tom","Toni","Uma","Urbi","Valen","Pepe Ecohabitar","Carlos","Monica","Franco","Ibai","Iñigo"]
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
		s = "Giuseppe el Bahrawy y Stefania del Conte"
	# Valen es ahora Valentin
	if "Valen" in s:
		s = "Juan Valentin Ruiz Lopez"
	# Carlos es ahora Martinez Mampay Carlos Alberto
	if "Carlos" in s:
		s = "Martinez Mampay Carlos Alberto"
	# Alf es ahora Alfonso Flaquer Carreras
	if "Alf" in s:
		s = "Alfonso Flaquer Carreras"
	# Maria es ahora maria begona garcia erviti 
	if "Maria" in s:
		s = "Maria Begona Garcia Erviti"
	# Mauge es ahora maria eugenia canada zorrilla
	if "Mauge" in s:
		s = "Maria Eugenia Canada Zorrilla"
	# Angel
	if "Angel" in s:
		s = "Angel Matilla"
	# Ana
	if "Ana" in s:
		s = "Ana Lucia Perez"
	# Ibai
	if "Ibai" in s:
		s = "Ibai Guemes"
	# Lore
	if "Lorena" in s:
		s = "Lorena Mompel"
	# Nahia
	if "Isa y Nahia" in s:
		s = "Isa y Nahia Agote"
	# Montxo
	if "Lide y Montxo" in s:
		s = "Lide y Montxo Gota"
	# Genny
	if "Genny" in s:
		s = "Genny Carraro"
	# Fanny y Adrián
	if "Fanny y Adrián" in s:
		s = "Fanny Eleonora y Adrián Areta"
	# Miracles y Toni
	if "Miracles y Toni" in s:
		s = "Juana Milagros y Toni"
	fuegos_lower.insert(index,unidecode.unidecode(s.casefold()))
for index, s in enumerate(personas, start = 1):
	# Christian le pongo apellidos para que lo encuentre
	if "Christian" in s:
		s = "Cristian Gomez Marquina"
	# Tom es ahora Tomas Feeney
	if "Tom" in s:
		s = "Tomas Feeney"
	# Peppe es ahora Giuseppe
	if "Peppe" in s:
		s = "Giuseppe el Bahrawy"
	# Valen es ahora Valentin
	if "Valen" in s:
		s = "Juan Valentin Ruiz Lopez"
	# Carlos es ahora Martinez Mampay Carlos Alberto
	if "Carlos" in s:
		s = "Martinez Mampay Carlos Alberto"
	# Alf es ahora Alfonso Flaquer Carreras
	if "Alf" in s:
		s = "Alfonso Flaquer Carreras"
	# Maria es ahora maria begona garcia erviti 
	if "Maria" in s:
		s = "Maria Begona Garcia Erviti"
	# Mauge es ahora maria eugenia canada zorrilla
	if "Mauge" in s:
		s = "Maria Eugenia Canada Zorrilla"	
	# Angel
	if "Angel" in s:
		s = "Angel Matilla"
	# Ana
	if "Ana" in s:
		s = "Ana Lucia Perez"
	# Ibai
	if "Ibai" in s:
		s = "Ibai Guemes"
	# Lore
	if "Lorena" in s:
		s = "Lorena Mompel"
	# Nahia
	if "Nahia" in s:
		s = "Nahia Agote"
	# Montxo
	if "Montxo" in s:
		s = "Montxo Gota"
	# Genny
	if "Genny" in s:
		s = "Genny Carraro"
	# Fannyn
	if "Fanny" in s:
		s = "Mw F"
	# Adrián
	if "Adrián" in s:
		s = "Adrián Areta"
	# Pepe Ecohabitar
	if "Pepe Ecohabitar" in s:
		s = "Jose Ignacio Rojas Rojas"
	# Miracles
	if "Miracles" in s:
		s = "Juana Milagros"
	personas_lower.insert(index,unidecode.unidecode(s.casefold()))

# print(fuegos_lower)
# print(personas_lower)
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

	## specific replacements before the ab1 parsing 
	#remove S.L in Ecohabitar
	if "ECOHABITAR VISIONES SOSTENIBLES, S.L" in row['Concepto']:
		new_concept = row['Concepto'].replace(", S.L","")
		row['Concepto'] = new_concept

	#remove last point in concepto
	if row['Concepto'][-1] == ".":
		new_concept = row['Concepto'][:-1]
		row['Concepto'] = new_concept
	
	# rule ab1.fuego.V:XXX.C:YYY.P:ZZZ.I:ZZZ.E:ZZZ.F:ZZZ
	# V stands for vivienda
	# C for comedor
	# P for proyecto
	# I for cuota integración
	# E for almuerzos
	# F for Fondo solidaridad
	if "ab1" in row['Concepto'].casefold():
		try:
			parts = row['Concepto'].casefold().split('.')
			# print(parts)
			# parts have to be at least 3: 'transferencia de xxx ab1', '<fuego>', '<quantity element>' (e.g. v:200 or p:45 or c:45,76)
			if (len(parts) < 3):
				raise Exception('badly formatted string. Not using point separation:  {}'.format(parts))
			# check the validity of the second element e.g. v:200 or p:45 or c:45,76
			# if length is < 3 discard it
			elif len(parts[2].strip()) < 3:
				raise Exception('badly formatted string. Not enough info in first quantity element:  {}'.format(parts))
			# if not starting with 'v', 'c' or 'p' and no ':' later -> discard it 
			elif (((parts[2].strip()[0] != "v") and (parts[2].strip()[0] != "c") and (parts[2].strip()[0] != "p") and (parts[2].strip()[0] != "i") and (parts[2].strip()[0] != "e") and (parts[2].strip()[0] != "f")) or (parts[2].strip()[1] != ":")):
				raise Exception('badly formatted string. first quantity element not well formed:  {}'.format(parts))

			# remove any additional element on the last part (after a space)
			if " " in parts[len(parts)-1]:
				rest = parts[len(parts)-1].split(" ", 1)[0]
				parts[len(parts)-1] = rest
			
			# check if sum of quantity elements is correct
			total_sum = 0
			for x in parts[2::]:
				if ((((x.strip())[0] == "v") or ((x.strip())[0] == "c") or ((x.strip())[0] == "p") or ((x.strip())[0] == "i") or ((x.strip())[0] == "e") or ((x.strip())[0] == "f")) and (((x.strip())[1] == ":") or any((x.strip())[1:4] in r for r in months))):
					numbers = re.findall(r"[-]?[\d]+[\.,]?\d*",x)
					for i in numbers:
						total_sum += float(i.replace(',','.'))
			if (total_sum != float(row['Importe'].replace(',','.'))):
				raise Exception('Total sum of quantity elements is not correctly calculated:  {}'.format(parts))

			# find fuego in list
			name = parts[0].split()
			# print(name[2]+" "+name[3])
			if any(name[2]+" "+name[3] in s for s in fuegos_lower):
				matching = [s for s in fuegos_lower if name[2]+" "+name[3] in s]
				indexFuegos = fuegos_lower.index(matching[0])
				# print(indexFuegos)
				array[5] = fuegos[indexFuegos]
			else:
				array[5] = ""
				indexFuegos = -1
			
			# find person in list
			if any(name[2]+" "+name[3] in s for s in personas_lower):
				matching = [s for s in personas_lower if name[2]+" "+name[3] in s]
				indexPersonas = personas_lower.index(matching[0])
				# print(indexPersonas)
				array[4] = personas[indexPersonas]
			else:
				array[4] = ""
				indexPersonas = -1
			# allocate first quantity element {parts[2]}
			
			## vivienda
			if (parts[2].strip())[0] == "v" :
				array[1] = "Gasto"
				array[3] = "Alquiler vivienda"
			
			## proyecto
			elif (parts[2].strip())[0] == "p":
				array[1] = "Gasto"
				array[3] = "Alquiler proyectos"
				if "global ecovillage network of europe" in row['Concepto'].casefold() or "GLOBAL ECOV.NETW.EUROPE".casefold() in row['Concepto'].casefold():
					array[6] = "GEN"
				elif "ecohabitar" in row['Concepto'].casefold():
					array[6] = "Ecohabitar"
				elif "ana lucia" in row['Concepto'].casefold():
					array[6] = "Oficina Oeste"
				elif "biararte" in row['Concepto'].casefold() or "biar arte" in row['Concepto'].casefold():
					array[6] = "Biar Arte"
			
			## comedor
			elif (parts[2].strip())[0] == "c":
				array[1] = "Comedor"
				array[3] = "Cuotas comedor"

			## almuerzos
			elif (parts[2].strip())[0] == "e":
				array[1] = "Comedor"
				array[3] = "Botes"
			
			## cuota integración
			elif (parts[2].strip())[0] == "i":
				array[1] = "Inversión"
				array[3] = "Inversión entrada a integración"

			## fondo solidaridad
			elif (parts[2].strip())[0] == "f":
				array[1] = "Inversión"
				array[3] = "Fondo Solidaridad Arterrana"

			else:
				raise Exception('badly formatted string. First letter of first quantity element wrong:  {}'.format(parts))
			
			# read number in first quantity element
			if (parts[2].strip())[1] == ":":
				numbers = re.findall(r"[-]?[\d]+[\.,]?\d*",(parts[2].strip())[2:len(parts[2].strip())])
				#print(numbers)
				if float(numbers[0].replace(',','.')) > 0:
					array[8] = float(numbers[0].replace(',','.'))
				else: 
					array[9] = abs(float(numbers[0].replace(',','.')))
			elif any((parts[2].strip())[1:4] in r for r in months):
				numbers = re.findall(r"[-]?[\d]+[\.,]?\d*",(parts[2].strip())[4:len(parts[2].strip())])
				#print(numbers)
				if float(numbers[0].replace(',','.')) > 0:
					array[8] = float(numbers[0].replace(',','.'))
				else: 
					array[9] = abs(float(numbers[0].replace(',','.')))
			else: 
				raise Exception('badly formatted string:  {}'.format(parts))
			
			# allocate other quantity elements beyond parts[2]. Need to create another row for each
			# rule ab1.fuego.V:XXX.C:YYY.P:ZZZ.I:ZZZ.E:ZZZ.F:ZZZ
			# V stands for vivienda
			# C for comedor
			# P for proyecto
			# I for cuota integración
			# E for almuerzos
			# F for Fondo solidaridad
			if len(parts) > 3:
				for q, x in enumerate(parts[3::], start=0):
					# check if parts[3] and more contains valid formatted data, if not cancel parsing
					# if not starting with 'v', 'c' or 'p' and no ':' later -> discard it 
					if (((x.strip()[0] != "v") and (x.strip()[0] != "c") and (x.strip()[0] != "p") and (x.strip()[0] != "e") and (x.strip()[0] != "i") and (x.strip()[0] != "f")) or (x.strip()[1] != ":")):
						print('***Warning***: badly formatted string. Quantity element number {} not well formed:  {}'.format(q+3,parts))
						continue
					extra_array.append(array.copy())
					
					## vivienda
					if x.strip()[0] == "v":
						extra_array[q][1] = "Gasto"
						extra_array[q][3] = "Alquiler vivienda"
						extra_array[q][4] = ""
						if indexFuegos != -1:
							extra_array[q][5] = fuegos[indexFuegos]
					## proyecto
					elif x.strip()[0] == "p":
						extra_array[q][1] = "Gasto"
						extra_array[q][3] = "Alquiler proyectos"
						if "global ecovillage network of europe" in row['Concepto'].casefold() or "GLOBAL ECOV.NETW.EUROPE".casefold() in row['Concepto'].casefold():
							extra_array[q][6] = "GEN"
						elif "ecohabitar" in row['Concepto'].casefold():
							extra_array[q][6] = "Ecohabitar"
						elif "ana lucia" in row['Concepto'].casefold():
							extra_array[q][6] = "Oficina Oeste"
						elif "biararte" in row['Concepto'].casefold() or "biar arte" in row['Concepto'].casefold():
							extra_array[q][6] = "Biar Arte"
							
					## comedor
					elif x.strip()[0] == "c":
						extra_array[q][1] = "Comedor"
						extra_array[q][3] = "Cuotas comedor"

					## almuerzos
					elif x.strip()[0] == "e":
						extra_array[q][1] = "Comedor"
						extra_array[q][3] = "Botes"
					
					## cuota integración
					elif x.strip()[0] == "i":
						extra_array[q][1] = "Inversión"
						extra_array[q][3] = "Inversión entrada a integración"

					## fondo solidaridad
					elif x.strip()[0] == "f":
						extra_array[q][1] = "Inversión"
						extra_array[q][3] = "Fondo Solidaridad Arterrana"
					
					else:
						print('WARNING: badly formatted string. Skipping quantity element:  {}'.format(x))
						extra_array.remove(extra_array[q])
						continue
					
					# read number in other quantity element
					if (x.strip())[1] == ":":
						numbers = re.findall(r"[-]?[\d]+[\.,]?\d*",(x.strip())[2:len(x.strip())])
						#print(numbers)
						if float(numbers[0].replace(',','.')) > 0:
							extra_array[q][8] = float(numbers[0].replace(',','.'))
						else: 
							extra_array[q][9] = abs(float(numbers[0].replace(',','.')))
					elif any((x.strip())[1:4] in r for r in months):
						numbers = re.findall(r"[-]?[\d]+[\.,]?\d*",(x.strip())[4:len(x.strip())])
						#print(numbers)
						if float(numbers[0].replace(',','.')) > 0:
							extra_array[q][8] = float(numbers[0].replace(',','.'))
						else: 
							extra_array[q][9] = abs(float(numbers[0].replace(',','.')))
					else: 
						print('WARNING: badly formatted string. Skipping quantity element:  {}'.format(x))
						continue

		except Exception as exception:
			print("***********************")
			logging.error(exception)
			print("***********************")
	# rule fanny (Enero C/ Abajo 1,1o) and word alquiler or renta
	if "abajo 1,1o" in row['Concepto'].casefold() or "renta" in row['Concepto'].casefold() or "mensualidad" in row['Concepto'].casefold():
		array[1] = "Gasto"
		array[3] = "Alquiler vivienda"
		# find fuego in list
		parts = row['Concepto'].casefold().split('.')
		name = parts[0].split()
		if any(name[2]+" "+name[3] in s for s in fuegos_lower):
			matching = [s for s in fuegos_lower if name[2]+" "+name[3] in s]
			array[5] = fuegos[fuegos_lower.index(matching[0])]
	# rule caldera
	if "huesillo" in row['Concepto'].casefold() and float(row['Importe'].replace(',','.')) < 0:
		array[1] = "Gasto"
		array[3] = "Calefacción"
	# rule banco
	if ("COMISION EMISION TRANSF".casefold() in row['Concepto'].casefold() \
	or "LIQUIDACION AHORRO".casefold() in row['Concepto'].casefold() \
	or "COMISION MANTENIM".casefold() in row['Concepto'].casefold()) \
	and float(row['Importe'].replace(',','.')) <= 0:
		array[1] = "Gasto"
		array[3] = "Banco"
	# rule agua
	if "tasa de agua" in row['Concepto'].casefold() and float(row['Importe'].replace(',','.')) < 0:
		array[1] = "Gasto"
		array[3] = "Agua"
	# rule telefonia
	if ("telefonica de espana" in row['Concepto'].casefold() or "sisnet" in row['Concepto'].casefold()) and float(row['Importe'].replace(',','.')) < 0:
		array[1] = "Gasto"
		array[3] = "Internet y teléfono"
	# rule web
	if "strato" in row['Concepto'].casefold() and float(row['Importe'].replace(',','.')) < 0:
		array[1] = "Gasto"
		array[3] = "Web"
	# rule garbileku
	if "garbileku" in row['Concepto'].casefold() and float(row['Importe'].replace(',','.')) < 0:
		array[1] = "Gasto"
		array[3] = "Aterpe"
	# rule pedidos comedor
	if "gumiel y mendia" in row['Concepto'].casefold() and float(row['Importe'].replace(',','.')) < 0:
		array[1] = "Comedor"
		array[3] = "Pedidos"
	# rule electricidad
	if "som energia" in row['Concepto'].casefold() and float(row['Importe'].replace(',','.')) < 0:
		array[1] = "Gasto"
		array[3] = "Electricidad término fijo"
		# create additional line for variable term
		extra_array.append(array.copy())
		extra_array[0][3] = "Electricidad término variable"
	# rule pagos cuotas comedor
	if "comedor" in row['Concepto'].casefold():
		array[1] = "Comedor"
		array[3] = "Cuotas comedor"
	# rule pagos alquiler arterra
	if "pedro enrique ramirez aragon" in row['Concepto'].casefold() or "geserlocal" in row['Concepto'].casefold():
		array[1] = "Gasto"
		array[3] = "Alquiler Arterra"
	# rule residuos Irati
	if "recibo mancomunidad r.s.u. irati" in row['Concepto'].casefold():
		array[1] = "Gasto"
		array[3] = "Residuos mancomunidad"
	# rule Contenedor
	# TODO: implement as part of ab1
	if "david.p" in row['Concepto'].casefold():
		array[1] = "Gasto"
		array[3] = "Alquiler proyectos"
		array[6] = "Contenedor de Ruido"
	# rule proyectos
	if "global ecovillage network of europe" in row['Concepto'].casefold() or "GLOBAL ECOV.NETW.EUROPE".casefold() in row['Concepto'].casefold():
		array[6] = "GEN"
	elif "ecohabitar" in row['Concepto'].casefold():
		array[4] = "Miracles"
		array[5] = "Miracles y Toni"
		array[6] = "Ecohabitar"
	elif "ana lucia" in row['Concepto'].casefold() and array[3] == "Alquiler proyectos":
		array[6] = "Oficina Oeste"
	elif "biararte" in row['Concepto'].casefold() or "biar arte" in row['Concepto'].casefold():
		array[6] = "Biar Arte"
	# rule butano
	if "butano" in row['Concepto'].casefold() and array[4]=="" and array[5]=="" and array[6]=="":
		array[1] = "Gasto"
		array[3] = "Butano"
	# rule Iñigo
	if "inigo" in row['Concepto'].casefold():
		array[4] = "Iñigo"
		array[5] = "Iñigo"

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
