#!/usr/bin/env python
import pytemplate as temp
import matplotlib.pyplot as plt

#Script per actualitzar els simbols i els templates segons la base de dades i representar els templates

temp.templateGenerator()
symboldB,tagClassification,averages=temp.readTemplate()
genTags={}		#Busca el significat independent de cada caracter i si la proporcio del caracter respecte el significat independent es molt baixa ho considera soroll i elimina el caracter
for character in tagClassification:
	if character[:-1] not in genTags:
		genTags[character[:-1]]=[]
	genTags[character[:-1]].append([character,len(tagClassification[character])])
for onlySym in genTags:
	for i in range(len(genTags[onlySym])):
		if genTags[onlySym][i][1]<0.06*sum([genTags[onlySym][caseID][1] for caseID in range(len(genTags[onlySym]))]):
			del tagClassification[genTags[onlySym][i][0]]
			del averages[genTags[onlySym][i][0]]
c=0
colors=['g-','b-','y-','r-']
for lletra in averages:
	fig=plt.figure(c)
	fig.canvas.set_window_title(lletra)
	c+=1
	for j in range(averages[lletra].tE.shape[0]):
		if j==0:
			ini=-1
		else:
			ini=averages[lletra].tE[j-1]
		plt.plot(averages[lletra].Coord[range(ini+1,int(averages[lletra].tE[j])+1),0],-averages[lletra].Coord[range(ini+1,int(averages[lletra].tE[j])+1),1],colors[j%4])
plt.show()
