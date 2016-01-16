#!/usr/bin/env python
from os import listdir as ls
import os

#Script per escriure en un fitxer al sistema tots els fitxers de la ubicacio de la base de dades especificada

locationList=['/home/leylo/OptiCalcRead/python/testData/CROHME_test','/home/leylo/OptiCalcRead/python/testData/testData']
if os.path.isfile('exampleLooker.txt'):
	os.remove('exampleLooker.txt')
lookFile=open('exampleLooker.txt','w')
for destiny in locationList:
	filesInkML=ls(destiny)
	for filenom in filesInkML:
		if '.inkml' in filenom:
			lookFile.write(destiny+'/'+filenom+'\n')
lookFile.close()
