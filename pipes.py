from imgs import PIPE_IMG
import random
import pygame

class Pipe:
    GAP = 200
    SPEED = 5
    def __init__(self, y):
        self.y = y
        self.dist = 0
        self.end

    def set_dist(self):
        self.dist = random.randrange(40,450)
        self.left = self.dist - self.PIPE_TOP.get_height()
        self.right = self.dist + self.GAP

    def move(self):
        self.y += self.SPEED
        