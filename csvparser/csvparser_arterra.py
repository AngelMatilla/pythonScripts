#!/usr/bin/env python
""" Csv Parser for Arterra Bizimodu Accounting.

The Csvparser reads the information out of the bank statements coming from Triodos for Arterra. 

Info on how to make a transfer:
https://git.gen-europe.org/angel/arterra-bizimodu/-/wikis/Pagos-por-transferencia-a-Arterra

Usage: 

Requires pyexcel_ods3 and unidecode libraries for py3

python3 ~/sources/python/csvparser/csvparser_arterra.py "/home/angel/Dropbox/Contabilidad_Arterra_2021/extractos_banco/05.mayo.csv" "/home/angel/Dropbox/Contabilidad_Arterra_2021/extractos_banco/people.csv" "/home/angel/Dropbox/Contabilidad_Arterra_2021/extractos_banco/output.ods"

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program. If not, see <http://www.gnu.org/licenses/>.
"""

__author__ = "Angel Matilla"
__contact__ = "angelmatilla@gmail.com"
__version__ = "0.0.1"

# execute with python 3!!
import csv
import sys
import os
import unidecode
import re
import logging
from datetime import datetime
from pyexcel_ods3 import save_data

if len(sys.argv) != 4:
	print ("Incorrect number of arguments:\nThe correct usage is csvparser.py inputfilebankentries.csv inputfilepeople.csv outputfile.ods\noutputfile.ods will be created if it doesn't exist")
	exit()
if '.csv' in sys.argv[1]:
	readerBankEntries = csv.DictReader(open(sys.argv[1]))
	linesBankEntries = [x for x in readerBankEntries]
else:
	print ("Please enter a csv formatted file as input for the bank entries (with extension .csv)")
	exit()
if '.csv' in sys.argv[2]:
	with open(sys.argv[2], newline='') as csvfilePeople:
		readerPeople = csv.reader(csvfilePeople, delimiter=',', quotechar='|')
		linesPeople = [y for y in readerPeople]
else:
	print ("Please enter a csv formatted file as input for the people (with extension .csv)")
	exit()
if '.ods' in sys.argv[3]:
	if os.path.exists(sys.argv[3]):
		os.remove(sys.argv[3])
	else:
		print("The ods file does not exist and will be created")
else:
	print ("Please enter a ods formatted file as output (with extension .ods)\nIf it does not exist it will be created")
	exit()

dictionary = dict()
months = ["ene" , "feb" , "mar", "abr", "may", "jun" , "jul" , "ago" , "sep" , "oct" , "nov" , "dic"]

# parse people
fuegos = linesPeople[0]
fuegos.pop(0) # remove initial name in first slot
fuegos_lower = linesPeople[1]
fuegos_lower.pop(0) # remove initial name in first slot
personas = linesPeople[2]
personas.pop(0) # remove initial name in first slot
personas_lower = linesPeople[3]
personas_lower.pop(0) # remove initial name in first slot

for index, s in enumerate(fuegos_lower):
	fuegos_lower[index] = unidecode.unidecode(s.casefold().replace(" ", ""))

for index, s in enumerate(personas_lower):
	personas_lower[index] = unidecode.unidecode(s.casefold().replace(" ", ""))

# parse bank entries
data = [["Fecha", "Caja", "Método", "Círculo/Área", "Persona", "Fuego", "Proyecto", "Concepto", "Entrada", "Salida", "Notas"]]
for row in linesBankEntries[::-1]:
	date = datetime.strptime(row['F. valor'],"%d/%m/%Y").date()
	# generate array
	array = [date, "", "Banco", "", "", "", "", row['Concepto'], "","",""]
	extra_array = []
	# add amount either to input or output
	#first remove throusand dot separator, then replace comma decimal by dot
	if float(row['Importe'].replace('.','').replace(',','.')) > 0: 
		array[8] = float(row['Importe'].replace('.','').replace(',','.'))
	else:
		array[9] = abs(float(row['Importe'].replace('.','').replace(',','.')))

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
			name = parts[0].replace('transf de ','').replace(' ab1','').replace(" ", "")
			#print(name)
			if any(name in s for s in fuegos_lower):
				#print("match in fuegos")
				matching = [s for s in fuegos_lower if name in s]
				#print(matching)
				indexFuegos = fuegos_lower.index(matching[0])
				array[5] = fuegos[indexFuegos]
			else:
				array[5] = ""
				indexFuegos = -1
			
			# find person in list
			if any(name in s for s in personas_lower):
				#print("match in personas")
				matching = [s for s in personas_lower if name in s]
				#print(matching)
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
				elif "ana lucia" in row['Concepto'].casefold() or "maria eugenia canada zorrilla" in row['Concepto'].casefold():
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
						elif "ana lucia" in row['Concepto'].casefold() or "maria eugenia canada zorrilla" in row['Concepto'].casefold():
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
	if "abajo 1, 1o".casefold() in row['Concepto'].casefold() or "abajo 1,1o".casefold() in row['Concepto'].casefold() or "renta" in row['Concepto'].casefold() or "mensualidad" in row['Concepto'].casefold():
		array[1] = "Gasto"
		array[3] = "Alquiler vivienda"
		# find fuego in list
		parts = row['Concepto'].casefold().split('.')
		name = parts[0].replace('transf de ','').replace(' ab1','').replace(" ", "").replace("c/abajo1,1o", "") \
		.replace("enero", "").replace("febrero", "").replace("marzo", "").replace("abril", "").replace("mayo", "") \
		.replace("junio", "").replace("julio", "").replace("agosto", "").replace("septiembre", "") \
		.replace("octubre", "").replace("noviembre", "").replace("diciembre", "")
		#print(name)
		if any(name in s for s in fuegos_lower):
			matching = [s for s in fuegos_lower if name in s]
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
	or "COMISION TARJETA".casefold() in row['Concepto'].casefold() \
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
		array[10] = "=(136,39+35,81+49,04+6,14)*1,21  pot contr + reactiva + impuesto + alquiler"
		# create additional line for variable term
		extra_array.append(array.copy())
		extra_array[0][3] = "Electricidad término variable"
		extra_array[0][10] = "=1227,32-J726"
	# rule pagos cuotas comedor
	if "comedor" in row['Concepto'].casefold() and not array[3]:
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
	elif "MARIA EUGENIA CANADA ZORRILLA".casefold() in row['Concepto'].casefold() and array[3] == "Alquiler proyectos":
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
	if ("butano" in row['Concepto'].casefold() or "tafagas" in row['Concepto'].casefold()) and array[4]=="" and array[5]=="" and array[6]=="":
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
save_data(sys.argv[3], dictionary)
print ('\nOds file has been generated.')
