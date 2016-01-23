import sys
import pygame
from Ship import Ship
from Settings import SIZE, FPS


run = True
pygame.init()
pygame.display.set_mode(SIZE.bottomright)
screen = pygame.display.get_surface()

ship = Ship((SIZE.w/2, SIZE.h/2))
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit()
        ship.events(event)
    dt = clock.tick(FPS)
    ship.update()
    screen.fill((0, 0, 0))
    ship.render(screen)
    pygame.display.flip()
