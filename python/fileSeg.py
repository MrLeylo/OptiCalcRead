import numpy as np
import math
import skimage
from skimage import morphology
from skimage import measure
from scipy import ndimage as ndi
import matplotlib.pyplot as plt
import SClass


#segment: torna els grups de traces que formen els simbols

def segment(coordinates,byAxis,difs):
	[x,y]=byAxis
	[difX,difY]=difs
	seguits=[]
	#Monta una imatge amb les traces, amb un gruix fix segons el numero de traces, per analitzar si al creuar-se s'han d'agrupar en un sol simbol
	structel2=np.array([[1 for k in range(int(math.sqrt(100/coordinates.shape[0]))+1)] for l in range(int(math.sqrt(100/coordinates.shape[0]))+1)], np.int32)
	for i in range(coordinates.shape[0]-1):
		seguits.append(-1)
		numO=1
		while numO==1:
			seguits[i]=seguits[i]+1
			imgAn=np.zeros((51, 501))
			for j in range (coordinates.shape[1]-1):
				#Segons si les coordenades avancen o retrocedeixen ordena l'omplerta de la imatge
				if (50*(coordinates[i+seguits[i],j,0]-min(x))/difX)>(50*(coordinates[i+seguits[i],j+1,0]-min(x))/difX):
					factx1=1
				else:
					factx1=0
				if (50*(coordinates[i+seguits[i],j,1]-min(y))/difY)>(50*(coordinates[i+seguits[i],j+1,1]-min(y))/difY):
					facty1=1
				else:
					facty1=0
				if (50*(coordinates[i+seguits[i]+1,j,0]-min(x))/difX)>(50*(coordinates[i+seguits[i]+1,j+1,0]-min(x))/difX):
					factx2=1
				else:
					factx2=0
				if (50*(coordinates[i+seguits[i]+1,j,1]-min(y))/difY)>(50*(coordinates[i+seguits[i]+1,j+1,1]-min(y))/difY):
					facty2=1
				else:
					facty2=0
				imgAn[np.array(range(int(((50*(coordinates[i+seguits[i],j+facty1,1]-min(y))/difY))),int(((50*(coordinates[i+seguits[i],j+1-facty1,1]-min(y))/difY)+1))),int),int(((500*(coordinates[i+seguits[i],j+factx1,0]-min(x))/difX))):int(((500*(coordinates[i+seguits[i],j+1-factx1,0]-min(x))/difX)+1))] = 1
				imgAn[np.array(range(int(((50*(coordinates[i+seguits[i]+1,j+facty2,1]-min(y))/difY))),int(((50*(coordinates[i+seguits[i]+1,j+1-facty2,1]-min(y))/difY)+1))),int),int(((500*(coordinates[i+seguits[i]+1,j+factx2,0]-min(x))/difX))):int(((500*(coordinates[i+seguits[i]+1,j+1-factx2,0]-min(x))/difX)+1))] = 1
			dilated=skimage.morphology.binary_dilation(imgAn,structel2)
			label_image = ndi.measurements.label(dilated)
			#Mira si hi ha mes d'un objecte separat entre 2 traces, si nomes queda un ho guarda com a traces dins un mateix simbol
			numO=np.amax(label_image[0])
			if (i+seguits[i])==coordinates.shape[0]-2:
				if numO==1:
					seguits[i]=seguits[i]+1
				numO=2
		del imgAn
	#Defineix el seguit de simbols segons el seu numero de traces
	seguits.append(0)
	qS=[]
	nS=0
	disc=0
	for i in range(coordinates.shape[0]):
		if disc==0:
			qS.append(1)
			while seguits[i+qS[nS]-1]!=0:
				qS[nS]=qS[nS]+seguits[i+qS[nS]-1]
			disc=qS[nS]-1
			nS=nS+1
		else:
			disc=disc-1
	print 'Traces grouped as'
	print qS
	#Representa i agrupa les traces en simbols
	cc=0
	cd=0
	tam=max(qS)*coordinates.shape[1]
	simbols=[]
	for i in range(len(qS)):
		ce=cd
		finished=0
		symCoordinates=np.zeros([tam,2],np.float64)
		tends=np.zeros([qS[i]],np.float64)
		for j in range(tam):
			if finished==0:
				symCoordinates[j]=coordinates[cd,cc]
				cc=cc+1
				if cc==coordinates.shape[1]:
					tends[cd-ce]=j
					cd=cd+1
					cc=0
					if qS[i]==(cd-ce):
						finished=1
			else:
				symCoordinates[j]=coordinates[cd-1,(coordinates.shape[1])-1]
		tends[tends.shape[0]-1]=symCoordinates.shape[0]-1
		nsi=SClass.Symbol(symCoordinates,tends)
		simbols.append(nsi)
	print 'Data segmented.'
	fig=plt.figure(2)
	fig.canvas.set_window_title('Regions')
	for i in range(len(simbols)):
		for j in range(simbols[i].tE.shape[0]):
			if j==0:
				ini=-1
			else:
				ini=int(simbols[i].tE[j-1])
			lineG,=plt.plot(simbols[i].Coord[range(ini+1,int(simbols[i].tE[j])+1),0],-simbols[i].Coord[range(ini+1,int(simbols[i].tE[j])+1),1],'-')
	return simbols,qS
