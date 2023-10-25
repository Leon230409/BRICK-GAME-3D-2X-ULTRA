import math

import pygame

pygame.init()
WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("BRICK BREAKER")
FPS = 60
PADDLE_WIDTH = 120
PADDLE_HEIGHT = 10
BALL_RADIUS = 10

LIVES_FONT = pygame.font.SysFont("comicsans", 40)


class Paddle:
    VEL = 5

    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))

    def move(self, direction):
        self.x = self.x + self.VEL * direction


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


class Brick:
    def __init__(self, x, y, width, height, health, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.health = health
        self.color = color

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))

    def hit(self):
        self.health -= 1


def draw(win, paddle, ball, bricks, lives):
    win.fill("white")
    paddle.draw(win)
    ball.draw(win)

    for brick in bricks:
        brick.draw(win)

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
        ball.set_position(paddle.x + paddle.width // 2, paddle.y - ball.radius)
        ball.set_vel(0, -ball.VEL)


def ball_paddle_collision(ball, paddle):
    if not (ball.x <= paddle.x + paddle.width and ball.x >= paddle.x):
        return
    if not (ball.y + ball.radius >= paddle.y):
        return

    paddle_center = paddle.x + paddle.width / 2
    distance_to_center = ball.x - paddle_center

    percent_width = distance_to_center / paddle.width
    angle = percent_width * 90
    angle_radians = math.radians(angle)

    x_vel = math.sin(angle_radians) * ball.VEL
    y_vel = math.cos(angle_radians) * ball.VEL
    ball.set_vel(x_vel, y_vel * -1)


def ball_brick_collision(brick, ball):
    if (brick.y < ball.y - ball.radius <= brick.y + brick.height) and (
            brick.x - ball.radius < ball.x < brick.x + brick.width + ball.radius):
        print(" удар снизу")
        brick.hit()
        # ball.set_positions(ball.x, ball.y + ball.VEL)
        ball.set_vel(ball.x_vel, ball.y_vel * -1)
        return True
    # удар справа
    if (ball.x + ball.radius >= brick.x) and (ball.x + ball.radius < brick.x + brick.width) and (
            brick.y < ball.y < brick.y + brick.height):
        print(" удар справа")
        brick.hit()
        ball.set_vel(ball.x_vel * -1, ball.y_vel)
        return True
    if (ball.x - ball.radius <= brick.x + brick.width) and (ball.x - ball.radius > brick.x) and (
            brick.y < ball.y < brick.y + brick.height):
        print(" удар слева")
        brick.hit()
        ball.set_vel(ball.x_vel * -1, ball.y_vel)
        return True
    if (brick.y <= ball.y + ball.radius < brick.y + brick.height) and (
            brick.x - ball.radius < ball.x < brick.x + brick.width + ball.radius):
        print(" удар сверху")
        brick.hit()
        # ball.set_positions(ball.x, ball.y - ball.VEL)
        ball.set_vel(ball.x_vel, ball.y_vel * -1)
        return True

    return False


def generate_bricks(rows, cols):
    gap = 5
    brick_width = (WIDTH - gap * (cols + 1)) // cols
    brick_height = 30
    print(brick_width)
    bricks = []
    for row in range(rows):
        for col in range(cols):
            brick = Brick(gap + col * (brick_width + gap), gap + row * (brick_height + gap), brick_width, brick_height,
                          1, "black")
            bricks.append(brick)
            print(brick.x, brick.y)
    return bricks


lives = 3


def main():
    global lives
    clock = pygame.time.Clock()

    paddle = Paddle(WIDTH / 2 - PADDLE_WIDTH / 2, HEIGHT - PADDLE_HEIGHT - 5, PADDLE_WIDTH, PADDLE_HEIGHT, "purple")

    ball = Ball(WIDTH / 2, HEIGHT - PADDLE_HEIGHT - 5 - BALL_RADIUS, BALL_RADIUS, 'black')
    bricks = generate_bricks(3, 5)
    run = True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and paddle.x > 0:
            paddle.move(-1)
        if keys[pygame.K_d] and paddle.x + paddle.width < WIDTH:
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
            paddle = Paddle(WIDTH / 2 - PADDLE_WIDTH / 2, HEIGHT - PADDLE_HEIGHT - 5, PADDLE_WIDTH, PADDLE_HEIGHT,
                            "purple")
            ball = Ball(WIDTH / 2, HEIGHT - PADDLE_HEIGHT - 5 - BALL_RADIUS, BALL_RADIUS, 'black')
            bricks = generate_bricks(3, 5)
            lives = 3

            lost_text = LIVES_FONT.render("HAHAHA YOU LOST!!!", 1, "red")
            win.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2 ))
            pygame.display.update()
            pygame.time.delay(5000)
        draw(win, paddle, ball, bricks, lives)
    pygame.quit()
    quit()


if __name__ == "__main__":
    main()
