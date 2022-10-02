import pygame, math, random

class TextOverlay(pygame.sprite.Sprite):

	playfield = pygame.Rect((0,0),(0,0))

	# Constructeur de la classe
	# playfield : Rect, La taille du playfield (pour le clipping)
	def __init__(self, playfield):
		pygame.sprite.Sprite.__init__(self)

		self.rect = pygame.Rect(0,0,1,1)
		self.deltaTime = 0
		self.playfield = playfield
		self.font = pygame.font.Font("fonts/Space Rave Italic.ttf", 36)

		self.setText('Text Overlay')
		self.setColor((255,255,255,255))
		self.setSize(36)


	def update(self,time):
		if(self.dirty):
			self.updateImage()
	
	def setPosition(self, x, y):
		self.rect = pygame.Rect(x,y,self.rect.width,self.rect.height)

	# Position courante du sprite pour les tests de collision
	def getPosition(self):
		return self.rect

	def setText(self, text):
		self.text = text
		self.dirty = True

	def setSize(self, size):
		self.size = size
		self.font = pygame.font.Font("fonts/Space Rave Italic.ttf", size)
		self.dirty = True

	def setColor(self, color):
		self.color = color
		self.dirty = True

	def updateImage(self):
		self.image = self.font.render(self.text, True, self.color)
		self.rect = pygame.Rect(self.rect.x, self.rect.y, self.image.get_width(), self.image.get_height()).clamp(self.playfield)
		self.dirty = False

