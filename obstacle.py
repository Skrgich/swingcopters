from imgs import OBSTACLE_IMG
import pygame

class Obstacle:
    SPEED = 5
    IMG = OBSTACLE_IMG

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.y
        self.tilt = 0
        self.side = True

    def draw(self, win, y):
        rotated_image = pygame.transform.rotate(self.IMG, self.tilt * self.side)
        new_rect = rotated_image.get_rect(center = self.IMG.get_rect(topleft = (self.x, y)).center)
        win.blit(rotated_image, new_rect.topleft)

    def move(self):
        if self.side:
            if self.tilt < 45:
                self.tilt += 5
            else:
                self.side = not self.side
                self.tilt -= 5
                self.IMG = pygame.transform.flip(self.IMG, True, False)
        else:
            if self.tilt > -45:
                self.tilt -= 5
            else:
                self.side = not self.side
                self.tilt += 5
                self.IMG = pygame.transform.flip(self.IMG, True, False)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)
