
#u2t:llegeix la base de dades UNIPEN i retorna les coordenades dels nous simbols

def u2t(filenom):
	file=open(filenom,"r")
	linea='o'
	trainTraces=[]
	marcador=-1
	ok=False
	#c=0
	while linea!='':
		#c+=1
		#print c
		linea=file.readline()
		if '.PEN_DOWN' in linea:
			ok=True
			trainTraces.append([])
			marcador+=1
		elif '.PEN_UP' in linea:
			ok=False
		if ok and '.PEN_DOWN' not in linea:
			if ' ' in linea[1:]:
				espai=linea.index(' ',1)
				trainTraces[marcador].append([float(linea[:espai]),float(linea[espai+1:].rstrip('\n'))])
	return trainTraces
