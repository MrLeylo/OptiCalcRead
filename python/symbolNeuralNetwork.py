#!/usr/bin/env python

import pytemplate as temp
import operator as op
import numpy as np
from pybrain.utilities import percentError
from pybrain.datasets import ClassificationDataSet as clds
from pybrain.tools.shortcuts import buildNetwork
from pybrain.structure.modules import SoftmaxLayer
from pybrain.supervised.trainers import BackpropTrainer

symboldB,tagClassification,averages=temp.readTemplate()
genTags={}
for character in tagClassification:
	if character[:-1] not in genTags:
		genTags[character[:-1]]=[]
	genTags[character[:-1]].append([character,len(tagClassification[character])])
for onlySym in genTags:
	for i in range(len(genTags[onlySym])):
		if genTags[onlySym][i][1]<0.05*sum([genTags[onlySym][caseID][1] for caseID in range(len(genTags[onlySym]))]):
			del tagClassification[genTags[onlySym][i][0]]
			del averages[genTags[onlySym][i][0]]
references={}
charCo=0
dataset=clds(270,1,len(tagClassification))
for character in tagClassification:
	references[character]=charCo
	charCo+=1
	while tagClassification[character][0].tE.shape[0]<3:
		print character
		for i in range(len(tagClassification[character])):
			tagClassification[character][i].liS=np.concatenate((tagClassification[character][i].liS,[tagClassification[character][i].liS[len(tagClassification[character][i].liS)-1]]),axis=0)
			tagClassification[character][i].accAngle=np.concatenate((tagClassification[character][i].accAngle,[tagClassification[character][i].accAngle[len(tagClassification[character][i].accAngle)-1]]),axis=0)
			tagClassification[character][i].quadraticError=np.concatenate((tagClassification[character][i].quadraticError,[tagClassification[character][i].quadraticError[len(tagClassification[character][i].quadraticError)-1]]),axis=0)
			tagClassification[character][i].relStrokeLength=np.concatenate((tagClassification[character][i].relStrokeLength,[tagClassification[character][i].relStrokeLength[len(tagClassification[character][i].relStrokeLength)-1]]),axis=0)
			tagClassification[character][i].coG=np.concatenate((tagClassification[character][i].coG,[tagClassification[character][i].coG[len(tagClassification[character][i].coG)-1]]),axis=0)
			tagClassification[character][i].tE=np.concatenate((tagClassification[character][i].tE,[tagClassification[character][i].tE[len(tagClassification[character][i].tE)-1]]),axis=0)
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
for character in tagClassification:
	for mostra in tagClassification[character]:
		dataset.addSample(np.concatenate((np.ravel(mostra.Coord),mostra.LP,mostra.turningAngle,mostra.turningAngleDifference,mostra.liS,mostra.accAngle,mostra.quadraticError,mostra.relStrokeLength,np.ravel(mostra.coG),np.ravel(mostra.Style)),0),references[character])
tstdata,trndata=dataset.splitWithProportion(0.25)
trndata._convertToOneOfMany()
tstdata._convertToOneOfMany()
print 'Building Network.....'
fnn=buildNetwork(trndata.indim,5,trndata.outdim,outclass=SoftmaxLayer)
print 'Training system.....'
trainer=BackpropTrainer(fnn,dataset=trndata,momentum=0.1,verbose=True,weightdecay=0.01)
for i in range(5):
	trainer.trainEpochs(1)
	trnresult = percentError(trainer.testOnClassData(),trndata['class'])
	tstresult = percentError(trainer.testOnClassData(dataset=tstdata),tstdata['class'])
	print 'epoch: ',trainer.totalepochs,'train error: ',trnresult,'test error: ', tstresult


		
	
