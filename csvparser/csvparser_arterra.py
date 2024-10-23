#!/usr/bin/env python
""" Csv Parser for Arterra Bizimodu Accounting.

The Csvparser reads the information out of the bank statements coming from Triodos for Arterra. 

Info on how to make a transfer:
https://git.gen-europe.org/angel/arterra-bizimodu/-/wikis/Pagos-por-transferencia-a-Arterra

Usage: 

Requires pyexcel_ods3 and unidecode libraries for py3

python3 ~/sources/python/csvparser/csvparser_arterra.py "/home/angel/Dropbox/Contabilidad_Arterra_2021/extractos_banco/05.mayo.csv" "/home/angel/Dropbox/Contabilidad_Arterra_2021/extractos_banco/configuration.csv" "/home/angel/Dropbox/Contabilidad_Arterra_2021/extractos_banco/additional-rules.json" "/home/angel/Dropbox/Contabilidad_Arterra_2021/extractos_banco/output.ods"

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
__version__ = "1.0.0"

# execute with python 3!!
import csv
import sys
import os
import unidecode
import re
import logging
import json
from datetime import datetime
from pyexcel_ods3 import save_data
from colorama import Fore, Back, Style, init
from sys import stdout

print("Starting csvparser")

init()

if len(sys.argv) != 5:
	print (Style.RESET_ALL + Fore.RED + "Incorrect number of arguments:\nThe correct usage is csvparser.py inputfilebankentries.csv configuration.csv additional-rules.json outputfile.ods\noutputfile.ods will be created if it doesn't exist")
	exit()
if '.csv' in sys.argv[1]:
	readerBankEntries = csv.DictReader(open(sys.argv[1]))
	linesBankEntries = [x for x in readerBankEntries]
else:
	print (Style.RESET_ALL + Fore.RED + "Please enter a csv formatted file as input for the bank entries (with extension .csv)")
	exit()
if '.csv' in sys.argv[2]:
	with open(sys.argv[2], newline='') as csvfileConfig:
		readerConfig = csv.reader(csvfileConfig, delimiter=',', quotechar='|')
		linesConfig = [y for y in readerConfig]
else:
	print (Style.RESET_ALL + Fore.RED + "Please enter a csv formatted file as input for the configuration (with extension .csv)")
	exit()
if '.json' in sys.argv[3]:
	with open(sys.argv[3], 'r') as jsonfileConfig:
		jsonData = json.load(jsonfileConfig)
else:
	print (Style.RESET_ALL + Fore.RED + "Please enter a csv formatted file as input for the configuration (with extension .csv)")
	exit()
if '.ods' in sys.argv[4]:
	if os.path.exists(sys.argv[4]):
		os.remove(sys.argv[4])
	else:
		print(Style.RESET_ALL + Fore.BLUE + "The ods file does not exist and will be created")
else:
	print (Style.RESET_ALL + Fore.RED + "Please enter a ods formatted file as output (with extension .ods)\nIf it does not exist it will be created")
	exit()

dictionary = dict()
months = ["ene" , "feb" , "mar", "abr", "may", "jun" , "jul" , "ago" , "sep" , "oct" , "nov" , "dic"]

# parse fuegos, people and projects
fuegosPretty = linesConfig[0]
fuegosPretty.pop(0) # remove initial name in first slot
fuegosCalc = linesConfig[1]
fuegosCalc.pop(0) # remove initial name in first slot
personasPretty = linesConfig[2]
personasPretty.pop(0) # remove initial name in first slot
personasCalc = linesConfig[3]
personasCalc.pop(0) # remove initial name in first slot
proyectosPretty = linesConfig[4]
proyectosPretty.pop(0) # remove initial name in first slot
proyectosCalc = linesConfig[5]
proyectosCalc.pop(0) # remove initial name in first slot

for index, s in enumerate(fuegosCalc):
	fuegosCalc[index] = unidecode.unidecode(s.casefold().replace(" ", ""))

for index, s in enumerate(personasCalc):
	personasCalc[index] = unidecode.unidecode(s.casefold().replace(" ", ""))

for index, s in enumerate(proyectosCalc):
	proyectosCalc[index] = unidecode.unidecode(s.casefold().replace(" ", ""))

#print(fuegosCalc)
#print(personasCalc)
#print(proyectosCalc)

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
#print("linesBankEntries")
#print(len(linesBankEntries))
for rowNumber, row in enumerate(linesBankEntries[::-1]):
	#print("row number")
	#print(rowNumber)
	
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
	
	accounting_array = [date, "", "", "Banco", "", "", "", "", row[concepto], "","",""]
	# add a new row in the accounting matrix
	if rowNumber == 0:
		accounting_matrix = []

	accounting_matrix.append(accounting_array)
	
	#print("accounting matrix")
	#print(accounting_matrix)
	#print("length accounting matrix")
	#print(len(accounting_matrix))
	
	# add amount either to input or output
	#first remove throusand dot separator, then replace comma decimal by dot
	if float(row['Importe'].replace('.','').replace(',','.')) > 0: 
		accounting_matrix[len(accounting_matrix)-1][9] = float(row['Importe'].replace('.','').replace(',','.'))
		#print(accounting_matrix[len(accounting_matrix)-1][9])
	else:
		accounting_matrix[len(accounting_matrix)-1][10] = abs(float(row['Importe'].replace('.','').replace(',','.')))
		#print(accounting_matrix[len(accounting_matrix)-1][10])

	## Case ab1 processing phase

	#print initial concepto
	#print("Initial concepto")
	#print(row[concepto])

	#concepto to lower case
	row[concepto] = row[concepto].casefold()

	#remove any dots before ab1 in concepto and get pre ab1 substring
	if "ab1" in row[concepto]:
		indx = row[concepto].index("ab1")
		#print(indx)
		pre_ab1_substring = row[concepto][:indx].replace(".","")
		new_concept = pre_ab1_substring + row[concepto][indx:]
		#print(new_concept)
		row[concepto] = new_concept
		pre_ab1_substring = pre_ab1_substring.rstrip()
	else: pre_ab1_substring = ""
	
	#print("pre ab1 substring")
	#print(pre_ab1_substring)

	# find fuego in pre ab1 substring

	nameTemp = pre_ab1_substring.replace('transf de ','').replace(" ", "").replace("ñ","n")
	#print("name temp")
	#print(nameTemp)
	
	matchingGranularity = 5
	isFuegoFound = False
	fuegosIndex = -1
	for index, s in enumerate(fuegosCalc):
		for i in range(len(nameTemp) - matchingGranularity):
			for j in range(len(s) - matchingGranularity):
				if nameTemp[i:i+6] == s[j:j+matchingGranularity+1]:
					isFuegoFound = True
					fuegosIndex = index

	if isFuegoFound == True:
		#print("match in fuegos")
		#print(fuegosPretty[fuegosIndex])
		accounting_matrix[len(accounting_matrix)-1][6] = fuegosPretty[fuegosIndex]
	else:
		accounting_matrix[len(accounting_matrix)-1][6] = ""

	# find persona in pre ab1 substring
	matchingGranularity = 5
	isPersonaFound = False
	personasIndex = -1
	for index, s in enumerate(personasCalc):
		for i in range(len(nameTemp) - matchingGranularity):
			for j in range(len(s) - matchingGranularity):
				if nameTemp[i:i+6] == s[j:j+matchingGranularity+1]:
					isPersonaFound = True
					personasIndex = index

	if isPersonaFound == True:
		#print("match in personas")
		#print(personasPretty[personasIndex])
		accounting_matrix[len(accounting_matrix)-1][5] = personasPretty[personasIndex]
	else:
		accounting_matrix[len(accounting_matrix)-1][5] = ""

	# find proyecto in pre ab1 substring
	matchingGranularity = 5
	isProyectoFound = False
	proyectosIndex = -1
	for index, s in enumerate(proyectosCalc):
		for i in range(len(nameTemp) - matchingGranularity):
			for j in range(len(s) - matchingGranularity):
				if nameTemp[i:i+6] == s[j:j+matchingGranularity+1]:
					isProyectoFound = True
					proyectosIndex = index

	if isProyectoFound == True:
		#print("match in proyectos")
		#print(proyectosPretty[proyectosIndex])
		accounting_matrix[len(accounting_matrix)-1][7] = proyectosPretty[proyectosIndex]
	else:
		accounting_matrix[len(accounting_matrix)-1][7] = ""

	# extract "ab1" substring using regular expresions
	ab1_substring_match = re.search(r"[aA][Bb]1(?:\(\))?\.*(\s*)[^0-9^.^\(\)]*((?:\(\))?\.*(\s*)[vVcCpPeEiIfFdDsSbBgG]:?(-?\d+(?:\,\d+)?))+",row[concepto])
	#print(row[concepto])
	if ab1_substring_match:
		ab1_substring = ab1_substring_match.group(0)
	else: ab1_substring = ""
	
	#print("ab1 substring")
	#print(ab1_substring)

	#find post ab1 substring
	index = row[concepto].find(ab1_substring)
	if index != -1:
		post_ab1_substring = row[concepto][index + len(ab1_substring):]
		post_ab1_substring = post_ab1_substring.lstrip()
	else: post_ab1_substring = ""
	
	#print("post ab1 substring")
	#print(post_ab1_substring)

	# replace " " or "()" by "." and ":" by "" before parsing ab1 substring
	if "()" or " " in ab1_substring:
		ab1_substring_processed = ab1_substring.replace("()",".").replace(" ",".").replace(":","")
		ab1_substring = ab1_substring_processed
		#print("ab1 substring partially processed")
		#print(ab1_substring_processed)
	ab1_substring_processed_match = re.search(r"[aA][Bb]1(?:\(\))?\.*(\s*)[^0-9^.^\(\)]*\.*",ab1_substring)
	if ab1_substring_processed_match:
		ab1_substring_to_remove = ab1_substring_processed_match.group(0)
	else: ab1_substring_to_remove = ""
	index = ab1_substring.find(ab1_substring_to_remove)
	if index != -1:
		ab1_substring_processed = ab1_substring[index + len(ab1_substring_to_remove):]
		ab1_substring_processed = ab1_substring_processed.lstrip()
	else: ab1_substring_processed = ""
	
	#print("ab1 substring processed")
	#print(ab1_substring_processed)

	# split segments in matrix
	parts = ab1_substring_processed.split('.')
	#print("parts")
	#print(parts)
	ab1_substring_processed_matrix = []
	if parts != ['']:
		for x in parts:
			#print(x[1:])
			letter = x[0]
			number = float(x[1:].replace(",","."))
			ab1_substring_processed_matrix.append((letter, number))
	
	#print("ab1 substring processed matrix")
	#print(ab1_substring_processed_matrix)

	# Loop through ab1 substring processed matrix and create necessary accounting entries
	total_sum = 0
	if ab1_substring_processed_matrix != []:
		# check if sum of quantity elements is correct and throw and exception if not
		for x in ab1_substring_processed_matrix:
			total_sum += x[1]
		#print("total sum")
		#print(total_sum)
		#print("importe")
		#print(float(row['Importe'].replace(',','.').replace('\'','.')))
		if (total_sum != float(row['Importe'].replace(',','.').replace('\'','.'))):
				raise Exception('Total sum of quantity elements is not correctly calculated:  {}'.format(row[concepto]))

		# rule ab1.fuego.V:XXX.C:YYY.P:ZZZ.I:ZZZ.E:ZZZ.F:ZZZ.D:ZZZ.S:ZZZ.B:ZZZ.G:ZZZ
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
		
		#print("loop through ab1 substring processed matrix elements")
		initialIndex = len(accounting_matrix)-1
		index = initialIndex
		for letter, value in ab1_substring_processed_matrix:
			if index > initialIndex:
				#print("accounting_matrix initial index")
				#print(initialIndex)
				#print(accounting_matrix[initialIndex])
				new_accounting_element = accounting_matrix[len(accounting_matrix)-1].copy()  # Create a copy of the last element
				accounting_matrix.append(new_accounting_element)
				#print("accounting_matrix current index")
				#print(len(accounting_matrix)-1)
				#print(accounting_matrix[len(accounting_matrix)-1])
			
			if letter == "v" : #vivienda
				accounting_matrix[index][2] = "Gasto"
				accounting_matrix[index][4] = "Cuotas vivienda"
			elif letter == "c" : #comedor
				accounting_matrix[index][2] = "Comedor"
				accounting_matrix[index][4] = "Cuotas comedor"
			elif letter == "p" : #proyectos
				accounting_matrix[index][2] = "Gasto"
				accounting_matrix[index][4] = "Cuotas proyectos"
			elif letter == "i": #cuota integración
				accounting_matrix[index][2] = "Inversión"
				accounting_matrix[index][4] = "Inversión entrada a integración"
			elif letter == "e" : #almuerzos
				accounting_matrix[index][2] = "Comedor"
				accounting_matrix[index][4] = "Almuerzos"
			elif letter == "f": #Fondo solidaridad 
				accounting_matrix[index][2] = "Inversión"
				accounting_matrix[index][4] = "Fondo Solidaridad Arterrana"
			elif letter == "d": #donación
				accounting_matrix[index][2] = "Inversión"
				accounting_matrix[index][4] = "Donación"
			elif letter == "s": #Visita Participativa vivienda
				accounting_matrix[index][2] = "Gasto"
				accounting_matrix[index][4] = "Cuotas visitas participativas"
			elif letter == "b": #Bote Comedor
				accounting_matrix[index][2] = "Comedor"
				accounting_matrix[index][4] = "Botes"
			elif letter == "g": #Grupo de Consumo
				accounting_matrix[index][2] = "Comedor"
				accounting_matrix[index][4] = "Grupo de Consumo"
			
			#add the value to the corresponding column
			if value > 0:
				accounting_matrix[index][9] = value
			else:
				accounting_matrix[index][10] = value
			#print("index and row")
			#print(index)
			#print(accounting_matrix[index])
			index += 1
	#print("accounting matrix after ab1 loop")
	#print(accounting_matrix)

	# rule Encuentro Arterra XXXX
	# create three entries and split the money between:
	# integración: 50%
	# comedor: 20%
	# gasto: 20%
	# Baratzan Blai 10%

	if "encuentro arterra" in row[concepto].casefold():
		try:
			#print("Caso Encuentro")
			rowsNumberEncuentros = 4		
			encuentroPercentages = [0.50,0.20,0.20,0.10]
			encuentroCajas = ['Inversión','Gasto','Comedor','Gasto']
			for index in range(rowsNumberEncuentros):
				#print(index)
				if index > 0:
					new_accounting_element = accounting_matrix[len(accounting_matrix)-1].copy()  # Create a copy of the last element
					accounting_matrix.append(new_accounting_element)
				# print(row[concepto].casefold()[row[concepto].casefold().index("encuentro arterra")+len("encuentro arterra "):])
				accounting_matrix[len(accounting_matrix)-1][2] = encuentroCajas[index]
				accounting_matrix[len(accounting_matrix)-1][4] = "Gestión y planificación de encuentros"
				if index == 3: accounting_matrix[len(accounting_matrix)-1][7] = "Baratzan Blai"
				accounting_matrix[len(accounting_matrix)-1][11] = row[concepto].casefold()[row[concepto].casefold().index("encuentro arterra")+len("encuentro arterra "):]
				# add amount either to input or output
				if float(row['Importe'].replace(',','.')) > 0:
					accounting_matrix[len(accounting_matrix)-1][9] = float(row['Importe'].replace(',','.'))*encuentroPercentages[index]
				else:
					accounting_matrix[len(accounting_matrix)-1][10] = abs(float(row['Importe'].replace(',','.')))*encuentroPercentages[index]

		except Exception as exception:
			print(Style.RESET_ALL + Fore.RED + "***********************")
			logging.error(exception)
			print(Style.RESET_ALL + Fore.RED + "***********************")

	## Additional rules. Processing json config file
	#print("Process json config file")
	additionalRules = jsonData['additionalRules']['rules']
	for rule in additionalRules:
		if_statement = "if "
		condition_was_true = False
		for condition in rule['conditions']:
			if condition['group'] == "begin":
				if_statement += "("
			if condition['isItSpecial'] == "yes":
				if condition['text'] == "negative": #el importe debe ser negativo
					conditionText = "float(row['Importe'].replace(',','.')) < 0"
				elif condition['text'] == "noCircle": #el campo de circulo está vacío
					conditionText = "accounting_matrix[len(accounting_matrix)-1][4]==''"
				elif condition['text'] == "noPerson": #el campo de persona está vacío
					conditionText = "accounting_matrix[len(accounting_matrix)-1][5]==''"
				elif condition['text'] == "noFire": #el campo de fuego está vacío
					conditionText = "accounting_matrix[len(accounting_matrix)-1][6]==''"
				elif condition['text'] == "noProject": #el campo de proyecto está vacío
					conditionText = "accounting_matrix[len(accounting_matrix)-1][7]==''"
				else: 
					conditionText = "'"+str(condition['text'].casefold())+' in '+str(row[concepto].casefold())+"'"
			else:
				conditionText = "'"+str(condition['text'].casefold())+"' in '"+str(row[concepto].casefold())+"'"
			if_statement += f"{conditionText} "
			if condition['group'] == "end":
				if_statement += ")"
			if_statement += f"{condition['operator']} "
		#print("if statement")
		#print(if_statement)
		if if_statement[len(if_statement)-2] == "r": if_statement = if_statement[:-3]  # Remove the last " or "
		elif if_statement[len(if_statement)-2] == "d": if_statement = if_statement[:-4]  # Remove the last " and "
		elif if_statement[len(if_statement)-3] == "r": if_statement = if_statement[:-4] + if_statement[-1]  # Remove the last " or " keeping the ")"
		elif if_statement[len(if_statement)-3] == "d": if_statement = if_statement[:-5] + if_statement[-1]  # Remove the last " and " keeping the ")"
		if_statement += """:
        condition_was_true = True"""
		# Execute the if statement using `exec`
		#print("truncated if statement")
		#print(if_statement)
		exec(if_statement)
		# Code to execute if any condition is true
		if condition_was_true:
			print("The set of conditions is true.")
			counter = 0
			for output in rule['outputs']:
				if counter > 0:
					new_accounting_element = accounting_matrix[len(accounting_matrix)-1].copy()  # Create a copy of the last element
					accounting_matrix.append(new_accounting_element)
				print(output)
				if output['caja'] != "":  accounting_matrix[len(accounting_matrix)-1][2] = output['caja']
				if output['circulo'] != "":  accounting_matrix[len(accounting_matrix)-1][4] = output['circulo']
				if output['notas'] != "":  accounting_matrix[len(accounting_matrix)-1][11] = output['notas']
				counter += 1
				print(accounting_matrix[len(accounting_matrix)-1])

	#print(Style.RESET_ALL + Style.DIM, *accounting_matrix[len(accounting_matrix)-1], sep = ";''")
	#print("end of loop")
	#print(accounting_matrix[len(accounting_matrix)-1])
	
# add accounting matrix elements into a list
#print("add accounting matrix elements into a list")
#print(accounting_matrix)
for idx, row in enumerate(accounting_matrix):
	print(Style.RESET_ALL + Style.DIM , *accounting_matrix[idx], sep = ";''")
	#print(idx)
	#print(row)
	data.append(row)

dictionary.update({"Sheet 1": data})
save_data(sys.argv[4], dictionary)
print (Style.RESET_ALL + Style.DIM + '\nOds file has been generated.')
print("csvparser done")

