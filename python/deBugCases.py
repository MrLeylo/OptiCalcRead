#!/usr/bin/env python
import pytemplate as temp
import symbolPreprocessing as spp
import numpy as np
import matplotlib.pyplot as plt

#Script per inspeccionar algun simbol de la base de dades

symboldB,tagClassification,averages=temp.readTemplate()
colors=['g-','b-','y-','r-']
lletra='\ldots3'
fig=plt.figure(0)
for cara in averages:
	print cara
fig.canvas.set_window_title(lletra)
for j in range(averages[lletra].tE.shape[0]):
	if j==0:
		ini=-1
	else:
		ini=averages[lletra].tE[j-1]
	plt.plot(averages[lletra].Coord[range(ini+1,int(averages[lletra].tE[j])+1),0],-averages[lletra].Coord[range(ini+1,int(averages[lletra].tE[j])+1),1],colors[j%4])
print averages[lletra].Coord
print averages[lletra].tE
c=1
for mostra in tagClassification[lletra]:
	print mostra.Coord
	print mostra.tE
	plt.figure(c)
	for j in range(mostra.tE.shape[0]):
		if j==0:
			ini=-1
		else:
			ini=mostra.tE[j-1]
		plt.plot(mostra.Coord[range(ini+1,int(mostra.tE[j])+1),0],-mostra.Coord[range(ini+1,int(mostra.tE[j])+1),1],colors[j%4])
		plt.plot(mostra.Coord[ini+1,0],-mostra.Coord[ini+1,1],'r*')
	c+=1
	plt.show()
#valids=[0,1,2,3,8,12,20,24,29,30,34,35,42,43,58,59,61]
#averageCoord=np.zeros([50,2],np.float64)
#plt.figure(1)
#for i in range(averageCoord.shape[0]):
#	averageCoord[i,0]=np.mean([tagClassification[lletra][valid].Coord[i,0] for valid in valids])
#	averageCoord[i,1]=np.mean([tagClassification[lletra][valid].Coord[i,1] for valid in valids])
#for j in range(tagClassification[lletra][0].tE.shape[0]):
#	if j==0:
#		ini=-1
#	else:
#		ini=tagClassification[lletra][0].tE[j-1]
#	plt.plot(averageCoord[range(ini+1,int(tagClassification[lletra][0].tE[j])+1),0],-averageCoord[range(ini+1,int(tagClassification[lletra][0].tE[j])+1),1],colors[j%4])
#	plt.plot(averageCoord[ini+1,0],-averageCoord[ini+1,1],'r*')
plt.show()
