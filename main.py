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
    text = FONT.render("Generation: " + str(gen), 1, (255, 255, 255))
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
    pipe_ind = 0
    t = 0
    while run:
        clock.tick(1000)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
        #     if event.type == pygame.KEYDOWN:
        #         if event.key == pygame.K_SPACE:
        #             for pilot in pilot_list:
        #                 pilot.turn()
        
        # pipe_ind = 0
        # if len(pilot_list) > 0:
        #     if len(pipes_list) > 1 and pilot_list[0].y < pipes_list[0].y + pipes_list[0].PIPE_LEFT.get_height() // 2:
        #         pipe_ind = 1
        #         if len(pipes_list) > 2 and pilot_list[0].y < pipes_list[1].y + pipes_list[1].PIPE_LEFT.get_height() // 2:
        #             pipe_ind = 2
                
        # else:
        if not pilot_list:
            run = False
            break
        # print(pipe_ind)
        for index, pilot in enumerate(pilot_list):
            pilot.move()
            ge[index].fitness += 1
            # if not pilot.side:
            #      output = nets[index].activate((pilot.x, 
            # pilot.x - pipes_list[pipe_ind].right,
            # pipes_list[pipe_ind].right_obstacle.new_rect.topleft[0],
            # pipes_list[pipe_ind].right_obstacle.new_rect.topleft[1]))
            # else:
            #      output = nets[index].activate((pilot.x, 
            # -pilot.x + pipes_list[pipe_ind].left, 
            # pipes_list[pipe_ind].left_obstacle.new_rect.topleft[0],
            # pipes_list[pipe_ind].left_obstacle.new_rect.topleft[1]))
            t = (t + 1) % 36
            output = nets[index].activate((pilot.y - pipes_list[pipe_ind].y, 
                (pilot.x - pipes_list[pipe_ind].left), 
                (pilot.x - pipes_list[pipe_ind].right),
                (pilot.x - pipes_list[pipe_ind].left_obstacle.new_rect.bottomright[0]),
                (pilot.y - pipes_list[pipe_ind].left_obstacle.new_rect.bottomright[1]),
                (pilot.x - pipes_list[pipe_ind].right_obstacle.new_rect.bottomleft[0]),
                (pilot.y - pipes_list[pipe_ind].right_obstacle.new_rect.bottomleft[1]),
                (pilot.side - 0.5) * 2
                ))

            # if pilot.side:
            #     output = nets[index].activate((pilot.y - pipes_list[pipe_ind].y, 
            #     (pilot.x - pipes_list[pipe_ind].left), 
            #     (pilot.x - pipes_list[pipe_ind].right),
            #     (pilot.x - pipes_list[pipe_ind].left_obstacle.new_rect.bottomright[0]),
            #     (pilot.y - pipes_list[pipe_ind].left_obstacle.new_rect.bottomright[1]),
            #     (pilot.x - pipes_list[pipe_ind].right_obstacle.new_rect.bottomleft[0]),
            #     (pilot.y - pipes_list[pipe_ind].right_obstacle.new_rect.bottomleft[1]),
            #     t
            #     ))
            # else:
            #     output = nets[index].activate((pilot.y - pipes_list[pipe_ind].y, 
            #     (pilot.x - pipes_list[pipe_ind].right),
            #     (pilot.x - pipes_list[pipe_ind].left), 
            #     (pilot.x - pipes_list[pipe_ind].right_obstacle.new_rect.bottomleft[0]),
            #     (pilot.y - pipes_list[pipe_ind].right_obstacle.new_rect.bottomleft[1]),
            #     (pilot.x - pipes_list[pipe_ind].left_obstacle.new_rect.bottomright[0]),
            #     (pilot.y - pipes_list[pipe_ind].left_obstacle.new_rect.bottomright[1]),
            #     t
            #     ))     
        
            if output[0] < 0:
                if pilot.side:
                    pilot.turn()
            else:
                if not pilot.side:
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
                    pipe_ind += 1
            
            if pipe.y >= 800:# pipe.PIPE_LEFT.get_height() + 800:
                rem.append(pipe)
            
            pipe.move()

        if add_pipe:
            score += 1
            pipes_list.append(pipes.Pipe(0))

            for g in ge:
                g.fitness += 5
        
        for p in rem:
            pipes_list.remove(p)
            pipe_ind -= 1
        
        for i, pilot in enumerate(pilot_list):
            if pilot.y + pilot.img.get_height() >= 730 or pilot.y < 0:
                pilot_list.pop(i)
                nets.pop(i)
                ge.pop(i)
        

        draw_window(win, pilot_list, pipes_list, base_list, score, gen)

def run(config_path):
    config=neat.config.Config(neat.DefaultGenome,neat.DefaultReproduction,neat.DefaultSpeciesSet,neat.DefaultStagnation,config_path)

    p=neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats=neat.StatisticsReporter()
    p.add_reporter(stats)

    winner=p.run(main)

if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    run(config_path)
