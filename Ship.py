import pygame
from Vectors import Vector
from Settings import *
import math

clock = pygame.time.Clock()


class Ship:
    #  Космический глаз кильки
    def __init__(self, pos):
        self.pos = Vector(pos)
        self.speed = Vector((1, 0))
        self.image = pygame.Surface((40, 40), pygame.SRCALPHA)
        self.status = NORMAL
        self.vect = self.speed
        self.speed_up = 0.5 * 60 / FPS
        self.draw()
        self.angle_turn = 10

    @property
    def angle(self):
        try:
            return 360 - math.degrees(math.acos(self.vect.x / self.vect.len)) if self.vect.y > 0 \
                else math.degrees(math.acos(self.vect.x / self.vect.len))
        except ZeroDivisionError:
            return 0

    def turn(self):
        if self.status == TURN_LEFT:
            self.speed.rotate(self.angle_turn * (60 / FPS) * (-1))
            if self.speed.len:
                self.vect = self.speed.normal
        elif self.status == TURN_RIGHT:
            self.speed.rotate(self.angle_turn * (60 / FPS))
            if self.speed.len:
                self.vect = self.speed.normal

    def speed_change(self):
        if self.status == SLOWLY:
            if self.speed.len == 0:
                return
            if self.speed.len <= self.speed_up:
                self.vect = self.speed.normal
                self.speed = Vector((0, 0))
            else:
                self.speed -= self.speed.normal * self.speed_up
        elif self.status == FASTER:
            if not self.speed.len:
                self.speed = self.vect * self.speed_up
            self.speed += self.speed.normal * self.speed_up

    def move(self):
        self.pos += self.speed * (60 / FPS)

        if self.pos.x > SIZE.w:
            self.pos.x = 0
        elif self.pos.x < 0:
            self.pos.x = SIZE.w
        if self.pos.y > SIZE.h:
            self.pos.y = 0
        elif self.pos.y < 0:
            self.pos.y = SIZE.h

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
        self.turn()
        self.speed_change()
        self.move()

    def rot_center(self, image, angle):
        # rotate with saving center of ship
        orig_rect = image.get_rect()
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image

    def draw(self):
        # draw_ship
        pygame.draw.circle(self.image, (100, 100, 255), (20, 20), 20)
        pygame.draw.polygon(self.image, (0, 255, 0), ((25, 15), (25, 25), (35, 20)))
        # draw frame
        pygame.draw.rect(self.image, (100, 100, 100), self.image.get_rect(), 2)

    def render(self, screen):
        image = self.rot_center(self.image, self.angle)
        screen.blit(image, self.pos.as_point())
        pygame.draw.line(screen, (200, 0, 0),
                         (self.pos.x + self.image.get_rect().w / 2, self.pos.y + self.image.get_rect().h / 2), (
                             (self.pos + self.speed * 5).x + self.image.get_rect().w / 2,
                             (self.pos + self.speed * 5).y + self.image.get_rect().h / 2))
