#!/usr/bin/env python
import SClass as nsi
import pyStructural as stru
import sys
import ink2Traces
import drawTraces
import fileSeg
import drawRegions
import matplotlib.pyplot as plt

#Script per provar pyStructural amb casos ben etiquetats

test=5
if test==1:
	testCase=[nsi.Symbol([0,0],[0]),nsi.Symbol([0,0],[0]),nsi.Symbol([0,0],[0]),nsi.Symbol([0,0],[0]),nsi.Symbol([0,0],[0]),nsi.Symbol([0,0],[0]),nsi.Symbol([0,0],[0]),nsi.Symbol([0,0],[0]),nsi.Symbol([0,0],[0]),nsi.Symbol([0,0],[0]),nsi.Symbol([0,0],[0]),nsi.Symbol([0,0],[0]),nsi.Symbol([0,0],[0]),nsi.Symbol([0,0],[0]),nsi.Symbol([0,0],[0]),nsi.Symbol([0,0],[0])]
	testCase[0].bBox=[0.75,4,1,3.5]
	testCase[1].bBox=[1.75,2.25,0.75,1.25]
	testCase[2].bBox=[2,2.25,3.5,4.5]
	testCase[3].bBox=[3,3.5,3.75,4.5]
	testCase[4].bBox=[2.5,2.75,3.75,4.1]
	testCase[5].bBox=[4.5,5,1.25,3.5]
	testCase[6].bBox=[5.5,6.75,2,3.25]
	testCase[7].bBox=[7,7.5,1.5,2]
	testCase[8].bBox=[7.5,8,1.5,2]
	testCase[9].bBox=[7,7.25,2.75,3.25]
	testCase[10].bBox=[8.25,9.25,2,2.75]
	testCase[11].bBox=[10,11,1.75,3.9]
	testCase[12].bBox=[11,11.5,1.25,1.75]
	testCase[13].bBox=[11.75,12,1.25,2]
	testCase[14].bBox=[11.4,11.6,2.75,3.5]
	testCase[15].bBox=[12.5,12.75,1,4]
	for ntc in range(len(testCase)):
		testCase[ntc].center=[(testCase[ntc].bBox[0]+testCase[ntc].bBox[1])/2.0,(testCase[ntc].bBox[2]+testCase[ntc].bBox[3])/2.0]
	for ntc in range(len(testCase)):
		plt.plot([testCase[ntc].bBox[0],testCase[ntc].bBox[1]],[-testCase[ntc].bBox[2],-testCase[ntc].bBox[2]],'r-')
		plt.plot([testCase[ntc].bBox[1],testCase[ntc].bBox[1]],[-testCase[ntc].bBox[2],-testCase[ntc].bBox[3]],'r-')
		plt.plot([testCase[ntc].bBox[1],testCase[ntc].bBox[0]],[-testCase[ntc].bBox[3],-testCase[ntc].bBox[3]],'r-')
		plt.plot([testCase[ntc].bBox[0],testCase[ntc].bBox[0]],[-testCase[ntc].bBox[3],-testCase[ntc].bBox[2]],'r-')
	#plt.show()
	tags=['\sum1','n1','i2','01','=2','(1','x2','21','x2','i2','+2','y1','21','y1','i2',')1']
	dominations,laTexExpr= stru.expreBuilder(testCase,tags)
	plt.figure(5)
	plt.text(0,0.5,'$%s$'%laTexExpr,fontsize=30)
	plt.show()
elif test==2:
	filenom=sys.argv[1]		#Llegir el nom del fitxer InkML de la consola
	Coord=ink2Traces.i2t(filenom)		#Extreure les coordenades donades pel fitxer
	img,byAxis,difs=drawTraces.draw(Coord)		#Mostrar resultat obtingut i montar imatge
	Symb,groupedStrokes=fileSeg.segment(Coord,byAxis,difs)		#Agrupar traces en simbols
	Symb=drawRegions.drawS(Symb)
	testCase=Symb
	plt.figure(4)
	for ntc in range(len(testCase)):
		plt.plot([testCase[ntc].bBox[0],testCase[ntc].bBox[1]],[-testCase[ntc].bBox[2],-testCase[ntc].bBox[2]],'r-')
		plt.plot([testCase[ntc].bBox[1],testCase[ntc].bBox[1]],[-testCase[ntc].bBox[2],-testCase[ntc].bBox[3]],'r-')
		plt.plot([testCase[ntc].bBox[1],testCase[ntc].bBox[0]],[-testCase[ntc].bBox[3],-testCase[ntc].bBox[3]],'r-')
		plt.plot([testCase[ntc].bBox[0],testCase[ntc].bBox[0]],[-testCase[ntc].bBox[3],-testCase[ntc].bBox[2]],'r-')
	tags=['a1','21','+2','b1','21','\div1','a1','+2','b1','+2','\div1','b1','21','+2','c1','21','b1','+2','c1','+2','\div1','c1','21','+2','a1','21','c1','+2','a1','\gt1','-1','a1','+2','b1','+2','c1']
	dominations,laTexExpr= stru.expreBuilder(testCase,tags)
	plt.figure(5)
	plt.text(0,0.5,'$%s$'%laTexExpr,fontsize=30)
	plt.show()
elif test==3:
	filenom=sys.argv[1]		#Llegir el nom del fitxer InkML de la consola
	Coord=ink2Traces.i2t(filenom)		#Extreure les coordenades donades pel fitxer
	img,byAxis,difs=drawTraces.draw(Coord)		#Mostrar resultat obtingut i montar imatge
	Symb,groupedStrokes=fileSeg.segment(Coord,byAxis,difs)		#Agrupar traces en simbols
	Symb=drawRegions.drawS(Symb)
	testCase=Symb
	plt.figure(4)
	for ntc in range(len(testCase)):
		plt.plot([testCase[ntc].bBox[0],testCase[ntc].bBox[1]],[-testCase[ntc].bBox[2],-testCase[ntc].bBox[2]],'r-')
		plt.plot([testCase[ntc].bBox[1],testCase[ntc].bBox[1]],[-testCase[ntc].bBox[2],-testCase[ntc].bBox[3]],'r-')
		plt.plot([testCase[ntc].bBox[1],testCase[ntc].bBox[0]],[-testCase[ntc].bBox[3],-testCase[ntc].bBox[3]],'r-')
		plt.plot([testCase[ntc].bBox[0],testCase[ntc].bBox[0]],[-testCase[ntc].bBox[3],-testCase[ntc].bBox[2]],'r-')
	tags=['(1','A2','-1','B1',')1','\\'+'times2','C1','-1','-1','(1','A3','\\'+'times2','C1',')1','-1','(1','B2','\\'+'times2','C1',')1']
	dominations,laTexExpr= stru.expreBuilder(testCase,tags)
	plt.figure(5)
	plt.text(0,0.5,'$%s$'%laTexExpr,fontsize=30)
	plt.show()
elif test==4:
	filenom=sys.argv[1]		#Llegir el nom del fitxer InkML de la consola
	Coord=ink2Traces.i2t(filenom)		#Extreure les coordenades donades pel fitxer
	img,byAxis,difs=drawTraces.draw(Coord)		#Mostrar resultat obtingut i montar imatge
	Symb,groupedStrokes=fileSeg.segment(Coord,byAxis,difs)		#Agrupar traces en simbols
	Symb=drawRegions.drawS(Symb)
	testCase=Symb
	plt.figure(4)
	for ntc in range(len(testCase)):
		plt.plot([testCase[ntc].bBox[0],testCase[ntc].bBox[1]],[-testCase[ntc].bBox[2],-testCase[ntc].bBox[2]],'r-')
		plt.plot([testCase[ntc].bBox[1],testCase[ntc].bBox[1]],[-testCase[ntc].bBox[2],-testCase[ntc].bBox[3]],'r-')
		plt.plot([testCase[ntc].bBox[1],testCase[ntc].bBox[0]],[-testCase[ntc].bBox[3],-testCase[ntc].bBox[3]],'r-')
		plt.plot([testCase[ntc].bBox[0],testCase[ntc].bBox[0]],[-testCase[ntc].bBox[3],-testCase[ntc].bBox[2]],'r-')
	tags=['(1','31','81','\\'+'times2','(1','21','81','-1','11','21','61',')1',')1','-1','72','01','\lt1','-1','-1','31','72','91','31']
	dominations,laTexExpr= stru.expreBuilder(testCase,tags)
	plt.figure(5)
	plt.text(0,0.5,'$%s$'%laTexExpr,fontsize=30)
	plt.show()
elif test==5:
	filenom=sys.argv[1]		#Llegir el nom del fitxer InkML de la consola
	Coord=ink2Traces.i2t(filenom)		#Extreure les coordenades donades pel fitxer
	img,byAxis,difs=drawTraces.draw(Coord)		#Mostrar resultat obtingut i montar imatge
	Symb,groupedStrokes=fileSeg.segment(Coord,byAxis,difs)		#Agrupar traces en simbols
	Symb=drawRegions.drawS(Symb)
	testCase=Symb
	plt.figure(4)
	for ntc in range(len(testCase)):
		plt.plot([testCase[ntc].bBox[0],testCase[ntc].bBox[1]],[-testCase[ntc].bBox[2],-testCase[ntc].bBox[2]],'r-')
		plt.plot([testCase[ntc].bBox[1],testCase[ntc].bBox[1]],[-testCase[ntc].bBox[2],-testCase[ntc].bBox[3]],'r-')
		plt.plot([testCase[ntc].bBox[1],testCase[ntc].bBox[0]],[-testCase[ntc].bBox[3],-testCase[ntc].bBox[3]],'r-')
		plt.plot([testCase[ntc].bBox[0],testCase[ntc].bBox[0]],[-testCase[ntc].bBox[3],-testCase[ntc].bBox[2]],'r-')
	tags=['\phi1','21','21','=2','\phi1','21','11']
	dominations,laTexExpr= stru.expreBuilder(testCase,tags)
	plt.figure(5)
	plt.text(0,0.5,'$%s$'%laTexExpr,fontsize=30)
	plt.show()
