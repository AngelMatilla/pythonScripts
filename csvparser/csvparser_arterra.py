"""
Hola a todas,
Os recuerdo que desde contabilidad pedimos que las transferencias a Arterra se hagan de una forma determinada. Hay novedades en la plantilla!!
 
Recuerdo que la vivienda se debería pagar hasta el día 5 de cada mes y que si tenéis más de un mes de deuda os corresponde poneros en contacto con contabilidad para plantear un escenario de cómo se va a saldar esa deuda y cuando.
Aquí los detalles de la cuenta: Nombre: Asociación Arterra BizimoduIBAN: ES97 1491 0001 2921 1057 3728BIC: TRIOESMMXXX 
Idealmente el fondo de solidaridad se debería pagar en un pago único, pero si no se puede, se puede ir pagando mensualmente. Recuerdo que el fondo de solidaridad corresponde a 60€/adulto en integración o integrado.

Es muy fácil hacerlo como plantilla si accedeis a vuestro banco online (os puedo ayudar si lo necesitáis). Idealmente se podría establecer la vivienda/proyecto como transferencia periódica y lo demás se puede ir haciendo a mano mes a mes.
 
Esta es la plantilla

AB1.Fuego.V:XXX.C:YYY.P:ZZZ.E:XXX.I:YYY.F:ZZZ.D:XXX.S:YYY.B:ZZZ

Notas sobre puntuación: 
* Nota 1: Fijaos que entre elementos no hay espacios sino que hay puntos.
* Nota 2: Los decimales en las cantidades se ponen con coma baja o alta: 32,50 o 32'50. No uséis punto por favor ya que se usa como separador (ni acento tampoco).
* Nota 3: En caso de que vuestro banco no admita comas "," o " ' ", evitad pagar cosas fraccionadas y redondead la cantidad
* Nota 4: los dos puntos después de la letra son opcionales en caso de que vuestro banco no permita ese caráctere.g. AB1.Fuego.VXXX.CYYY.PZZZ.EXXX.IYYY.FZZZ.DXXX.SYYY.BZZZ
* Nota 5: si vuestro banco no os permite usar el punto "." podeis usar dos paréntesis "()"e.g. AB1()Fuego()V:XXX()C:YYY()P:ZZZ()E:XXX()I:YYY()F:ZZZ()D:XXX()S:YYY()B:ZZZ
* Nota 6: las notas 4 y 5 son combinables :) 

Notas sobre el significado de las letras: 
V es cuotas de vivienda (va seguido de dos puntos (opciona) y la cantidad)
C es cuotas de comedor (va seguido de dos puntos (opciona) y la cantidad)
P es cuotas de proyecto (va seguido de dos puntos (opciona) y la cantidad)
E es cuotas de almuerzos (va seguido de dos puntos (opciona) y la cantidad)
I es cuota de integración (va seguido de dos puntos (opciona) y la cantidad)
F es fondo de solidaridad (va seguido de dos puntos (opciona) y la cantidad)
D es una donación (va seguido de dos puntos (opciona) y la cantidad)
S es visita participativa [vivienda] (va seguido de dos puntos (opciona) y la cantidad)
B es bote [comedor de visitas] (va seguido de dos puntos (opciona) y la cantidad)

Podéis usar los elementos por separado o todos juntos en un mismo pago.

Si queréis añadir algo porque lo necesitáis como concepto lo podéis añadir después del código separado por un espacio

Ejemplos:

* AB1.Angel.V:300.E:20.F:60
* AB1.montxo-lide.C:46 mensaje que necesitan montxo y lide
* AB1.Ana.V:282.P:50
* AB1.Mauge.V:250.C:50.P:20
* AB1.Valen.V:250.C:40.F:60
* AB1.monica-franco.B:30 Comidas visitas
* AB1.Peppe.D:67
"""
# execute with python 3!!
import csv
import sys
import os
import unidecode
import re
import logging
from datetime import datetime
from pyexcel_ods3 import save_data

fuegos = ["Ana","Angel","Fanny y Adrián","Genny","Lide y Montxo","Lorena","Lurdes y Christian","Maria","Marta","Mauge","Miracles y Toni","Nadia","Silbia","Valen","Isa y Nahia","Alf","Jess y Tom","Stefania y Peppe","Carlos","Monica y Franco","Ibai","Iñigo","Alsu","Beñat","Moni y Tiko","Ione y Leona"]
personas = ["Adrián","Alf","Ametz","Ana","Angel","Aratz","Chester","Christian","Eki","Fanny","Genny","Ibrahim","Isa","Jess","Lide","Lluch","Lorena","Lurdes","Manuel","Maria","Mariona","Marta","Mauge","Miracles","Montxo","Nadia","Nahia","Noa","Peppe","Salma","Selba","Silbia","Stefania","Tom","Toni","Uma","Urbi","Valen","Pepe Ecohabitar","Carlos","Monica","Franco","Ibai","Iñigo","Alsu","Beñat","Bianca","Moni","Tiko","Leona","Ione"]
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
	# Monica y Franco
	if "Monica y Franco" in s:
		s = "Monica Cuende Lozano y Franco de Sena Llobera"
	# Alsu
	if "Alsu" in s:
		s = "Alsu MURATOVA MURATOVA"
	# Moni y Tiko
	if "Moni y Tiko" in s:
		s = "Moni y VICENTE ESTEVE SUBIES"
	# Beñat
	if "Beñat" in s:
		s = "BENAT GURMENDI CULLA"
	# Nadia
	if "Nadia" in s:
		s = "NADIA CALDERON DELGADO"
	# Leona
	if "Ione y Leona" in s:
		s = "Ione y Leona Berengo"
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
	# Stefania es ahora Stefania del Conte
	if "Stefania" in s:
		s = "Stefania del Conte"
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
		s = "Jose Ignacio ROJAS ROJAS"
	# Miracles
	if "Miracles" in s:
		s = "Juana Milagros"
	# Monica
	if "Monica" in s:
		s = "Monica Cuende Lozano"
	# Franco
	if "Franco" in s:
		s = "Franco de Sena Llobera"
	# Alsu
	if "Alsu" in s:
		s = "Alsu MURATOVA MURATOVA"
	# Tiko
	if "Tiko" in s:
		s = "VICENTE ESTEVE SUBIES"
	# Beñat
	if "Beñat" in s:
		s = "BENAT GURMENDI CULLA"
	# Nadia
	if "Nadia" in s:
		s = "NADIA CALDERON DELGADO"
	# Leona
	if "Leona" in s:
		s = "Leona Berengo"
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
data = [["Fecha", "Caja", "Método", "Círculo/Área", "Persona", "Fuego", "Proyecto", "Concepto", "Entrada", "Salida", "Notas"]]
for row in lines[::-1]:
	date = datetime.strptime(row['F. valor'],"%d/%m/%Y").date()
	# generate array
	array = [date, "", "Banco", "", "", "", "", row['Concepto'], "","",""]
	extra_array = []
	# add amount either to input or output
	if float(row['Importe'].replace(',','.')) > 0:
		array[8] = float(row['Importe'].replace(',','.'))
	else:
		array[9] = abs(float(row['Importe'].replace(',','.')))

	# replace "()" by "." before parsing in concept
	if "()" in row['Concepto']:
		new_concept = row['Concepto'].replace("()",".")
		row['Concepto'] = new_concept

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
	# D for Donación
	# S for Visita Participativa vivienda
	# B for Bote Comedor
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
			# if not starting with 'v', 'c', 'p', 'e', 'f', 'd', 's' or 'b' and no ':' later -> discard it 
			elif (((parts[2].strip()[0] != "v") and (parts[2].strip()[0] != "c") and (parts[2].strip()[0] != "p") and (parts[2].strip()[0] != "i") \
				and (parts[2].strip()[0] != "e") and (parts[2].strip()[0] != "f") and (parts[2].strip()[0] != "d") and (parts[2].strip()[0] != "s") \
				and (parts[2].strip()[0] != "b")) ): # or (parts[2].strip()[1] != ":")):
					raise Exception('badly formatted string. first quantity element not well formed:  {}'.format(parts))

			# remove any additional element on the last part (after a space)
			if " " in parts[len(parts)-1]:
				rest = parts[len(parts)-1].split(" ", 1)[0]
				parts[len(parts)-1] = rest
			
			# check if sum of quantity elements is correct
			total_sum = 0
			for x in parts[2::]:
				if ((((x.strip())[0] == "v") or ((x.strip())[0] == "c") or ((x.strip())[0] == "p") or ((x.strip())[0] == "i") \
					or ((x.strip())[0] == "e") or ((x.strip())[0] == "f") or ((x.strip())[0] == "d") or ((x.strip())[0] == "s") \
					or ((x.strip())[0] == "b")) or any((x.strip())[1:4] in r for r in months)): # and (((x.strip())[1] == ":")
						numbers = re.findall(r"[-]?[\d]+[,.']?\d*",unidecode.unidecode(x))
						for i in numbers:
							total_sum += float(i.replace(',','.').replace('\'','.'))
			if (total_sum != float(row['Importe'].replace(',','.').replace('\'','.'))):
				raise Exception('Total sum of quantity elements is not correctly calculated:  {}'.format(parts))

			# find fuego in list
			name = parts[0].split()
			if any(name[2]+" "+name[3] in s for s in fuegos_lower):
				matching = [s for s in fuegos_lower if name[2]+" "+name[3] in s]
				indexFuegos = fuegos_lower.index(matching[0])
				array[5] = fuegos[indexFuegos]
			else:
				array[5] = ""
				indexFuegos = -1
			
			# find person in list
			if any(name[2]+" "+name[3] in s for s in personas_lower):
				matching = [s for s in personas_lower if name[2]+" "+name[3] in s]
				indexPersonas = personas_lower.index(matching[0])
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
				elif "fanny" in row['Concepto'].casefold() or "ceramica" in row['Concepto'].casefold():
					array[6] = "Taller cerámica"
			
			## comedor
			elif (parts[2].strip())[0] == "c":
				array[1] = "Comedor"
				array[3] = "Cuotas comedor"

			## almuerzos
			elif (parts[2].strip())[0] == "e":
				array[1] = "Comedor"
				array[3] = "Almuerzos"
			
			## cuota integración
			elif (parts[2].strip())[0] == "i":
				array[1] = "Inversión"
				array[3] = "Inversión entrada a integración"

			## fondo solidaridad
			elif (parts[2].strip())[0] == "f":
				array[1] = "Inversión"
				array[3] = "Fondo Solidaridad Arterrana"

			## donación
			elif (parts[2].strip())[0] == "d":
				array[1] = "Inversión"
				array[3] = "Donación"

			## Visita Participativa vivienda
			elif (parts[2].strip())[0] == "s":
				array[1] = "Gasto"
				array[3] = "Visitas participativas"

			## Bote Comedor
			elif (parts[2].strip())[0] == "b":
				array[1] = "Comedor"
				array[3] = "Botes"

			else:
				raise Exception('badly formatted string. First letter of first quantity element wrong:  {}'.format(parts))
			
			# read number in first quantity element
			numbers = re.findall(r"[-]?[\d]+[\.,']?\d*",(unidecode.unidecode(parts[2].strip())[1:len(parts[2].strip())]))
			if numbers:
				if float(numbers[0].replace(',','.').replace('\'','.')) > 0:
					array[8] = float(numbers[0].replace(',','.').replace('\'','.'))
				else: 
					array[9] = abs(float(numbers[0].replace(',','.').replace('\'','.')))
			else:
				raise Exception('badly formatted string:  {}'.format(parts))
			
			"""
			if (parts[2].strip())[1] == ":":
				numbers = re.findall(r"[-]?[\d]+[\.,']?\d*",(parts[2].strip())[2:len(parts[2].strip())])
				#print(numbers)
				if float(numbers[0].replace(',','.').replace('\'','.')) > 0:
					array[8] = float(numbers[0].replace(',','.').replace('\'','.'))
				else: 
					array[9] = abs(float(numbers[0].replace(',','.').replace('\'','.')))
			elif any((parts[2].strip())[1:4] in r for r in months):
				numbers = re.findall(r"[-]?[\d]+[\.,'']?\d*",(parts[2].strip())[4:len(parts[2].strip())])
				#print(numbers)
				if float(numbers[0].replace(',','.').replace('\'','.')) > 0:
					array[8] = float(numbers[0].replace(',','.').replace('\'','.'))
				else: 
					array[9] = abs(float(numbers[0].replace(',','.').replace('\'','.')))
			else: 
				raise Exception('badly formatted string:  {}'.format(parts))
			"""
			
			# allocate other quantity elements beyond parts[2]. Need to create another row for each
			# rule ab1.fuego.V:XXX.C:YYY.P:ZZZ.I:ZZZ.E:ZZZ.F:ZZZ
			# V stands for vivienda
			# C for comedor
			# P for proyecto
			# I for cuota integración
			# E for almuerzos
			# F for Fondo solidaridad
			# D for Donación
			# S for Visita Participativa vivienda
			# B for Bote Comedor
			if len(parts) > 3:
				for q, x in enumerate(parts[3::], start=0):
					# check if parts[3] and more contains valid formatted data, if not cancel parsing
					# if not starting with 'v', 'c' or 'p' and no ':' later -> discard it 
					if (((x.strip()[0] != "v") and (x.strip()[0] != "c") and (x.strip()[0] != "p") and (x.strip()[0] != "e") and (x.strip()[0] != "i") \
						and (x.strip()[0] != "f") and (x.strip()[0] != "d") and (x.strip()[0] != "s") and (x.strip()[0] != "b"))): # or (x.strip()[1] != ":")):
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
						elif "fanny" in row['Concepto'].casefold() or "ceramica" in row['Concepto'].casefold():
							extra_array[q][6] = "Taller cerámica"
							
					## comedor
					elif x.strip()[0] == "c":
						extra_array[q][1] = "Comedor"
						extra_array[q][3] = "Cuotas comedor"

					## almuerzos
					elif x.strip()[0] == "e":
						extra_array[q][1] = "Comedor"
						extra_array[q][3] = "Almuerzos"
					
					## cuota integración
					elif x.strip()[0] == "i":
						extra_array[q][1] = "Inversión"
						extra_array[q][3] = "Inversión entrada a integración"

					## fondo solidaridad
					elif x.strip()[0] == "f":
						extra_array[q][1] = "Inversión"
						extra_array[q][3] = "Fondo Solidaridad Arterrana"

					## donación
					elif x.strip()[0] == "d":
						extra_array[q][1] = "Inversión"
						extra_array[q][3] = "Donación"

					## Visita Participativa vivienda
					elif x.strip()[0] == "s":
						extra_array[q][1] = "Gasto"
						extra_array[q][3] = "Visitas participativas"

					## Bote Comedor
					elif x.strip()[0] == "b":
						extra_array[q][1] = "Comedor"
						extra_array[q][3] = "Botes"
					
					else:
						print('WARNING: badly formatted string. Skipping quantity element:  {}'.format(x))
						extra_array.remove(extra_array[q])
						continue
					
					# read number in other quantity element
					numbers = re.findall(r"[-]?[\d]+[\.,']?\d*",(unidecode.unidecode(x.strip())[1:len(x.strip())]))
					if numbers:
						if float(numbers[0].replace(',','.').replace('\'','.')) > 0:
							extra_array[q][8] = float(numbers[0].replace(',','.').replace('\'','.'))
						else: 
							extra_array[q][9] = abs(float(numbers[0].replace(',','.').replace('\'','.')))
					else:
						raise Exception('badly formatted string:  {}'.format(parts))

					"""
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
					"""

		except Exception as exception:
			print("***********************")
			logging.error(exception)
			print("***********************")


	# rule Encuentro Arterra XXXX
	# create three entries and split the money between:
	# integración: 60%
	# comedor: 25%
	# gasto: 15%

	# todo introducir nombre de encuentro en K de desglose, partir cantidad equitativamente

	if "encuentro arterra" in row['Concepto'].casefold():
		try:
			# print(row['Concepto'].casefold()[row['Concepto'].casefold().index("encuentro arterra")+len("encuentro arterra "):])
			array[1] = "Inversión"
			array[3] = "Centro de encuentros"
			array[10] = row['Concepto'].casefold()[row['Concepto'].casefold().index("encuentro arterra")+len("encuentro arterra "):]
			# add amount either to input or output
			if float(row['Importe'].replace(',','.')) > 0:
				array[8] = float(row['Importe'].replace(',','.'))*0.60
			else:
				array[9] = abs(float(row['Importe'].replace(',','.')))*0.60

			# create other two rows
			extra_array.append(array.copy())
			extra_array[0][1] = "Gasto"
			extra_array[0][3] = "Centro de encuentros"
			extra_array[0][10] = row['Concepto'].casefold()[row['Concepto'].casefold().index("encuentro arterra")+len("encuentro arterra "):]
			# add amount either to input or output
			if float(row['Importe'].replace(',','.')) > 0:
				extra_array[0][8] = float(row['Importe'].replace(',','.'))*0.15
			else:
				extra_array[0][9] = abs(float(row['Importe'].replace(',','.')))*0.15

			extra_array.append(array.copy())
			extra_array[1][1] = "Comedor"
			extra_array[1][3] = "Centro de encuentros"
			extra_array[1][10] = row['Concepto'].casefold()[row['Concepto'].casefold().index("encuentro arterra")+len("encuentro arterra "):]
			# add amount either to input or output
			if float(row['Importe'].replace(',','.')) > 0:
				extra_array[1][8] = float(row['Importe'].replace(',','.'))*0.25
			else:
				extra_array[1][9] = abs(float(row['Importe'].replace(',','.')))*0.25

		except Exception as exception:
			print("***********************")
			logging.error(exception)
			print("***********************")

	# rule fanny (Enero C/ Abajo 1,1o) and word alquiler or renta
	if "abajo 1, 1o" in row['Concepto'].casefold() or "abajo 1,1o" in row['Concepto'].casefold() or "renta" in row['Concepto'].casefold() or "mensualidad" in row['Concepto'].casefold():
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
	or "COMISION MANTENIM".casefold() in row['Concepto'].casefold() \
	or "INGRESO EN CORREOS".casefold() in row['Concepto'].casefold() \
	or "COMIS. INGRESO GIRO POSTAL CORREOS".casefold() in row['Concepto'].casefold()) :
	# and float(row['Importe'].replace(',','.')) <= 0:
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
		array[1] = "Gasto"
		array[3] = "Alquiler proyectos"
	elif "ecohabitar" in row['Concepto'].casefold():
		array[1] = "Gasto"
		array[3] = "Alquiler proyectos"
		array[4] = "Miracles"
		array[5] = "Miracles y Toni"
		array[6] = "Ecohabitar"
	elif "ana lucia" in row['Concepto'].casefold() and array[3] == "Alquiler proyectos":
		array[1] = "Gasto"
		array[3] = "Alquiler proyectos"
		array[6] = "Oficina Oeste"
	elif "biararte" in row['Concepto'].casefold() or "biar arte" in row['Concepto'].casefold():
		array[1] = "Gasto"
		array[3] = "Alquiler proyectos"
		array[6] = "Biar Arte"
	elif "baratzan" in row['Concepto'].casefold():
		array[1] = "Gasto"
		array[3] = "Alquiler proyectos"
		array[6] = "Baratzan Blai"
	# rule butano
	if "butano" in row['Concepto'].casefold() and array[4]=="" and array[5]=="" and array[6]=="":
		array[1] = "Gasto"
		array[3] = "Butano"
	# rule Iñigo
	if "inigo" in row['Concepto'].casefold():
		array[4] = "Iñigo"
		array[5] = "Iñigo"
	# rule Pepe Ecohabitar
	if "jose ignacio rojas rojas" in row['Concepto'].casefold():
		array[1] = "Comedor"
		array[3] = "Cuotas comedor"
		array[4] = "Pepe Ecohabitar"
	# rule seguro + impuesto circulación camión
	if "helvetia compania suiza" in row['Concepto'].casefold() and array[4]=="" and array[5]=="" and array[6]=="":
		array[1] = "Gasto"
		array[3] = "Camión"

	# rule seguro + impuesto circulación camión
	if "ayuntamiento del valle de eges" in row['Concepto'].casefold() and array[4]=="" and array[5]=="" and array[6]=="":
		array[1] = "Gasto"
		array[3] = "Camión"
	# rule Responsabilidad Civil
	if "mic responsabilidad civil" in row['Concepto'].casefold() and array[4]=="" and array[5]=="" and array[6]=="":
		array[1] = "Gasto"
		array[3] = "Seguro Responsabilidad Civil"
	
	# cuotas redes varias
	if "REAS NAVARRA CUOTA ANUAL REAS".casefold() in row['Concepto'].casefold():
		array[1] = "Gasto"
		array[3] = "Cuotas redes varias"

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
