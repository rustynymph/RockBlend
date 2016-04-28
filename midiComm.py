import pygame, pygame.midi

inp = None

def initPygame():
	global inp
	pygame.init()
	pygame.midi.init()
	inp = pygame.midi.Input(3)	
	pygame.time.wait(10)