import pygame, math, random
import json, os

class HiScore(pygame.sprite.Sprite):

	playfield = pygame.Rect((0,0),(0,0))

	# Constructeur de la classe
	# FPS: le nombre d'images par secondes (pour les animations)
	# playfield : Rect, La taille du playfield (pour le clipping)
	def __init__(self, FPS, playfield):
		pygame.sprite.Sprite.__init__(self)

		self.image = None
		self.rect = pygame.Rect(0,0,52,52)
		self.rect.bottom = 52
	
		self.font = pygame.font.Font("fonts/Space Rave Italic.ttf", 64)

		self.dirty = True
		self.hiscoremaxlistsize = 10
		self.hiscore = list()

		if(os.path.isfile('hiscores.json')):
			# on charge les scores sur disque
			# si le fichier existe
			with open('hiscores.json', 'r') as filehandle:
				self.hiscore = json.load(filehandle)
		else:
			# sinon on créé une table de hiscores par défaut
			self.addScore(10000, "JOHN WICK")
			self.addScore(9000, "JACK REACHER")
			self.addScore(8000, "HARRY POTTER")
			self.addScore(7000, "JAMES BOND")
			self.addScore(6000, "JACK SPARROW")
			self.addScore(5000, "JOHN CALAGAN")
			self.addScore(4000, "HENRI FONDA")
			self.addScore(3000, "BILBON SAQUET")
			self.addScore(2000, "SARAH CONNORS")
			self.addScore(1000, "VOLDEMORT")

		self.playfield = playfield

		self.createImage()

		self.deltaTime = 0

	def update(self,time):
		self.deltaTime = self.deltaTime + time
		
		if self.deltaTime>=30:
			self.deltaTime = 0

			if(self.rect.y>=100):
				self.rect = self.rect.move(0,-2)
	
		if(self.dirty):
			# on sauvegarde les scores sur disque
			# car la table de highscore a été modifiée
			with open('hiscores.json', 'w') as filehandle:
				json.dump(self.hiscore, filehandle)
			# on met a jour l'image à afficher
			self.createImage()

	def setPosition(self, x, y):
		self.positionx = x
		self.positiony = y
		self.rect = pygame.Rect(x,y,self.image.get_width(),self.image.get_height())

	def getPosition(self):
		return self.rect

	# Ajoute un nouveau score dans la liste
	def addScore(self, score, playername):
		# on ajoute le score avec une logique de tri par insertion
		i=0
		inserted = False
		while(i<len(self.hiscore)):
			(currentscore, currentname) = self.hiscore[i]
			if(score>currentscore):
				self.hiscore.insert(i, (score, playername))
				inserted = True
				break
			i += 1
		# si le score n'a pas été inséré dans la liste
		# alors on l'ajoute a la fin de la liste
		if(not inserted):
			self.hiscore.append((score, playername))

		# on limite la taille totale de la liste à self.hiscoremaxlistsize elements
		# en supprimant le ou les derniers elements
		while(len(self.hiscore)>self.hiscoremaxlistsize):
			del self.hiscore[-1]

		self.dirty = True

	def createImage(self):
		# on consolide les textes a afficher
		text = list()
		text.append("*** HALL OF FAME ***")
		text.append("")
		for (currentscore, currentname) in self.hiscore:
			scorestr = str(currentscore).zfill(5)
			txt = scorestr+" "+currentname
			text.append(txt)

		# on créé une grande image
		self.image = pygame.Surface([1080,len(text*140)], pygame.SRCALPHA, 32)
		self.image = self.image.convert_alpha()
		self.rect = pygame.Rect(200,self.playfield.height+50,self.image.get_width(),self.image.get_height())

		# on prépare des variables pour faire un dégradé de couleur qui part du blanc pour aller vers une couleur finale
		colr = 255
		colg = 255
		colb = 255
		red = 179
		green = 121
		blue = 37
		decr = (colr-red)/len(text)
		decg = (colg-green)/len(text)
		decb = (colb-blue)/len(text)

		# on écrit le texte dans la grande image
		offsetx = 0
		for txt in text:
			part = self.font.render(txt, True, (colr, colg, colb))
			colr -= decr
			colg -= decg
			colb -= decb
			self.image.blit(part, (0,offsetx))
			offsetx += 70

		self.dirty = False
