# #####################################################################################
#
# Un exemple de jeu Asteroids en Python
#
# Julien FAIVRE
# #####################################################################################

# Ne pas oublier d'installer les librairies manquantes:
# pip install pygame

import sys,pygame,random
import tkinter as tk

from Spaceship import Spaceship
from Asteroid import Asteroid
from Fireball import Fireball
from Explosion import Explosion
from LaserBullet import LaserBullet
from JetFlame import JetFlame
from Hiscore import HiScore
from TextOverlay import TextOverlay
from Particle import Particle
from tkinter import simpledialog

# Paramètres principaux du jeu
WIDTH = 1920
HEIGHT = 1080
FPS = 60 
FULLSCREEN = False
SHOWFPS = True
MUSIC = True
TITLE = "Astero-Py"
PLAYERNAME = None
MUNITIONS = 200
WITHPARTICLESENGINE = True # Active le moteur de particules pour simuler le moteur, plus joli mais un peu plus lent
INDESTRUCTIBLE = False # Pour les tests uniquement ! (tricheur :-p)

# NOM DU JOUEUR
# -------------
# Le nom du joueur est passé en parametre de ligne de commande
if(len(sys.argv)>1):
	PLAYERNAME = sys.argv[1]
# sinon on demande le nom du joueur
if(PLAYERNAME == None):
	application_window = tk.Tk()
	application_window.withdraw()
	PLAYERNAME = simpledialog.askstring("Joueur 1", "Quel est ton prénom?\t\t\t\t\t\t",
									parent=application_window, initialvalue="Julien")
	application_window.destroy()
# Par défaut on met Anonyme
if(PLAYERNAME == None or len(PLAYERNAME.lstrip().rstrip())==0):
	PLAYERNAME = "Anonyme"
else:
	PLAYERNAME = PLAYERNAME.lstrip().rstrip() # on enleve les espaces au debut et à la fin
	PLAYERNAME = PLAYERNAME[:20] # on prend les 20 premiers caractères 

# On initialise les variables du jeu
pygame.init()
pygame.mixer.init()
if(FULLSCREEN):
	screen = pygame.display.set_mode((WIDTH,HEIGHT), pygame.FULLSCREEN | pygame.DOUBLEBUF, vsync=1)
	WIDTH = screen.get_width()
	HEIGHT = screen.get_height()
else:
	screen = pygame.display.set_mode((WIDTH,HEIGHT))


pygame.display.set_caption(TITLE)
playfield = pygame.Rect(0,0,WIDTH,HEIGHT)

# on charge et on retaille les images si besoin en les centrant sur l'ecran
imageAccueil = pygame.image.load("splashscreens/splashscreen.jpg").convert()
tmp = pygame.Surface([WIDTH,HEIGHT])
(iw,ih) = imageAccueil.get_size()
tmp.blit(imageAccueil, ((WIDTH-iw)/2,(HEIGHT-ih)/2))
imageAccueil = tmp

fond = pygame.image.load("splashscreens/fond.jpg").convert()
tmp = pygame.Surface([WIDTH,HEIGHT])
(iw,ih) = fond.get_size()
tmp.blit(fond, ((WIDTH-iw)/2,(HEIGHT-ih)/2))
fond = tmp

gameover = pygame.image.load("splashscreens/fin.jpg").convert()
tmp = pygame.Surface([WIDTH,HEIGHT])
(iw,ih) = gameover.get_size()
tmp.blit(gameover, ((WIDTH-iw)/2,(HEIGHT-ih)/2))
gameover = tmp

# on charge la musique
pygame.mixer.music.load('soundtracks/My Pixels Are Weapons.mp3')

# on cache le curseur de la souris
pygame.mouse.set_visible(False)

# On démarre la musique en boucle
if MUSIC:
	pygame.mixer.music.play(loops=-1)

# on initialise la table de hiscore
hiscore = HiScore(FPS, playfield)

while True: # on boucle entre ecran accueil -> jeu -> panneau de fin de partie

	# ##################################################
	# ##################################################
	# Ecran d'acceuil
	# ##################################################
	# ##################################################
	(w,h) = pygame.display.get_surface().get_size()
	pygame.draw.rect(screen, (0,0,0), pygame.Rect(0,0,w,h))
	(iw,ih) = imageAccueil.get_size()

	# on affiche l'image d'accueil au centre de l'ecran
	screen.blit(imageAccueil, ((w-iw)/2,(h-ih)/2))

	clock = pygame.time.Clock()
	ecranprincipal = True
	while ecranprincipal:
		# on limite l'affichage à FPS images par secondes
		time = clock.tick(FPS)	
		
		# on gère les evenements clavier
		###################
		for event in pygame.event.get():
			if event.type == pygame.QUIT: 
				pygame.quit()
				sys.exit(0)
			elif event.type == pygame.KEYDOWN:
				# on active/desactive la musique
				if event.key == pygame.K_m:
					if(MUSIC):
						pygame.mixer.music.fadeout(1000)
						MUSIC = False
					else:
						pygame.mixer.music.play(loops=-1)
						MUSIC = True
				# on quitte si on appui sur la touche ESC
				if event.key == pygame.K_ESCAPE:
					pygame.quit()
					sys.exit(0)
			# on gère l'appui sur la barre espace
				elif event.key == pygame.K_SPACE:
					ecranprincipal = False

		pygame.display.flip()

	# ##################################################
	# ##################################################
	# Boucle principale du jeu
	# ##################################################
	# ##################################################
	jeuencours = True
	nbasteroids = 15
	nbfireballs = 0
	score = 0
	scorecounter = 0
	ammunition = MUNITIONS
	while(jeuencours):
		# on initialise une liste d'asteroids
		asteroids = pygame.sprite.RenderClear()
		for i in range(0,nbasteroids):
			# on calcule au hazard des coordonnées de départ
			# pour les asteroides tout en evitant le centre de l'ecran
			# car il y a le vaisseau
			
			x=0
			y=0
			if(random.randint(0,2)==1):
				if(random.randint(0,2)==1): # asteroid a gauche ou a droite au hasard
					x = random.randint(0,int(WIDTH/16))
					y = random.randint(0,HEIGHT)			
				else:
					x = WIDTH-random.randint(0,int(WIDTH/16))
					y = random.randint(0,HEIGHT)			
			else:
				if(random.randint(0,2)==1): # asteroid en haut ou en bas au hasard
					x = random.randint(0,WIDTH)
					y = random.randint(0,int(HEIGHT/16))			
				else:
					x = random.randint(0,WIDTH)
					y = HEIGHT-random.randint(0,int(HEIGHT/16))			
			asteroid = Asteroid(FPS, playfield)
			asteroid.setPosition(x, y)
			asteroid.setDirection(random.randint(0,359)) # direction au hasard
			asteroid.setVitesse(1+random.randint(1, 20)/10) # vitesse au hasard mais au moins égale à 1

			asteroids.add(asteroid)

		# on initialise une liste de boules de feu
		fireballs = pygame.sprite.RenderClear()
		for i in range(0,int(nbfireballs)):
			# on calcule au hazard des coordonnées de départ
			# pour les asteroides tout en evitant le centre de l'ecran
			# car il y a le vaisseau
			
			x=0
			y=0
			if(random.randint(0,2)==1):
				if(random.randint(0,2)==1): # asteroid a gauche ou a droite au hasard
					x = int(WIDTH/16)+100+random.randint(0,int(WIDTH/16))
					y = random.randint(0,HEIGHT)			
				else:
					x = WIDTH-int(WIDTH/16)-100-random.randint(0,int(WIDTH/16))
					y = random.randint(0,HEIGHT)			
			else:
				if(random.randint(0,2)==1): # asteroid en haut ou en bas au hasard
					x = random.randint(0,WIDTH)
					y = int(HEIGHT/16)+100+random.randint(0,int(HEIGHT/16))			
				else:
					x = random.randint(0,WIDTH)
					y = HEIGHT-int(HEIGHT/16)-100-random.randint(0,int(HEIGHT/16))			
			fireball = Fireball(FPS, playfield)
			fireball.setPosition(x, y)
			fireball.setDirection(random.randint(0,359)) # direction au hasard
			fireball.setVitesse(3+random.randint(1, 30)/10) # vitesse au hasard mais au moins égale à 3

			fireballs.add(fireball)

		# on initialise le vaisseau spatial
		spaceship = Spaceship(FPS, playfield)
		xpos = (playfield.width-spaceship.rect.width)/2
		ypos = (playfield.height-spaceship.rect.height)/2
		spaceship.setPosition(xpos, ypos)

		# on initialise les flammes du booster du vaisseau spatial
		jetflame = JetFlame(FPS, playfield, spaceship)

		# on efface l'ecran
		(w,h) = pygame.display.get_surface().get_size()
		pygame.draw.rect(screen, (0,0,0), pygame.Rect(0,0,w,h))
		(iw,ih) = fond.get_size()
		screen.blit(fond, ((w-iw)/2,(h-ih)/2))

		# on initialise des listes qui contiendront
		# les explosions en cours
		# ainsi que les balles en cours
		explosions = pygame.sprite.RenderClear()
		bullets = pygame.sprite.RenderClear()

		# Le vaisseau spatial
		spaceshipGroup = pygame.sprite.RenderClear()
		spaceshipGroup.add(spaceship)
		flameGroup = pygame.sprite.RenderClear()
		flameGroup.add(jetflame)
		particleGroup = pygame.sprite.RenderClear() # contient les particules du moteur (si WITHPARTICLESENGINE = True)

		engineon = False # passe a True quand les moteurs sont allumés


		# le score et les munitions
		scorewidget = TextOverlay(playfield)
		scorewidget.setPosition(10,0)
		scorewidget.setSize(96)
		scorewidget.setText("SCORE 00000")

		ammunitionwidget = TextOverlay(playfield)
		ammunitionwidget.setPosition(WIDTH-950,0)
		ammunitionwidget.setSize(96)
		ammunitionwidget.setText("AMMUNITION 0000")

		fpswidget = TextOverlay(playfield)
		fpswidget.setPosition(0,HEIGHT-50)
		fpswidget.setSize(36)
		fpswidget.setText("00 FPS")

		overlays = pygame.sprite.RenderClear()
		overlays.add(scorewidget)
		overlays.add(ammunitionwidget)
		if(SHOWFPS):
			overlays.add(fpswidget)

		clock = pygame.time.Clock()
		deltatime = 0

		# on boucle tant que:
		# - le jeu est en cours (vaisseau en vie et pas d'appui sur la touche ESC)
		# - il reste des asteroids
		# on attend aussi avant de sortir que toutes les animations d'explosion soient finies
		fire = False
		while (jeuencours and len(asteroids)>0) or len(explosions)>0:
			time = clock.tick(FPS)	# on limite l'affichage à FPS images par secondes
			deltatime += time # temps total depuis le debut du jeu en ms
			
			# on gère les evenements clavier
			###################
			for event in pygame.event.get():
				if event.type == pygame.QUIT: 
					pygame.quit()
					sys.exit(0)
				elif event.type == pygame.KEYDOWN:
					# on active/desactive la musique
					if event.key == pygame.K_m:
						if(MUSIC):
							pygame.mixer.music.fadeout(1000)
							MUSIC = False
						else:
							pygame.mixer.music.play(loops=-1)
							MUSIC = True
					# on active/desactive le mode triche (invincible)
					elif event.key == pygame.K_u:
						INDESTRUCTIBLE = not INDESTRUCTIBLE
					# on ajoute des munitions (mode triche)
					elif event.key == pygame.K_r:
						ammunition += 100
						if(ammunition>9999):
							ammunition = 9999
					# on active/desactive les FPS
					elif event.key == pygame.K_f:
						SHOWFPS = not SHOWFPS
						if(SHOWFPS):
							overlays.add(fpswidget)
						else:
							overlays.remove(fpswidget)

					# on quitte la partie sur touche escape						
					if event.key == pygame.K_ESCAPE:
						jeuencours = False
					# on gere les touches du jeu
					elif event.key == pygame.K_LEFT:
						spaceship.goLeft()
					elif event.key == pygame.K_RIGHT:
						spaceship.goRight()
					elif event.key == pygame.K_SPACE:
						spaceship.accelerate()
						engineon = True
					elif event.key == pygame.K_LCTRL:
						fire = True
				elif event.type == pygame.KEYUP:
					if event.key == pygame.K_LEFT:
						spaceship.stopLeft()
					elif event.key == pygame.K_RIGHT:
						spaceship.stopRight()
					elif event.key == pygame.K_SPACE:
						spaceship.slowdown()
						engineon = False
					elif event.key == pygame.K_LCTRL:
						fire = False

			# si le moteur est allumé en mode "particules" alors on alimente la table des particules
			if(WITHPARTICLESENGINE):
				if(jeuencours and engineon):
					for i in range(0,10):
						particle = Particle(FPS, playfield)
						particle.setPositionCenter(spaceship.getEnginePosition().x,spaceship.getEnginePosition().y)
						particle.setDirection((180+spaceship.getDirection())%360)
						particleGroup.add(particle)

			# plus de munitions? le vaisseau explose...
			if(jeuencours and ammunition==0 and len(bullets)==0):
				explosion = Explosion(FPS, playfield, spaceship)
				explosions.add(explosion)
				explosion.playSound()

				spaceship.kill()
				jetflame.kill()
				#spaceshipGroup.empty()
				#flameGroup.empty()
				
				jeuencours = False

			# le vaisseau tire un laser
			if(fire and jeuencours): # on doit tirer?
				if(spaceship.canFire(time)): # le vaisseau peut tirer?
					if(ammunition>0): # il reste des munitions?						
						ammunition -= 1
						bullet = LaserBullet(FPS, playfield, spaceship)
						bullets.add(bullet)
						bullet.playSound()

			# on traite les collisions
			# entre les lasers et les asteroides
			laserhits = pygame.sprite.groupcollide(bullets, asteroids, True, True, pygame.sprite.collide_mask)
			for laserhit in laserhits: # si des lasers ont touchés des asteroids
				asteroidshit = laserhits.get(laserhit) # pour chaque laser on récupère la liste des asteroides qui ont été touchés
				for collision_ennemi in asteroidshit:
					# on créé une explosion à l'emplacement de l'asteroide
					explosion = Explosion(FPS, playfield, collision_ennemi)
					explosions.add(explosion)
					explosion.playSound()
					# on augmente le score
					score += 100

			# on traite les collisions
			# entre les lasers et les fireballs
			laserhits = pygame.sprite.groupcollide(bullets, fireballs, True, False, pygame.sprite.collide_mask)
			for laserhit in laserhits: # si des lasers ont touchés des asteroids
				asteroidshit = laserhits.get(laserhit) # pour chaque laser on récupère la liste des fireballs qui ont été touchés
				for collision_ennemi in asteroidshit:
					# on créé une explosion à l'emplacement du fireball
					explosion = Explosion(FPS, playfield, collision_ennemi)
					explosions.add(explosion)
					explosion.playSound()


			# on traite les collisions
			# entre les fireballs et les asteroides
			fireballhits = pygame.sprite.groupcollide(fireballs, asteroids, False, False, pygame.sprite.collide_mask)
			for fireballhit in fireballhits: # si des lasers ont touchés des asteroids
				asteroidshit = fireballhits.get(fireballhit) # pour chaque laser on récupère la liste des asteroides qui ont été touchés
				for collision_ennemi in asteroidshit:
					fireballhit.setDirection(fireballhit.getDirection()+90)
					collision_ennemi.collision()
					collision_ennemi.setDirection(collision_ennemi.getDirection()+90)
					collision_ennemi.setVitesse(collision_ennemi.getVitesse()+1)

			# on traite les collisions
			# entre le vaisseau et les asteroides
			if(deltatime > 2000 and not INDESTRUCTIBLE): # on laisse 2 secondes au démarrage du jeu pour eviter de mourir tout de suite
				collisionlist = pygame.sprite.spritecollide(spaceship,asteroids,True, pygame.sprite.collide_mask)
				for collision_ennemi in collisionlist: # collision détectée
					# on créé une explosion à l'emplacement de l'asteroide
					positionvaisseau = spaceship.getPositionCenter()
					explosion = Explosion(FPS, playfield)
					explosion.setPositionCenter(positionvaisseau.x, positionvaisseau.y)
					explosions.add(explosion)
					explosion.playSound()
					# on arrete la partie
					spaceship.kill()
					jetflame.kill()
					#spaceshipGroup.empty()
					#flameGroup.empty()
					jeuencours = False

			# on traite les collisions
			# entre le vaisseau et les fireballs
			if(deltatime > 2000 and not INDESTRUCTIBLE): # on laisse 2 secondes au démarrage du jeu pour eviter de mourir tout de suite
				collisionlist = pygame.sprite.spritecollide(spaceship,fireballs,True, pygame.sprite.collide_mask)
				for collision_ennemi in collisionlist: # collision détectée
					# on créé une explosion à l'emplacement de l'asteroide
					positionvaisseau = spaceship.getPositionCenter()
					explosion = Explosion(FPS, playfield)
					explosion.setPositionCenter(positionvaisseau.x, positionvaisseau.y)
					explosions.add(explosion)
					explosion.playSound()
					# on arrete la partie
					spaceship.kill()
					jetflame.kill()
					#spaceshipGroup.empty()
					#flameGroup.empty()
					jeuencours = False

			# on met a jour les overlays
			# on calcule le nombre de FPS
			if(SHOWFPS):
				nbimagessec = 1000//time
				txtnbimagessec = str(nbimagessec) + " FPS"
				fpswidget.setText(txtnbimagessec)
			# on met a jour le widget score
			if(scorecounter<score): # petite animation sur le score
				scorecounter += max((score-scorecounter)//10,1)
			scoretxt = "SCORE "+str(scorecounter).zfill(5)
			scorewidget.setText(scoretxt)
			# on met a jour le widget munitions
			ammunitiontxt = "AMMUNITION "+str(ammunition).zfill(4)
			ammunitionwidget.setText(ammunitiontxt)

			# on met a jour les positions des sprites
			# (on met a jour les positions apres les tests de collision pour afficher le chevauchement entre les sprites en cas de collision)
			bullets.update(time)
			asteroids.update(time)
			fireballs.update(time)
			explosions.update(time)

			spaceshipGroup.update(time)
			if(WITHPARTICLESENGINE):
				particleGroup.update(time)
			else:
				flameGroup.update(time)

			overlays.update(time)

			# on efface le fond
			asteroids.clear(screen, fond)
			fireballs.clear(screen, fond)
			bullets.clear(screen, fond)
			explosions.clear(screen, fond)
			spaceshipGroup.clear(screen, fond)
			overlays.clear(screen, fond)

			if(WITHPARTICLESENGINE):
				particleGroup.clear(screen, fond)
			else:
				flameGroup.clear(screen, fond)

			# on met a jour l'ecran

			# le moteur
			if(WITHPARTICLESENGINE):
				particleGroup.draw(screen) # on affiche les particules du moteur si il y en as
			else:
				if(engineon): # on affiche des flammes sous le vaisseau si les moteurs sont allumés
						flameGroup.draw(screen)

			# on affiche les lasers
			bullets.draw(screen)
			# on affiche les asteroides
			asteroids.draw(screen)
			fireballs.draw(screen)
			# on affiche les explosions
			explosions.draw(screen)
			# on affiche le vaisseau
			spaceshipGroup.draw(screen)
			# on affiche les textes
			overlays.draw(screen)

			# on rafraichit l'écran
			pygame.display.update()

		# on passe au niveau suivant:
		nbasteroids += 5 # on augmente le nombre d'asteroids et on part sur un nouveau niveau
		nbfireballs += 0.5 # on augmente le nombre de fireballs et on part sur un nouveau niveau
		ammunition += nbasteroids*2 # on recharge les munitions, on ajoute 2x plus de munitions que d'asteroides à détruire

	# ##################################################
	# ##################################################
	# fin
	# ##################################################
	# ##################################################

	# on insere le score du joueur
	# dans la table des HiScore
	hiscore.addScore(score, PLAYERNAME)

	# on efface l'ecran
	(w,h) = pygame.display.get_surface().get_size()
	pygame.draw.rect(screen, (0,0,0), pygame.Rect(0,0,w,h))
	(iw,ih) = gameover.get_size()

	clock = pygame.time.Clock()
	jeuencours = True
	while jeuencours:
		# on limite l'affichage à FPS images par secondes
		time = clock.tick(FPS)	
		
		# on gère les evenements clavier
		###################
		for event in pygame.event.get():
			if event.type == pygame.QUIT: 
				pygame.quit()
				sys.exit(0)
			elif event.type == pygame.KEYDOWN:
				# on quitte si on appui sur la touche ESC
				if event.key == pygame.K_ESCAPE:
					pygame.quit()
					sys.exit(0)
			# on gère l'appui sur la barre espace
				elif event.key == pygame.K_SPACE:
					jeuencours = False

		# on met a jour le défilement de la table des HiScore
		hiscore.update(time)

		# on affiche le fond au centre de l'ecran
		screen.blit(gameover, ((w-iw)/2,(h-ih)/2))
		# on affiche la table des HiScore
		screen.blit(hiscore.image, hiscore.rect)

		# on raffraichit tout l'écran
		pygame.display.flip()

