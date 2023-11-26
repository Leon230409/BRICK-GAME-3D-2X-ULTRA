import math
import random

import pygame

pygame.init()
WIDTH, HEIGHT = 850, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("BRICK BREAKER")
background_image = pygame.image.load('images/IM3.JPG')
FPS = 60
PADDLE_WIDTH = 120
PADDLE_HEIGHT = 10
BALL_RADIUS = 10
all_sprites = pygame.sprite.Group()
# brick_sprites = pygame.sprite.Group()
LIVES_FONT = pygame.font.SysFont("comicsans", 40)


class Paddle(pygame.sprite.Sprite):
    VEL = 5

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/paddle.png')
        self.rect = self.image.get_rect()
        self.width = self.rect[2]
        self.height = self.rect[3]
        self.rect.center = (WIDTH // 2, HEIGHT - self.height)

    # def draw(self, win):
    #     pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))

    def move(self, direction):
        self.rect.x = self.rect.x + self.VEL * direction


class Ball:
    VEL = 5

    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.x_vel = 0
        self.y_vel = -self.VEL

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

    def set_vel(self, x_vel, y_vel):
        self.x_vel = x_vel
        self.y_vel = y_vel

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)

    def set_position(self, x, y):
        self.x = x
        self.y = y


class Brick(pygame.sprite.Sprite):
    def __init__(self, x, y, health):
        pygame.sprite.Sprite.__init__(self)
        self.health = health
        self.images = []
        self.numDir = random.choice(range(1,4))
        self.images.append(pygame.image.load(f'images/bt{self.numDir}/bt{self.numDir}_1.png'))
        self.images.append(pygame.image.load(f'images/bt{self.numDir}/bt{self.numDir}_2.png'))
        self.imageIndex = 0
        self.image = self.images[self.imageIndex]
        self.rect = self.image.get_rect()
        self.width = self.rect[2]
        self.height = self.rect[3]
        self.rect.topleft = (x, y)

    # def draw(self, win):
        # pygame.draw.rect(win, (self.x, self.y, self.width, self.height))

    def hit(self):
        self.health -= 1
        self.imageIndex += 1
        if self.imageIndex < len(self.images):
            self.image = self.images[self.imageIndex]


def draw(win, paddle, ball, bricks, lives, back, sprites):
    # win.fill("white")
    win.blit(back, back.get_rect())
    # paddle.draw(win)

    sprites.update()
    sprites.draw(win)

    bricks.update()
    bricks.draw(win)

    ball.draw(win)

    # for brick in bricks:
    #     brick.draw(win)

    lives_text = LIVES_FONT.render(f"HP:{lives}", 1, 'black')
    win.blit(lives_text, (10, HEIGHT - lives_text.get_height() - 10))

    pygame.display.update()


def ball_collision(ball):
    if ball.x - BALL_RADIUS <= 0 or ball.x + BALL_RADIUS >= WIDTH:
        ball.set_vel(ball.x_vel * -1, ball.y_vel)
    if ball.y - BALL_RADIUS <= 0:
        ball.set_vel(ball.x_vel, ball.y_vel * -1)


def ball_flor_collision(ball, paddle):
    global lives
    if ball.y + BALL_RADIUS >= HEIGHT:
        lives -= 1
        ball.set_position(paddle.rect.x + paddle.width // 2, paddle.rect.y - ball.radius)
        ball.set_vel(0, -ball.VEL)


def ball_paddle_collision(ball, paddle):
    if not (ball.x <= paddle.rect.x + paddle.width and ball.x >= paddle.rect.x):
        return
    if not (ball.y + ball.radius >= paddle.rect.y):
        return

    distance_to_center = ball.x - paddle.rect.centerx

    percent_width = distance_to_center / paddle.width
    angle = percent_width * 90
    angle_radians = math.radians(angle)

    x_vel = math.sin(angle_radians) * ball.VEL
    y_vel = math.cos(angle_radians) * ball.VEL
    ball.set_vel(x_vel, y_vel * -1)


def ball_brick_collision(brick, ball):
    if (brick.rect.y < ball.y - ball.radius <= brick.rect.y + brick.height) and (
            brick.rect.x - ball.radius < ball.x < brick.rect.x + brick.width + ball.radius):
        print(" удар снизу")
        brick.hit()
        ball.set_position(ball.x, ball.y + ball.VEL)
        ball.set_vel(ball.x_vel, ball.y_vel * -1)
        return True
    # удар справа
    if (ball.x + ball.radius >= brick.rect.x) and (ball.x + ball.radius < brick.rect.x + brick.width) and (
            brick.rect.y < ball.y < brick.rect.y + brick.height):
        print(" удар справа")
        brick.hit()
        ball.set_vel(ball.x_vel * -1, ball.y_vel)
        return True
    if (ball.x - ball.radius <= brick.rect.x + brick.width) and (ball.x - ball.radius > brick.rect.x) and (
            brick.rect.y < ball.y < brick.rect.y + brick.height):
        print(" удар слева")
        brick.hit()
        ball.set_vel(ball.x_vel * -1, ball.y_vel)
        return True
    if (brick.rect.y <= ball.y + ball.radius < brick.rect.y + brick.height) and (
            brick.rect.x - ball.radius < ball.x < brick.rect.x + brick.width + ball.radius):
        print(" удар сверху")
        brick.hit()
        ball.set_positions(ball.x, ball.y - ball.VEL)
        ball.set_vel(ball.x_vel, ball.y_vel * -1)
        return True

    return False


def generate_bricks(rows):
    brick_sprites = pygame.sprite.Group()

    brick_width = 100
    brick_height = 30
    windowSize = pygame.display.get_window_size()
    cols = windowSize[0] // brick_width
    gap = (windowSize[0] - brick_width * cols) / (cols + 1)
    for row in range(rows):
        for col in range(cols):
            brick = Brick(gap + col * (brick_width + gap), gap + row * (brick_height + gap), 2)
            brick_sprites.add(brick)
            print(brick.rect.x, brick.rect.y)
    return brick_sprites


lives = 3


def main():
    global lives
    clock = pygame.time.Clock()

    paddle = Paddle()
    all_sprites.add(paddle)

    ball = Ball(WIDTH / 2, HEIGHT - PADDLE_HEIGHT - 5 - BALL_RADIUS, BALL_RADIUS, 'black')
    bricks = generate_bricks(3)
    run = True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and paddle.rect.x > 0:
            paddle.move(-1)
        if keys[pygame.K_d] and paddle.rect.x + paddle.width < WIDTH:
            paddle.move(1)
        ball.move()
        ball_collision(ball)
        ball_paddle_collision(ball, paddle)
        ball_flor_collision(ball, paddle)
        for brick in bricks:
            ball_brick_collision(brick, ball)
            if brick.health <= 0:
                bricks.remove(brick)

        if lives <= 0:
            all_sprites.remove(paddle)
            paddle = Paddle()
            all_sprites.add(paddle)
            ball = Ball(WIDTH / 2, HEIGHT - PADDLE_HEIGHT - 5 - BALL_RADIUS, BALL_RADIUS, 'black')
            bricks = generate_bricks(3)
            lives = 3

            lost_text = LIVES_FONT.render("HAHAHA YOU LOST!!!", 1, "red")
            win.blit(lost_text, (WIDTH / 2 - lost_text.get_width() / 2, HEIGHT / 2 - lost_text.get_height() / 2))
            pygame.display.update()
            pygame.time.delay(5000)
        draw(win, paddle, ball, bricks, lives, background_image, all_sprites)
    pygame.quit()
    quit()


if __name__ == "__main__":
    main()
