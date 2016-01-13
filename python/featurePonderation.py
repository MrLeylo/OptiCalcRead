import numpy as np
import statistics
import operator
import math
import copy
import os
import pickle

#Random

#FindConcentration: Guarda al sistema les desviacions estandar

def findConcentration(tagClassification):
	#Selecciona les features a analitzar i adapta en format numeric les altres
	featList=vars(tagClassification['a1'][0])
	del featList['tE']
	del featList['tag']
	del featList['bBox']
	del featList['center']
	feats2Rec=copy.deepcopy(featList)
	del feats2Rec['Coord']
	del feats2Rec['Style']
	del feats2Rec['coG']
	l1=[symbol for symbol in tagClassification if symbol[-1]=='1']
	l2=[symbol for symbol in tagClassification if symbol[-1]=='2']
	l3=[symbol for symbol in tagClassification if symbol[-1]=='3']
	standevs={}
	for fe in feats2Rec:
		for llet in tagClassification:
			for i in range(len(tagClassification[llet])):
				new=True
				for j in range(len(vars(tagClassification[llet][i])[fe])):
					if math.isnan(vars(tagClassification[llet][i])[fe][j]) and new:
						tagClassification[llet][i].computeFeatures()
						new=False
	for symbol in tagClassification:
		for i in range(len(tagClassification[symbol])):
			if tagClassification[symbol][i].Style=='diagonal':
				tagClassification[symbol][i].Style=[[1,1]]
			elif tagClassification[symbol][i].Style=='horizontal':
				tagClassification[symbol][i].Style=[[1,2]]
			elif tagClassification[symbol][i].Style=='vertical':
				tagClassification[symbol][i].Style=[[2,1]]
			elif tagClassification[symbol][i].Style=='closed':
				tagClassification[symbol][i].Style=[[2,2]]
	for feature in featList:
		getFileName(feature,True)
		fdata=open(getFileName(feature,False)[0],'w')
		fdata.write('TION\n')
		if type(getFileName(feature,False)[1]) is str:
			fvars=open(getFileName(feature,False)[1],'w')
			fvars.write('TION\n')
		elif type(getFileName(feature,False)[1]) is list:
			fvars=[]
			for nam in getFileName(feature,False)[1]:
				fvars.append(open(nam,'w'))
				fvars[len(fvars)-1].write('TION\n')
		print feature
		if feature=='Style':
			standevs[feature]=[]
			outStdVar=math.sqrt(((statistics.pstdev(reduce(operator.add,[[vars(mostra)[feature][0][0] for mostra in tagClassification[symbol]] for symbol in tagClassification])))**2)+((statistics.pstdev(reduce(operator.add,[[vars(mostra)[feature][0][1] for mostra in tagClassification[symbol]] for symbol in tagClassification])))**2))
			for symbol in tagClassification:
				fdata.write(symbol+':\n')
				for m in tagClassification[symbol]:
					fdata.write(str(vars(m)[feature][0][0])+','+str(vars(m)[feature][0][1])+'\n')
				fdata.write('------------------------------------------------------------------------------\n')
				inStdVar=math.sqrt(((statistics.pstdev([vars(mostra)[feature][0][0] for mostra in tagClassification[symbol]]))**2)+((statistics.pstdev([vars(mostra)[feature][0][1] for mostra in tagClassification[symbol]]))**2))
				fvars.write(symbol+':'+str(inStdVar)+'\n')
				standevs[feature].append(inStdVar/float(outStdVar+0.0000001))
			fvars.write('OUT:'+str(outStdVar)+'\n')
			fdata.close()
			fvars.close()
		elif feature=='turningAngle' or feature=='turningAngleDifference' or feature=='LP':
			L=50
			standevs[feature]=[]
			outStdVar=[]
			for i in range(L):
				outStdVar.append(statistics.pstdev(reduce(operator.add,[[vars(mostra)[feature][i] for mostra in tagClassification[symbol]] for symbol in tagClassification])))
			textLocal=[]
			notYet=True
			for symbol in tagClassification:
				fdata.write(symbol+':\n')
				for m in tagClassification[symbol]:
					for i in range(50):
						fdata.write(str(vars(m)[feature][i])+',')
					fdata.write('\n')
				fdata.write('------------------------------------------------------------------------------\n')
				localStdv=[]
				for i in range(L):
					if notYet:
						textLocal.append('')
					inStdVar=statistics.pstdev([vars(mostra)[feature][i] for mostra in tagClassification[symbol]])
					localStdv.append(inStdVar/float(outStdVar[i]+0.0000001))
					textLocal[i]+='('+str(i)+')'+symbol+':'+str(localStdv[i])+'\n'
				standevs[feature].append(np.nansum(localStdv)/float(L))
				notYet=False
			for i in range(L):
				fvars.write(textLocal[i])
				fvars.write('OUT:'+str(outStdVar[i])+'\n')
			fdata.close()
			fvars.close()
		elif feature=='Coord':
			L=50
			standevs[feature]=[]
			outStdVar=[]
			for i in range(L):
				outStdVar.append(math.sqrt(((statistics.pstdev(reduce(operator.add,[[vars(mostra)[feature][i][0] for mostra in tagClassification[symbol]] for symbol in tagClassification])))**2)+((statistics.pstdev(reduce(operator.add,[[vars(mostra)[feature][i][1] for mostra in tagClassification[symbol]] for symbol in tagClassification])))**2)))
			for symbol in tagClassification:
				fdata.write(symbol+':\n')
				for m in tagClassification[symbol]:
					for i in range(50):
						fdata.write('['+str(vars(m)[feature][i][0])+','+str(vars(m)[feature][i][1])+'],')
					fdata.write('\n')
				fdata.write('------------------------------------------------------------------------------\n')
				localStdv=[]
				for i in range(L):
					if notYet:
						textLocal.append('')
					inStdVar=math.sqrt(((statistics.pstdev([vars(mostra)[feature][i][0] for mostra in tagClassification[symbol]]))**2)+((statistics.pstdev([vars(mostra)[feature][i][1] for mostra in tagClassification[symbol]]))**2))
					localStdv.append(inStdVar/float(outStdVar[i]+0.0000001))
					textLocal[i]+='('+str(i)+')'+symbol+':'+str(localStdv[i])+'\n'
				standevs[feature].append(np.nansum(localStdv[i])/float(L))
				notYet=False
			for i in range(L):
				fvars.write(textLocal[i])
				fvars.write('OUT:'+str(outStdVar[i])+'\n')
			fdata.close()
			fvars.close()
		elif feature=='liS' or feature=='relStrokeLength' or feature=='accAngle' or feature=='quadraticError':
			standevs[feature]=[]
			oneOut=np.nansum([statistics.pstdev(reduce(operator.add,[[vars(mostra)[feature][i] for mostra in tagClassification[symbol]] for symbol in l1])) for i in range(1)])/1.0
			twoOut=np.nansum([statistics.pstdev(reduce(operator.add,[[vars(mostra)[feature][i] for mostra in tagClassification[symbol]] for symbol in l2])) for i in range(2)])/2.0
			threeOut=np.nansum([statistics.pstdev(reduce(operator.add,[[vars(mostra)[feature][i] for mostra in tagClassification[symbol]] for symbol in l3])) for i in range(3)])/3.0
			outStdVar=((oneOut*len(l1))+(twoOut*len(l2))+(threeOut*len(l3)))/float(len(l1)+len(l2)+len(l3))
			text1=''
			text2=''
			text3=''
			for symbol in tagClassification:
				fdata.write(symbol+':\n')
				for m in tagClassification[symbol]:
					for i in range(len(vars(m)[feature])):
						fdata.write(str(vars(m)[feature][i])+',')
					fdata.write('\n')
				fdata.write('------------------------------------------------------------------------------\n')
				inStdVar=np.nansum([statistics.pstdev([vars(mostra)[feature][i] for mostra in tagClassification[symbol]]) for i in range(len(vars(tagClassification[symbol][0])[feature]))])/float(len(vars(tagClassification[symbol][0])[feature]))
				if symbol in l1:
					text1+=symbol+':'+str(inStdVar)+'\n'
				elif symbol in l2:
					text2+=symbol+':'+str(inStdVar)+'\n'
				elif symbol in l3:
					text3+=symbol+':'+str(inStdVar)+'\n'
				standevs[feature].append(inStdVar/float(outStdVar+0.0000001))
			text1+='OUT:'+str(oneOut)+'\n'
			text2+='OUT:'+str(twoOut)+'\n'
			text3+='OUT:'+str(threeOut)+'\n'
			fvars[0].write(text1)
			fvars[1].write(text2)
			fvars[2].write(text3)
			fdata.close()
			fvars[0].close()
			fvars[1].close()
			fvars[2].close()
		elif feature=='coG':
			standevs[feature]=[]
			oneOut=np.nansum([math.sqrt(((statistics.pstdev(reduce(operator.add,[[vars(mostra)[feature][i][0] for mostra in tagClassification[symbol]] for symbol in l1])))**2)+((statistics.pstdev(reduce(operator.add,[[vars(mostra)[feature][i][1] for mostra in tagClassification[symbol]] for symbol in l1])))**2)) for i in range(1)])/1.0
			twoOut=np.nansum([math.sqrt(((statistics.pstdev(reduce(operator.add,[[vars(mostra)[feature][i][0] for mostra in tagClassification[symbol]] for symbol in l2])))**2)+((statistics.pstdev(reduce(operator.add,[[vars(mostra)[feature][i][1] for mostra in tagClassification[symbol]] for symbol in l2])))**2)) for i in range(2)])/2.0
			threeOut=np.nansum([math.sqrt(((statistics.pstdev(reduce(operator.add,[[vars(mostra)[feature][i][0] for mostra in tagClassification[symbol]] for symbol in l3])))**2)+((statistics.pstdev(reduce(operator.add,[[vars(mostra)[feature][i][1] for mostra in tagClassification[symbol]] for symbol in l3])))**2)) for i in range(3)])/3.0
			outStdVar=((oneOut*len(l1))+(twoOut*len(l2))+(threeOut*len(l3)))/float(len(l1)+len(l2)+len(l3))
			text1=''
			text2=''
			text3=''
			for symbol in tagClassification:
				for m in tagClassification[symbol]:
					for i in range(len(vars(m)[feature])):
						fdata.write(str(vars(m)[feature][i][0])+','+str(vars(m)[feature][i][1])+']'+',')
					fdata.write('\n')
				fdata.write('------------------------------------------------------------------------------\n')
				inStdVar=np.nansum([math.sqrt(((statistics.pstdev([vars(mostra)[feature][i][0] for mostra in tagClassification[symbol]]))**2)+((statistics.pstdev([vars(mostra)[feature][i][1] for mostra in tagClassification[symbol]]))**2)) for i in range(len(vars(tagClassification[symbol][0])[feature]))])/float(len(vars(tagClassification[symbol][0])[feature]))
				if symbol in l1:
					text1+=symbol+':'+str(inStdVar)+'\n'
				elif symbol in l2:
					text2+=symbol+':'+str(inStdVar)+'\n'
				elif symbol in l3:
					text3+=symbol+':'+str(inStdVar)+'\n'
				standevs[feature].append(inStdVar/float(outStdVar+0.0000001))
			text1+='OUT:'+str(oneOut)+'\n'
			text2+='OUT:'+str(twoOut)+'\n'
			text3+='OUT:'+str(threeOut)+'\n'
			fvars[0].write(text1)
			fvars[1].write(text2)
			fvars[2].write(text3)
			fdata.close()
			fvars[0].close()
			fvars[1].close()
			fvars[2].close()
	print standevs
	if os.path.isfile('varStandarDevs.txt'):
		os.remove('varStandarDevs.txt')
	f = open('varStandarDevs.txt','wb')
	pickle.dump(standevs,f)
	f.close()

#GetFileName:segons la feature, genera el nom de l'arxiu on guardara la desviacio estandar, on toDel es un boolean que indica si ha d'esborrar l'arxiu anterior o afegir-lo
	
def getFileName(feature,toDel):
	nomData='fAn_'+feature+'.txt'
	if os.path.isfile(nomData) and toDel:
		os.remove(nomData)
	nomVars='vAn_'+feature+'.txt'
	if os.path.isfile(nomVars):
		os.remove(nomVars)
	if feature=='liS' or feature=='relStrokeLength' or feature=='accAngle' or feature=='quadraticError' or feature=='coG':
		 nomVars=['vAn_'+feature+'01.txt','vAn_'+feature+'02.txt','vAn_'+feature+'03.txt']
		 for n in nomVars:
			 if os.path.isfile(n) and toDel:
				os.remove(n)
	else:
		nomVars='vAn_'+feature+'.txt'
		if os.path.isfile(nomVars) and toDel:
			os.remove(nomVars)
	return [nomData,nomVars]

#FindConcentrationAux: Mateix resultat que findConcentration de forma alternativa

def findConcentrationAux(tagClassification):
	featList=vars(tagClassification['a1'][0])
	del featList['tE']
	del featList['tag']
	del featList['bBox']
	del featList['center']
	feats2Rec=copy.deepcopy(featList)
	del feats2Rec['Coord']
	del feats2Rec['Style']
	del feats2Rec['coG']
	l1=[symbol for symbol in tagClassification if symbol[-1]=='1']
	l2=[symbol for symbol in tagClassification if symbol[-1]=='2']
	l3=[symbol for symbol in tagClassification if symbol[-1]=='3']
	standevs={}
	for fe in feats2Rec:
		for llet in tagClassification:
			for i in range(len(tagClassification[llet])):
				new=True
				for j in range(len(vars(tagClassification[llet][i])[fe])):
					if math.isnan(vars(tagClassification[llet][i])[fe][j]) and new:
						tagClassification[llet][i].computeFeatures()
						new=False
	for symbol in tagClassification:
		for i in range(len(tagClassification[symbol])):
			if tagClassification[symbol][i].Style=='diagonal':
				tagClassification[symbol][i].Style=[[1,1]]
			elif tagClassification[symbol][i].Style=='horizontal':
				tagClassification[symbol][i].Style=[[1,2]]
			elif tagClassification[symbol][i].Style=='vertical':
				tagClassification[symbol][i].Style=[[2,1]]
			elif tagClassification[symbol][i].Style=='closed':
				tagClassification[symbol][i].Style=[[2,2]]
	for feature in featList:
		print feature
		if feature=='Coord' or feature=='Style' or feature=='coG':
			standevs[feature]=[math.sqrt((((float(float(np.nansum([statistics.pstdev([vars(mostra)[feature][i][0] for mostra in tagClassification[symbol]])/np.mean([vars(mostra)[feature][i][0] for mostra in tagClassification[symbol]]) for i in range(len(vars(tagClassification[symbol][0])[feature]))]))/len(vars(tagClassification[symbol][0])[feature])))/(float((np.nansum([statistics.pstdev(reduce(operator.add,[[vars(mostra)[feature][j][0] for mostra in tagClassification[altSymbol]] for altSymbol in l1]))/np.mean(reduce(operator.add,[[vars(mostra)[feature][j][0] for mostra in tagClassification[altSymbol]] for altSymbol in l1])) for j in range(len(vars(tagClassification['a1'][0])[feature]))])/len(vars(tagClassification[symbol][0])[feature]))+(np.nansum([statistics.pstdev(reduce(operator.add,[[vars(mostra)[feature][j][0] for mostra in tagClassification[altSymbol]] for altSymbol in l2]))/np.mean(reduce(operator.add,[[vars(mostra)[feature][j][0] for mostra in tagClassification[altSymbol]] for altSymbol in l2])) for j in range(len(vars(tagClassification['+2'][0])[feature]))])/len(vars(tagClassification[symbol][0])[feature]))+(np.nansum([statistics.pstdev(reduce(operator.add,[[vars(mostra)[feature][j][0] for mostra in tagClassification[altSymbol]] for altSymbol in l3]))/np.mean(reduce(operator.add,[[vars(mostra)[feature][j][0] for mostra in tagClassification[altSymbol]] for altSymbol in l3])) for j in range(len(vars(tagClassification['A3'][0])[feature]))])/len(vars(tagClassification[symbol][0])[feature])))/3))**2)+(((float(float(np.nansum([statistics.pstdev([vars(mostra)[feature][i][1] for mostra in tagClassification[symbol]])/np.mean([vars(mostra)[feature][i][1] for mostra in tagClassification[symbol]]) for i in range(len(vars(tagClassification[symbol][0])[feature]))]))/len(vars(tagClassification[symbol][0])[feature])))/(float((np.nansum([statistics.pstdev(reduce(operator.add,[[vars(mostra)[feature][j][1] for mostra in tagClassification[altSymbol]] for altSymbol in l1]))/np.mean(reduce(operator.add,[[vars(mostra)[feature][j][1] for mostra in tagClassification[altSymbol]] for altSymbol in l1])) for j in range(len(vars(tagClassification['a1'][0])[feature]))])/len(vars(tagClassification[symbol][0])[feature]))+(np.nansum([statistics.pstdev(reduce(operator.add,[[vars(mostra)[feature][j][1] for mostra in tagClassification[altSymbol]] for altSymbol in l2]))/np.mean(reduce(operator.add,[[vars(mostra)[feature][j][1] for mostra in tagClassification[altSymbol]] for altSymbol in l2])) for j in range(len(vars(tagClassification['+2'][0])[feature]))])/len(vars(tagClassification[symbol][0])[feature]))+(np.nansum([statistics.pstdev(reduce(operator.add,[[vars(mostra)[feature][j][1] for mostra in tagClassification[altSymbol]] for altSymbol in l3]))/np.mean(reduce(operator.add,[[vars(mostra)[feature][j][1] for mostra in tagClassification[altSymbol]] for altSymbol in l3])) for j in range(len(vars(tagClassification['A3'][0])[feature]))])/len(vars(tagClassification[symbol][0])[feature])))/3))**2)) for symbol in tagClassification]
		else:
			standevs[feature]=[((float(float(np.nansum([statistics.pstdev([vars(mostra)[feature][i] for mostra in tagClassification[symbol]])/np.mean([vars(mostra)[feature][i] for mostra in tagClassification[symbol]]) for i in range(len(vars(tagClassification[symbol][0])[feature]))]))/len(vars(tagClassification[symbol][0])[feature])))/(float((np.nansum([statistics.pstdev(reduce(operator.add,[[vars(mostra)[feature][j] for mostra in tagClassification[altSymbol]] for altSymbol in l1]))/np.mean(reduce(operator.add,[[vars(mostra)[feature][j] for mostra in tagClassification[altSymbol]] for altSymbol in l1])) for j in range(len(vars(tagClassification['a1'][0])[feature]))])/len(vars(tagClassification[symbol][0])[feature]))+(np.nansum([statistics.pstdev(reduce(operator.add,[[vars(mostra)[feature][j] for mostra in tagClassification[altSymbol]] for altSymbol in l2]))/np.mean(reduce(operator.add,[[vars(mostra)[feature][j] for mostra in tagClassification[altSymbol]] for altSymbol in l2])) for j in range(len(vars(tagClassification['+2'][0])[feature]))])/len(vars(tagClassification[symbol][0])[feature]))+(np.nansum([statistics.pstdev(reduce(operator.add,[[vars(mostra)[feature][j] for mostra in tagClassification[altSymbol]] for altSymbol in l3]))/np.mean(reduce(operator.add,[[vars(mostra)[feature][j] for mostra in tagClassification[altSymbol]] for altSymbol in l3])) for j in range(len(vars(tagClassification['A3'][0])[feature]))])/len(vars(tagClassification[symbol][0])[feature])))/3))	for symbol in tagClassification]
	print standevs
	if os.path.isfile('varStandarDevs.txt'):
		os.remove('varStandarDevs.txt')
	f = open('varStandarDevs.txt','wb')
	pickle.dump(standevs,f)
	f.close()

#PonderateByConcentration: Retorna la ponderacio de les features segons les desviacions estandar que carrega del sistema
	
def ponderateByConcentration():
	print 'Loading feature concentration..........'
	sdFile = open('varStandarDevs.txt','rb')
	standevs=pickle.load(sdFile)
	sdFile.close()
	totDevs={}
	for feature in standevs:
		totDevs[feature]=sum([abs(standevs[feature][si]) for si in range(len(standevs[feature]))])/len(standevs[feature])
	localF=['turningAngle','turningAngleDifference','Coord','LP']
	globalF=['accAngle','coG','relStrokeLength','liS','quadraticError']
	totalF=['turningAngle','turningAngleDifference','Coord','LP','Style','accAngle','coG','relStrokeLength','liS','quadraticError']
	print 'Ponderating features..........'
	weights={}
	norm=np.nansum([1/float(math.sqrt(totDevs[feature])) for feature in totalF])
	for feature in totalF:
		weights[feature]=(1/float(math.sqrt(totDevs[feature])))/float(norm)
	print 'Features weighted as'
	print weights
	return weights
	
		
	
