#!/usr/bin/python

import sys

if len(sys.argv) != 3:
	print ("Incorrect number of arguments.\nThe correct usage is csvparser.py inputfile.csv outputfile.csv")
	exit()

print ('Number of arguments:', len(sys.argv), 'arguments.')
print ('Argument List:', str(sys.argv))
print ('Argument 0:', sys.argv[0])
print ('Argument 1:', sys.argv[1])
print ('Argument 2:', sys.argv[2])
