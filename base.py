from imgs import BASE_IMG

class Base:
    SPEED = 5
    WIDTH = BASE_IMG.get_width()
    IMG = BASE_IMG

    def __init__(self):
        self.y = self.WIDTH
    
    def move(self):
        self.y += 5

    def draw(self, win):
        win.blit(self.IMG, (0,self.y))
