import pytemplate as temp
import pyDom as dom
import copy
import numpy as np
import SClass as nsi
import symbolPreprocessing as spp

#ExpreBuilder:De la llista de simbols i la llista d'etiquetes retorna una expressio en Tex

def expreBuilder(symbols,tag):
	#Els simbols i les etiquetes s'ordenen segons la ubicacio de les bounding box d'esquerra a dreta
	print 'Solving expression structure..........'
	auxL=zip(symbols,tag)
	zs=sorted(auxL,key=lambda x: x[0].bBox[0])
	symbols,tag=map(list,zip(*zs))
	symbols,tag=reAssign(symbols,tag)
	#Es fixen les regions de cada simbol
	symbolTypeCatalog={'nonscripted':[['+','-','\\'+'times','/','=','\\'+'neq','\gt','\geq','\lt','\leq','\ldots','.','COMMA','!','\exists','\in','\\'+'forall','\\'+'rightarrow','(','[','\{','\infty']],'superscripted':[['\sin','\cos','\\'+'tan','\log','e','\pi'],['0','1','2','3','4','5','6','7','8','9']],'scripted':[['a','c','e','i','m','n','r','x','z','A','B','C','F','X','Y','\\'+'alpha','\\'+'beta','\gamma','\\'+'theta','\phi','\pm',')',']','\}'],['b','d','f','k','t','\\'+'int'],['g','j','p','y']],'sumlike':[['\sum','\pi']],'limlike':[['\lim']],'rootlike':[['\sqrt']],'barlike':[['\div']]}
	for sNum in range(len(symbols)):
		if tag[sNum][:-1] not in [v1 for vx in [v2 for vy in symbolTypeCatalog.values() for v2 in vy] for v1 in vx]:
			print tag[sNum][:-1],'not in database'
		else:
			if tag[sNum][:-1] in [v2 for vy in symbolTypeCatalog['nonscripted'] for v2 in vy]:
				symbols[sNum].setRegions('nosc','cent')
			elif tag[sNum][:-1] in [v2 for vy in symbolTypeCatalog['superscripted'] for v2 in vy]:
				if tag[sNum][:-1] in symbolTypeCatalog['superscripted'][0]:
					symbols[sNum].setRegions('supsc','cent')
				elif tag[sNum][:-1] in symbolTypeCatalog['superscripted'][1]:
					symbols[sNum].setRegions('supsc','asc')
			elif tag[sNum][:-1] in [v2 for vy in symbolTypeCatalog['scripted'] for v2 in vy]:
				if tag[sNum][:-1] in symbolTypeCatalog['scripted'][0]:
					symbols[sNum].setRegions('sc','cent')
				elif tag[sNum][:-1] in symbolTypeCatalog['scripted'][1]:
					symbols[sNum].setRegions('sc','asc')
				elif tag[sNum][:-1] in symbolTypeCatalog['scripted'][2]:
					symbols[sNum].setRegions('sc','desc')
			elif tag[sNum][:-1] in [v2 for vy in symbolTypeCatalog['sumlike'] for v2 in vy]:
				symbols[sNum].setRegions('slik','cent')
			elif tag[sNum][:-1] in [v2 for vy in symbolTypeCatalog['limlike'] for v2 in vy]:
				symbols[sNum].setRegions('llik','cent')
			elif tag[sNum][:-1] in [v2 for vy in symbolTypeCatalog['rootlike'] for v2 in vy]:
				symbols[sNum].setRegions('rlik','cent')
			elif tag[sNum][:-1] in [v2 for vy in symbolTypeCatalog['barlike'] for v2 in vy]:
				symbols[sNum].setRegions('blik','cent')
	#Casos especials
	for inspected in symbols:
		if inspected.tag[:-1]=='-':
			hasAbove=False
			hasBelow=False
			for s in symbols:
				if s.ref!=inspected.ref and s.centroid[0]>inspected.bBox[0] and s.centroid[0]<inspected.bBox[1]:
					if s.centroid[1]<inspected.centroid[1]:
						hasAbove=True
					else:
						hasBelow=True
			if hasAbove and hasBelow:
				inspected.tag='\div'+inspected.tag[-1:]
				inspected.setRegions('blik','cent')
		if inspected.tag[:-1]=='\div':
			hasAbove=False
			hasBelow=False
			for s in symbols:
				if s.ref!=inspected.ref and s.centroid[0]>inspected.bBox[0] and s.centroid[0]<inspected.bBox[1]:
					if s.centroid[1]<inspected.centroid[1]:
						hasAbove=True
					else:
						hasBelow=True
			if hasAbove==False and hasBelow==False:
				inspected.tag='-'+inspected.tag[-1:]
				inspected.setRegions('nosc','cent')	
	for symbol in symbols:
		if symbol.tag[:-1]=='-':
			symbol.bBox[2]=symbol.center[1]-((symbol.bBox[1]-symbol.bBox[0])/2)
			symbol.bBox[3]=symbol.center[1]+((symbol.bBox[1]-symbol.bBox[0])/2)
	dominations=[]
	#Es miren dominis directes
	for curSNum in range(len(symbols)):
		for candSNum in range(len(symbols)):
			if curSNum!=candSNum:
				if symbols[curSNum].kinds[0]=='blik':
					if symbols[candSNum].centroid[0]<symbols[curSNum].bBox[1] and symbols[candSNum].centroid[0]>symbols[curSNum].bBox[0]:
						if symbols[candSNum].centroid[1]<symbols[curSNum].centroid[1]:
							dominations.append(dom.hardDomination('above',symbols[curSNum],symbols[candSNum]))
						else:
							dominations.append(dom.hardDomination('below',symbols[curSNum],symbols[candSNum]))
				elif symbols[curSNum].kinds[0]=='supsc':
					if symbols[candSNum].centroid[0]<symbols[curSNum].outbBox[1] and symbols[candSNum].centroid[0]>symbols[curSNum].bBox[0] and symbols[candSNum].centroid[1]<symbols[curSNum].superThresh and symbols[candSNum].centroid[1]>symbols[curSNum].outbBox[2] and symbols[candSNum].bBox[3]<symbols[curSNum].bBox[3]:
						dominations.append(dom.hardDomination('superscript',symbols[curSNum],symbols[candSNum]))
				elif symbols[curSNum].kinds[0]=='sc':
					auxMarker=symbols[curSNum].bBox[0]
					if symbols[candSNum].centroid[0]<symbols[curSNum].outbBox[1] and symbols[candSNum].centroid[0]>auxMarker and symbols[candSNum].centroid[1]<symbols[curSNum].superThresh and symbols[candSNum].centroid[1]>symbols[curSNum].outbBox[2] and symbols[candSNum].bBox[3]<symbols[curSNum].bBox[3]:
						dominations.append(dom.hardDomination('superscript',symbols[curSNum],symbols[candSNum]))
					elif symbols[candSNum].centroid[0]<symbols[curSNum].outbBox[1] and symbols[candSNum].centroid[0]>symbols[curSNum].bBox[0] and symbols[candSNum].centroid[1]>symbols[curSNum].subThresh and symbols[candSNum].centroid[1]<symbols[curSNum].outbBox[3] and symbols[candSNum].bBox[2]>symbols[curSNum].bBox[2]:
						dominations.append(dom.hardDomination('subscript',symbols[curSNum],symbols[candSNum]))
				elif symbols[curSNum].kinds[0]=='slik':
					if symbols[candSNum].centroid[0]<symbols[curSNum].bBox[1] and symbols[candSNum].centroid[0]>symbols[curSNum].bBox[0] and symbols[candSNum].centroid[1]<symbols[curSNum].superThresh:
						dominations.append(dom.hardDomination('above',symbols[curSNum],symbols[candSNum]))
					elif symbols[candSNum].centroid[0]<symbols[curSNum].bBox[1] and symbols[candSNum].centroid[0]>symbols[curSNum].bBox[0] and symbols[candSNum].centroid[1]>symbols[curSNum].subThresh:
						dominations.append(dom.hardDomination('below',symbols[curSNum],symbols[candSNum]))
					elif symbols[candSNum].centroid[0]>symbols[curSNum].bBox[0] and symbols[candSNum].centroid[0]<symbols[curSNum].bBox[1] and symbols[candSNum].centroid[1]>symbols[curSNum].superThresh and symbols[candSNum].centroid[1]<symbols[curSNum].subThresh:
						dominations.append(dom.hardDomination('inside',symbols[curSNum],symbols[candSNum]))
				elif symbols[curSNum].kinds[0]=='llik':
					if symbols[candSNum].centroid[0]<symbols[curSNum].outbBox[1] and symbols[candSNum].centroid[0]>symbols[curSNum].bBox[1] and symbols[candSNum].centroid[1]<symbols[curSNum].superThresh and symbols[candSNum].bBox[3]<symbols[curSNum].bBox[3]:
						dominations.append(dom.hardDomination('superscript',symbols[curSNum],symbols[candSNum]))
					elif symbols[candSNum].centroid[0]<symbols[curSNum].outbBox[1] and symbols[candSNum].centroid[0]>symbols[curSNum].outbBox[0] and symbols[candSNum].centroid[1]>symbols[curSNum].subThresh:
						dominations.append(dom.hardDomination('below',symbols[curSNum],symbols[candSNum]))
				elif symbols[curSNum].kinds[0]=='rlik':
					if symbols[candSNum].centroid[0]<symbols[curSNum].outbBox[1] and symbols[candSNum].centroid[0]>symbols[curSNum].bBox[1] and symbols[candSNum].centroid[1]<symbols[curSNum].superThresh and symbols[candSNum].centroid[1]>symbols[curSNum].outbBox[2] and symbols[candSNum].bBox[3]<symbols[curSNum].bBox[3]:
						dominations.append(dom.hardDomination('superscript',symbols[curSNum],symbols[candSNum]))
					elif symbols[candSNum].centroid[0]>symbols[curSNum].outbBox[0] and symbols[candSNum].centroid[0]<symbols[curSNum].bBox[1] and symbols[candSNum].centroid[1]<symbols[curSNum].superThresh and symbols[candSNum].centroid[1]>symbols[curSNum].outbBox[2]:
						dominations.append(dom.hardDomination('above',symbols[curSNum],symbols[candSNum]))
					elif symbols[candSNum].centroid[0]>symbols[curSNum].bBox[0] and symbols[candSNum].centroid[0]<symbols[curSNum].bBox[1] and symbols[candSNum].centroid[1]>symbols[curSNum].bBox[2] and symbols[candSNum].centroid[1]<symbols[curSNum].bBox[3]:
						dominations.append(dom.hardDomination('inside',symbols[curSNum],symbols[candSNum]))
	#Es miren els veins de forma directe
	for curSNum in range(len(symbols)):
		noSoft=True
		canGoOn=True
		c=0
		if hasattr(symbols[curSNum],'superThresh'):
			limUp=symbols[curSNum].superThresh
		else:
			limUp=symbols[curSNum].bBox[2]
		while c<len(symbols) and noSoft and canGoOn:
			if c!=curSNum and symbols[c].centroid[1]>limUp and symbols[c].centroid[1]<symbols[curSNum].bBox[3] and symbols[c].centroid[0]>symbols[curSNum].bBox[1] and symbols[curSNum].centroid[1]>symbols[c].bBox[2] and symbols[curSNum].centroid[1]<symbols[c].bBox[3]:      #!!!!!!!!!!!!!!!!!!!!!!!!!
				dominators=[]
				for dA in dominations:
					if dA.submissive.ref==symbols[c].ref and isinstance(dA,dom.hardDomination):
						dominators.append(dA.dominant.ref)
				if len(dominators)==0:
					dominations.append(dom.softDomination('rightNeigh',symbols[curSNum],symbols[c]))
					noSoft=False
				else:
					if [dominators[0],symbols[curSNum].ref] in [[doi.dominant.ref,doi.submissive.ref] for doi in dominations]:
						dominations.append(dom.softDomination('rightNeigh',symbols[curSNum],symbols[c]))
						noSoft=False
					else:
						canGoOn=False
				del dominators
			c+=1
	softDomed=[]
	wheresD=[]
	c=0
	#Es llisten els simbols dominats i que son veins d'un altre
	for domi in dominations:
		if isinstance(domi,dom.softDomination):
			softDomed.append(domi.submissive.ref)
			wheresD.append(c)
		c+=1
	for sNum in range(len(symbols)):
		while softDomed.count(sNum)>1:
			indecs=softDomed.index(sNum)
			del dominations[wheresD[indecs]]
			softDomed.remove(sNum)
			del wheresD[indecs]
			for i in range(indecs,len(wheresD)):
				wheresD[i]-=1
	hardDomed=[]
	whereH=[]
	c=0
	for domi in dominations:
		if isinstance(domi,dom.hardDomination):
			hardDomed.append(domi.submissive.ref)
			whereH.append(c)
		c+=1
	#Elimina els dominis mutus
	for domn in dominations:
		if [domn.dominant.ref,domn.submissive.ref] in [[domt.submissive.ref,domt.dominant.ref] for domt in dominations]:
			del dominations[[[domt.submissive.ref,domt.dominant.ref] for domt in dominations].index([domn.dominant.ref,domn.submissive.ref])]
			for i in range(hardDomed.index(domn.dominant.ref),len(whereH)):
				whereH[i]-=1
			for i in range(len(wheresD)):
				wheresD[i]-=1
			del hardDomed[hardDomed.index(domn.dominant.ref)]		
	#Recalcula hardDomed i softDomed
	hardDomed=[]
	whereH=[]
	c=0
	for domi in dominations:
		if isinstance(domi,dom.hardDomination):
			hardDomed.append(domi.submissive.ref)
			whereH.append(c)
		c+=1
	#Si la relacio entre dos simbols es de domini soft i hard elimina el domini soft
	for dmnoi in dominations:
		if isinstance(dmnoi,dom.softDomination):
			for domt in dominations:
				if isinstance(domt,dom.hardDomination) and dmnoi.submissive.ref==domt.submissive.ref:
					if [domt.dominant.ref,dmnoi.dominant.ref] not in [[domans.dominant.ref,domans.submissive.ref] for domans in dominations]:
						dominations.remove(dmnoi)
					elif isinstance(dominations[[[domans.dominant.ref,domans.submissive.ref] for domans in dominations].index([domt.dominant.ref,dmnoi.dominant.ref])],dom.softDomination):
						dominations.remove(dmnoi)
	softDomed=[]
	wheresD=[]
	c=0
	for domi in dominations:
		if isinstance(domi,dom.softDomination):
			softDomed.append(domi.submissive.ref)
			wheresD.append(c)
		c+=1
	#Crea la dominantBaseLine i elimina els veins de simbols de fora de la dominantBaseLine
	dominantBaseline=[]
	for sNum in range(len(symbols)):
		if sNum not in hardDomed:
			dominantBaseline.append(sNum)
	for dBlSym in dominantBaseline:
		if dBlSym in softDomed:
			if dominations[wheresD[softDomed.index(dBlSym)]].dominant.ref not in dominantBaseline:
				dominantBaseline.remove(dBlSym)
	#Fa veins als elements de la dominantBaseLine
	for i in range(len(dominantBaseline)-1):
		if ['rightNeigh',symbols[dominantBaseline[i]].ref,symbols[dominantBaseline[i+1]].ref] not in [[domin.typedom,domin.dominant.ref,domin.submissive.ref] for domin in dominations]:
			dominations.append(dom.softDomination('rightNeigh',symbols[dominantBaseline[i]],symbols[dominantBaseline[i+1]]))
	#Llista les dades dels dominins hard i soft
	hdomsList=[]
	cd=0
	for d in dominations:
		if isinstance(d,dom.hardDomination):
			hdomsList.append([d.dominant.ref,d.submissive.ref,cd])
		cd+=1
	sdomsList=[]
	cd=0
	for d in dominations:
		if isinstance(d,dom.softDomination):
			sdomsList.append([d.dominant.ref,d.submissive.ref,cd])
		cd+=1
	#Assigna domini entre un simbol i un altre si aquest es vei d'un simbol dominat pel primer, del tipus d'aquest domini, i elimina els dominis quan un simbol es dominat per un altre que tambe es dominat per un simbol dominat pel primer (fa que els simbols nets no puguin ser tambe fills), DOBLEMENT perque el primer pas tambe tingui en compte els efectes del segon
	fullSons=copy.deepcopy(dominantBaseline)
	c=0
	while len(fullSons)!=0:
		currentLine=copy.deepcopy(fullSons)
		fullSons=[]
		for dBlSym in currentLine:
			sons=dominates(dBlSym,dominations,'hard')
			if len(sons)!=0:
				for son in sons:
					if len(dominates(son,dominations,'soft'))!=0:
						grandsons=dominates(son,dominations,'soft')
						for grandson in grandsons:
							if [symbols[dBlSym].ref,symbols[grandson].ref,dominations[hdomsList[[hdomsList[do][1] for do in range(len(hdomsList))].index(son)][2]].typedom] not in [[domina.dominant.ref,domina.submissive.ref,domina.typedom] for domina in dominations]:
								dominations.append(dom.hardDomination(dominations[hdomsList[[[hdomsList[do][0],hdomsList[do][1]] for do in range(len(hdomsList))].index([dBlSym,son])][2]].typedom,symbols[dBlSym],symbols[grandson]))
								hdomsList.append([symbols[dBlSym].ref,symbols[grandson].ref,len(dominations)-1])
								if grandson in dominantBaseline:
									dominantBaseline.remove(grandson)
					parents=[]
					grandParents=[]
					for d in hdomsList:
						if d[1]==dBlSym:
							grandParents.append(d)
						elif d[1]==son:
							parents.append(d)
					for parent in parents:
						if parent[0] in [g[0] for g in grandParents]:
							where=[h[2] for h in hdomsList].index(parent[2])
							del dominations[parent[2]]
							del hdomsList[where]
							for i in range(where,len(hdomsList)):
								hdomsList[i][2]-=1
							c+=1
				fullSons.extend(sons)
	fullSons=copy.deepcopy(dominantBaseline)
	c=0
	while len(fullSons)!=0:
		currentLine=copy.deepcopy(fullSons)
		fullSons=[]
		for dBlSym in currentLine:
			sons=dominates(dBlSym,dominations,'hard')
			if len(sons)!=0:
				for son in sons:
					if len(dominates(son,dominations,'soft'))!=0:
						grandsons=dominates(son,dominations,'soft')
						for grandson in grandsons:
							if [symbols[dBlSym].ref,symbols[grandson].ref,dominations[hdomsList[[hdomsList[do][1] for do in range(len(hdomsList))].index(son)][2]].typedom] not in [[domina.dominant.ref,domina.submissive.ref,domina.typedom] for domina in dominations]:
								dominations.append(dom.hardDomination(dominations[hdomsList[[[hdomsList[do][0],hdomsList[do][1]] for do in range(len(hdomsList))].index([dBlSym,son])][2]].typedom,symbols[dBlSym],symbols[grandson]))
								hdomsList.append([symbols[dBlSym].ref,symbols[grandson].ref,len(dominations)-1])
								if grandson in dominantBaseline:
									dominantBaseline.remove(grandson)
					parents=[]
					grandParents=[]
					for d in hdomsList:
						if d[1]==dBlSym:
							grandParents.append(d)
						elif d[1]==son:
							parents.append(d)
					for parent in parents:
						if parent[0] in [g[0] for g in grandParents]:
							where=[h[2] for h in hdomsList].index(parent[2])
							del dominations[parent[2]]
							del hdomsList[where]
							for i in range(where,len(hdomsList)):
								hdomsList[i][2]-=1
							c+=1
				fullSons.extend(sons)
	co=0
	#Elimina els dobles dominis d'un simbol sobre un altre
	for nd in range(len(dominations)):
		if [[doimn.dominant.ref,doimn.submissive.ref] for doimn in dominations].count([dominations[nd-co].dominant.ref,dominations[nd-co].submissive.ref])>1:
			del dominations[nd-co]
			co+=1
	#Assigna un domini sobre els simbols sense assignar segons la posicio on els trobi
	for sym in symbols:
		sons=dominates(sym.ref,dominations,'hard')
		sons=sorted(sons)
		domdic={}
		for son in sons:
			tip=dominations[[[doi.dominant.ref,doi.submissive.ref] for doi in dominations].index([sym.ref,son])].typedom
			if tip not in domdic:
				domdic[tip]=[]
			domdic[tip].append(son)
		gone=[]
		for tip in domdic:
			for ele in range(len(domdic[tip])-1):
				if symbols[domdic[tip][ele]].ref not in gone:
					if [domdic[tip][ele],domdic[tip][ele+1],'rightNeigh'] not in [[doi.dominant.ref,doi.submissive.ref,doi.typedom] for doi in dominations]:
						if symbols[domdic[tip][ele+1]].centroid[1]<symbols[domdic[tip][ele]].bBox[2] and symbols[domdic[tip][ele]].kinds[0]!='blik' and symbols[domdic[tip][ele]].kinds[0]!='nosc':							
							while symbols[domdic[tip][ele+1]].ref in [doim.submissive.ref for doim in dominations]:
								del dominations[[doim.submissive.ref for doim in dominations].index(symbols[domdic[tip][ele+1]].ref)]
							if symbols[domdic[tip][ele+1]].centroid[0]>symbols[domdic[tip][ele]].bBox[1]:
								if symbols[domdic[tip][ele]].kinds[0]=='slik':
									dominations.append(dom.hardDomination('above',symbols[domdic[tip][ele]],symbols[domdic[tip][ele+1]]))
								else:
									dominations.append(dom.hardDomination('superscript',symbols[domdic[tip][ele]],symbols[domdic[tip][ele+1]]))
							else:
								if symbols[domdic[tip][ele]].kinds[0]=='slik' or symbols[domdic[tip][ele]].kinds[0]=='rlik':
									dominations.append(dom.hardDomination('above',symbols[domdic[tip][ele]],symbols[domdic[tip][ele+1]]))
								else:
									dominations.append(dom.hardDomination('superscript',symbols[domdic[tip][ele]],symbols[domdic[tip][ele+1]]))
						elif symbols[domdic[tip][ele+1]].centroid[1]>symbols[domdic[tip][ele]].bBox[3] and (symbols[domdic[tip][ele]].kinds[0]=='sc' or symbols[domdic[tip][ele]].kinds[0]=='slik' or symbols[domdic[tip][ele]].kinds[0]=='llik'):
							while symbols[domdic[tip][ele+1]].ref in [doim.submissive.ref for doim in dominations]:
								del dominations[[doim.submissive.ref for doim in dominations].index(symbols[domdic[tip][ele+1]].ref)]
							if symbols[domdic[tip][ele]].kinds[0]=='sc':
								dominations.append(dom.hardDomination('subscript',symbols[domdic[tip][ele]],symbols[domdic[tip][ele+1]]))
							else:
								dominations.append(dom.hardDomination('below',symbols[domdic[tip][ele]],symbols[domdic[tip][ele+1]]))
						else:
							dominations.append(dom.softDomination('rightNeigh',symbols[domdic[tip][ele]],symbols[domdic[tip][ele+1]]))
						gone.append(symbols[domdic[tip][ele+1]].ref)
	#Recalcula hdomsList i sdomsList
	hdomsList=[]
	cd=0
	for d in dominations:
		if isinstance(d,dom.hardDomination):
			hdomsList.append([d.dominant.ref,d.submissive.ref,cd])
		cd+=1
	sdomsList=[]
	cd=0
	for d in dominations:
		if isinstance(d,dom.softDomination):
			sdomsList.append([d.dominant.ref,d.submissive.ref,cd])
		cd+=1
	#Repeteix la inclosio dels veins dels fills i la exclosio dels nets feta i comentada anteriorment
	fullSons=copy.deepcopy(dominantBaseline)
	c=0
	while len(fullSons)!=0:
		currentLine=copy.deepcopy(fullSons)
		fullSons=[]
		for dBlSym in currentLine:
			sons=dominates(dBlSym,dominations,'hard')
			if len(sons)!=0:
				for son in sons:
					if len(dominates(son,dominations,'soft'))!=0:
						grandsons=dominates(son,dominations,'soft')
						for grandson in grandsons:
							if [symbols[dBlSym].ref,symbols[grandson].ref,dominations[hdomsList[[hdomsList[do][1] for do in range(len(hdomsList))].index(son)][2]].typedom] not in [[domina.dominant.ref,domina.submissive.ref,domina.typedom] for domina in dominations]:
								dominations.append(dom.hardDomination(dominations[hdomsList[[[hdomsList[do][0],hdomsList[do][1]] for do in range(len(hdomsList))].index([dBlSym,son])][2]].typedom,symbols[dBlSym],symbols[grandson]))
								hdomsList.append([symbols[dBlSym].ref,symbols[grandson].ref,len(dominations)-1])
								if grandson in dominantBaseline:
									dominantBaseline.remove(grandson)
					parents=[]
					grandParents=[]
					for d in hdomsList:
						if d[1]==dBlSym:
							grandParents.append(d)
						elif d[1]==son:
							parents.append(d)
					for parent in parents:
						if parent[0] in [g[0] for g in grandParents]:
							where=[h[2] for h in hdomsList].index(parent[2])
							del dominations[parent[2]]
							del hdomsList[where]
							for i in range(where,len(hdomsList)):
								hdomsList[i][2]-=1
							c+=1
				fullSons.extend(sons)
	#Si la relacio entre dos simbols es de domini soft i hard elimina el domini soft
	for dmnoi in dominations:
		if isinstance(dmnoi,dom.softDomination):
			for domt in dominations:
				if isinstance(domt,dom.hardDomination) and dmnoi.submissive.ref==domt.submissive.ref:
					if [domt.dominant.ref,dmnoi.dominant.ref] not in [[domans.dominant.ref,domans.submissive.ref] for domans in dominations]:
						dominations.remove(dmnoi)
					elif isinstance(dominations[[[domans.dominant.ref,domans.submissive.ref] for domans in dominations].index([domt.dominant.ref,dmnoi.dominant.ref])],dom.softDomination):
						dominations.remove(dmnoi)
	#Filtra el nombre de cops que un simbol pot ser vei a 1
	for sIn in range(len(symbols)):
		following=dominates(sIn,dominations,'soft')
		following=sorted(following)
		while len(following)>1:
			if [following[0],following[len(following)-1]] in [[dmn.dominant.ref,dmn.submissive.ref] for dmn in dominations]:
				del dominations[[[doim.dominant.ref,doim.submissive.ref] for doim in dominations].index([sIn,following[len(following)-1]])]
			del following[len(following)-1]
	auxiliarSyms=[s.ref for s in symbols]
	c1=-1
	auxhdslist=copy.deepcopy(hdomsList)
	deleted=[]
	numdel=0
	#Cap simbol pot ser dominat per mes d'un simbol
	for hds in auxhdslist:
		c1+=1
		c2=-1
		stillDomined=True
		for hds2 in auxhdslist:
			c2+=1
			if c1!=c2 and hds[1]==hds2[1] and stillDomined and c2 not in deleted:
				del dominations[hds[2]-numdel]
				del hdomsList[c1-numdel]
				for i in range(c1-numdel,len(hdomsList)):
					hdomsList[i][2]-=1
				deleted.append(c1)
				stillDomined=False
				numdel+=1
	co=0
	#Elimina els dominis dobles
	for nd in range(len(dominations)):
		if [[doimn.dominant.ref,doimn.submissive.ref] for doimn in dominations].count([dominations[nd-co].dominant.ref,dominations[nd-co].submissive.ref])>1:
			del dominations[nd-co]
			co+=1
	#Guarda en cada simbol els simbols que domina
	while len(auxiliarSyms)!=0:
		cs=0
		yetNotDone=True
		while cs!=len(auxiliarSyms) and yetNotDone:
			sons=dominates(auxiliarSyms[cs],dominations,'hard')
			if all(son not in auxiliarSyms for son in sons):
				yetNotDone=False
				domines={}
				for son in sons:
					tip=dominations[[[doi.dominant.ref,doi.submissive.ref] for doi in dominations].index([auxiliarSyms[cs],son])].typedom
					if tip not in domines:
						domines[tip]=[]
					domines[tip].append(symbols[son])
				symbols[auxiliarSyms[cs]]=symbolFamily(symbols[auxiliarSyms[cs]],domines)
				del auxiliarSyms[cs]
			cs+=1
	for si in symbols:
		print si.ref,si.tag,si.kinds
	#Recalcula la dominantBaseLine
	hardDomed=[]
	whereH=[]
	c=0
	for domi in dominations:
		if isinstance(domi,dom.hardDomination):
			hardDomed.append(domi.submissive.ref)
			whereH.append(c)
		c+=1
	softDomed=[]
	wheresD=[]
	c=0
	for domi in dominations:
		if isinstance(domi,dom.softDomination):
			softDomed.append(domi.submissive.ref)
			wheresD.append(c)
		c+=1
	for sNum in range(len(symbols)):
		while softDomed.count(sNum)>1:
			indecs=softDomed.index(sNum)
			del dominations[wheresD[indecs]]
			softDomed.remove(sNum)
			del wheresD[indecs]
			for i in range(indecs,len(wheresD)):
				wheresD[i]-=1
	dominantBaseline=[]
	for sNum in range(len(symbols)):
		if sNum not in hardDomed:
			dominantBaseline.append(sNum)
	for dBlSym in dominantBaseline:
		if dBlSym in softDomed:
			if dominations[wheresD[softDomed.index(dBlSym)]].dominant.ref not in dominantBaseline:
				dominantBaseline.remove(dBlSym)
	print dominantBaseline
	#Monta l'expressio
	expression=''
	print 'Final symbols:'
	for dblIn in dominantBaseline:
		expression+=getTex(symbols[dblIn])
	print 'List of dominations:'
	print [[do.dominant.tag[:-1],do.dominant.ref,do.submissive.tag[:-1],do.submissive.ref,do.typedom] for do in dominations]
	return dominations,expression
	
def dominates(father,doms,td):
	sons=[]
	if td=='hard':
		tip=dom.hardDomination
	elif td=='soft':
		tip=dom.softDomination
	for domin in doms:
		if domin.dominant.ref==father and isinstance(domin,tip):
			sons.append(domin.submissive.ref)
	return sons

#SymbolFamily: guarda en el simbol que es symbol els dominis especificats en symbolDomines segons el tipus de simbol
	
def symbolFamily(symbol,symbolDomines):
	if symbol.kinds[0]=='supsc':
		if 'superscript' in symbolDomines:
			symbol.addSupsc(symbolDomines['superscript'])
	elif symbol.kinds[0]=='sc':
		if 'superscript' in symbolDomines:
			symbol.addSupsc(symbolDomines['superscript'])
		if 'subscript' in symbolDomines:
			symbol.addSubsc(symbolDomines['subscript'])
	elif symbol.kinds[0]=='slik':
		if 'above' in symbolDomines:
			symbol.addAb(symbolDomines['above'])
		if 'below' in symbolDomines:
			symbol.addBe(symbolDomines['below'])
		if 'inside' in symbolDomines:
			symbol.addIns(symbolDomines['inside'])
	elif symbol.kinds[0]=='llik':
		if 'superscript' in symbolDomines:
			symbol.addSupsc(symbolDomines['superscript'])
		if 'below' in symbolDomines:
			symbol.addBe(symbolDomines['below'])
	elif symbol.kinds[0]=='rlik':
		if 'superscript' in symbolDomines:
			symbol.addSupsc(symbolDomines['superscript'])
		if 'above' in symbolDomines:
			symbol.addAb(symbolDomines['above'])
		if 'inside' in symbolDomines:
			symbol.addIns(symbolDomines['inside'])
	elif symbol.kinds[0]=='blik':
		if 'above' in symbolDomines:
			symbol.addAb(symbolDomines['above'])
		if 'below' in symbolDomines:
			symbol.addBe(symbolDomines['below'])
	return symbol

#GetTex: torna en format Tex el simbol symbol
	
def getTex(symbol):
	symbol.reTag()
	texExpr=''
	if symbol.kinds[0]=='nosc':
		texExpr+=symbol.texTag+' '
	elif symbol.kinds[0]=='supsc':
		texExpr+=symbol.texTag+' '
		if hasattr(symbol,'superscripts'):
			texExpr+='^{'
			for member in symbol.superscripts:
				texExpr+=getTex(member)
			texExpr+='}'
	elif symbol.kinds[0]=='sc':
		texExpr+=symbol.texTag+' '
		if hasattr(symbol,'superscripts'):
			texExpr+='^{'
			for member in symbol.superscripts:
				texExpr+=getTex(member)
			texExpr+='}'
		if hasattr(symbol,'subscripts'):
			texExpr+='_{'
			for member in symbol.subscripts:
				texExpr+=getTex(member)
			texExpr+='}'
	elif symbol.kinds[0]=='slik':
		texExpr+=symbol.texTag+' '
		if hasattr(symbol,'aboves') or hasattr(symbol,'belows'):
			if hasattr(symbol,'belows'):
				texExpr+='_{'
				for member in symbol.belows:
					texExpr+=getTex(member)
				texExpr+='}'
			if hasattr(symbol,'aboves'):
				texExpr+='^{'
				for member in symbol.aboves:
					texExpr+=getTex(member)
				texExpr+='}'
		if hasattr(symbol,'containing'):
			for member in symbol.containing:
				texExpr+=getTex(member)
	elif symbol.kinds[0]=='llik':
		texExpr+=symbol.texTag+' '
		if hasattr(symbol,'belows'):
			texExpr+='_{'
			for member in symbol.belows:
				texExpr+=getTex(member)
			texExpr+='}'
		if hasattr(symbol,'superscripts'):
			texExpr+='^{'
			for member in symbol.superscripts:
				texExpr+=getTex(member)
			texExpr+='}'
	elif symbol.kinds[0]=='rlik':
		texExpr+=symbol.texTag+' '
		if hasattr(symbol,'aboves'):
			if all([(member.tag[:-1]=='0') or (member.tag[:-1]=='1') or (member.tag[:-1]=='2') or (member.tag[:-1]=='3') or (member.tag[:-1]=='4') or (member.tag[:-1]=='5') or (member.tag[:-1]=='6') or (member.tag[:-1]=='7') or (member.tag[:-1]=='8') or (member.tag[:-1]=='9') for member in symbol.aboves]):
				texExpr+='['
				for member in symbol.aboves:
					texExpr+=getTex(member)
				texExpr+=']'
		if hasattr(symbol,'containing'):
			texExpr+='{'
			for member in symbol.containing:
				texExpr+=getTex(member)
			texExpr+='}'
		else:
			texExpr+='{?}'
		if hasattr(symbol,'superscripts'):
			texExpr+='^{'
			for member in symbol.superscripts:
				texExpr+=getTex(member)
			texExpr+='}'
	elif symbol.kinds[0]=='blik':
		texExpr+=symbol.texTag+' '
		texExpr+='{'
		if hasattr(symbol,'aboves'):
			for member in symbol.aboves:
				texExpr+=getTex(member)
		else:
			texExpr+='?'
		texExpr+='}'
		texExpr+='{'
		if hasattr(symbol,'belows'):
			for member in symbol.belows:
				texExpr+=getTex(member)
		else:
			texExpr+='?'
		texExpr+='}'
	return texExpr

#ReAssign: segons la llista de simbols i les etiquetes, converteix alguns simbols en un altre

def reAssign(symbols,tags):
	for sNum in range(len(symbols)):
		symbols[sNum].tagUntagged(tags[sNum],sNum)
	equals=[]
	geqs=[]
	leqs=[]
	twoDots=[]
	for inspected in symbols:
		if inspected.tag[:-1]=='-' or inspected.tag[:-1]=='\div':
			hasAbove=False
			hasBelow=False
			for s in symbols:
				if s.ref!=inspected.ref and s.center[0]>inspected.bBox[0] and s.center[0]<inspected.bBox[1]:
					if s.center[1]<inspected.center[1]:
						hasAbove=True
						other=s
					else:
						hasBelow=True
						other=s
			if (hasAbove and hasBelow==False) or (hasAbove==False and hasBelow):
				if (other.tag[:-1]=='-' or other.tag[:-1]=='\div') and [other.ref,inspected.ref] not in equals:
					equals.append([inspected.ref,other.ref])
				elif other.tag[:-1]=='\gt' and [other.ref,inspected.ref] not in geqs:
					geqs.append([inspected.ref,other.ref])
				elif other.tag[:-1]=='\lt' and [other.ref,inspected.ref] not in leqs:
					leqs.append([inspected.ref,other.ref])
		elif inspected.tag[:-1]=='.':
			hasAbove=False
			hasBelow=False
			for s in symbols:
				if s.ref!=inspected.ref and s.center[0]>inspected.bBox[0] and s.center[0]<inspected.bBox[1] and s.tag[:-1]=='.':
					if s.center[1]<inspected.center[1]:
						hasAbove=True
						other=s
					else:
						hasBelow=True
						other=s
			if (hasAbove and hasBelow==False) or (hasAbove==False and hasBelow):
				if [other.ref,inspected.ref] not in twoDots:
					twoDots.append([inspected.ref,other.ref])
	removed=[]
	for eq in equals:
		newPos=min(eq)
		removed.append(max(eq))
		reduSim=[spp.arcLengthResampling([symbols[eq[0]]],25)[0].Coord,spp.arcLengthResampling([symbols[eq[1]]],25)[0].Coord]
		extSim=np.concatenate((reduSim[0],reduSim[1]),axis=0)
		newEq=nsi.taggedSymbol(extSim,np.array([24,49],np.float64),'=2')
		newEq.ref=newPos
		newEq.draw()
		del symbols[max(eq)]
		del symbols[min(eq)]
		symbols.insert(newPos,newEq)
	for gq in geqs:
		newPos=min(gq)
		removed.append(newPos)
		reduSim=[spp.arcLengthResampling([symbols[gq[0]]],25)[0].Coord,spp.arcLengthResampling([symbols[gq[1]]],25)[0].Coord]
		extSim=np.concatenate((reduSim[0],reduSim[1]),axis=0)
		newGq=nsi.taggedSymbol(extSim,np.array([24,49],np.float64),'\geq2')
		newGq.ref=newPos
		newGq.draw()
		del symbols[max(gq)]
		del symbols[min(gq)]
		symbols.insert(newPos,newGq)
	for lq in leqs:
		newPos=min(lq)
		removed.append(max(lq))
		reduSim=[spp.arcLengthResampling([symbols[lq[0]]],25)[0].Coord,spp.arcLengthResampling([symbols[lq[1]]],25)[0].Coord]
		extSim=np.concatenate((reduSim[0],reduSim[1]),axis=0)
		newLq=nsi.taggedSymbol(extSim,np.array([24,49],np.float64),'\leq2')
		newLq.ref=newPos
		newLq.draw()
		del symbols[max(lq)]
		del symbols[min(lq)]
		symbols.insert(newPos,newLq)
	for tD in twoDots:
		newPos=min(tD)
		removed.append(max(tD))
		reduSim=[spp.arcLengthResampling([symbols[tD[0]]],25)[0].Coord,spp.arcLengthResampling([symbols[tD[1]]],25)[0].Coord]
		extSim=np.concatenate((reduSim[0],reduSim[1]),axis=0)
		newtD=nsi.taggedSymbol(extSim,np.array([24,49],np.float64),':2')
		newtD.ref=newPos
		newtD.draw()
		del symbols[max(tD)]
		del symbols[min(tD)]
		symbols.insert(newPos,newtD)
	if len(removed)!=0:
		c=0
		for sn in range(max([s.ref for s in symbols])+1):
			if sn in [s.ref for s in symbols]:
				symbols[[s.ref for s in symbols].index(sn)].ref-=c
			if sn in removed:
				c+=1
	return symbols,[si.tag for si in symbols]
		
