import fulldataBase as dB
import symbolPreprocessing as spp
import numpy as np
import matplotlib.pyplot as plt
import os
import pickle
import SClass as nsi

#TemplateGenerator: Guarda al sistema el conjunt de simbols extret de la base de dades i el template que es genera

def templateGenerator():
	symboldB,tagClassification=dB.readCROHMEdB(['trainData/CROHME_training','trainData/trainData_v2','trainData/TrainINKML'])
	option=3
	counta=0
	tagAverages={}
	#Opcio 1: S'adapten els simbols de la base de dades amb el minim nombre de traces trobat
	if option==1:
		for character in tagClassification:
			counta+=1
			print character,':',len(tagClassification[character])
			numStrokes=[len(tagClassification[character][i].tE) for i in range(len(tagClassification[character]))]
			nStrokesTemp=min(numStrokes)
			tagClassification[character]=spp.strokeReduction(tagClassification[character],nStrokesTemp,True)
			eachStroke=np.asarray([int(sum([tagClassification[character][i].tE[j] for i in range(len(tagClassification[character]))])/len(tagClassification[character])) for j in range(nStrokesTemp)])
			tagClassification[character]=spp.altArcLengthResampling(tagClassification[character],eachStroke)
			average=np.zeros([len(tagClassification[character][0].Coord),2],np.float64)
			for example in tagClassification[character]:
				average=np.array([[(average[i,0]+example.Coord[i,0]),(average[i,1]+example.Coord[i,1])] for i in range(example.Coord.shape[0])],np.float64)
			average=np.array([[average[i,0]/len(tagClassification[character]),average[i,1]/len(tagClassification[character])] for i in range(example.Coord.shape[0])],np.float64)
			tagAverages[character]=average
			plt.figure(counta)
			for j in range(nStrokesTemp):
				if j==0:
					ini=-1
				else:
					ini=int(eachStroke[j-1])
				plt.plot(average[range(ini+1,int(eachStroke[j])+1),0],-average[range(ini+1,int(eachStroke[j])+1),1],'r')
	#Opcio 2: S'adapten els simbols de la base de dades amb el maxim nombre de traces trobat
	elif option==2:
		for character in tagClassification:
			counta+=1
			print character,':',len(tagClassification[character])
			numStrokes=[len(tagClassification[character][i].tE) for i in range(len(tagClassification[character]))]
			nStrokesTemp=int(round(sum(numStrokes)/float(len(numStrokes))))
			tagClassification[character]=spp.strokeReduction(tagClassification[character],nStrokesTemp,True)
			eachStroke=np.asarray([int(sum([tagClassification[character][i].tE[j] for i in range(len(tagClassification[character]))])/len(tagClassification[character])) for j in range(nStrokesTemp)])
			tagClassification[character]=spp.altArcLengthResampling(tagClassification[character],eachStroke)
			average=np.zeros([len(tagClassification[character][0].Coord),2],np.float64)
			for example in tagClassification[character]:
				average=np.array([[(average[i,0]+example.Coord[i,0]),(average[i,1]+example.Coord[i,1])] for i in range(example.Coord.shape[0])],np.float64)
			average=np.array([[average[i,0]/len(tagClassification[character]),average[i,1]/len(tagClassification[character])] for i in range(example.Coord.shape[0])],np.float64)
			tagAverages[character]=average
	#Opcio 3: Es separen els simbols segons el seu numero de traces
	elif option==3:
		charList=[character for character in tagClassification]
		for charInd in range(len(charList)):
			numStrokes=[len(tagClassification[charList[charInd]][i].tE) for i in range(len(tagClassification[charList[charInd]]))]
			c=0
			typesByN=[]
			for n in numStrokes:
				if n not in typesByN:
					typesByN.append(n)
					tagClassification[charList[charInd]+str(n)]=[]
				tagClassification[charList[charInd]+str(n)].append(tagClassification[charList[charInd]][c])
				c+=1
			del tagClassification[charList[charInd]]
		print tagClassification['-1'][0].LP
		#Soroll de la dB
		del tagClassification['\exists2'][1]
		del tagClassification['\pi2']
		del tagClassification['\\'+'forall3']
		del tagClassification['Y2']
		del tagClassification['x2']
		del tagClassification['Y3']
		tagClassification['k1']=[tagClassification['k1'][valid] for valid in [0,1,2,3,8,12,20,24,29,30,34,35,42,43,58,59,61]]
		tagClassification['\sum2']=[tagClassification['\sum2'][valid] for valid in [1,5,13,18,24,25,28,32,35,37,38,45,61]]
		tagClassification[']2']=[tagClassification[']2'][valid] for valid in [3,4]]
		tagClassification['[2']=[tagClassification['[2'][valid] for valid in [0,8]]
		tagClassification['\\'+'theta2']=[tagClassification['\\'+'theta2'][valid] for valid in [1,2,5,7,9,12,13,28,29,31,32,34,37,39,40,41,52,61,65,66,67,69]]
		tagClassification['\div3']=[tagClassification['\div3'][valid] for valid in [10,24,38]]
		tagClassification['\\'+'tan3']=[tagClassification['\\'+'tan3'][valid] for valid in [0,4,5,16,22,34,41,45,50,53,72,86,144]]
		tagClassification['\lim3']=[tagClassification['\lim3'][9]]
		###	
		os.remove('results.txt')
		report=open('results.txt','w')
		for character in tagClassification:
			#EachStroke fa referencia a com es reparteixen els grups en traces, segons la mitjana d'aquesta distribucio a la base de dades
			eachStroke=np.asarray([int(sum([tagClassification[character][i].tE[j] for i in range(len(tagClassification[character]))])/len(tagClassification[character])) for j in range(tagClassification[character][0].tE.shape[0])])
			tagClassification[character]=spp.altArcLengthResampling(tagClassification[character],eachStroke)
			counta+=1
			print character,':',len(tagClassification[character])
			#Totes les features del template d'una etiqueta es calculen com la seva mitjana en els simbols d'aquesta etiqueta
			average=np.zeros([len(tagClassification[character][0].Coord),2],np.float64)
			for example in tagClassification[character]:
				average=np.array([[(average[i,0]+example.Coord[i,0]),(average[i,1]+example.Coord[i,1])] for i in range(example.Coord.shape[0])],np.float64)
			average=np.array([[average[i,0]/len(tagClassification[character]),average[i,1]/len(tagClassification[character])] for i in range(example.Coord.shape[0])],np.float64)
			tagAverages[character]=nsi.taggedSymbol(average,eachStroke,character)
			tagAverages[character].computeFeatures()
			tagAverages[character].LP=[np.nansum([tagClassification[character][i].LP[j] for i in range(len(tagClassification[character]))])/len(tagClassification[character]) for j in range(len(tagClassification[character][0].LP))]
			tagAverages[character].accAngle=[np.nansum([tagClassification[character][i].accAngle[j] for i in range(len(tagClassification[character]))])/len(tagClassification[character]) for j in range(len(tagClassification[character][0].accAngle))]
			tagAverages[character].coG=[[np.nansum([tagClassification[character][i].coG[j][0] for i in range(len(tagClassification[character]))])/len(tagClassification[character]),np.nansum([tagClassification[character][i].coG[j][1] for i in range(len(tagClassification[character]))])/len(tagClassification[character])] for j in range(len(tagClassification[character][0].coG))]
			tagAverages[character].liS=[np.nansum([tagClassification[character][i].liS[j] for i in range(len(tagClassification[character]))])/len(tagClassification[character]) for j in range(len(tagClassification[character][0].liS))]
			tagAverages[character].quadraticError=[np.nansum([tagClassification[character][i].quadraticError[j] for i in range(len(tagClassification[character]))])/len(tagClassification[character]) for j in range(len(tagClassification[character][0].quadraticError))]
			tagAverages[character].relStrokeLength=[np.nansum([tagClassification[character][i].relStrokeLength[j] for i in range(len(tagClassification[character]))])/len(tagClassification[character]) for j in range(len(tagClassification[character][0].relStrokeLength))]
			tagAverages[character].turningAngle=[np.nansum([tagClassification[character][i].turningAngle[j] for i in range(len(tagClassification[character]))])/len(tagClassification[character]) for j in range(len(tagClassification[character][0].turningAngle))]
			tagAverages[character].turningAngleDifference=[np.nansum([tagClassification[character][i].turningAngleDifference[j] for i in range(len(tagClassification[character]))])/len(tagClassification[character]) for j in range(len(tagClassification[character][0].turningAngleDifference))]
			styles=['horizontal','vertical','diagonal','closed']
			tagAverages[character].Style=styles[np.argmax([[tagClassification[character][i].Style for i in range(len(tagClassification[character]))].count('horizontal'),[tagClassification[character][i].Style for i in range(len(tagClassification[character]))].count('vertical'),[tagClassification[character][i].Style for i in range(len(tagClassification[character]))].count('diagonal'),[tagClassification[character][i].Style for i in range(len(tagClassification[character]))].count('closed')])]
			report.write('-----------------------------------------------\n')
			report.write(character+'      |\n')
			report.write('---------\n')
			for i in range(len(tagClassification[character])):
				report.write(str(tagClassification[character][i].tE)+'       :\n')
				for j in range(tagClassification[character][i].Coord.shape[0]):
					report.write(str(tagClassification[character][i].Coord[j])+', ')
				report.write('\n')
			report.write('average:\n               ')
			for j in range(average.shape[0]):
				report.write(str(average[j])+', ')
			report.write('\n')
	#Guarda els resultats al sistema
	if os.path.isfile('varSimbdB.txt'):
		os.remove('varSimbdB.txt')
	f = open('varSimbdB.txt','wb')
	pickle.dump(symboldB,f)
	f.close()
	if os.path.isfile('varTagClass.txt'):
		os.remove('varTagClass.txt')
	f = open('varTagClass.txt','wb')
	pickle.dump(tagClassification,f)
	f.close()
	if os.path.isfile('varAverages.txt'):
		os.remove('varAverages.txt')
	f = open('varAverages.txt','wb')
	pickle.dump(tagAverages,f)
	f.close()	
	report.close()
	plt.show()
	
#ReadTemplate: Carrega la base de dades de simbols, la classificacio de la base de dades i els templates
	
def readTemplate():
	print 'Loading templates..........'
	symFile = open('varSimbdB.txt','rb')
	symboldB=pickle.load(symFile)
	symFile.close()
	tagFile = open('varTagClass.txt','rb')
	tagClassification=pickle.load(tagFile)
	tagFile.close()
	avFile = open('varAverages.txt','rb')
	averages=pickle.load(avFile)
	avFile.close()
	return symboldB,tagClassification,averages
		
			
			
