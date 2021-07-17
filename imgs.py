import pygame
import os

PILOT_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pilot1.png"))),
              pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pilot2.png")))]

PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))

OBSTACLE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "obstacle.png")))

BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))

BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))