from obstacle import Obstacle
from imgs import PIPE_IMG
import obstacle
import random
import pygame

class Pipe:
    GAP = 200
    SPEED = 5
    def __init__(self, y):
        self.y = y
        self.dist = 0
        self.left = 0
        self.right = 0
        self.PIPE_RIGHT = pygame.transform.flip(PIPE_IMG, False, True)
        self.PIPE_LEFT = PIPE_IMG
        self.passed = False
        self.set_dist()
        self.left_obstacle = Obstacle(self.left, self.y)
        self.right_obstacle = Obstacle(self.right, self.y)
    

    def set_dist(self):
        self.dist = random.randrange(40,450)
        self.left = self.dist - self.PIPE_LEFT.get_height()
        self.right = self.dist + self.GAP

    def move(self):
        self.y += self.SPEED

    def draw(self, win):
        win.blit(self.PIPE_LEFT,(self.y, self.left))
        win.blit(self.PIPE_LEFT, (self.y, self.right))

    def collide(self, pilot):
        pilot_mask = pilot.get_mask()
        left_mask = pygame.mask.from_surface(self.PIPE_LEFT)
        right_mask = pygame.mask.from_surface(self.PIPE_RIGHT)

        left_offset = (self.left - pilot.x, self.y - round(pilot.y))
        right_offset = (self.right - pilot.x, self.y - round(pilot.y))

        left_point = pilot_mask.overlap(left_mask, left_offset)
        right_point = pilot_mask.overlap(right_mask, right_offset)

        if left_point or right_point:
            return True
        return False