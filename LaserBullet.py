import pygame, math, random

def rot_center(image, angle, width, height):
	angle = angle%360
	rotated_image = pygame.transform.rotate(image, angle)
	new_rect = rotated_image.get_rect(center = image.get_rect(center = (width, height)).center)
	return rotated_image, new_rect

class LaserBullet(pygame.sprite.Sprite):

	playfield = pygame.Rect((0,0),(0,0))
	spriteSheet = pygame.image.load("./Sprites/laser.png")
	lasersound = None

	spriteArray = None
	maskArray = None
	offsetArray = None
	sizeArray = None

	# Constructeur de la classe
	# FPS: le nombre d'images par secondes (pour les animations)
	# playfield : Rect, La taille du playfield (pour le clipping)
	def __init__(self, FPS, playfield, spaceship = None):
		pygame.sprite.Sprite.__init__(self)

		self.spriteSheet.convert_alpha()
		
		# on précalcule le laser sur 360 degrés
		if(LaserBullet.spriteArray == None):
			LaserBullet.spriteArray = list()
			LaserBullet.maskArray = list()
			# ces variables nous permettent de corriger la position du sprite lorsqu'une rotation est en cours
			# regarde cette URL pour comprendre le probleme
			# https://stackoverflow.com/questions/4183208/how-do-i-rotate-an-image-around-its-center-using-pygame
			LaserBullet.offsetArray = list()
			LaserBullet.sizeArray = list()
			for direction in range(0,360):
				(image,newrect) = rot_center(LaserBullet.spriteSheet.subsurface(pygame.Rect(0,0,64,64)), direction, 32, 32)
				mask = pygame.mask.from_surface(image)
				LaserBullet.spriteArray.append(image)
				LaserBullet.maskArray.append(mask)
				LaserBullet.offsetArray.append( ((newrect.width-64)/2, (newrect.height-64)/2) )
				LaserBullet.sizeArray.append( (newrect.width, newrect.height) )

		self.positionx = 0	
		self.positiony = 0	

		self.image = LaserBullet.spriteSheet.subsurface(pygame.Rect(0,0,64,64))
		self.mask = pygame.mask.from_surface(self.image)
		self.rect = pygame.Rect(self.positionx,self.positiony,64,64)
		self.rect.bottom = 64

		self.deltaTime = 0

		self.vitesse = 5
		self.direction = 0
			
		self.playfield = playfield

		if(LaserBullet.lasersound==None):
			LaserBullet.lasersound = pygame.mixer.Sound("sounds/laser.mp3")
			LaserBullet.lasersound.set_volume(0.5)

		if(spaceship!=None):
			weaponposition = spaceship.getWeaponPosition()
			direction = spaceship.getDirection()
			vitesse = spaceship.getVitesse()
			self.setDirection(direction)
			self.setVitesse(vitesse+5)
			self.setPositionCenter(weaponposition.x, weaponposition.y)

	def update(self,time):
		self.deltaTime = self.deltaTime + time
		
		deplx = math.cos(self.direction*2*3.14/360) * self.vitesse
		deply = -math.sin(self.direction*2*3.14/360) * self.vitesse

		self.positionx += deplx
		self.positiony += deply

		if(self.positionx<-64):
			self.kill()
		if(self.positiony<-64):
			self.kill()
		if(self.positionx>self.playfield.width+64):
			self.kill()
		if(self.positiony>self.playfield.height+64):
			self.kill()

		self.image = LaserBullet.spriteArray[self.direction]
		self.mask = LaserBullet.maskArray[self.direction]

		offsetx = LaserBullet.offsetArray[self.direction][0]
		offsety = LaserBullet.offsetArray[self.direction][1]
		width = LaserBullet.sizeArray[self.direction][0]
		height = LaserBullet.sizeArray[self.direction][1]
		self.rect = pygame.Rect(self.positionx-offsetx, self.positiony-offsety, width, height)

		if(self.deltaTime>50):
			self.deltaTime = 0
			self.vitesse += 1
			if(self.vitesse>20):
				self.vitesse=20
	
	def setPosition(self, x, y):
		self.positionx = x
		self.positiony = y
		self.rect = pygame.Rect(x,y,64,64)

	def setPositionCenter(self, x, y):
		self.positionx = x-64/2
		self.positiony = y-64/2
		self.rect = pygame.Rect(self.positionx,self.positiony,64,64)

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

	def setDirection(self, direction):
		self.direction = direction%360

	def getDirection(self):
		return self.direction

	def playSound(self):
		LaserBullet.lasersound.play()


