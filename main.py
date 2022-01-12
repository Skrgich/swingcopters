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
scores = []
with open ('scores.txt', mode='w') as f:
    pass

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

    text = FONT.render("Rezultat: " + str(score), 1, (255, 255, 255))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))
    text = FONT.render("Generacija: " + str(gen), 1, (255, 255, 255))
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

        if not pilot_list:
            run = False
            break

        for index, pilot in enumerate(pilot_list):
            pilot.move()
            ge[index].fitness += 1

            t = (t + 1) % 36
            output = nets[index].activate(
                (pilot.y - pipes_list[pipe_ind].y, 
                (pilot.x - pipes_list[pipe_ind].left), 
                (pilot.x - pipes_list[pipe_ind].left_obstacle.new_rect.bottomright[0]),
                (pilot.y - pipes_list[pipe_ind].left_obstacle.new_rect.bottomright[1]),
                (pilot.side - 0.5) * 2
                ))

            if output[0] < 0:
                if pilot.side:
                    pilot.turn()
            else:
                if not pilot.side:
                    pilot.turn()

        base_list.move()
        rem = []
        add_pipe = False
        for pipe in pipes_list:
            for i, pilot in enumerate(pilot_list):
                if pipe.collide(pilot):
                    ge[i].fitness -= abs(pilot_list[i].x - (pipe.right - pipe.GAP // 2))
                    pilot_list.pop(i)
                    nets.pop(i)
                    ge.pop(i)
                
                if not pipe.passed and pipe.y > pilot.y:
                    pipe.passed = True
                    add_pipe = True
                    pipe_ind += 1
            
            if pipe.y >= 800:
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

    with open ('scores.txt', mode='a') as f:
        f.write("{:4} {}\n".format(gen,score))

def run(config_path):
    config=neat.config.Config(neat.DefaultGenome,neat.DefaultReproduction,neat.DefaultSpeciesSet,neat.DefaultStagnation,config_path)

    p=neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats=neat.StatisticsReporter()
    p.add_reporter(stats)

    winner=p.run(main)

if __name__ == '__main__':
    input()
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    run(config_path)
    while True:
        print(1)
    print(scores)
