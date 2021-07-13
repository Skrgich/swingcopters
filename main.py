from pygame.surfarray import pixels_green
from imgs import BG_IMG
import pygame
import time
import os
import random
import imgs
import pilots
import base
import pipes
import obstacle

WIN_WIDTH = 500
WIN_HEIGHT = 800
pygame.font.init()
FONT = pygame.font.SysFont('comicsans', 50)

GEN = 0

def get_mask(self):
    return pygame.mask.from_surface(self.img)

def draw_window(win, pilot_list, pipes_list, obstacles_list, base_list, score, gen):
    win.blit(imgs.BG_IMG,(0, 0))

    for pipe in pipes_list:
        pipe.draw(win)
        pipe.left_obstacle.draw(win)
        pipe.right_obstacle.draw(win)

    text = FONT.render("Score: " + str(score), 1, (255, 255, 255))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))
    text = FONT.render("Generation: " + str(score), 1, (255, 255, 255))
    win.blit(text, (10, 10))

    base_list.draw(win)
    for pilot in pilot_list:
        pilot.draw(win)

    pygame.display.update()

def main():

    base_list = base.Base(730)
    pipes_list = [pipes.Pipe(500)]
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()
    run = True
    score = 0
    while run:
        clock.tick(1000)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
        
        pipe_ind = 0
        if len(pilot_list) > 0:
            if len(pipes_list) > 1 and pilot_list[0].x > pipes_list[0].x + pipes_list[0].PIPE_LEFT.get_width():
                pipe_ind = 1
        else:
            run = False
            break
    
        for index, pilot in enumerate(pilot_list):
            pilot.move()

            pilot.turn()

