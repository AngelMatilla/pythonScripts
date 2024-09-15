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
__version__ = "0.1.0"

# execute with python 3!!
import csv
import sys
import os
import unidecode
import re
import logging
from datetime import datetime
from pyexcel_ods3 import save_data
from colorama import Fore, Back, Style, init
from sys import stdout

print("Starting csvparser")

init()

if len(sys.argv) != 4:
	print (Style.RESET_ALL + Fore.RED + "Incorrect number of arguments:\nThe correct usage is csvparser.py inputfilebankentries.csv inputfilepeople.csv outputfile.ods\noutputfile.ods will be created if it doesn't exist")
	exit()
if '.csv' in sys.argv[1]:
	readerBankEntries = csv.DictReader(open(sys.argv[1]))
	linesBankEntries = [x for x in readerBankEntries]
else:
	print (Style.RESET_ALL + Fore.RED + "Please enter a csv formatted file as input for the bank entries (with extension .csv)")
	exit()
if '.csv' in sys.argv[2]:
	with open(sys.argv[2], newline='') as csvfilePeople:
		readerPeople = csv.reader(csvfilePeople, delimiter=',', quotechar='|')
		linesPeople = [y for y in readerPeople]
else:
	print (Style.RESET_ALL + Fore.RED + "Please enter a csv formatted file as input for the people (with extension .csv)")
	exit()
if '.ods' in sys.argv[3]:
	if os.path.exists(sys.argv[3]):
		os.remove(sys.argv[3])
	else:
		print(Style.RESET_ALL + Fore.BLUE + "The ods file does not exist and will be created")
else:
	print (Style.RESET_ALL + Fore.RED + "Please enter a ods formatted file as output (with extension .ods)\nIf it does not exist it will be created")
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

#print(fuegos_lower)
#print(personas_lower)

# detect whether it's Fiare or Triodos
print (Style.RESET_ALL + Fore.BLUE + "Detect bank")
if "Fecha Valor" in linesBankEntries[0]:
	bankType = "Fiare"
	fechaValor = 'Fecha Valor'
	concepto = 'Descripcion'
	print (Style.RESET_ALL + Fore.BLUE + "Fiare")
else:
	bankType = "Triodos"
	fechaValor = 'F. valor'
	concepto = 'Concepto'
	print (Style.RESET_ALL + Fore.BLUE + "Triodos")

# parse bank entries
data = [["Fecha", "Entidad", "Caja", "Método", "Círculo/Área", "Persona", "Fuego", "Proyecto", "Concepto", "Entrada", "Salida", "Notas"]]
for row in linesBankEntries[::-1]:
	if (bankType == "Triodos"):
		date = datetime.strptime(row[fechaValor],"%d/%m/%Y").date()
	else:
		date = datetime.strptime(row[fechaValor],"%Y-%m-%d").date()
		if "TRF." in row[concepto]:
			new_concept = row[concepto].replace("TRF.","transf de ")
			row[concepto] = new_concept
		elif "RCBO." in row[concepto]:
			new_concept = row[concepto].replace("RCBO.","recibo de ")
			row[concepto] = new_concept
	# generate array
	array = [date, "", "", "Banco", "", "", "", "", row[concepto], "","",""]
	extra_array = []
	# add amount either to input or output
	#first remove throusand dot separator, then replace comma decimal by dot
	if float(row['Importe'].replace('.','').replace(',','.')) > 0: 
		array[9] = float(row['Importe'].replace('.','').replace(',','.'))
	else:
		array[10] = abs(float(row['Importe'].replace('.','').replace(',','.')))

	# replace "()" by "." before parsing in concept
	if "()" in row[concepto]:
		new_concept = row[concepto].replace("()",".")
		row[concepto] = new_concept

	## specific replacements before the ab1 parsing 
	#remove S.L in Ecohabitar
	if "ECOHABITAR VISIONES SOSTENIBLES, S.L" in row[concepto]:
		new_concept = row[concepto].replace(", S.L","")
		row[concepto] = new_concept

	#include dots in Genny's concept
	# if "TRANSF DE GENNY CARRARO . AB1" in row[concepto]:
		#new_concept = row[concepto].replace("CARRARO . AB1","CARRARO AB1")
		#row[concepto] = new_concept
		#print(new_concept)

	#(include dots instead of spaces in AB1) and remove any dots before AB1
	row[concepto] = row[concepto].casefold()

	if "ab1" in row[concepto]:
		indx = row[concepto].index("ab1")
		#print(indx)
		new_concept = row[concepto][:indx].replace(".","") + row[concepto][indx:]#.replace(" ",".")
		#print(new_concept)
		row[concepto] = new_concept

	#include dots instead of spaces in AB1
	row[concepto] = row[concepto].casefold()
	#print(row[concepto])

	if "ab1 " in row[concepto]:
		indx = row[concepto].index("ab1")
		#print(indx)
		new_concept = row[concepto][:indx] + row[concepto][indx:].replace(" ",".")
		#print(new_concept)
		row[concepto] = new_concept
	
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
	# G for Grupo de Consumo
	if "ab1" in row[concepto].casefold():
		try:
			parts = row[concepto].casefold().split('.')
			#print(row[concepto].casefold())
			#print(parts)
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
				and (parts[2].strip()[0] != "b") and (parts[2].strip()[0] != "g")) ): # or (parts[2].strip()[1] != ":")):
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
					or ((x.strip())[0] == "b") or ((x.strip())[0] == "g")) or any((x.strip())[1:4] in r for r in months)): # and (((x.strip())[1] == ":")
						numbers = re.findall(r"[-]?[\d]+[,.']?\d*",unidecode.unidecode(x))
						for i in numbers:
							total_sum += float(i.replace(',','.').replace('\'','.'))
			if (total_sum != float(row['Importe'].replace(',','.').replace('\'','.'))):
				raise Exception('Total sum of quantity elements is not correctly calculated:  {}'.format(parts))

			# find fuego in list
			#print(parts[0])
			d = " "
			nameTemp = parts[0].replace('transf de ','').replace(' ab1','')
			#print(nameTemp)
			#name = d.join(nameTemp.split(d, 2)[:2]).replace(" ", "") #Returns nameTemp truncated at the 2nd occurrence of the delimiter d, without spaces
			name = nameTemp.replace(" ", "").replace("ñ","n") #this option works better if fuegos_lower and personas_lower has all surnames
			#print(name)
			if any(name in s for s in fuegos_lower):
				#print("match in fuegos")
				matching = [s for s in fuegos_lower if name in s]
				#print(matching)
				indexFuegos = fuegos_lower.index(matching[0])
				array[6] = fuegos[indexFuegos]
			else:
				array[6] = ""
				indexFuegos = -1
			
			# find person in list
			if any(name in s for s in personas_lower):
				#print("match in personas")
				matching = [s for s in personas_lower if name in s]
				#print(matching)
				indexPersonas = personas_lower.index(matching[0])
				array[5] = personas[indexPersonas]
				
			else:
				array[5] = ""
				indexPersonas = -1
			# allocate first quantity element {parts[2]}
			
			## vivienda
			if (parts[2].strip())[0] == "v" :
				array[2] = "Gasto"
				array[4] = "Cuotas vivienda"
			
			## proyecto
			elif (parts[2].strip())[0] == "p":
				array[2] = "Gasto"
				array[4] = "Cuotas proyectos"
				if "global ecovillage network of europe" in row[concepto].casefold() or "GLOBAL ECOV.NETW.EUROPE".casefold() in row[concepto].casefold():
					array[7] = "GEN"
				elif "ecohabitar" in row[concepto].casefold():
					array[7] = "Ecohabitar"
				elif "ana lucia" in row[concepto].casefold() or "maria eugenia" in row[concepto].casefold():
					array[7] = "Oficina Oeste"
				elif "biararte" in row[concepto].casefold() or "biar arte" in row[concepto].casefold():
					array[7] = "Biar Arte"
				elif "fanny" in row[concepto].casefold() or "ceramica" in row[concepto].casefold():
					array[7] = "Taller cerámica"
				elif "genny" in row[concepto].casefold():
					array[7] = "Oficina Genny"
			
			## comedor
			elif (parts[2].strip())[0] == "c":
				array[2] = "Comedor"
				array[4] = "Cuotas comedor"

			## almuerzos
			elif (parts[2].strip())[0] == "e":
				array[2] = "Comedor"
				array[4] = "Almuerzos"
			
			## cuota integración
			elif (parts[2].strip())[0] == "i":
				array[2] = "Inversión"
				array[4] = "Inversión entrada a integración"

			## fondo solidaridad
			elif (parts[2].strip())[0] == "f":
				array[2] = "Inversión"
				array[4] = "Fondo Solidaridad Arterrana"

			## donación
			elif (parts[2].strip())[0] == "d":
				array[2] = "Inversión"
				array[4] = "Donación"

			## Visita Participativa vivienda
			elif (parts[2].strip())[0] == "s":
				array[2] = "Gasto"
				array[4] = "Cuotas visitas participativas"

			## Bote Comedor
			elif (parts[2].strip())[0] == "b":
				array[2] = "Comedor"
				array[4] = "Botes"
			
			## Grupo de Consumo
			elif (parts[2].strip())[0] == "g":
				array[2] = "Comedor"
				array[4] = "Grupo de Consumo"

			else:
				raise Exception('badly formatted string. First letter of first quantity element wrong:  {}'.format(parts))
			
			# read number in first quantity element
			numbers = re.findall(r"[-]?[\d]+[\.,']?\d*",(unidecode.unidecode(parts[2].strip())[1:len(parts[2].strip())]))
			if numbers:
				if float(numbers[0].replace(',','.').replace('\'','.')) > 0:
					array[9] = float(numbers[0].replace(',','.').replace('\'','.'))
				else: 
					array[10] = abs(float(numbers[0].replace(',','.').replace('\'','.')))
			else:
				raise Exception('badly formatted string:  {}'.format(parts))
			
			"""
			if (parts[2].strip())[1] == ":":
				numbers = re.findall(r"[-]?[\d]+[\.,']?\d*",(parts[2].strip())[2:len(parts[2].strip())])
				#print(numbers)
				if float(numbers[0].replace(',','.').replace('\'','.')) > 0:
					array[9] = float(numbers[0].replace(',','.').replace('\'','.'))
				else: 
					array[10] = abs(float(numbers[0].replace(',','.').replace('\'','.')))
			elif any((parts[2].strip())[1:4] in r for r in months):
				numbers = re.findall(r"[-]?[\d]+[\.,'']?\d*",(parts[2].strip())[4:len(parts[2].strip())])
				#print(numbers)
				if float(numbers[0].replace(',','.').replace('\'','.')) > 0:
					array[9] = float(numbers[0].replace(',','.').replace('\'','.'))
				else: 
					array[10] = abs(float(numbers[0].replace(',','.').replace('\'','.')))
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
			# G for Grupo de Consumo
			if len(parts) > 3:
				for q, x in enumerate(parts[3::], start=0):
					# check if parts[3] and more contains valid formatted data, if not cancel parsing
					# if not starting with 'v', 'c' or 'p' and no ':' later -> discard it 
					if (((x.strip()[0] != "v") and (x.strip()[0] != "c") and (x.strip()[0] != "p") and (x.strip()[0] != "e") and (x.strip()[0] != "i") \
						and (x.strip()[0] != "f") and (x.strip()[0] != "d") and (x.strip()[0] != "s") and (x.strip()[0] != "b") and (x.strip()[0] != "g"))): # or (x.strip()[1] != ":")):
							print(Style.RESET_ALL + Fore.RED + '***Warning***: badly formatted string. Quantity element number {} not well formed:  {}'.format(q+3,parts))
							continue
					extra_array.append(array.copy())
					extra_array[q][9] = ""
					extra_array[q][10] = ""
					
					## vivienda
					if x.strip()[0] == "v":
						extra_array[q][2] = "Gasto"
						extra_array[q][4] = "Cuotas vivienda"
						extra_array[q][5] = ""
						if indexFuegos != -1:
							extra_array[q][6] = fuegos[indexFuegos]
					## proyecto
					elif x.strip()[0] == "p":
						extra_array[q][2] = "Gasto"
						extra_array[q][4] = "Cuotas proyectos"
						if "global ecovillage network of europe" in row[concepto].casefold() or "GLOBAL ECOV.NETW.EUROPE".casefold() in row[concepto].casefold():
							extra_array[q][7] = "GEN"
						elif "ecohabitar" in row[concepto].casefold():
							extra_array[q][7] = "Ecohabitar"
						elif "ana lucia" in row[concepto].casefold() or "maria eugenia" in row[concepto].casefold():
							extra_array[q][7] = "Oficina Oeste"
						elif "biararte" in row[concepto].casefold() or "biar arte" in row[concepto].casefold():
							extra_array[q][7] = "Biar Arte"
						elif "fanny" in row[concepto].casefold() or "ceramica" in row[concepto].casefold():
							extra_array[q][7] = "Taller cerámica"
						elif "genny" in row[concepto].casefold():
							extra_array[q][7] = "Oficina Genny"
						elif "nahia" in row[concepto].casefold():
							extra_array[q][7] = "CW Nahia"
							
					## comedor
					elif x.strip()[0] == "c":
						extra_array[q][2] = "Comedor"
						extra_array[q][4] = "Cuotas comedor"

					## almuerzos
					elif x.strip()[0] == "e":
						extra_array[q][2] = "Comedor"
						extra_array[q][4] = "Almuerzos"
					
					## cuota integración
					elif x.strip()[0] == "i":
						extra_array[q][2] = "Inversión"
						extra_array[q][4] = "Inversión entrada a integración"

					## fondo solidaridad
					elif x.strip()[0] == "f":
						extra_array[q][2] = "Inversión"
						extra_array[q][4] = "Fondo Solidaridad Arterrana"

					## donación
					elif x.strip()[0] == "d":
						extra_array[q][2] = "Inversión"
						extra_array[q][4] = "Donación"

					## Visita Participativa vivienda
					elif x.strip()[0] == "s":
						extra_array[q][2] = "Gasto"
						extra_array[q][4] = "Cuotas visitas participativas"

					## Bote Comedor
					elif x.strip()[0] == "b":
						extra_array[q][2] = "Comedor"
						extra_array[q][4] = "Botes"
					
					## Grupo de Consumo
					elif x.strip()[0] == "g":
						extra_array[q][2] = "Comedor"
						extra_array[q][4] = "Grupo de Consumo"
					
					else:
						print(Style.RESET_ALL + Fore.RED + 'WARNING: badly formatted string. Skipping quantity element:  {}'.format(x))
						extra_array.remove(extra_array[q])
						continue
					
					# read number in other quantity element
					numbers = re.findall(r"[-]?[\d]+[\.,']?\d*",(unidecode.unidecode(x.strip())[1:len(x.strip())]))
					if numbers:
						if float(numbers[0].replace(',','.').replace('\'','.')) > 0:
							extra_array[q][9] = float(numbers[0].replace(',','.').replace('\'','.'))
						else: 
							extra_array[q][10] = abs(float(numbers[0].replace(',','.').replace('\'','.')))
					else:
						raise Exception('badly formatted string:  {}'.format(parts))

					"""
					if (x.strip())[1] == ":":
						numbers = re.findall(r"[-]?[\d]+[\.,]?\d*",(x.strip())[2:len(x.strip())])
						#print(numbers)
						if float(numbers[0].replace(',','.')) > 0:
							extra_array[q][9] = float(numbers[0].replace(',','.'))
						else: 
							extra_array[q][10] = abs(float(numbers[0].replace(',','.')))
					elif any((x.strip())[1:4] in r for r in months):
						numbers = re.findall(r"[-]?[\d]+[\.,]?\d*",(x.strip())[4:len(x.strip())])
						#print(numbers)
						if float(numbers[0].replace(',','.')) > 0:
							extra_array[q][9] = float(numbers[0].replace(',','.'))
						else: 
							extra_array[q][10] = abs(float(numbers[0].replace(',','.')))
					else: 
						print('WARNING: badly formatted string. Skipping quantity element:  {}'.format(x))
						continue
					"""

		except Exception as exception:
			print(Style.RESET_ALL + Fore.RED + "***********************")
			logging.error(exception)
			print(Style.RESET_ALL + Fore.RED + "***********************")


	# rule Encuentro Arterra XXXX
	# create three entries and split the money between:
	# integración: 50%
	# comedor: 20%
	# gasto: 20%
	# Baratzan Blai 10%

	# todo introducir nombre de encuentro en K de desglose, partir cantidad equitativamente

	if "encuentro arterra" in row[concepto].casefold():
		try:
			# print(row[concepto].casefold()[row[concepto].casefold().index("encuentro arterra")+len("encuentro arterra "):])
			array[2] = "Inversión"
			array[4] = "Gestión y planificación de encuentros"
			array[11] = row[concepto].casefold()[row[concepto].casefold().index("encuentro arterra")+len("encuentro arterra "):]
			# add amount either to input or output
			if float(row['Importe'].replace(',','.')) > 0:
				array[9] = float(row['Importe'].replace(',','.'))*0.50
			else:
				array[10] = abs(float(row['Importe'].replace(',','.')))*0.50

			# create other three rows
			extra_array.append(array.copy())
			extra_array[0][2] = "Gasto"
			extra_array[0][4] = "Gestión y planificación de encuentros"
			extra_array[0][11] = row[concepto].casefold()[row[concepto].casefold().index("encuentro arterra")+len("encuentro arterra "):]
			# add amount either to input or output
			if float(row['Importe'].replace(',','.')) > 0:
				extra_array[0][9] = float(row['Importe'].replace(',','.'))*0.20
			else:
				extra_array[0][10] = abs(float(row['Importe'].replace(',','.')))*0.20

			extra_array.append(array.copy())
			extra_array[1][2] = "Comedor"
			extra_array[1][4] = "Gestión y planificación de encuentros"
			extra_array[1][11] = row[concepto].casefold()[row[concepto].casefold().index("encuentro arterra")+len("encuentro arterra "):]
			# add amount either to input or output
			if float(row['Importe'].replace(',','.')) > 0:
				extra_array[1][9] = float(row['Importe'].replace(',','.'))*0.20
			else:
				extra_array[1][10] = abs(float(row['Importe'].replace(',','.')))*0.20

			extra_array.append(array.copy())
			extra_array[2][2] = "Gasto"
			extra_array[2][4] = "Cuotas proyectos"
			extra_array[2][7] = "Baratzan Blai"
			extra_array[2][11] = row[concepto].casefold()[row[concepto].casefold().index("encuentro arterra")+len("encuentro arterra "):]
			# add amount either to input or output
			if float(row['Importe'].replace(',','.')) > 0:
				extra_array[2][9] = float(row['Importe'].replace(',','.'))*0.10
			else:
				extra_array[2][10] = abs(float(row['Importe'].replace(',','.')))*0.10

		except Exception as exception:
			print(Style.RESET_ALL + Fore.RED + "***********************")
			logging.error(exception)
			print(Style.RESET_ALL + Fore.RED + "***********************")

	# rule fanny (Enero C/ Abajo 1,1o) and word alquiler or renta
	if "abajo 1, 1o".casefold() in row[concepto].casefold() or "abajo 1,1o".casefold() in row[concepto].casefold() or "renta" in row[concepto].casefold() or "mensualidad" in row[concepto].casefold():
		array[2] = "Gasto"
		array[4] = "Cuotas vivienda"
		# find fuego in list
		parts = row[concepto].casefold().split('.')
		name = parts[0].replace('transf de ','').replace(' ab1','').replace(" ", "").replace("c/abajo1,1o", "") \
		.replace("enero", "").replace("febrero", "").replace("marzo", "").replace("abril", "").replace("mayo", "") \
		.replace("junio", "").replace("julio", "").replace("agosto", "").replace("septiembre", "") \
		.replace("octubre", "").replace("noviembre", "").replace("diciembre", "")
		#print(name)
		if any(name in s for s in fuegos_lower):
			matching = [s for s in fuegos_lower if name in s]
			array[6] = fuegos[fuegos_lower.index(matching[0])]
	# rule caldera
	if "huesillo" in row[concepto].casefold() and float(row['Importe'].replace(',','.')) < 0:
		array[2] = "Gasto"
		array[4] = "Huesillo"
	# rule banco
	if ("COMISION EMISION TRANSF".casefold() in row[concepto].casefold() \
	or "LIQUIDACION AHORRO".casefold() in row[concepto].casefold() \
	or "COMISION MANTENIM".casefold() in row[concepto].casefold() \
	or "INGRESO EN CORREOS".casefold() in row[concepto].casefold() \
	or "COMISION TARJETA".casefold() in row[concepto].casefold() \
	or "COMIS. INGRESO GIRO POSTAL CORREOS".casefold() in row[concepto].casefold()) :
	# and float(row['Importe'].replace(',','.')) <= 0:
		array[2] = "Gasto"
		array[4] = "Banco"
	# rule agua
	if "tasa de agua" in row[concepto].casefold() and float(row['Importe'].replace(',','.')) < 0:
		array[2] = "Gasto"
		array[4] = "Agua"
	# rule telefonia
	if ("telefonica de espana" in row[concepto].casefold() or "sisnet" in row[concepto].casefold()) and float(row['Importe'].replace(',','.')) < 0:
		array[2] = "Gasto"
		array[4] = "Internet y teléfono"
	# rule web
	if "strato" in row[concepto].casefold() and float(row['Importe'].replace(',','.')) < 0:
		array[2] = "Gasto"
		array[4] = "Web"
	# rule garbileku
	if "garbileku" in row[concepto].casefold() and float(row['Importe'].replace(',','.')) < 0:
		array[2] = "Gasto"
		array[4] = "Aterpe"
	# rule agroleku
	if "agroleku" in row[concepto].casefold() and float(row['Importe'].replace(',','.')) < 0:
		array[2] = "Gasto"
		array[4] = "Animales"
	# rule pedidos comedor
	if ("gumiel y mendia" in row[concepto].casefold() \
	 or "ecomatarranya" in row[concepto].casefold() \
	 or "pirineki" in row[concepto].casefold() \
	 or "quesos" in row[concepto].casefold() \
	 or "mandarinas" in row[concepto].casefold() \
	 or "naranjas" in row[concepto].casefold() \
	 or "laket" in row[concepto].casefold() \
	 or "zazpe sca" in row[concepto].casefold() \
	 or "azokoop" in row[concepto].casefold() \
	 or "citricos" in row[concepto].casefold()) \
		and float(row['Importe'].replace(',','.')) < 0:
		array[2] = "Comedor"
		array[4] = "Pedidos"
	# rule electricidad
	if "som energia" in row[concepto].casefold() and float(row['Importe'].replace(',','.')) < 0:
		array[2] = "Gasto"
		array[4] = "Electricidad término fijo"
		array[11] = "=(136,39+35,81+49,04+6,14)*1,21  pot contr + reactiva + impuesto + alquiler"
		# create additional line for variable term
		extra_array.append(array.copy())
		extra_array[0][4] = "Electricidad término variable"
		extra_array[0][11] = "=1227,32-J726"
	# rule pagos cuotas comedor
	if "comedor" in row[concepto].casefold() and not array[4]:
		array[2] = "Comedor"
		array[4] = "Cuotas comedor"
	# rule pagos alquiler arterra
	if "pedro enrique ramirez aragon" in row[concepto].casefold() or "geserlocal" in row[concepto].casefold():
		array[2] = "Gasto"
		array[4] = "Alquiler Arterra"
	# rule residuos Irati
	if "recibo mancomunidad r.s.u. irati" in row[concepto].casefold():
		array[2] = "Gasto"
		array[4] = "Residuos mancomunidad"
	# rule Contenedor
	# TODO: implement as part of ab1
	if "david.p" in row[concepto].casefold():
		array[2] = "Gasto"
		array[4] = "Cuotas proyectos"
		array[7] = "Contenedor de Ruido"
	# rule proyectos
	if "global ecovillage network of europe" in row[concepto].casefold() or "GLOBAL ECOV.NETW.EUROPE".casefold() in row[concepto].casefold():
		array[7] = "GEN"
		array[2] = "Gasto"
		array[4] = "Cuotas proyectos"
	elif "ecohabitar" in row[concepto].casefold():
		array[2] = "Gasto"
		array[4] = "Cuotas proyectos"
		array[5] = "Miracles"
		array[6] = "Miracles y Toni"
		array[7] = "Ecohabitar"
	elif "ana lucia" in row[concepto].casefold() and array[4] == "Cuotas proyectos":
		array[2] = "Gasto"
		array[4] = "Cuotas proyectos"
		array[7] = "Oficina Oeste"
	elif "MARIA EUGENIA CANADA ZORRILLA".casefold() in row[concepto].casefold() and array[4] == "Cuotas proyectos":
		array[2] = "Gasto"
		array[4] = "Cuotas proyectos"
		array[7] = "Oficina Oeste"
	elif "biararte" in row[concepto].casefold() or "biar arte" in row[concepto].casefold():
		array[2] = "Gasto"
		array[4] = "Cuotas proyectos"
		array[7] = "Biar Arte"
	elif "baratzan" in row[concepto].casefold():
		array[2] = "Gasto"
		array[4] = "Cuotas proyectos"
		array[7] = "Baratzan Blai"
	# rule butano
	if ("butano" in row[concepto].casefold() or "tafagas" in row[concepto].casefold()) and array[5]=="" and array[6]=="" and array[7]=="":
		array[2] = "Gasto"
		array[4] = "Butano"
	# rule Iñigo
	if "inigo" in row[concepto].casefold():
		array[5] = "Iñigo"
		array[6] = "Iñigo"
	# rule Pepe Ecohabitar
	if "jose ignacio rojas rojas" in row[concepto].casefold():
		array[2] = "Comedor"
		array[4] = "Cuotas comedor"
		array[5] = "Pepe Ecohabitar"
	# rule seguro + impuesto circulación camión
	if "helvetia compania suiza" in row[concepto].casefold() and array[5]=="" and array[6]=="" and array[7]=="":
		array[2] = "Gasto"
		array[4] = "Camión"

	# rule seguro + impuesto circulación camión
	if "ayuntamiento del valle de eges" in row[concepto].casefold() and array[5]=="" and array[6]=="" and array[7]=="":
		array[2] = "Gasto"
		array[4] = "Camión"
	# rule Responsabilidad Civil
	if ("mic responsabilidad civil" in row[concepto].casefold() or "om suscripcion" in row[concepto].casefold()) and array[5]=="" and array[6]=="" and array[7]=="":
		array[2] = "Gasto"
		array[4] = "Seguro Responsabilidad Civil"
	
	# rule reas
	if "REAS NAVARRA CUOTA ANUAL REAS".casefold() in row[concepto].casefold() and array[5]=="" and array[6]=="" and array[7]=="":
		array[2] = "Gasto"
		array[4] = "Cuotas redes varias"

	# rule el salto
	if "cuota el salto".casefold() in row[concepto].casefold() and array[5]=="" and array[6]=="" and array[7]=="":
		array[2] = "Gasto"
		array[4] = "Cuotas redes varias"
	
	# rule cooperativa cerealista
	if "cerealista".casefold() in row[concepto].casefold() and array[5]=="" and array[6]=="" and array[7]=="":
		array[2] = "Gasto"
		array[4] = "Animales"

	# rule hipoteca fiare
	if ("PReSTAMO0018633156" in row[concepto].casefold() or "PRÉSTAMO0018633156" in row[concepto].casefold()) and array[5]=="" and array[6]=="" and array[7]=="":
		array[2] = "Gasto"
		array[4] = "Devolución hipoteca"

	# rule devolucion prestamo carlos
	if "DEVOLUCION PRESTAMO CARLOS".casefold() in row[concepto].casefold() and array[5]=="" and array[6]=="" and array[7]=="":
		array[2] = "Inversión"
		array[4] = "Prestamos"

	# rule devolucion hipoteca
	if "PReSTAMO0018633156".casefold() in row[concepto].casefold() and array[5]=="" and array[6]=="" and array[7]=="":
		array[2] = "Inversión"
		array[4] = "Prestamos"
	
	# rule ESC pocket money, sending org and travel refund
	if "pocket money".casefold() in row[concepto].casefold() or "travel refund".casefold() in row[concepto].casefold() or "sending org".casefold() in row[concepto].casefold():
		array[2] = "PI"

	print(Style.RESET_ALL + Style.DIM, *array, sep = ";''")
	# for w in array:
		# print(w + Style.RESET_ALL)
	data.append(array)
	if len(extra_array) > 0:
		for idx, row in enumerate(extra_array):
			print(Style.RESET_ALL + Style.DIM , *extra_array[idx], sep = ";''")
			data.append(row)
	#reset extra array
	extra_array = []
dictionary.update({"Sheet 1": data})
save_data(sys.argv[3], dictionary)
print (Style.RESET_ALL + Style.DIM + '\nOds file has been generated.')
print("csvparser done")

