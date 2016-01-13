from __future__ import division
import math
import numpy as np
from skimage.measure import approximate_polygon as polyapx
from pprint import pprint

#preprocessing:aplica totes les tecniques de preprocessat sobre symbols, on symbols es una llista d'elements de la classe simbol


def preprocessing(symbols):
	print 'Initializing symbol preprocessing..........'
	symbols=noiseReduction(symbols)
	symbols=normalization(symbols)
	print 'Preprocessing complete.'
	return symbols

#noiseReduction: elimina punts, variacions locals molt petites i terminacions molt tancades i simplifica la forma, on symbols es una llista d'elements de la classe simbol

def noiseReduction(symbols):
	print 'Reducing noise.....(1/2)'
	symbols=pointDeleting(symbols)
	symbols=smoothing(symbols)
	symbols=pointClustering(symbols)
	symbols=dehooking(symbols)
	symbols=polyAproximation(symbols)
	symbols=pointDeleting(symbols)
	return symbols

#normalization: normalitza els punts mostrejats de la forma, la direccio i ordre de les traces i el tamany i posicio del simbol i limita el nombre de traces, on symbols es una llista d'elements de la classe simbol 

def normalization(symbols):
	print 'Normalizing.....(2/2)'	
	symbols=arcLengthResampling(symbols,50)
	symbols=strokeDirOrder(symbols)
	symbols=strokeReduction(symbols,3,False)
	symbols=sizeNorm(symbols)
	return symbols

#pointDeleting:elimina les traces que consisteixen en un punt, on symbols es una llista d'elements de la classe simbol

def pointDeleting(symbols):
	for i in range(len(symbols)):
		act=0
		for j in range(symbols[i].tE.shape[0]):
			ja=j-act
			if ja==0:
				ini=-1
			else:
				ini=int(symbols[i].tE[ja-1])
			#Elimina quan les traces nomes tenen una coordenada o quan la seva longitud es 0
			if symbols[i].tE[ja]-ini==1 or (lcomp(symbols[i].Coord,int(symbols[i].tE[ja])+1)-lcomp(symbols[i].Coord,ini+2))==0:
				act+=1
				#Elimina el marcador i les coordenades del trace i actualitza els marcadors
				symbols[i].Coord=np.delete(symbols[i].Coord,[jr for jr in range(ini+1,int(symbols[i].tE[ja])+1)],0)
				retro=symbols[i].tE[ja]-ini
				symbols[i].tE=np.delete(symbols[i].tE,ja,0)
				for k in range(ja,symbols[i].tE.shape[0]):
					symbols[i].tE[k]-=retro
	return symbols

#smoothing: pondera els punts dels simbols amb els punts veins i retorna els simbols ponderats, on symbols es una llista d'elements de la classe simbol

def smoothing(symbols):
	newSymbols=[[[]]]
	#Per cada simbol mira cada punt
	for i in range(len(symbols)):
		if symbols[i].Coord.shape[0]>1:
			for j in range(symbols[i].Coord.shape[0]):
			#Pel primer punt del simbol aplica aquesta ponderacio sobre ell mateix i el segon punt
				if j==0 or (j-1) in symbols[i].tE[range(symbols[i].tE.shape[0])]:
					nX=(2/3)*symbols[i].Coord[j,0]+(1/3)*symbols[i].Coord[j+1,0]
					nY=(2/3)*symbols[i].Coord[j,1]+(1/3)*symbols[i].Coord[j+1,1]
					if j==0:
						newSymbols.append([[nX,nY]])
					else:
						newSymbols[i+1].append([nX,nY])
				#Per l'ultim punt del simbol aplica aquesta ponderacio sobre ell mateix i el penultim punt
				elif j==symbols[i].Coord.shape[0]-1 or j in symbols[i].tE[range(symbols[i].tE.shape[0])]:
					nX=(1/3)*symbols[i].Coord[j-1,0]+(2/3)*symbols[i].Coord[j,0]
					nY=(1/3)*symbols[i].Coord[j-1,1]+(2/3)*symbols[i].Coord[j,1]
					newSymbols[i+1].append([nX,nY])
				#Per la resta de punts aplica aquesta ponderacio sobre el punt, l'anterior i el seguent
				else:
					nX=0.25*symbols[i].Coord[j-1,0]+0.5*symbols[i].Coord[j,0]+0.25*symbols[i].Coord[j+1,0]
					nY=0.25*symbols[i].Coord[j-1,1]+0.5*symbols[i].Coord[j,1]+0.25*symbols[i].Coord[j+1,1]
					newSymbols[i+1].append([nX,nY])
		symbols[i].Coord=np.asarray(newSymbols[i+1])
	return symbols
	
#pointClustering: recalcula els punts dels simbols com la mitjana dels punts en un radi, on symbols es una llista d'elements de la classe simbol

	
def pointClustering(symbols):
	symbolsClust=[]
	#Per cada simbol calcula la longitud i amb ella el radi amb el que filtrara
	for i in range(len(symbols)):
		c=0
		#Mira tots els punts, quants dels seguents punts estan inclosos en el radi per inclourels en el vector cP, quan es surt del radi calcula la mitja en cP i ho assigna a aftP
		cP=np.array([[0,0]],np.float64)
		cG=np.array([[0,0]],np.float64)
		aftP=np.array([[0,0]],np.float64)
		div=np.array([[0,0]],np.float64)
		tevec=np.zeros([symbols[i].tE.shape[0]],np.float64)
		tec=0
		for ik in range(symbols[i].tE.shape[0]):
			if ik==0:
				ini=-1
			else:
				ini=int(symbols[i].tE[ik-1])
			L=lcomp(symbols[i].Coord,int(symbols[i].tE[ik])+1)-lcomp(symbols[i].Coord,ini+2)
			rad=L/80
			for j in range(ini+1,int(symbols[i].tE[ik])+1):
				distance=math.sqrt(((symbols[i].Coord[j,0]-symbols[i].Coord[j-c,0])**2)+((symbols[i].Coord[j,1]-symbols[i].Coord[j-c,1])**2))
				if distance<=rad:
					c=c+1
				else:
					sum=[0,0]
					for k in range(c+1):
						sum[0]=sum[0]+cP[k,0]
						sum[1]=sum[1]+cP[k,1]
					div[0,0]=sum[0]/c
					div[0,1]=sum[1]/c
					aftP=np.append(aftP,div,0)
					cG=np.append(cG,cP,0)
					del cP
					cP=np.array([[0,0]],np.float64)
					c=1
				cP=np.append(cP,[symbols[i].Coord[j]],0)
				if j==symbols[i].tE[min(tec,symbols[i].tE.shape[0]-1)]:
					tevec[tec]=aftP.shape[0]-1
					tec=tec+1
		sum=[0,0]
		#Ho aplica tambe en l'ultim cP
		for k in range(c+1):
			sum[0]=sum[0]+cP[k,0]
			sum[1]=sum[1]+cP[k,1]
		div[0,0]=sum[0]/c
		div[0,1]=sum[1]/c
		aftP=np.append(aftP,div,0)
		cG=np.append(cG,cP,0)
		aftP=np.delete(aftP,0,0)
		symbolsClust.append(aftP)
		symbols[i].Coord=np.asarray(symbolsClust[i])
		symbols[i].tE=tevec
	return symbols
	
#dehooking: elimina els "hooks" en els extrems dels simbols, on symbols es una llista d'elements de la classe simbol

def dehooking(symbols):
	alpha=0.12
	angleThP=(17/36)*math.pi
	angleThN=-(17/36)*math.pi
	#En cada simbol calcula la longitud
	for i in range(len(symbols)):
		#newCoord=np.zeros([symbols[i].Coord.shape[0],2],np.float64)
		newCoord=np.copy(symbols[i].Coord)
		for k in range(symbols[i].tE.shape[0]):
			if k==0:
				ini=-1
			else:
				ini=int(symbols[i].tE[k-1])
			L=lcomp(symbols[i].Coord,int(symbols[i].tE[k])+1)-lcomp(symbols[i].Coord,ini+2)
			#En cada punt calcula la longitud del simbol fins a ell i a partir de ell(lRelI i lRelF)
			unlock=0
			for j in range(ini+1,int(symbols[i].tE[k])+1):
				if unlock==0:
					lRelI=lcomp(symbols[i].Coord,j+1)-lcomp(symbols[i].Coord,ini+2)
					lRelF=L-lRelI
					ct=0
					cr=0
					if lRelI==0 or lRelF==0:
						angle=math.pi
					else:
						while math.sqrt(((symbols[i].Coord[j+ct+1,0]-symbols[i].Coord[j,0])**2)+((symbols[i].Coord[j+ct+1,1]-symbols[i].Coord[j,1])**2))==0:
							ct=ct+1
						while math.sqrt(((symbols[i].Coord[j,0]-symbols[i].Coord[j-cr-1,0])**2)+((symbols[i].Coord[j,1]-symbols[i].Coord[j-cr-1,1])**2))==0:
							cr=cr+1
						A=math.acos((symbols[i].Coord[j,0]-symbols[i].Coord[j-1-cr,0])/(math.sqrt(((symbols[i].Coord[j,0]-symbols[i].Coord[j-1-cr,0])**2)+((symbols[i].Coord[j,1]-symbols[i].Coord[j-1-cr,1])**2))))
						if symbols[i].Coord[j,1]>symbols[i].Coord[j-1-cr,1]:
							A=-A
						B=math.acos((symbols[i].Coord[j+ct+1,0]-symbols[i].Coord[j,0])/(math.sqrt(((symbols[i].Coord[j+ct+1,0]-symbols[i].Coord[j,0])**2)+((symbols[i].Coord[j+ct+1,1]-symbols[i].Coord[j,1])**2))))
						if symbols[i].Coord[j+ct+1,1]>symbols[i].Coord[j,1]:
							B=-B
						angle=A-B
						if angle<0:
							angle=angle+math.pi
						else:
							angle=angle-math.pi
					#Calcula els angles i mira si un punt te l'angle massa tancat
					if angle<angleThP and angle>angleThN:
						if lRelI<alpha*L:
							newCoord[range(ini+1,j)]=symbols[i].Coord[j]
						elif lRelF<alpha*L:
							unlock=1
							newCoord[range(j+1,int(symbols[i].tE[k])+1)]=symbols[i].Coord[j]
		symbols[i].Coord=newCoord
	return symbols
	
#polyAproximation: retorna simbols amb una aproximacio poligonal de tolerancia que depen del tamany de la bounding box, on symbols es una llista d'elements de la classe simbol


def polyAproximation(symbols):
	newSymbols=[[[]]]
	#Aproxima cada simbol amb una tolerancia depenent de la mida de la bounding box
	for i in range(len(symbols)):
		tolerance=(math.sqrt((symbols[i].bBox[1]-symbols[i].bBox[0])*(symbols[i].bBox[3]-symbols[i].bBox[2])))/25
		ntE=np.zeros([symbols[i].tE.shape[0]],np.float64)
		for j in range(symbols[i].tE.shape[0]):
			if j==0:
				newSymbols.append(polyapx(symbols[i].Coord[range(0,int(symbols[i].tE[j])+1)],tolerance))
			else:
				newSymbols[i+1]=np.append(newSymbols[i+1],polyapx(symbols[i].Coord[range(int(symbols[i].tE[j-1])+1,int(symbols[i].tE[j])+1)],tolerance),0)
			ntE[j]=newSymbols[i+1].shape[0]-1
		symbols[i].Coord=newSymbols[i+1]
		symbols[i].tE=ntE
	return symbols
	
#def arcLengthResampling: retorna els simbols dividits en el numero de punts especificat en npoints, on symbols es una llista d'elements de la classe simbol i npoints es un enter

def arcLengthResampling(symbols,npoints):
	#Per cada simbol calcula la longitud i la longitud on trobara cada punt en el que dividira el poligon (en vc)
	for i in range(len(symbols)):
		newtE=np.zeros([symbols[i].tE.shape[0]],np.float64)
		curSymbol=np.zeros([npoints,2],np.float64)
		gcrt=0
		L=0
		Lg=0
		for ik in range(symbols[i].tE.shape[0]):
			if ik==0:
				ini=-1
				iniD=-1
			else:
				ini=int(newtE[ik-1])
				iniD=int(symbols[i].tE[ik-1])
			newtE[ik]=int((npoints-symbols[i].tE.shape[0])*((symbols[i].tE[ik]+1-(ik+1))/(symbols[i].Coord.shape[0]-symbols[i].tE.shape[0])))-1+(ik+1)
			relat=int(newtE[ik]-ini)
			L=lcomp(symbols[i].Coord,int(symbols[i].tE[ik])+1)-lcomp(symbols[i].Coord,iniD+2)
			prt=L/(relat-1)
			vc=[v*prt for v in range(relat)]
			crt=0
			unlock=0
			#Per cada punt (j) mirara si te punts de la nova divisio anteriors(crt), si els te els buscara i els afegeix a curSymbol
			Lg=lcomp(symbols[i].Coord,iniD+2)
			for j in range(iniD+1,int(symbols[i].tE[ik]+1)):
				Lc=lcomp(symbols[i].Coord,j+1)-Lg
				while (Lc+0.0001)>=vc[crt] and unlock==0:
					diferencia=Lc-vc[crt]
					dt=math.sqrt(((symbols[i].Coord[j,0]-symbols[i].Coord[j-1,0])**2)+((symbols[i].Coord[j,1]-symbols[i].Coord[j-1,1])**2))
					dtx=symbols[i].Coord[j,0]-symbols[i].Coord[j-1,0]
					dty=symbols[i].Coord[j,1]-symbols[i].Coord[j-1,1]
					if dt!=0:
						curSymbol[gcrt+crt]=[(symbols[i].Coord[j-1,0]+(dtx*(1-(diferencia/dt)))),(symbols[i].Coord[j-1,1]+(dty*(1-(diferencia/dt))))]
					else:
						curSymbol[gcrt+crt]=symbols[i].Coord[j]
					crt=crt+1
					if crt==len(vc):
						#Quan ha omplert el nou simbol desbloqueja la sortida del bucle(unlock)
						gcrt=crt+gcrt
						crt=0
						unlock=1
		symbols[i].tE=newtE
		symbols[i].Coord=curSymbol
		del curSymbol
	return symbols
	
#altArcLengthResampling: retorna els simbols dividits per traces segons especifica eachStroke, on symbols es una llista d'elements de la classe simbol i eachStroke es una llista amb els punts a cada trace
	
def altArcLengthResampling(symbols,eachStroke):
	for i in range(len(symbols)):
		for j in range(len(eachStroke)):
			curSymbol=np.zeros([symbols[i].Coord.shape[0],2],np.float64)
			gcrt=0
			L=0
			Lg=0
			#Ajusta cada trace entre els punts marcats per eachStroke
			for ik in range(symbols[i].tE.shape[0]):
				if ik==0:
					ini=-1
					iniD=-1
				else:
					ini=int(eachStroke[ik-1])
					iniD=int(symbols[i].tE[ik-1])
				relat=int(eachStroke[ik]-ini)
				L=lcomp(symbols[i].Coord,int(symbols[i].tE[ik])+1)-lcomp(symbols[i].Coord,iniD+2)
				prt=L/(relat-1)
				vc=[v*prt for v in range(relat)]
				crt=0
				unlock=0
				#Per cada punt (j) mirara si te punts de la nova divisio anteriors(crt), si els te els buscara i els afegeix a curSymbol
				Lg=lcomp(symbols[i].Coord,iniD+2)
				for j in range(iniD+1,int(symbols[i].tE[ik]+1)):
					Lc=lcomp(symbols[i].Coord,j+1)-Lg
					while (Lc+0.0001)>=vc[crt] and unlock==0:
						diferencia=Lc-vc[crt]
						dt=math.sqrt(((symbols[i].Coord[j,0]-symbols[i].Coord[j-1,0])**2)+((symbols[i].Coord[j,1]-symbols[i].Coord[j-1,1])**2))
						dtx=symbols[i].Coord[j,0]-symbols[i].Coord[j-1,0]
						dty=symbols[i].Coord[j,1]-symbols[i].Coord[j-1,1]
						if dt!=0:
							curSymbol[gcrt+crt]=[(symbols[i].Coord[j-1,0]+(dtx*(1-(diferencia/dt)))),(symbols[i].Coord[j-1,1]+(dty*(1-(diferencia/dt))))]
						else:
							curSymbol[gcrt+crt]=symbols[i].Coord[j]
						crt=crt+1
						if crt==len(vc):
							#Quan ha omplert el nou simbol desbloqueja la sortida del bucle(unlock)
							gcrt=crt+gcrt
							crt=0
							unlock=1
		symbols[i].tE=eachStroke
		symbols[i].Coord=curSymbol
		del curSymbol
	return symbols
			
		

#strokeDirOrder:retorna els simbols amb l'ordre normalitzat (si detecta que esta invers ho inverteix) i una llista que conte els tipus de cada simbol, on symbols es una llista d'elements de la classe simbol

	
def strokeDirOrder(symbols):
	deltha=0.5
	for i in range(len(symbols)):
		#Busca l'estil de cada simbol
		rx=math.fabs(symbols[i].Coord[symbols[i].Coord.shape[0]-1,0]-symbols[i].Coord[0,0])
		ry=math.fabs(symbols[i].Coord[symbols[i].Coord.shape[0]-1,1]-symbols[i].Coord[0,1])
		diag=math.sqrt(((symbols[i].bBox[1]-symbols[i].bBox[0])**2)+((symbols[i].bBox[3]-symbols[i].bBox[2])**2))
		rax,ray=rx/diag,ry/diag
		if rax>deltha and ray<deltha:
			symbols[i].Style='horizontal'
		elif rax>deltha and ray>deltha:
			symbols[i].Style='diagonal'
		elif rax<deltha and ray>deltha:
			symbols[i].Style='vertical'
		else:
			symbols[i].Style='closed'
		for j in range(symbols[i].tE.shape[0]):
			if j==0:
				ini=-1
			else:
				ini=int(symbols[i].tE[j-1])
			#Segons l'estil de cada trace assigna la seva direccio
			rx=math.fabs(symbols[i].Coord[symbols[i].tE[j],0]-symbols[i].Coord[ini+1,0])
			ry=math.fabs(symbols[i].Coord[symbols[i].tE[j],1]-symbols[i].Coord[ini+1,1])
			diag=math.sqrt(((max([symbols[i].Coord[k,0] for k in range(ini+1,int(symbols[i].tE[j]+1))])-min([symbols[i].Coord[k,0] for k in range(ini+1,int(symbols[i].tE[j]+1))]))**2)+((max([symbols[i].Coord[k,1] for k in range(ini+1,int(symbols[i].tE[j]+1))])-min([symbols[i].Coord[k,1] for k in range(ini+1,int(symbols[i].tE[j]+1))]))**2))
			rax,ray=rx/diag,ry/diag
			if (rax>deltha and symbols[i].Coord[ini+1,0]>symbols[i].Coord[symbols[i].tE[j],0]) or (rax<deltha and ray>deltha and symbols[i].Coord[ini+1,1]>symbols[i].Coord[symbols[i].tE[j],1]):
				symbols[i].Coord[range(ini+1,int(symbols[i].tE[j]+1))]=np.flipud(symbols[i].Coord[range(ini+1,int(symbols[i].tE[j]+1))])
		#Mira l'angle del final de cada trace amb la horitzontal superior de la bounding box i ordena els traces de mes tancat a mes obert 
		finals=np.zeros([symbols[i].tE.shape[0],2],np.float64)
		angle=np.zeros([symbols[i].tE.shape[0]],np.float64)
		for j in range(symbols[i].tE.shape[0]):
			finals[j]=symbols[i].Coord[symbols[i].tE[j]]
			angle[j]=math.acos((finals[j,0]-symbols[i].bBox[0])/float(math.sqrt(((finals[j,0]-symbols[i].bBox[0])**2)+((finals[j,1]-symbols[i].bBox[2])**2))))
		ordre=np.argsort(angle)
		co=0
		nu=np.zeros([symbols[i].Coord.shape[0],2],np.float64)
		ndotE=np.zeros([symbols[i].tE.shape[0]],np.float64)
		for j in range(ordre.shape[0]):
			if ordre[j]==0:
				iu=-1
			else:
				iu=symbols[i].tE[ordre[j]-1]
			nu[range(co,co+int(symbols[i].tE[ordre[j]])-int(iu))]=symbols[i].Coord[range(int(iu)+1,int(symbols[i].tE[ordre[j]])+1)]
			co+=int(symbols[i].tE[ordre[j]])-int(iu)
			if j==0:
				ido=-1
			else:
				ido=ndotE[j-1]
			ndotE[j]=symbols[i].tE[ordre[j]]-iu+ido
		symbols[i].tE=ndotE
		symbols[i].Coord=nu
		del finals
		del angle	
	return symbols
	
#strokeReduction: limita el nombre de traces a l'especificat a nStrokes, i si se li indica a adapted (es un boolean) tambe adapta a aquest nombre els simbols amb menys traces, on symbols es una llista d'elements de la classe simbol i nStrokes un enter
	
def strokeReduction(symbols,nStrokes,adaptation):
	for i in range(len(symbols)):
		if nStrokes<len(symbols[i].tE):
			symbols[i].tE=np.delete(symbols[i].tE,range(nStrokes-1,len(symbols[i].tE)-1),0)
		elif nStrokes>len(symbols[i].tE) and adaptation:
			if len(symbols[i].tE)>1:
				newDiv=round(symbols[i].tE[len(symbols[i].tE)-2]+((symbols[i].tE[len(symbols[i].tE)-1]-symbols[i].tE[len(symbols[i].tE)-2])/2))
			else:
				newDiv=round(symbols[i].tE[0]/2)
			symbols[i].tE=np.insert(symbols[i].tE,len(symbols[i].tE)-1,newDiv)
	return symbols

#sizeNorm: retorna els simbols normalitzats desde el centre menys 1 fins al centre mes 1, on simbols es un numpy array de 3 dimensions, bboxes es un numpy array de 2 dimensions amb les 4 coordenades de les bounding box de cada simbol, i centers es un numpy array de 2 dimensions amb les 2 coordenades dels centres de cada simbol
		
def sizeNorm(symbols):
	#Per cada simbol busca la nova posicio dels seus punts, desdel mateix centre i normalitzat entre 1 i -1
	for i in range(len(symbols)):
		for j in range(symbols[i].Coord.shape[0]):
			if symbols[i].bBox[0]==symbols[i].bBox[1]:
				symbols[i].Coord[j,0]=0
			else:
				symbols[i].Coord[j,0]=((symbols[i].Coord[j,0]-symbols[i].center[0])*(1/(symbols[i].center[0]-symbols[i].bBox[0])))
			if symbols[i].bBox[2]==symbols[i].bBox[3]:
				symbols[i].Coord[j,1]=0
			else:
				symbols[i].Coord[j,1]=((symbols[i].Coord[j,1]-symbols[i].center[1])*(1/(symbols[i].center[1]-symbols[i].bBox[2])))
	return symbols
	
#lcomp: calcula la longitud del segment de symbols amb el numero de punts indicat en index, on symbol es un array de 2 dimensions i index es un enter


def lcomp(symbol,index):
	d=0
	if index==1 or index==0:
		L=0
	else:
		for i in range(index-1):
			d=d+math.sqrt(((symbol[i+1,0]-symbol[i,0])**2)+((symbol[i+1,1]-symbol[i,1])**2))
		L=d
	return L
	
#dista: Torna la distancia entre el segment entre (x1,y1) i (x2,y2)	i el punt (x3,y3), on x1, y1, x2, y2, x3 i y3 son floats
	
def dista(x1,y1, x2,y2, x3,y3):
		px = x2-x1
		py = y2-y1
		something = px*px + py*py
		if something==0:
			something=0.0000001
		u =  ((x3 - x1) * px + (y3 - y1) * py) / float(something)
		if u > 1:
			u = 1
		elif u < 0:
			u = 0
		x = x1 + u * px
		y = y1 + u * py
		dx = x - x3
		dy = y - y3
		dist = math.sqrt(dx*dx + dy*dy)
		return dist
