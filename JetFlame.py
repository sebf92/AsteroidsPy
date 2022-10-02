import pygame, math, random

def rot_center(image, angle, width, height):
	angle = angle%360
	rotated_image = pygame.transform.rotate(image, angle)
	new_rect = rotated_image.get_rect(center = image.get_rect(center = (width, height)).center)
	return rotated_image, new_rect

class JetFlame(pygame.sprite.Sprite):

	playfield = pygame.Rect((0,0),(0,0))

	spriteSheet = pygame.image.load("./Sprites/jetflame.png")

	# Constructeur de la classe
	# FPS: le nombre d'images par secondes (pour les animations)
	# playfield : Rect, La taille du playfield (pour le clipping)
	def __init__(self, FPS, playfield, spaceship):
		pygame.sprite.Sprite.__init__(self)

		self.spriteSheet.convert_alpha()
		self.spaceship = spaceship

		self.image = JetFlame.spriteSheet.subsurface(pygame.Rect(0,0,256,256))
		self.rect = pygame.Rect(0,0,256,256)
		self.rect.bottom = 256

		self.deltaTime = 0

		self.direction = 0
			
		self.playfield = playfield

	def update(self,time):
		self.deltaTime = self.deltaTime + time

		spaceshipPosition = self.spaceship.getPositionCenter()
		spaceshipDirection = self.spaceship.getDirection()
		self.setDirection(spaceshipDirection)

		deplx = math.cos(self.direction*2*3.14/360) * 80
		deply = -math.sin(self.direction*2*3.14/360) * 80

		self.rect = pygame.Rect(spaceshipPosition.x-self.rect.width/2-deplx, spaceshipPosition.y-self.rect.height/2-deply, self.rect.width, self.rect.height)

		if(self.deltaTime>50):
			self.deltaTime = 0
	
	def setPosition(self, x, y):
		self.rect = pygame.Rect(x,y,self.rect.width,self.rect.height)

	# Position courante du sprite pour les tests de collision
	def getPosition(self):
		return self.rect

	def setDirection(self, direction):
		newdirection = int(direction)%360
		if(self.direction!=newdirection):
			self.direction = direction%360

			(self.image,newrect) = rot_center(JetFlame.spriteSheet.subsurface(pygame.Rect(0,0,256,256)), direction, 256/2, 256/2)
			self.rect = pygame.Rect(self.rect.x, self.rect.y, newrect.width, newrect.height)


