from os import listdir as ls
import takeDS as tds
from pprint import pprint
import matplotlib.pyplot as plt
import ink2Traces
import symbolPreprocessing as spp
import ownSegGenerator as sg
import os
import shutil

def readUNIPENdB(location):
	weHave=ls(location)
	if 'data' in weHave:
		sdB=[]
		tagClassification={}
		folders=ls(location+'/data')
		for curFolder in folders:
			altFol=ls(location+'/data/'+curFolder)
			for curAltFold in altFol:
				if curAltFold=='aga':
					dataFiles=ls(location+'/data/'+curFolder+'/'+curAltFold)
					for curFile in dataFiles:
						fullPath=location+'/data/'+curFolder+'/'+curAltFold+'/'+curFile
						print fullPath+':'
						sdB=sdB+tds.mountDS(fullPath,'UNIPEN')
		for symbol in sdB:
			symbol.draw()
		psdB=spp.preprocessing(sdB)
		for symbol in psdB:
			symbol.computeFeatures()
			if symbol.tag not in tagClassification:
				tagClassification[symbol.tag]=[]
			tagClassification[symbol.tag].append(symbol)
		print type(tagClassification)
	return psdB,tagClassification

#ReadCROHMEdB: Llegeix la base de dades de text i la torna en forma de variables, on locationList es un string amb la ruta a la base de dades
		
def readCROHMEdB(locationList):
	#Fa una llista amb els arxius a extreure la base de dades i ho ordena al sistema
	sdB=[]
	tagClassification={}
	os.remove('toTrain.txt')
	trainListFile=open('toTrain.txt','w')
	for destiny in locationList:
		filesInkML=ls(destiny)
		for filenom in filesInkML:
			if '.inkml' in filenom:
				trainListFile.write(destiny+'/'+filenom+'\n')
	trainListFile.close()
	trainListFile=open('toTrain.txt','r')
	linea='o'
	lcont=0
	while linea!='':
		lcont+=1
		linea=trainListFile.readline()
		if linea!='':
			if os.path.exists('segmentedData/'+'Folder000'+str(lcont)):
				shutil.rmtree('segmentedData/'+'Folder000'+str(lcont))
			os.makedirs('segmentedData/'+'Folder000'+str(lcont))
			sg.main(['GO',linea,'segmentedData/'+'Folder000'+str(lcont)+'/trainFile'])
	#Escaneja els arxius de la base de dades i guarda les coordenades
	for cases in os.listdir('segmentedData'):
		filesHere=sorted(os.listdir('segmentedData/'+cases))
		filesHere.remove('trainFile_GT.txt')
		filesHere=['trainFile'+str(sorted([int(filesHere[i].strip('trainFile').strip('.inkml')) for i in range(len(filesHere))])[j])+'.inkml' for j in range(len(filesHere))]
		Gfile=open('segmentedData/'+cases+'/trainFile_GT.txt')
		linea='o'
		filco=0
		while linea!='':
			linea=Gfile.readline()
			if linea!='':
				whereInd=linea.index(',')
				etiq=linea[whereInd+1:].rstrip('\n')
				sdB.append(ink2Traces.i2trained('segmentedData/'+cases+'/'+filesHere[filco],etiq))
				filco+=1
	#Preprocessa i troba els atributs dels simbols de la base de dades
	for symbol in sdB:
		symbol.draw()
	psdB=spp.preprocessing(sdB)
	for symbol in psdB:
		symbol.computeFeatures()
		if symbol.tag not in tagClassification:
			tagClassification[symbol.tag]=[]
		tagClassification[symbol.tag].append(symbol)
	return psdB,tagClassification
