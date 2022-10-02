import pygame, math, random

class Particle(pygame.sprite.Sprite):

	playfield = pygame.Rect((0,0),(0,0))
	images = None

	# Constructeur de la classe
	# FPS: le nombre d'images par secondes (pour les animations)
	# playfield : Rect, La taille du playfield (pour le clipping)
	def __init__(self, FPS, playfield):
		pygame.sprite.Sprite.__init__(self)

		self.initialradius = 5+(3-random.randint(0,6))	# taille initiale du cercle
		self.decreaseradius = 0.3+(0.05-random.randint(0,10)/100) # vitesse a laquelle la taille du cercle réduit
		self.speed = 15+random.randint(0,5) # vitesse initiale
		self.decreaseSpeed = 5*random.randint(0,9)/50 # facteur de deceleration
		self.direction = 0 # direction initiale (passée par setDirection())
		self.overture = 20 # ouverture des turbines (largeur de dispersion des particules)
		self.ttl = 30 # temps de vie maximum d'une particule en nombre d'animations

		self.radius = self.initialradius
		# la direction réelle de la particule est pondérée par l'ouverture des turbines, 
		# on utilise pour cela une répartition statistique basée sur une "loi normale", tu verras ca apres le bac
		self.gauss = random.gauss(0, self.overture)
		self.realdirection = self.direction+self.gauss 

		# un compteur pour faire disparaitre la particule une fois qu'elle a atteint le TTL
		self.counter = 0

		# on précacule les images des différentes tailles
		if(Particle.images == None):
			Particle.images = list()
			for i in range (0,9):
				image = pygame.Surface([16,16], pygame.SRCALPHA, 32)
				image = image.convert_alpha()
				pygame.draw.circle(image, (90,199,228,64), (8, 8), i)
				Particle.images.append(image)

		self.image = Particle.images[min(max(int(self.radius), 0),8)]
		self.rect = pygame.Rect(0,0,16,16)
		
		self.deltaTime = 0
		self.playfield = playfield

	def update(self,time):
		self.deltaTime = self.deltaTime + time
		if(self.deltaTime>50):
			self.deltaTime = 0

			self.image = Particle.images[min(max(int(self.radius), 0),8)]

			deplx = math.cos(self.realdirection*2*3.14/360) * self.speed
			deply = -math.sin(self.realdirection*2*3.14/360) * self.speed
			self.rect = self.rect.move(deplx, deply)

			self.speed = max(self.speed-self.decreaseSpeed, 0)
			if(self.speed==0):
				self.kill()

			self.radius = max(self.radius-self.decreaseradius, 0)
			if(self.radius==0):
				self.kill()

			self.counter += 1
			if(self.counter>self.ttl):
				self.kill()
	
	def setPosition(self, x, y):
		self.rect = pygame.Rect(x,y,self.rect.width,self.rect.height)

	def setPositionCenter(self, x, y):
		self.rect = pygame.Rect(x-self.rect.width/2,y-self.rect.height/2,self.rect.width,self.rect.height)

	# Position courante du sprite pour les tests de collision
	def getPosition(self):
		return self.rect

	def setDirection(self, direction):
		self.direction = direction%360
		self.realdirection = self.direction+self.gauss


