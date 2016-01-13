#!/usr/bin/env python
import os

#Script per provar tots els arxius de la base de dades

f=open('exampleLooker.txt')
line='o'
while line!='':
	line=f.readline()
	os.system('./overAll.py '+line)
f.close()
