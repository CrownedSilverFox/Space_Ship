import sys
import pygame
from Vectors import Vector

NORMAL = 0
TURN_LEFT = 1
TURN_RIGHT = 2
SLOWLY = 3
FASTER = 4
FPS = 60
SIZE = (800, 600)


class Ship:
    #  Космический корабль-килька
    def __init__(self, pos):
        self.pos = Vector(pos)
        self.speed = Vector((1, 0))
        self.image = pygame.Surface((40, 40))
        self.status = NORMAL
        self.vect = self.speed
        self.speed_up = 1.4

    def move(self):
        if self.status == TURN_LEFT:
            self.speed.rotate(-10)
        elif self.status == TURN_RIGHT:
            self.speed.rotate(10)
        elif self.status == SLOWLY:
            if self.speed.len == 0:
                return
            if self.speed.len < self.speed_up:
                self.vect = self.speed.normal() * self.speed_up
                self.speed = Vector((0, 0))
            else:
                self.speed -= (self.speed.normal()) * self.speed_up
        elif self.status == FASTER:
            if self.speed.len == 0:
                self.speed = self.vect
            self.speed += self.speed.normal() * self.speed_up
        self.pos += self.speed
        if self.pos.x > SIZE[0]:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = SIZE[0]
        if self.pos.y > SIZE[1]:
            self.pos.y = 0
        if self.pos.y < 0:
            self.pos.y = SIZE[1]

    def events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.status = TURN_LEFT
            elif event.key == pygame.K_RIGHT:
                self.status = TURN_RIGHT
            elif event.key == pygame.K_DOWN:
                self.status = SLOWLY
            elif event.key == pygame.K_UP:
                self.status = FASTER
        elif event.type == pygame.KEYUP:
            self.status = NORMAL

    def update(self):
        self.move()

    def draw(self):
        # draw_ship
        pygame.draw.circle(self.image, (100, 100, 255), (20, 20), 20)
        # draw rect
        pygame.draw.rect(self.image, (100, 100, 100), self.image.get_rect(), 2)

    def render(self, screen):
        screen.blit(self.image, self.pos.as_point())
        pygame.draw.line(screen, (200, 0, 0), (self.pos.as_point()[0]+20, self.pos.as_point()[1]+20), ((self.pos + self.
                                                                                                       speed * 5).
                                                                                                       as_point()[0]+20, (self.pos + self.
                                                                                                       speed * 5).as_point()[1]+20))
        self.draw()


run = True
pygame.init()
pygame.display.set_mode(SIZE)
screen = pygame.display.get_surface()

ship = Ship((400, 300))
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
    print(dt)
    ship.update()
    screen.fill((0, 0, 0))
    ship.render(screen)
    pygame.display.flip()
