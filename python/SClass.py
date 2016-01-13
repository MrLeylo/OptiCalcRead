import matplotlib.pyplot as plt
import numpy as np
import symbolPreprocessing as spp
import math

#Symbol: Classe general per simbols sense etiquetar, necessita coordenades i marcadors de traces, on Coordinates es un numpy array de 2 dimensions amb les coordenades del simbol i traceEnds son els marcadors dels punts on finalitzen els traces

class Symbol(object):
	def __init__(self, Coordinates, traceEnds):
		self.Coord =Coordinates
		self.tE=traceEnds
		self.Style='unknown'
		
	#Draw:Segons les coordenades assigna la bounding box i en centre
		
	def draw(self):
		self.bBox=np.zeros([4],np.float64)
		self.center=np.zeros([2],np.float64)
		#Busca les coordenades extremes de cada simbol per fixar els marges i els centres
		leftBorder=min([a[0] for a in self.Coord])
		rightBorder=max([a[0] for a in self.Coord])
		upBorder=min(a[1] for a in self.Coord)
		downBorder=max(a[1] for a in self.Coord)
		self.bBox[0]=leftBorder
		self.bBox[1]=rightBorder
		self.bBox[2]=upBorder
		self.bBox[3]=downBorder
		self.center[0]=(leftBorder+rightBorder)/2
		self.center[1]=(upBorder+downBorder)/2
		
	#ComputeFeatures:calcula les features a analitzar del simbol
	
	def computeFeatures(self):
		self.localFeatures()
		self.globalFeatures()
		
	#LocalFeatures:features referents a cada punt
		
	def localFeatures(self):
		self.compTurning()
		self.compTurnDif()
		self.lengthPosition()
	
	#GlobalFeatures:features referents a les traces
	
	def globalFeatures(self):
		self.centerOfGravity()
		self.lengthInStroke()
		self.relativeStrokeLength()
		self.accumAngle()
		self.compQE()
	
	#CompTurning:Guarda l'angle del segment que surt de cada punt respecte la horitzontal, assignant l'ultim angle en cada trace sempre com PI
	
	def compTurning(self):
		self.turningAngle=np.zeros([self.Coord.shape[0]],np.float64)
		for j in range(self.Coord.shape[0]-1):
			self.turningAngle[j]=math.acos((self.Coord[j+1,0]-self.Coord[j,0])/math.sqrt(((self.Coord[j+1,0]-self.Coord[j,0])**2)+((self.Coord[j+1,1]-self.Coord[j,1])**2)))
			#Si l'angle es major de 
			if self.Coord[j+1,1]>self.Coord[j,1]:
				self.turningAngle[j]=-self.turningAngle[j]
			if j in self.tE:
				self.turningAngle[j]=math.pi
		self.turningAngle[self.Coord.shape[0]-1]=math.pi
	
	#CompTurnDif:Guarda l'angle entre els segments incidents en cada punt, i en l'ultim assigna 0
	
	def compTurnDif(self):
		self.turningAngleDifference=np.zeros([self.Coord.shape[0]],np.float64)
		for j in range(self.Coord.shape[0]-1):
			self.turningAngleDifference[j]=self.turningAngle[j+1]-self.turningAngle[j]
			if j in self.tE:
				self.turningAngleDifference[j]=0
		self.turningAngleDifference[self.Coord.shape[0]-1]=0
	
	#LengthPosition: Guarda la posicio relativa a 1 respecte el recorregut sencer del simbol de cada punt
	
	def lengthPosition(self):
		self.LP=np.zeros([self.Coord.shape[0]],np.float64)
		Lan=0
		for ik in range(self.tE.shape[0]):
			if ik==0:
				ini=-1
			else:
				ini=int(self.tE[ik-1])
			L=Lan+spp.lcomp(self.Coord,int(self.tE[ik])+1)-spp.lcomp(self.Coord,ini+1)
			Lan=L
		Lan=0
		for ik in range(self.tE.shape[0]):
			if ik==0:
				ini=-1
			else:
				ini=int(self.tE[ik-1])
			for j in range(ini+1,int(self.tE[ik])+1):
				Lr=Lan+spp.lcomp(self.Coord,j+1)-spp.lcomp(self.Coord,ini+1)
				self.LP[j]=Lr/L
			Lan=Lr
	
	#CenterOfGravity: Guarda el centre de gravetat (mitjana dels punts) de cada trace
	
	def centerOfGravity(self):
		self.coG=np.zeros([self.tE.shape[0],2],np.float64)
		for i in range(self.tE.shape[0]):
			sumX=0
			sumY=0
			if i==0:
				ini=-1
			else:
				ini=int(self.tE[i-1])
			for j in range(ini+1,int(self.tE[i]+1)):
				sumX=sumX+self.Coord[j,0]
				sumY=sumY+self.Coord[j,1]
			div=[sumX,sumY]/(self.tE[i]-ini)
			self.coG[i,0]=div[0]
			self.coG[i,1]=div[1]
	
	#LengthInStroke:Guarda la longitud de cada trace
	
	def lengthInStroke(self):
		self.liS=np.zeros([self.tE.shape[0]],np.float64)
		anteriors=0
		for i in range(self.tE.shape[0]):
			acDi=spp.lcomp(self.Coord,int(self.tE[i]+1))
			self.liS[i]=acDi-anteriors
			anteriors=acDi
	
	#RelativeStrokeLength: Guarda la longitud de cada trace respecte la longitud total
	
	def relativeStrokeLength(self):
		self.relStrokeLength=np.zeros([self.tE.shape[0]],np.float64)
		for i in range(self.tE.shape[0]):
			if i==0:
				ini=-1
			else:
				ini=int(self.tE[i-1])
			self.relStrokeLength[i]=math.sqrt(((self.Coord[self.tE[i],0]-self.Coord[ini+1,0])**2)+((self.Coord[self.tE[i],1]-self.Coord[ini+1,1])**2))/self.liS[i]
	
	#AccumAngle: Guarda l'angle dels extrems de cada trace
	
	def accumAngle(self):
		self.accAngle=np.zeros([self.tE.shape[0]],np.float64)
		for i in range(self.tE.shape[0]):
			suma=0
			if i==0:
				ini=-1
			else:
				ini=int(self.tE[i-1])
			for j in range(ini+1,int(self.tE[i]+1)):
				suma=suma+self.turningAngle[j]
			self.accAngle[i]=suma/(2*math.pi)
	
	#CompQE: Guarda l'error quadratic respecte els extrems en cada trace
	
	def compQE(self):
		self.quadraticError=np.zeros([self.tE.shape[0]],np.float64)
		for i in range(self.tE.shape[0]):
			suma=0
			if i==0:
				ini=-1
			else:
				ini=int(self.tE[i-1])
			for j in range(ini+1,int(self.tE[i]+1)):
				di=spp.dista(self.Coord[ini+1,0],self.Coord[ini+1,1],self.Coord[self.tE[i],0],self.Coord[self.tE[i],1],self.Coord[j,0],self.Coord[j,1])
				suma=suma+(di**2)
			self.quadraticError[i]=suma/(self.tE[i]-ini)
			
	#SetRegions: Assigna les regions de cada simbol segons el tipus 
	
	def setRegions(self,scKind,projKind):
		width=self.bBox[1]-self.bBox[0]
		height=self.bBox[3]-self.bBox[2]
		big=max(width,height)
		self.outbBox=[self.bBox[0]-big,self.bBox[1]+big,self.bBox[2]-big,self.bBox[3]+big]
		if projKind=='cent':
			self.centroid=[self.center[0],self.bBox[2]+(0.5*height)]
			sup=self.bBox[2]+(0.2*height)
			sub=self.bBox[2]+(0.75*height)
		elif projKind=='asc':
			self.centroid=[self.center[0],self.bBox[2]+(0.66*height)]
			sup=self.bBox[2]+(0.33*height)
			sub=self.bBox[2]+(0.8*height)
		elif projKind=='desc':
			self.centroid=[self.center[0],self.bBox[2]+(0.33*height)]
			sup=self.bBox[2]+(0.1*height)
			sub=self.bBox[2]+(0.4*height)
		if scKind=='nosc':
			self.rightOut=self.outbBox[1]+(2.5*width)
		elif scKind=='supsc':
			self.rightOut=self.outbBox[1]+(1.5*width)
			self.superThresh=sup
		elif scKind=='sc':
			self.rightOut=self.outbBox[1]+(1.5*width)
			self.superThresh=sup
			self.subThresh=sub
		elif scKind=='slik':
			self.rightOut=self.outbBox[1]+(1.5*width)
			self.superThresh=sup
			self.subThresh=sub
		elif scKind=='llik':
			self.rightOut=self.outbBox[1]+(1.5*width)
			self.superThresh=sup
			self.subThresh=sub
		elif scKind=='rlik':
			self.rightOut=self.outbBox[1]+(1.5*width)
			self.superThresh=sup
		elif scKind=='blik':
			self.rightOut=self.outbBox[1]+(1.5*width)
		self.kinds=[scKind,projKind]
	
	#AddSupsc:Afegeix un superscript
		
	def addSupsc(self,slist):
		self.superscripts=slist
		
	#AddSubsc:Afegeix un subscript
		
	def addSubsc(self,slist):
		self.subscripts=slist
		
	#AddAbove:Afegeix un superior
		
	def addAb(self,slist):
		self.aboves=slist
		
	#AddSupsc:Afegeix un inferior
		
	def addBe(self,slist):
		self.belows=slist
		
	#AddSupsc:Afegeix un contingut
		
	def addIns(self,slist):
		self.containing=slist	
	
	#AddSupsc:Etiqueta un simbol amb l'etiqueta de tag i la referencia de sNum, on tag es un string i sNum un enter
		
	def tagUntagged(self,tag,sNum):
		self.tag=tag
		self.ref=sNum
	
	#ReTag:Adapta l'etiqueta per ser comprensible per Tex
		
	def reTag(self):
		if self.tag[:-1]=='\div':
			self.texTag='\\'+'frac'
		elif self.tag[:-1]=='\ldots':
			self.texTag='\colon'
		elif self.tag[:-1]=='.':
			self.texTag='\cdotp'
		elif self.tag[:-1]=='COMMA':
			self.texTag=','
		elif self.tag[:-1]=='\!':
			self.texTag='!'
		elif self.tag[:-1]=='\gt':
			self.texTag='>'
		elif self.tag[:-1]=='\lt':
			self.texTag='<'
		else:
			self.texTag=self.tag[:-1]


class taggedSymbol(Symbol):
	def __init__(self, Coordinates, traceEnds,tag):
		self.Coord =Coordinates
		self.tE=traceEnds
		self.Style='unknown'
		self.tag=tag
