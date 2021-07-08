import imgs
import pygame

class Bird:
    IMGS=imgs.PILOT_IMGS
    MAX_ROTATION=25
    ROT_VEL=20
    ANIMATION_TIME=5

    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.tilt=0
        self.side = True
        self.speed=0
        self.height=self.y
        self.img_count=0
        self.img=self.IMGS[0]

    def turn(self):
        self.side = not self.side

    def move(self):
        self.x += 5 * int((self.side - 0.5) * 2)
        
