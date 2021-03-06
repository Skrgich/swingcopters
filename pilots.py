import imgs
import pygame

class Pilot:
    IMGS=imgs.PILOT_IMGS
    MAX_ROTATION=25
    ROT_VEL=20
    ANIMATION_TIME=5

    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.tilt=20
        self.side = True
        self.speed=0
        self.height=self.y
        self.img_count=0
        self.img=self.IMGS[[pic for pic in self.IMGS][0]]

    def turn(self):
        self.side = not self.side
        self.tilt = self.tilt
        #pygame.transform.rotate(pygame.transform.flip(self.img, not self.side, 0))

    def move(self):
        self.x += 5 * int((self.side - 0.5) * 2)

    def draw(self, win):
        rotated_image = pygame.transform.rotate(pygame.transform.flip(self.img, not self.side, 0), self.tilt * int((self.side - 0.5) * 2))
        new_rect = rotated_image.get_rect(center = self.img.get_rect(topleft = (self.x, self.y)).center)
        win.blit(rotated_image, new_rect.topleft)
        self.img = self.IMGS[self.img]

    def get_mask(self):
        return pygame.mask.from_surface(self.img)


