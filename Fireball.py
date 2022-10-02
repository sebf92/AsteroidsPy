import pygame, math, random

class Fireball(pygame.sprite.Sprite):

	playfield = pygame.Rect((0,0),(0,0))

	spriteSheet = pygame.image.load("./Sprites/fireball.png")

	spritearray = None
	maskarray = None

	# Constructeur de la classe
	# FPS: le nombre d'images par secondes (pour les animations)
	# playfield : Rect, La taille du playfield (pour le clipping)
	def __init__(self, FPS, playfield):
		pygame.sprite.Sprite.__init__(self)

		Fireball.spriteSheet.convert_alpha()

		self.positionx = 0	
		self.positiony = 0	
		self.spritesize = 77

		# on précalcule les sprites et les masques correspondants
		# pour les animations
		if(Fireball.spritearray == None):
			Fireball.spritearray = []
			Fireball.maskarray = []
			for i in range(0,24):
				sprite = Fireball.spriteSheet.subsurface(pygame.Rect(32+(i%6)*133,37+(i//6)*133,self.spritesize,self.spritesize))
				Fireball.spritearray.append(sprite)
				Fireball.maskarray.append(pygame.mask.from_surface(sprite))
				


		self.image = Fireball.spritearray[0]
		self.mask = Fireball.maskarray[0]

		self.rect = pygame.Rect(self.positionx,self.positiony,self.spritesize,self.spritesize)
		self.rect.bottom = self.spritesize
		self.previousrect = self.rect

		self.numeroImage = 0

		self.deltaTime = 0

		self.vitesse = 0
		self.direction = 0
			
		self.playfield = playfield

	def update(self,time):
		self.deltaTime = self.deltaTime + time
		
		deplx = math.cos(self.direction*2*3.14/360) * self.vitesse
		deply = -math.sin(self.direction*2*3.14/360) * self.vitesse

		self.positionx += deplx
		self.positiony += deply

		self.previousrect = pygame.Rect(self.rect.x, self.rect.y, 52, 52)
		self.rect = pygame.Rect(self.positionx, self.positiony, self.spritesize, self.spritesize)

		if (self.rect.x<-self.spritesize):
			self.rect.x = -self.spritesize
			self.direction = self.direction+120 + (random.randint(0,46)-23)
		if (self.rect.x>self.playfield.width):
			self.rect.x = self.playfield.width
			self.direction = self.direction+120 + (random.randint(0,46)-23)
		if (self.rect.y<-self.spritesize):
			self.rect.y = -self.spritesize
			self.direction = self.direction+120 + (random.randint(0,46)-23)
		if (self.rect.y>self.playfield.height):
			self.rect.y = self.playfield.height
			self.direction = self.direction+120 + (random.randint(0,46)-23)

		if self.deltaTime>=250/(self.vitesse+1):
			self.deltaTime = 0

			# on calcule l'image à afficher
			self.image = Fireball.spritearray[self.numeroImage]
			self.mask = Fireball.maskarray[self.numeroImage]
			
			self.numeroImage = self.numeroImage+1
			self.numeroImage = self.numeroImage%len(Fireball.spritearray)
			
	
	def setPosition(self, x, y):
		self.positionx = x
		self.positiony = y
		self.rect = pygame.Rect(x,y,self.spritesize,self.spritesize)

	def collision(self):
		self.rect = self.previousrect

	# Position courante du sprite pour les tests de collision
	def getPosition(self):
		return self.rect

	def getPositionCenter(self):
		x = self.rect.x+self.rect.width/2
		y = self.rect.y+self.rect.height/2
		return pygame.Rect(x,y,self.rect.width, self.rect.height)

	def setVitesse(self, vitesse):
		self.vitesse = vitesse
		if(self.vitesse<0):
			self.vitesse = 0
		if(self.vitesse>10):
			self.vitesse = 10

	def getVitesse(self):
		return self.vitesse

	def setDirection(self, direction):
		self.direction = direction%360

	def getDirection(self):
		return self.direction

