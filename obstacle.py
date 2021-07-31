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
        self.rotated_image = pygame.transform.rotate(self.IMG, self.tilt )
        self.new_rect = self.rotated_image.get_rect(center = self.IMG.get_rect(topleft = (self.x + 8 + 9 * self.side, y - self.rotated_image.get_height() / 2 + 11)).center)


    def draw(self, win, y, side):
        rotated_image = pygame.transform.rotate(self.IMG, self.tilt )
        new_rect = rotated_image.get_rect(center = self.IMG.get_rect(topleft = (self.x + 8 + 9 * side, y - rotated_image.get_height() / 2 + 11)).center)
        win.blit(rotated_image, new_rect.topleft)
        self.rotated_image = rotated_image
        self.new_rect = new_rect

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
