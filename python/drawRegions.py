import matplotlib.pyplot as plt
import numpy as np

#draw: troba la bounding box de cada simbol i les representa


def drawS(symbols):
	print 'Setting attributes..........'
	for i in range(len(symbols)):
		symbols[i].draw()
	#Representa
	for i in range(len(symbols)):
		plt.plot(symbols[i].bBox[[0,1,1,0,0]],-symbols[i].bBox[[3,3,2,2,3]],'-')
		plt.plot(symbols[i].center[0],-symbols[i].center[1],'g*')
	return symbols
