import pygame
import os

p1 = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pilot1.png")))
p2 = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pilot2.png")))
PILOT_IMGS = {
    p1 : p2,
    p2 : p1
}

PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))

OBSTACLE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "obstacle.png")))

BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))

BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))