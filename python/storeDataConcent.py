#!/usr/bin/env python

import pytemplate as temp
import featurePonderation as fP

#Script per guardar les concentracions de les diferents features

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
specialByBboxSize=[averages['i2'],averages['\ldots3'],averages['.1'],averages['/1'],averages['-1'],averages['!2']]
del averages['i2'],averages['\ldots3'],averages['.1'],averages['/1'],averages['-1'],averages['!2']
fP.findConcentration(tagClassification)
#weights=fP.ponderateByConcentration()
