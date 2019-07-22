import pygame
from pygame.locals import *

pygame.init()
pygame.display.set_mode((700,700))

while(1):
    events = pygame.event.get()
	
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                print ('left')
            if event.key == pygame.K_RIGHT:
                print ('right')
                