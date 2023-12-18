import pygame
import math
import random
from levels import gameLevels

# Constants
WIDTH, HEIGHT = 850, 600
FPS = 60
PADDLE_WIDTH = 120
PADDLE_HEIGHT = 10
BALL_RADIUS = 10
pygame.font.init()
LIVES_FONT = pygame.font.SysFont("comicsans", 40)
LEVEL = 1


# Game class
class Game:
    def __init__(self):
        self.ball = Ball(WIDTH / 2, HEIGHT - PADDLE_HEIGHT - 5 - BALL_RADIUS, BALL_RADIUS,
                         gameLevels[LEVEL]["ballColor"])
        self.paddle = Paddle()
        pygame.init()
        self.win = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("BRICK BREAKER")
        self.clock = pygame.time.Clock()
        self.all_sprites = pygame.sprite.Group()
        self.bricks = pygame.sprite.Group()
        self.initialize_game()
        self.LIVES = 3

    def initialize_game(self):
        # Initialize game objects
        self.bricks = self.generate_bricks()
        self.LIVES = 3

        # Add sprites to the sprite group
        self.all_sprites.add(self.paddle)

        # Load background image
        self.background_image = pygame.image.load(gameLevels[LEVEL]["bckImg"])
        self.background_image = pygame.transform.scale(self.background_image, (WIDTH, HEIGHT))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and self.paddle.rect.x > 0:
            self.paddle.move(-1)
        if keys[pygame.K_d] and self.paddle.rect.x + self.paddle.width < WIDTH:
            self.paddle.move(1)
        if keys[pygame.K_z]:
            print("STOP")
        return True

    def update_game_state(self):
        self.ball.move()
        self.ball_collision(self.ball)
        self.ball_paddle_collision()
        self.ball_flor_collision()

        for brick in self.bricks:
            self.ball_brick_collision(brick)
            if brick.health <= 0:
                self.bricks.remove(brick)

        if len(self.bricks) <= 0:
            self.load_next_level()

        if self.LIVES <= 0:
            self.reset_game()

    def load_next_level(self):
        global LEVEL
        LEVEL += 1
        self.all_sprites.remove(self.paddle)
        self.paddle = Paddle()
        self.all_sprites.add(self.paddle)
        self.ball = Ball(WIDTH / 2, HEIGHT - PADDLE_HEIGHT - 5 - BALL_RADIUS, BALL_RADIUS,
                         gameLevels[LEVEL]["ballColor"])
        self.bricks = self.generate_bricks()
        self.background_image = pygame.image.load(gameLevels[LEVEL]["bckImg"])
        self.background_image = pygame.transform.scale(self.background_image, (WIDTH, HEIGHT))
        self.LIVES = 3

    def reset_game(self):
        global LEVEL
        LEVEL = 1
        self.all_sprites.remove(self.paddle)
        self.paddle = Paddle()
        self.all_sprites.add(self.paddle)
        self.ball = Ball(WIDTH / 2, HEIGHT - PADDLE_HEIGHT - 5 - BALL_RADIUS, BALL_RADIUS,
                         gameLevels[LEVEL]["ballColor"])
        self.bricks = self.generate_bricks()
        self.background_image = pygame.image.load(gameLevels[LEVEL]["bckImg"])
        self.background_image = pygame.transform.scale(self.background_image, (WIDTH, HEIGHT))
        self.LIVES = 3

    def generate_bricks(self):
        brick_sprites = pygame.sprite.Group()

        helpBrick = Brick(-100, -100, 0)
        brick_width = helpBrick.rect.width
        brick_height = helpBrick.rect.height

        gap = 5.55
        bricksMatrix = gameLevels[LEVEL]["brickMap"]
        for row in range(len(bricksMatrix)):
            for col in range(len(bricksMatrix[row])):
                if bricksMatrix[row][col] == 1:
                    brick = Brick(gap + col * (brick_width + gap), gap + row * (brick_height + gap), 2)
                    brick_sprites.add(brick)
                    print(brick.rect.x, brick.rect.y)
        return brick_sprites

    def ball_collision(self, ball):
        if ball.x - BALL_RADIUS <= 0:
            ball.set_position(WIDTH - ball.radius * 2, ball.y)
        elif ball.x + BALL_RADIUS >= WIDTH:
            ball.set_position(0 + ball.radius * 2, ball.y)

        if ball.y - BALL_RADIUS <= 0:
            ball.set_vel(ball.x_vel, ball.y_vel * -1)

    def ball_flor_collision(self):
        if self.ball.y + BALL_RADIUS >= HEIGHT:
            self.LIVES -= 1
            self.ball.set_position(self.paddle.rect.x + self.paddle.width // 2, self.paddle.rect.y - self.ball.radius)
            self.ball.set_vel(0, -self.ball.VEL)

    def ball_paddle_collision(self):
        if not ((self.ball.x <= (self.paddle.rect.x + self.paddle.width)) and (self.ball.x >= self.paddle.rect.x)):
            return
        if not (self.ball.y + self.ball.radius >= self.paddle.rect.y):
            return

        distance_to_center = self.ball.x - self.paddle.rect.centerx

        percent_width = distance_to_center / self.paddle.width
        angle = percent_width * 90
        angle_radians = math.radians(angle)

        x_vel = math.sin(angle_radians) * self.ball.VEL
        y_vel = math.cos(angle_radians) * self.ball.VEL
        self.ball.set_vel(x_vel, y_vel * -1)

    def ball_brick_collision(self, brick):
        if (brick.rect.y < self.ball.y - self.ball.radius <= brick.rect.bottom) and (
                brick.rect.x - self.ball.radius < self.ball.x < brick.rect.right + self.ball.radius):
            print(" удар снизу")
            brick.hit()
            self.ball.set_position(self.ball.x, self.ball.y + self.ball.VEL)
            self.ball.set_vel(self.ball.x_vel, self.ball.y_vel * -1)
        # удар справа
        elif (self.ball.x + self.ball.radius >= brick.rect.x) and (
                self.ball.x + self.ball.radius < brick.rect.right) and (brick.rect.y < self.ball.y < brick.rect.bottom):
            print(" удар справа")
            brick.hit()
            self.ball.set_position(self.ball.x - self.ball.VEL, self.ball.y)
            self.ball.set_vel(self.ball.x_vel * -1, self.ball.y_vel)
        elif (self.ball.x - self.ball.radius <= brick.rect.right) and (
                self.ball.x - self.ball.radius > brick.rect.x) and (brick.rect.y < self.ball.y < brick.rect.bottom):
            print(" удар слева")
            brick.hit()
            self.ball.set_position(self.ball.x + self.ball.VEL, self.ball.y)
            self.ball.set_vel(self.ball.x_vel * -1, self.ball.y_vel)
        elif (brick.rect.y <= self.ball.y + self.ball.radius < brick.rect.bottom) and (
                brick.rect.x - self.ball.radius < self.ball.x < brick.rect.right + self.ball.radius):
            print(" удар сверху")
            brick.hit()
            self.ball.set_position(self.ball.x, self.ball.y - self.ball.VEL)
            self.ball.set_vel(self.ball.x_vel, self.ball.y_vel * -1)

    def draw(self):
        self.win.blit(self.background_image, self.background_image.get_rect())
        self.all_sprites.update()
        self.all_sprites.draw(self.win)
        self.bricks.update()
        self.bricks.draw(self.win)
        self.ball.draw(self.win)
        lives_text = LIVES_FONT.render(f"HP:{self.LIVES}", 1, gameLevels[LEVEL]["textColor"])
        self.win.blit(lives_text, (10, HEIGHT - lives_text.get_height() - 10))
        pygame.display.update()

    def run(self):
        run = True
        while run:
            run = self.handle_events()
            self.update_game_state()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()
        quit()


class Paddle(pygame.sprite.Sprite):
    VEL = 5

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/paddle.png')
        self.rect = self.image.get_rect()
        self.width = self.rect[2]
        self.height = self.rect[3]
        self.rect.center = (WIDTH // 2, HEIGHT - self.height)

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


if __name__ == "__main__":
    game = Game()
    game.run()
