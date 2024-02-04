import math
import random
import pygame
from levels import gameLevels
# Я написал этот восхитительный и очень нужный комментарий
pygame.init()

WIDTH, HEIGHT = 850, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("BRICK BREAKER")
FPS = 60
PADDLE_WIDTH = 120
PADDLE_HEIGHT = 10
BALL_RADIUS = 10
all_sprites = pygame.sprite.Group()

# brick_sprites = pygame.sprite.Group()
LIVES_FONT = pygame.font.SysFont("comicsans", 40)

LEVEL = 1
background_image = pygame.image.load(gameLevels[LEVEL]["bckImg"])
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))


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
        self.numDir = random.choice(range(1, 4))
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

    lives_text = LIVES_FONT.render(f"HP:{lives}", 1, gameLevels[LEVEL]["textColor"])
    win.blit(lives_text, (10, HEIGHT - lives_text.get_height() - 10))

    pygame.display.update()


def ball_collision(ball):
    if ball.x - BALL_RADIUS <= 0:
        ball.set_position(WIDTH - ball.radius * 2, ball.y)
    elif ball.x + BALL_RADIUS >= WIDTH:
        ball.set_position(0 + ball.radius * 2, ball.y)

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
    # Рассчитываем ближайшие точки на кирпиче к центру шара
    closest_x = max(brick.rect.x, min(ball.x, brick.rect.x + brick.rect.width))
    closest_y = max(brick.rect.y, min(ball.y, brick.rect.y + brick.rect.height))

    # Вычисляем расстояние между центром шара и ближайшей точкой на кирпиче
    distance_x = ball.x - closest_x
    distance_y = ball.y - closest_y

    # Проверяем, с какой стороны было столкновение
    if (distance_x ** 2 + distance_y ** 2) < ball.radius ** 2:
        # Столкновение произошло
        if distance_x > 0:
            # Столкновение с правой стороной кирпича
            print(" удар справа")
            brick.hit()
            ball.set_vel(ball.x_vel * -1, ball.y_vel)
            return True
        elif distance_x < 0:
            # Столкновение с левой стороной кирпича
            print(" удар слева")
            brick.hit()
            ball.set_vel(ball.x_vel * -1, ball.y_vel)
            return True
        elif distance_y > 0:
            # Столкновение с нижней стороной кирпича
            print(" удар снизу")
            brick.hit()
            ball.set_vel(ball.x_vel, ball.y_vel * -1)
            return True
        else:
            # Столкновение с верхней стороной кирпича
            print(" удар сверху")
            brick.hit()
            ball.set_vel(ball.x_vel, ball.y_vel * -1)
    return False


def generate_bricks(level):
    brick_sprites = pygame.sprite.Group()

    helpBrick = Brick(-100, -100, 0)
    brick_width = helpBrick.width
    brick_height = helpBrick.height

    gap = 5.55
    bricksMatrix = gameLevels[level]["brickMap"]
    for row in range(len(bricksMatrix)):
        for col in range(len(bricksMatrix[row])):
            if bricksMatrix[row][col] == 1:
                brick = Brick(gap + col * (brick_width + gap), gap + row * (brick_height + gap), 2)
                brick_sprites.add(brick)
                print(brick.rect.x, brick.rect.y)
    return brick_sprites


lives = 3


def main():
    global lives, LEVEL, background_image, all_sprites
    clock = pygame.time.Clock()

    paddle = Paddle()
    all_sprites.add(paddle)

    ball = Ball(WIDTH / 2, HEIGHT - PADDLE_HEIGHT - 5 - BALL_RADIUS, BALL_RADIUS, gameLevels[LEVEL]["ballColor"])
    bricks = generate_bricks(LEVEL)
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

        if len(bricks) <= 0:
            LEVEL += 1
            all_sprites = pygame.sprite.Group()
            paddle = Paddle()
            all_sprites.add(paddle)
            ball = Ball(WIDTH / 2, HEIGHT - PADDLE_HEIGHT - 5 - BALL_RADIUS, BALL_RADIUS,
                        gameLevels[LEVEL]["ballColor"])
            bricks = generate_bricks(LEVEL)
            background_image = pygame.image.load(gameLevels[LEVEL]["bckImg"])
            background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
            lives = 3

        if lives <= 0:
            LEVEL = 1
            all_sprites = pygame.sprite.Group()
            paddle = Paddle()
            all_sprites.add(paddle)
            ball = Ball(WIDTH / 2, HEIGHT - PADDLE_HEIGHT - 5 - BALL_RADIUS, BALL_RADIUS,
                        gameLevels[LEVEL]["ballColor"])
            bricks = generate_bricks(LEVEL)
            background_image = pygame.image.load(gameLevels[LEVEL]["bckImg"])
            background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
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
