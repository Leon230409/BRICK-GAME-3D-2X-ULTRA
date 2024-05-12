import pygame


class Paddle(pygame.sprite.Sprite):
    VEL = 5

    def __init__(self, screen):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/paddle.png')
        self.rect = self.image.get_rect()
        self.normalWidth = self.rect.width
        self.height = self.rect[3]
        self.rect.center = (screen[0] // 2, screen[1] - self.height)

    def move(self, direction):
        self.rect.x = self.rect.x + self.VEL * direction

    def set_plus_size(self):
        center = self.rect.center
        self.rect.width = self.normalWidth * 1.5

        self.rect.center = center
        self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))
        print(self.rect.size)

    def set_posX(self, x):
        self.rect.centerx = x
