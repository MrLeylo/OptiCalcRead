import matplotlib.pyplot as plt

#Repr:representa els simbols de la llista symbols

def repr(symbols):
	plt.figure(4)
	colors=['g-','b-','y-','r-']
	for i in range(len(symbols)):
		for j in range(symbols[i].tE.shape[0]):
			if j==0:
				ini=-1
			else:
				ini=int(symbols[i].tE[j-1])
			lineG,=plt.plot(symbols[i].Coord[range(ini+1,int(symbols[i].tE[j])+1),0],-symbols[i].Coord[range(ini+1,int(symbols[i].tE[j])+1),1],colors[i%4])
	return
