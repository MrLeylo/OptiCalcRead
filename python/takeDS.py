import unip2Traces as uptr
import SClass as nsi
import numpy as np
import matplotlib.pyplot as plt

#MountDS:torna la base de dades de l'arxiu de nom name si se li especifica UNIPEN a whichdB

def mountDS(name,whichdB):
	if whichdB=='UNIPEN':
		fileTags=open(name,"r")
		linea='o'
		symbolsdB=[]
		while linea!='':
			linea=fileTags.readline()
			if '.INCLUDE' in linea:
				espai=linea.index(' ')
				incPath='UnipenData/include/'+linea[espai+1:].rstrip('\n')
				print incPath
				trainTraces=uptr.u2t(incPath)
			elif '.SEGMENT CHARACTER' in linea:
				espaiFi=linea.index(' ',19)
				segSel=linea[19:espaiFi]
				if '-' in segSel:
					numOfTr=segSel.count('-')+1
					trInd=[]
					longC=0
					tEnds=np.zeros([numOfTr],np.float64)
					for i in range(numOfTr):
						if i==0:
							prevI=-1
						if i==numOfTr-1:
							nowI=len(segSel)
						else:
							nowI=segSel.index('-',prevI+1)
						trInd.append(int(segSel[prevI+1:nowI]))
						prevI=nowI
						longC+=len(trainTraces[trInd[i]])
						tEnds[i]=longC-1
						if i==0:
							symCoord=np.array(trainTraces[trInd[0]],np.float64)
						else:
							symCoord=np.vstack((symCoord,np.asarray(trainTraces[trInd[i]])))
				else:
					trInd=[int(segSel)]
					longC=len(trainTraces[trInd[0]])
					tEnds=np.array([longC-1],np.float64)
					symCoord=np.array(trainTraces[trInd[0]],np.float64)
				mk1=linea.index('"')+1
				mk2=linea.index('"',mk1)
				etiqueta=linea[mk1:mk2]
				symbolsdB.append(nsi.taggedSymbol(symCoord,tEnds,etiqueta))
	#elif whichdB=='CROHME':
		
	return symbolsdB
