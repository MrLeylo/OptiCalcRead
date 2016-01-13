import numpy as np
import Image
import matplotlib.pyplot as plt

#draw: representa el dibuix de les coordenades i monta la seva imatge de tamany normalitzat (50,500)

def draw(coordinates):
	#Escaneja la matriu i representa la imatge
	fig=plt.figure(1)
	fig.canvas.set_window_title('Input')
	for i in range(coordinates.shape[0]):
		if[0,0] in coordinates[i]:
			indexos=np.where(coordinates[i]==[0,0])
			for j in range(len(indexos[1])):
				for k in range(2):
					coordinates[i,indexos[0][j],indexos[1]]=coordinates[i,indexos[0][0]-1,indexos[1]]
		lineP,=plt.plot(coordinates[i,range(coordinates.shape[1]),0],-coordinates[i,range(coordinates.shape[1]),1],'-')
	#Busquem la x i la y maximes de la imatge total, mirant totes les coordenades de la matriu
	print 'Initializing segmentation..........'
	listcoordinates=coordinates.tolist()
	x=[]
	y=[]
	for j in range(len(listcoordinates)):
		xb, yb = [i[0] for i in listcoordinates[j]], [i[1] for i in listcoordinates[j]]
		x.extend(xb)
		y.extend(yb)
	difX, difY = max(x)-min(x), max(y)-min(y)
	#Monta i omple la imatge normalitzada
	imatge = np.zeros([50,500])
	for i in range(len(x)):
		imatge[(50*(y[i]-min(y))/difY)-1, (500*(x[i]-min(x))/difX)-1] = 1
	img=Image.fromarray(imatge*255)
	return img,[x,y],[difX,difY]
