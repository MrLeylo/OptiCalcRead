#!/usr/bin/env python

import pytemplate as temp
import os

#Script per escriure el diccionari de la base de dades

symboldB,tagClassification,averages=temp.readTemplate()
if os.path.isfile('symbolDictionary.txt'):
	os.remove('symbolDictionary.txt')
dicti=open('symbolDictionary.txt','w')
for s in tagClassification:
	dicti.write(s+'\n')
dicti.close()
