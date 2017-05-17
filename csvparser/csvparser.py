# execute with python 3!!
import csv
import sys

if len(sys.argv) != 3:
	print ("Incorrect number of arguments:\nThe correct usage is csvparser.py inputfile.csv outputfile.csv\noutputfile.csv will be created if it doesn't exist")
	exit()
if '.csv' in sys.argv[1]:
	reader = csv.reader(open(sys.argv[1]))
else:
	print ("Please enter a csv formatted file as input (with extension .csv)")
	exit()
if '.csv' in sys.argv[2]:
	writer = csv.writer(open(sys.argv[2], 'w+'))
else:
	print ("Please enter a csv formatted file as output (with extension .csv)\nIf it does not exist it will be created")
	exit()

for row in reader:
	for j,string in enumerate(row):
		string = string.replace("&aacute;", "á")
		string = string.replace("&agrave;", "à")
		string = string.replace("&Aacute;", "Á")
		string = string.replace("&Agrave;", "À")
		string = string.replace("&eacute;", "é")
		string = string.replace("&egrave;", "è")
		string = string.replace("&Eacute;", "É")
		string = string.replace("&Egrave;", "È")
		string = string.replace("&oacute;", "ó")
		string = string.replace("&ograve;", "ò")
		string = string.replace("&Oacute;", "Ó")
		string = string.replace("&Ograve;", "Ò")
		string = string.replace("&iacute;", "í")
		string = string.replace("&Iacute;", "Í")
		string = string.replace("&uacute;", "ú")
		string = string.replace("&Uacute;", "Ú")
		string = string.replace("&ccedil;", "ç")
		string = string.replace("&Ccedil;", "Ç")
		string = string.replace("&iuml;", "ï")
		string = string.replace("&Iuml;", "Ï")
		string = string.replace("&uuml;", "ü")
		string = string.replace("&Uuml;", "Ü")
		string = string.replace("&middot;", "·")
		string = string.replace("&ntilde;", "ñ")
		string = string.replace("&Ntilde;", "Ñ")
		string = string.replace("&iexcl;", "¡")
		string = string.replace("&ordf;", "ª")
		string = string.replace("&iquest;", "¿")
		string = string.replace("&ordm;", "º")
		string = string.replace("&euro;", "€")
		string = string.replace("&pound;", "£")
		string = string.replace("&laquo;", "«")
		string = string.replace("&raquo;", "»")
		string = string.replace("&bull;", "•")
		string = string.replace("&dagger;", "†")
		string = string.replace("&copy;", "©")
		string = string.replace("&reg;", "®")
		string = string.replace("&trade;", "™")
		string = string.replace("&deg;", "°")
		string = string.replace("&permil;", "‰")
		string = string.replace("&micro;", "µ")
		string = string.replace("&middot;", "·")
		string = string.replace("&ndash;", "–")
		string = string.replace("&mdash;", "—")
		string = string.replace("&#8470;", "№")
		row[j] = string
	writer.writerow(row)
print ('\nUTF-8 character replacing was successful')
