import math
import numpy as np
import symbolPreprocessing as spp
import featurePonderation as fP

#ElasticMatching: Segons el simbol symbolToRec, els templates charTemplates i les ponderacions weights decideix l'etiqueta mes probable

def elasticMatching(charTemplates,symbolToRec,weights,amp,alt):
	costCoord=[]
	costLP=[]
	costtAngle=[]
	costtAD=[]
	costliS=[]
	costaA=[]
	costqE=[]
	costrSL=[]
	costcog=[]
	coststyle=[]
	reference=[]
	cost=[]
	for character in charTemplates:
		#Nomes si tenen el mateix nombre de traces ho decideix
		if character[-1:]=='1':
			tNum=1
		elif character[-1:]=='2':
			tNum=2
		elif character[-1:]=='3':
			tNum=3
		if tNum==symbolToRec.tE.shape[0]:
			adaptedSymbol=spp.altArcLengthResampling([symbolToRec],charTemplates[character].tE)[0]
			adaptedSymbol.computeFeatures()
			#Busca el cost de cada feature
			costCoord.append(sum([math.sqrt(((charTemplates[character].Coord[i,0]-adaptedSymbol.Coord[i,0])**2)+((charTemplates[character].Coord[i,1]-adaptedSymbol.Coord[i,1])**2)) for i in range(adaptedSymbol.Coord.shape[0])]))
			costLP.append(sum([abs(charTemplates[character].LP[i]-adaptedSymbol.LP[i]) for i in range(adaptedSymbol.LP.shape[0])]))
			costtAngle.append(sum([abs(charTemplates[character].turningAngle[i]-adaptedSymbol.turningAngle[i]) for i in range(adaptedSymbol.turningAngle.shape[0])]))
			costtAD.append(sum([abs(charTemplates[character].turningAngleDifference[i]-adaptedSymbol.turningAngleDifference[i]) for i in range(adaptedSymbol.turningAngleDifference.shape[0])]))
			if adaptedSymbol.liS.shape[0]!=len(charTemplates[character].liS):
				costliS.append(spp.lcomp(adaptedSymbol.Coord,adaptedSymbol.Coord.shape[0]))
			else:
				costliS.append(sum([abs(charTemplates[character].liS[i]-adaptedSymbol.liS[i]) for i in range(adaptedSymbol.liS.shape[0])]))
			if adaptedSymbol.accAngle.shape[0]!=len(charTemplates[character].accAngle):
				costaA.append(adaptedSymbol.tE.shape[0]*2*math.pi)
			else:	
				costaA.append(sum([abs(charTemplates[character].accAngle[i]-adaptedSymbol.accAngle[i]) for i in range(adaptedSymbol.accAngle.shape[0])]))
			if adaptedSymbol.quadraticError.shape[0]!=len(charTemplates[character].quadraticError):
				costqE.append(math.sqrt(8)*adaptedSymbol.tE.shape[0])
			else:
				costqE.append(sum([abs(charTemplates[character].quadraticError[i]-adaptedSymbol.quadraticError[i]) for i in range(adaptedSymbol.quadraticError.shape[0])]))
			if adaptedSymbol.relStrokeLength.shape[0]!=len(charTemplates[character].relStrokeLength):
				costrSL.append(1)
			else:
				costrSL.append(sum([abs(charTemplates[character].relStrokeLength[i]-adaptedSymbol.relStrokeLength[i]) for i in range(adaptedSymbol.relStrokeLength.shape[0])]))	
			if adaptedSymbol.coG.shape[0]!=len(charTemplates[character].coG):
				costcog.append(adaptedSymbol.tE.shape[0]*math.sqrt(8))
			else:
				costcog.append(sum([math.sqrt(((charTemplates[character].coG[i][0]-adaptedSymbol.coG[i][0])**2)+((charTemplates[character].coG[i][1]-adaptedSymbol.coG[i][1])**2)) for i in range(adaptedSymbol.coG.shape[0])]))
			if charTemplates[character].Style==adaptedSymbol.Style:
				coststyle.append(0)
			else:
				coststyle.append(1)
			reference.append(character)
			cost.append(0)
	allThisCost={}
	kindsOfCost={'Coord':costCoord,'LP':costLP,'turningAngle':costtAngle,'turningAngleDifference':costtAD,'liS':costliS,'accAngle':costaA,'quadraticError':costqE,'relStrokeLength':costrSL,'coG':costcog,'Style':coststyle}
	probByCost={}
	fiProb={}
	#Segons el cost busca una probabilitat i la pondera
	for kind in kindsOfCost:
		allThisCost[kind]=np.nansum(kindsOfCost[kind])
		probByCost[kind]=[allThisCost[kind]/float(ch) for ch in kindsOfCost[kind]]
		totProb=np.nansum(probByCost[kind])
		fiProb[kind]=[ch/float(totProb) for ch in probByCost[kind]]
	probPonderada=[np.nansum([weights[kind]*fiProb[kind][i] for kind in fiProb]) for i in range(len(cost))]
	while charTemplates[reference[np.argmax(probPonderada)]].tE.shape[0]!=adaptedSymbol.tE.shape[0]:
		del reference[np.argmax(probPonderada)]
		del probPonderada[np.argmax(probPonderada)]
	etiqBelongs=reference[np.argmax(probPonderada)]
	#Casos especials amb bounding box petita
	if (symbolToRec.bBox[1]-symbolToRec.bBox[0])<0.0125*amp and (symbolToRec.bBox[3]-symbolToRec.bBox[2])<0.017*alt:
		etiqBelongs='.1'
	elif ((symbolToRec.bBox[1]-symbolToRec.bBox[0])>0.0125*amp and (symbolToRec.bBox[3]-symbolToRec.bBox[2])<0.017*alt):
		etiqBelongs='-1'
	elif (symbolToRec.bBox[1]-symbolToRec.bBox[0])<0.0125*amp and (symbolToRec.bBox[3]-symbolToRec.bBox[2])>0.017*alt:
		if symbolToRec.tE.shape[0]==1:
			etiqBelongs='11'
		elif symbolToRec.tE.shape[0]==2:
			if abs(symbolToRec.Coord[0,1]-symbolToRec.Coord[symbolToRec.tE[0],1])*(symbolToRec.bBox[3]-symbolToRec.bBox[2])<0.017*alt and abs(symbolToRec.Coord[symbolToRec.tE[0]+1,1]-symbolToRec.Coord[symbolToRec.tE[1],1])*(symbolToRec.bBox[3]-symbolToRec.bBox[2])<0.017*alt:
				etiqBelongs='\ldots2'
			elif (abs(symbolToRec.Coord[0,1]-symbolToRec.Coord[symbolToRec.tE[0],1])*(symbolToRec.bBox[3]-symbolToRec.bBox[2])>0.017*alt and abs(symbolToRec.Coord[symbolToRec.tE[0]+1,1]-symbolToRec.Coord[symbolToRec.tE[1],1])*(symbolToRec.bBox[3]-symbolToRec.bBox[2])<0.017*alt) or (abs(symbolToRec.Coord[0,1]-symbolToRec.Coord[symbolToRec.tE[0],1])*(symbolToRec.bBox[3]-symbolToRec.bBox[2])<0.017*alt and abs(symbolToRec.Coord[symbolToRec.tE[0]+1,1]-symbolToRec.Coord[symbolToRec.tE[1],1])*(symbolToRec.bBox[3]-symbolToRec.bBox[2])>0.017*alt):
				if symbolToRec.coG[0,1]<symbolToRec.coG[1,1]:
					etiqBelongs='i2'
				else:
					etiqBelongs='!2'
		else:
			etiqBelongs='\ldots3'
	if (symbolToRec.bBox[1]-symbolToRec.bBox[0])>(symbolToRec.bBox[3]-symbolToRec.bBox[2])*8:
		etiqBelongs='-1'
	return etiqBelongs
