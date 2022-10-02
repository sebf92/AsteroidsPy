import pygame,math,time

def rot_center(image, angle, width, height):
	angle = angle%360
	rotated_image = pygame.transform.rotate(image, angle)
	new_rect = rotated_image.get_rect(center = image.get_rect(center = (width, height)).center)
	return rotated_image, new_rect

def getTimeMillis():
	milliseconds = int(round(time.time() * 1000))
	return milliseconds

#
# Un sprite vaisseau spacial pour Asteroids
#
class Spaceship(pygame.sprite.Sprite):

	playfield = pygame.Rect((0,0),(0,0))

	spriteSheet = pygame.image.load("Sprites/spaceship.png")
	engineSound = None
	FPS = 60

	# Constructeur de la classe
	# FPS: le nombre d'images par secondes (pour les animations)
	# playfield : Rect, La taille du playfield (pour le clipping)
	def __init__(self, FPS, playfield):
		pygame.sprite.Sprite.__init__(self)

		# on converti le sprite pour activer la transparence
		self.spriteSheet.convert_alpha()

		if(Spaceship.engineSound==None):
			Spaceship.engineSound = pygame.mixer.Sound("sounds/engine.mp3")
			#Spaceship.engineSound.set_volume(0.5)

		# on initialise les variables
		self.image = Spaceship.spriteSheet
		self.mask = pygame.mask.from_surface(self.image)
		# la position du sprite
		self.position = pygame.Rect(0,0,128,128) # la VRAI position du sprite
		self.position.bottom = 128
		self.positionprecedente = self.position
		self.rect = self.position # la position a afficher (nous verrons que la rotation du sprite nous oblige a recalculer la position d'affichage (a cause de pythagore :-p))

		
		self.directioncourante = 0 # la direction courante du sprite en degrés (0 à 359)
		self.directionprecedente = 0

		# le débit du canon en nombre de coups par seconde
		self.weaponFlow = 10

		# il y a plusieurs variables pour gérer le déplacement de notre sprite car on veut
		# créer un effet d'inertie en fonction de si on appuie ou relache les touches
		# normalement lorsque l'on relache toutes les touches le vaiseau spatial fini par s'arreter tout seul

		# la gestion de la rotation du sprite
		self.rotation = 0 # son angle de rotation courant si il tourne
		self.rotationvel = 0 # la velocité de la rotation (tant que l'on reste appuyé sur la touche)
		self.rotationinertie = 0.125 # l'inertie de la rotation (lorsque l'on relache la touche)

		# la gestion de la vitesse du sprite
		self.velocite = 0 # la velocite du sprite (sa vitesse courante)
		self.acceleration = 0 # l'acceleration du sprite (tant que l'on reste appuyé sur la touche)
		self.inertie = 0.25 # l'inertie de la vitesse (lorsque l'on relache la touche)

		# permet de savoir si le vaiseau spatial s'est fait touché... utile pour les animations
		self.isInjured = False

		# ces variables nous permettent de corriger la position du sprite lorsqu'une rotation est en cours
		# regarde cette URL pour comprendre le probleme
		# https://stackoverflow.com/questions/4183208/how-do-i-rotate-an-image-around-its-center-using-pygame
		self.offsetx = 0
		self.offsety = 0
		self.currentwidth = 128
		self.currentheight = 128

		# des variables techniques...
		self.deltaTime = 0
		self.FPS = FPS
		self.playfield = playfield

		self.lastFireTime = 0

	def update(self,time):
		self.deltaTime = self.deltaTime + time
		
		# on sauvegarde la position courante pour revenir en arriere en cas de collision
		self.positionprecedente = pygame.Rect(self.position.x, self.position.y, self.position.width, self.position.height)

		# on gere l'acceleration et l'inertie
		if (self.acceleration==0):
			# pas d'acceleration en cours,
			# c'est donc l'inertie du vaisseau qui s'applique
			# pour le ralentir petit à petit
			self.velocite -= self.inertie
			if(self.velocite<0):
				self.velocite = 0
		else:
			# sinon une acceleration est en cours
			# donc on accelere!
			self.velocite += self.acceleration
			if(self.velocite>12): # enfin, pas trop quand meme...
				self.velocite = 12


		# on met a jour la position
		# si un deplacement est en cours
		if(self.velocite != 0):
			deplx = math.cos(self.directioncourante*2*3.14/360) * self.velocite
			deply = -math.sin(self.directioncourante*2*3.14/360) * self.velocite
			self.position = pygame.Rect(self.position.x+deplx, self.position.y+deply, self.position.width, self.position.height)

		self.position = self.position.clamp(self.playfield) # on garde le vaisseau dans l'ecran
		
		# une demande de rotation est en cours
		# on met a jour l'increment
		if(self.rotationvel!=0):
			self.rotation += self.rotationvel
			if(self.rotation<-3):
				self.rotation = -3
			elif(self.rotation>3):
				self.rotation = 3
		else:
			if(self.rotation>0):
				self.rotation -= self.rotationinertie
				if(self.rotation<0):
					self.rotation = 0
			elif(self.rotation<0):
				self.rotation += self.rotationinertie
				if(self.rotation>0):
					self.rotation = 0

		# on met a jour la direction courante
		self.directioncourante = self.directioncourante + self.rotation

		# on calcule l'image à afficher
		# -----------------------------
		# on calcule une nouvelle image si la direction du vaisseau a changé
		if(self.directionprecedente != self.directioncourante):
			self.directionprecedente = self.directioncourante
			(self.image, newrect) = rot_center(Spaceship.spriteSheet, self.directioncourante, 64, 64)			
			self.mask = pygame.mask.from_surface(self.image)
			self.offsetx = (newrect.width-128)/2
			self.offsety = (newrect.height-128)/2
			self.currentwidth = newrect.width
			self.currentheight = newrect.height

		# on met a jour la position du sprite
		# on est obligé de calculer un carré d'affichage différent de la position
		# car lorsque le sprite tourne, sa taille augmente... (rappelle toi Pythagore!)
		self.rect = pygame.Rect(self.position.x-self.offsetx, self.position.y-self.offsety,self.currentwidth, self.currentheight)

	def goLeft(self):
		self.rotationvel = 0.25

	def stopLeft(self):
		self.rotationvel = 0

	def goRight(self):
		self.rotationvel = -0.25

	def stopRight(self):
		self.rotationvel = 0

	def accelerate(self):
		self.acceleration = 0.25
		self.playEngineSound()

	def slowdown(self):
		self.acceleration = 0
		self.stopEngineSound()

	# retourne True si c'est un nouveau dommage, False si un dommage est deja en cours de traitement
	def injured(self):
		self.isInjured = True
		return True

	def collision(self):
		# on reinitialise la position courante du sprite a la position precedente
		self.rect = pygame.Rect(self.positionprecedente.x, self.positionprecedente.y, self.positionprecedente.width, self.positionprecedente.height)

		# si le saut est consécutif a un dommage, on reactive le compteur de dommage
		self.isInjured = False

	def setPosition(self, x, y):
		self.position = pygame.Rect(x, y, 128, 128)

	# Position courante du sprite pour les tests de collision
	# on retourne la position reelle
	def getPosition(self):
		return self.position

	def getDirection(self):
		return int(self.directioncourante)

	def getWeaponPosition(self):
		deplx = math.cos(self.directioncourante*2*3.14/360) * 58
		deply = -math.sin(self.directioncourante*2*3.14/360) * 58
		x = self.position.x + 64
		y = self.position.y + 64
		x += deplx
		y += deply

		return pygame.Rect(x,y,1,1)

	def getEnginePosition(self):
		deplx = math.cos((self.directioncourante+180)*2*3.14/360) * 45
		deply = -math.sin((self.directioncourante+180)*2*3.14/360) * 45
		x = self.position.x + 64
		y = self.position.y + 64
		x += deplx
		y += deply

		return pygame.Rect(x,y,1,1)

	def getPositionCenter(self):
		x = self.rect.x+self.rect.width/2
		y = self.rect.y+self.rect.height/2
		return pygame.Rect(x,y,self.rect.width, self.rect.height)

	def getVitesse(self):
		return self.velocite

	# permet de savoir si on peut tirer
	# gere le débit du canon
	def canFire(self, time):
		time = getTimeMillis()
		if(time-self.lastFireTime>(1000/self.weaponFlow)): # self.weaponFlow coups par seconde
			self.lastFireTime = time
			return True
		else:
			return False

	def playEngineSound(self):
		Spaceship.engineSound.play(loops=-1)

	def stopEngineSound(self):
		Spaceship.engineSound.stop()

	def kill(self):
		pygame.sprite.Sprite.kill(self)
		self.stopEngineSound()

