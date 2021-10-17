from obstacle import Obstacle
from imgs import PIPE_IMG
import obstacle
import random
import pygame

class Pipe:
    GAP = 165
    SPEED = 5
    def __init__(self, y):
        self.y = y - PIPE_IMG.get_height()
        self.dist = 0
        self.left = 0
        self.right = 0
        self.PIPE_RIGHT = pygame.transform.flip(PIPE_IMG, True, True)
        self.PIPE_LEFT = PIPE_IMG
        self.passed = False
        self.set_dist()
        self.left_obstacle = Obstacle(self.dist - 55, self.y)  #(self.left, self.y)
        self.right_obstacle = Obstacle(self.right - 30, self.y)
    

    def set_dist(self):
        self.dist = random.randrange(100, 400)
        self.left = self.dist - self.PIPE_LEFT.get_width()
        self.right = self.dist + self.GAP

    def move(self):
        self.y += self.SPEED

    def draw(self, win):
        win.blit(self.PIPE_LEFT,(self.left, self.y))
        win.blit(self.PIPE_RIGHT, (self.right, self.y))

    def collide(self, pilot):
        pilot_mask = pilot.get_mask()
        left_mask = pygame.mask.from_surface(self.PIPE_LEFT)
        right_mask = pygame.mask.from_surface(self.PIPE_RIGHT)

        left_offset = (self.left - pilot.x, self.y - round(pilot.y))
        right_offset = (self.right - pilot.x, self.y - round(pilot.y))

        left_point = pilot_mask.overlap(left_mask, left_offset)
        right_point = pilot_mask.overlap(right_mask, right_offset)

        left_mask_obstacle = pygame.mask.from_surface(self.left_obstacle.IMG)
        right_mask_obstacle = pygame.mask.from_surface(self.right_obstacle.IMG)

        left_offset_obstacle = (self.left_obstacle.new_rect.topleft[0] - pilot.x, self.left_obstacle.new_rect.topleft[1] - round(pilot.y))
        right_offset_obstacle = (self.right_obstacle.new_rect.topleft[0] - pilot.x, self.right_obstacle.new_rect.topleft[1] - round(pilot.y))

        left_point_obstacle = pilot_mask.overlap(left_mask_obstacle, left_offset_obstacle)
        right_point_obstacle = pilot_mask.overlap(right_mask_obstacle, right_offset_obstacle)


        if left_point or right_point:
            return True
        if left_point_obstacle or right_point_obstacle:
            return True
        return False