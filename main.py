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
import sys
import neat

WIN_WIDTH = 500
WIN_HEIGHT = 800
pygame.font.init()
FONT = pygame.font.SysFont('comicsans', 50)

gen = 0

def get_mask(self):
    return pygame.mask.from_surface(self.img)

def draw_window(win, pilot_list, pipes_list, base_list, score, gen):
    win.blit(imgs.BG_IMG,(0, 0))

    for pipe in pipes_list:
        pipe.draw(win)
        pipe.left_obstacle.draw(win, pipe.y, False)
        pipe.right_obstacle.draw(win, pipe.y, True)
        pipe.left_obstacle.move()
        pipe.right_obstacle.move()

    text = FONT.render("Score: " + str(score), 1, (255, 255, 255))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))
    text = FONT.render("Generation: " + str(score), 1, (255, 255, 255))
    win.blit(text, (10, 10))

    base_list.draw(win)
    for pilot in pilot_list:
        pilot.draw(win)

    pygame.display.update()

def main(genomes, config):
    global gen
    gen += 1
    nets = []
    ge = []
    pilot_list = []

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        pilot_list.append(pilots.Pilot(230,500))
        g.fitness = 0
        ge.append(g)


    base_list = base.Base()
    pipes_list = [pipes.Pipe(0), pipes.Pipe(250)]
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()
    run = True
    score = 0
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    for pilot in pilot_list:
                        pilot.turn()
        
        pipe_ind = 0
        if len(pilot_list) > 0:
            if len(pipes_list) > 1 and pilot_list[0].y < pipes_list[0].y + pipes_list[0].PIPE_LEFT.get_width():
                pipe_ind = 1
        else:
            run = False
            break
    
        for index, pilot in enumerate(pilot_list):
            pilot.move()
            ge[index].fitness += 1
            output = nets[index].activate((pilot.y, abs(pilot.x - pipes_list[pipe_ind].left), abs(pilot.left - pipes_list[pipe_ind].right)))

            if output[0] > 0.5:
                pilot.turn()

            #pilot.turn()

        base_list.move()
        rem = []
        add_pipe = False
        for pipe in pipes_list:
            for i, pilot in enumerate(pilot_list):
                if pipe.collide(pilot):
                    pilot_list.pop(i)
                    ge[i].fitness -= 1
                    nets.pop(i)
                    ge.pop(i)
                
                if not pipe.passed and pipe.y > pilot.y:
                    pipe.passed = True
                    add_pipe = True
            
            if pipe.y + pipe.PIPE_LEFT.get_height() < 0:
                rem.append(pipe)
            
            pipe.move()

        if add_pipe:
            score += 1
            pipes_list.append(pipes.Pipe(0))

            for g in ge:
                g.fitness += 5
        
        for p in rem:
            pipes_list.remove(p)
        
        for i, pilot in enumerate(pilot_list):
            if pilot.y + pilot.img.get_height() >= 730 or pilot.y < 0:
                pilot_list.pop(i)
                nets.pop(i)
                ge.pop(i)
        

        draw_window(win, pilot_list, pipes_list, base_list, score, gen)


main()