import pytemplate as temp
import ink2Traces
import drawTraces
import fileSeg
import drawRegions
import SClass as nsi
import symbolPreprocessing as spp
import os
import copy
from pprint import pprint

#Script per comparar les features entre 2 casos

symboldB,tagClassification,average=temp.readTemplate()
genTags={}
for character in tagClassification:
	if character[:-1] not in genTags:
		genTags[character[:-1]]=[]
	genTags[character[:-1]].append([character,len(tagClassification[character])])
for onlySym in genTags:
	for i in range(len(genTags[onlySym])):
		if genTags[onlySym][i][1]<0.05*sum([genTags[onlySym][caseID][1] for caseID in range(len(genTags[onlySym]))]):
			del tagClassification[genTags[onlySym][i][0]]
			del average[genTags[onlySym][i][0]]
filenom='algb02.inkml'
Coord=ink2Traces.i2t(filenom)		#Extreure les coordenades donades pel fitxer
img,byAxis,difs=drawTraces.draw(Coord)		#Mostrar resultat obtingut i montar imatge
Symb,groupedStrokes=fileSeg.segment(Coord,byAxis,difs)		#Agrupar traces en simbols
Symb=drawRegions.drawS(Symb)
symbol=spp.preprocessing([Symb[1]])
symbol[0].computeFeatures()
#pprint(vars(symbol[0]))
#for i in range(len(symbol[0].LP)):
#	print str(symbol[0].LP[i])+', '
auxAverage=copy.deepcopy(average)
auxAverage['21'].computeFeatures()
auxAverage['r1'].computeFeatures()
os.remove('features.txt')
report=open('features.txt','w')
report.write('||||||||||||||||||||||||||||||||||||||||||||||||||||||\n')
report.write('LP:\n')
for i in range(len(tagClassification['21'])):
	for j in range(len(tagClassification['21'][i].LP)):
		report.write(str(tagClassification['21'][i].LP[j])+', ')
	report.write('\n')
report.write('--------------------------------------------------\n')
for i in range(len(tagClassification['r1'])):
	for j in range(len(tagClassification['r1'][i].LP)):
		report.write(str(tagClassification['r1'][i].LP[j])+', ')
	report.write('\n')
report.write('--------------------------------------------------\n')
for i in range(len(average['21'].LP)):
	report.write(str(average['21'].LP[i])+', ')
report.write('\n--------------------------------------------------\n')
for i in range(len(average['r1'].LP)):
	report.write(str(average['r1'].LP[i])+', ')
report.write('\n--------------------------------------------------\n')
for i in range(len(auxAverage['21'].LP)):
	report.write(str(auxAverage['21'].LP[i])+', ')
report.write('\n--------------------------------------------------\n')
for i in range(len(auxAverage['r1'].LP)):
	report.write(str(auxAverage['r1'].LP[i])+', ')
report.write('\n--------------------------------------------------\n')
for i in range(len(symbol[0].LP)):
	report.write(str(symbol[0].LP[i])+', ')
report.write('\n||||||||||||||||||||||||||||||||||||||||||||||||||||||\n')
report.write('accAngle:\n')
for i in range(len(tagClassification['21'])):
	for j in range(len(tagClassification['21'][i].accAngle)):
		report.write(str(tagClassification['21'][i].accAngle[j])+', ')
	report.write('\n')
report.write('--------------------------------------------------\n')
for i in range(len(tagClassification['r1'])):
	for j in range(len(tagClassification['r1'][i].accAngle)):
		report.write(str(tagClassification['r1'][i].accAngle[j])+', ')
	report.write('\n')
report.write('--------------------------------------------------\n')
for i in range(len(average['21'].accAngle)):
	report.write(str(average['21'].accAngle[i])+', ')
report.write('\n--------------------------------------------------\n')
for i in range(len(average['r1'].accAngle)):
	report.write(str(average['r1'].accAngle[i])+', ')
report.write('\n--------------------------------------------------\n')
for i in range(len(auxAverage['21'].accAngle)):
	report.write(str(auxAverage['21'].accAngle[i])+', ')
report.write('\n--------------------------------------------------\n')
for i in range(len(auxAverage['r1'].accAngle)):
	report.write(str(auxAverage['r1'].accAngle[i])+', ')
report.write('\n--------------------------------------------------\n')
for i in range(len(symbol[0].accAngle)):
	report.write(str(symbol[0].accAngle[i])+', ')
report.write('\n||||||||||||||||||||||||||||||||||||||||||||||||||||||\n')
report.write('coG:\n')
for i in range(len(tagClassification['21'])):
	for j in range(len(tagClassification['21'][i].coG)):
		report.write(str(tagClassification['21'][i].coG[j])+', ')
	report.write('\n')
report.write('--------------------------------------------------\n')
for i in range(len(tagClassification['r1'])):
	for j in range(len(tagClassification['r1'][i].coG)):
		report.write(str(tagClassification['r1'][i].coG[j])+', ')
	report.write('\n')
report.write('--------------------------------------------------\n')
for i in range(len(average['21'].coG)):
	report.write(str(average['21'].coG[i])+', ')
report.write('\n--------------------------------------------------\n')
for i in range(len(average['r1'].coG)):
	report.write(str(average['r1'].coG[i])+', ')
report.write('\n--------------------------------------------------\n')
for i in range(len(auxAverage['21'].coG)):
	report.write(str(auxAverage['21'].coG[i])+', ')
report.write('\n--------------------------------------------------\n')
for i in range(len(auxAverage['r1'].coG)):
	report.write(str(auxAverage['r1'].coG[i])+', ')
report.write('\n--------------------------------------------------\n')
for i in range(len(symbol[0].coG)):
	report.write(str(symbol[0].coG[i])+', ')
report.write('\n||||||||||||||||||||||||||||||||||||||||||||||||||||||\n')
report.write('liS:\n')
for i in range(len(tagClassification['21'])):
	for j in range(len(tagClassification['21'][i].liS)):
		report.write(str(tagClassification['21'][i].liS[j])+', ')
	report.write('\n')
report.write('--------------------------------------------------\n')
for i in range(len(tagClassification['r1'])):
	for j in range(len(tagClassification['r1'][i].liS)):
		report.write(str(tagClassification['r1'][i].liS[j])+', ')
	report.write('\n')
report.write('--------------------------------------------------\n')
for i in range(len(average['21'].liS)):
	report.write(str(average['21'].liS[i])+', ')
report.write('\n--------------------------------------------------\n')
for i in range(len(average['r1'].liS)):
	report.write(str(average['r1'].liS[i])+', ')
report.write('\n--------------------------------------------------\n')
for i in range(len(auxAverage['21'].liS)):
	report.write(str(auxAverage['21'].liS[i])+', ')
report.write('\n--------------------------------------------------\n')
for i in range(len(auxAverage['r1'].liS)):
	report.write(str(auxAverage['r1'].liS[i])+', ')
report.write('\n--------------------------------------------------\n')
for i in range(len(symbol[0].liS)):
	report.write(str(symbol[0].liS[i])+', ')
report.write('\n||||||||||||||||||||||||||||||||||||||||||||||||||||||\n')
report.write('quadraticError:\n')
for i in range(len(tagClassification['21'])):
	for j in range(len(tagClassification['21'][i].quadraticError)):
		report.write(str(tagClassification['21'][i].quadraticError[j])+', ')
	report.write('\n')
for i in range(len(tagClassification['r1'])):
	for j in range(len(tagClassification['r1'][i].quadraticError)):
		report.write(str(tagClassification['r1'][i].quadraticError[j])+', ')
	report.write('\n')
report.write('--------------------------------------------------\n')
for i in range(len(average['21'].quadraticError)):
	report.write(str(average['21'].quadraticError[i])+', ')
report.write('\n--------------------------------------------------\n')
for i in range(len(average['r1'].quadraticError)):
	report.write(str(average['r1'].quadraticError[i])+', ')
report.write('\n--------------------------------------------------\n')
for i in range(len(auxAverage['21'].quadraticError)):
	report.write(str(auxAverage['21'].quadraticError[i])+', ')
report.write('\n--------------------------------------------------\n')
for i in range(len(auxAverage['r1'].quadraticError)):
	report.write(str(auxAverage['r1'].quadraticError[i])+', ')
report.write('\n--------------------------------------------------\n')
for i in range(len(symbol[0].quadraticError)):
	report.write(str(symbol[0].quadraticError[i])+', ')
report.write('\n||||||||||||||||||||||||||||||||||||||||||||||||||||||\n')
report.write('relStrokeLength:\n')
for i in range(len(tagClassification['21'])):
	for j in range(len(tagClassification['21'][i].relStrokeLength)):
		report.write(str(tagClassification['21'][i].relStrokeLength[j])+', ')
	report.write('\n')
report.write('--------------------------------------------------\n')
for i in range(len(tagClassification['r1'])):
	for j in range(len(tagClassification['r1'][i].relStrokeLength)):
		report.write(str(tagClassification['r1'][i].relStrokeLength[j])+', ')
	report.write('\n')
report.write('--------------------------------------------------\n')
for i in range(len(average['21'].relStrokeLength)):
	report.write(str(average['21'].relStrokeLength[i])+', ')
report.write('\n--------------------------------------------------\n')
for i in range(len(average['r1'].relStrokeLength)):
	report.write(str(average['r1'].relStrokeLength[i])+', ')
report.write('\n--------------------------------------------------\n')
for i in range(len(auxAverage['21'].relStrokeLength)):
	report.write(str(auxAverage['21'].relStrokeLength[i])+', ')
report.write('\n--------------------------------------------------\n')
for i in range(len(auxAverage['r1'].relStrokeLength)):
	report.write(str(auxAverage['r1'].relStrokeLength[i])+', ')
report.write('\n--------------------------------------------------\n')
for i in range(len(symbol[0].relStrokeLength)):
	report.write(str(symbol[0].relStrokeLength[i])+', ')
report.write('\n||||||||||||||||||||||||||||||||||||||||||||||||||||||\n')
report.write('turningAngle:\n')
for i in range(len(tagClassification['21'])):
	for j in range(len(tagClassification['21'][i].turningAngle)):
		report.write(str(tagClassification['21'][i].turningAngle[j])+', ')
	report.write('\n')
report.write('--------------------------------------------------\n')
for i in range(len(tagClassification['r1'])):
	for j in range(len(tagClassification['r1'][i].turningAngle)):
		report.write(str(tagClassification['r1'][i].turningAngle[j])+', ')
	report.write('\n')
report.write('--------------------------------------------------\n')
for i in range(len(average['21'].turningAngle)):
	report.write(str(average['21'].turningAngle[i])+', ')
report.write('\n--------------------------------------------------\n')
for i in range(len(average['r1'].turningAngle)):
	report.write(str(average['r1'].turningAngle[i])+', ')
report.write('\n--------------------------------------------------\n')
for i in range(len(auxAverage['21'].turningAngle)):
	report.write(str(auxAverage['21'].turningAngle[i])+', ')
report.write('\n--------------------------------------------------\n')
for i in range(len(auxAverage['r1'].turningAngle)):
	report.write(str(auxAverage['r1'].turningAngle[i])+', ')
report.write('\n--------------------------------------------------\n')
for i in range(len(symbol[0].turningAngle)):
	report.write(str(symbol[0].turningAngle[i])+', ')
report.write('\n||||||||||||||||||||||||||||||||||||||||||||||||||||||\n')
report.write('turningAngleDifference:\n')
for i in range(len(tagClassification['21'])):
	for j in range(len(tagClassification['21'][i].turningAngleDifference)):
		report.write(str(tagClassification['21'][i].turningAngleDifference[j])+', ')
	report.write('\n')
report.write('--------------------------------------------------\n')
for i in range(len(tagClassification['r1'])):
	for j in range(len(tagClassification['r1'][i].turningAngleDifference)):
		report.write(str(tagClassification['r1'][i].turningAngleDifference[j])+', ')
	report.write('\n')
report.write('--------------------------------------------------\n')
for i in range(len(average['21'].turningAngleDifference)):
	report.write(str(average['21'].turningAngleDifference[i])+', ')
report.write('\n--------------------------------------------------\n')
for i in range(len(average['r1'].turningAngleDifference)):
	report.write(str(average['r1'].turningAngleDifference[i])+', ')
report.write('\n--------------------------------------------------\n')
for i in range(len(auxAverage['21'].turningAngleDifference)):
	report.write(str(auxAverage['21'].turningAngleDifference[i])+', ')
report.write('\n--------------------------------------------------\n')
for i in range(len(auxAverage['r1'].turningAngleDifference)):
	report.write(str(auxAverage['r1'].turningAngleDifference[i])+', ')
report.write('\n--------------------------------------------------\n')
for i in range(len(symbol[0].turningAngleDifference)):
	report.write(str(symbol[0].turningAngleDifference[i])+', ')
report.close()
	

