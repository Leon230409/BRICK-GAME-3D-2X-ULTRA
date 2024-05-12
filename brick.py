import random
import pygame


class BrickFactory:
    @staticmethod
    def create_brick(x, y, brick_type):
        if brick_type == 1:
            return Brick(x, y, 2)
        elif brick_type == 2:
            return BonusBrick(x, y)
        elif brick_type == 3:
            return ForceBrick(x, y)
        elif brick_type == 4:
            return LongPaddleBrick(x, y)
        elif brick_type == 5:
            return X2BallBrick(x, y)
        elif brick_type == 6:
            return SlowBrick(x, y)
        elif brick_type == 7:
            return MetalicaBrick(x, y)
        else:
            raise ValueError("Unsupported brick type")


class Brick(pygame.sprite.Sprite):
    def __init__(self, x, y, health):
        pygame.sprite.Sprite.__init__(self)
        self.name = "normal"
        self.health = health
        self.images = []
        self.numDir = random.choice(range(1, 4))
        self.images.extend([pygame.image.load(f'images/bt{self.numDir}/bt{self.numDir}_1.png'),
                            pygame.image.load(f'images/bt{self.numDir}/bt{self.numDir}_2.png')])
        self.imageIndex = 0
        self.image = self.images[self.imageIndex]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def hit(self):
        self.health -= 1
        self.imageIndex += 1
        if self.imageIndex < len(self.images):
            self.image = self.images[self.imageIndex]


class BonusBrick(Brick):
    def __init__(self, x, y):
        super().__init__(x, y, 1)
        self.name = "speed"
        self.images = [pygame.image.load(f'images/bt_speed.png')]
        self.image = self.images[self.imageIndex]


class ForceBrick(Brick):
    def __init__(self, x, y):
        super().__init__(x, y, 1)
        self.name = "force"
        self.images = [pygame.image.load(f'images/bt_force.png')]
        self.image = self.images[self.imageIndex]


class LongPaddleBrick(Brick):
    def __init__(self, x, y):
        super().__init__(x, y, 1)
        self.name = "longPaddle"
        self.images = [pygame.image.load(f'images/bt_longPaddle.png')]
        self.image = self.images[self.imageIndex]


class X2BallBrick(Brick):
    def __init__(self, x, y):
        super().__init__(x, y, 1)
        self.name = "X2Ball"
        self.images = [pygame.image.load(f'images/bt_balls.png')]
        self.image = self.images[self.imageIndex]


class SlowBrick(Brick):
    def __init__(self, x, y):
        super().__init__(x, y, 1)
        self.name = "slow"
        self.images = [pygame.image.load(f'images/bt_slow.png')]
        self.image = self.images[self.imageIndex]


class MetalicaBrick(Brick):
    def __init__(self, x, y):
        super().__init__(x, y, 1)
        self.images = [pygame.image.load('images/bt5/bt5_1.png'), ]
        self.image = self.images[self.imageIndex]

    def hit(self):
        pass
