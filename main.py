import pygame
import math
import random
from levels import gameLevels
from Ball import *
from Paddle import *
from brick import *
import os

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
        self.mass_balls = [Ball(WIDTH / 2, HEIGHT - PADDLE_HEIGHT - 50 - BALL_RADIUS, BALL_RADIUS,
                                gameLevels[LEVEL]["ballColor"], 5)]
        self.paddle = Paddle((WIDTH, HEIGHT))
        pygame.init()
        self.win = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("BRICK BREAKER")
        self.clock = pygame.time.Clock()
        self.all_sprites = pygame.sprite.Group()
        self.bricks = pygame.sprite.Group()
        self.initialize_game()
        self.LIVES = 3
        self.FORCE = False


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
            elif event.type == pygame.KEYDOWN:  # Обработка нажатия клавиши
                if event.key == pygame.K_SPACE:  # Пример: если нажата клавиша Пробел
                    self.ballsX2(self.mass_balls[0])


        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and self.paddle.rect.x > 0:
            self.paddle.move(-1)
        if keys[pygame.K_d] and self.paddle.rect.x + self.paddle.rect.width < WIDTH:
            self.paddle.move(1)
        if keys[pygame.K_z]:
            print("STOP")
        if keys[pygame.K_f]:
            self.paddle.set_plus_size()

        return True

    def update_game_state(self):
        for ball in self.mass_balls:
            ball.move()
            self.ball_collision(ball)

        self.ball_paddle_collision()
        self.ball_flor_collision()

        for brick in self.bricks:

            ball = self.ball_brick_collision(brick)
            if brick.health <= 0:
                self.bricks.remove(brick)
                if brick.name == "speed":
                    for b in self.mass_balls:
                        if b.VEL < 7:
                            b.VEL += 2
                elif brick.name == 'force':
                    self.FORCE = True
                elif brick.name == 'longPaddle':
                    self.paddle.set_plus_size()
                elif brick.name == 'X2Ball':
                    self.ballsX2(ball)
                elif brick.name == 'slow':
                    for b in self.mass_balls:
                        if b.VEL > 3:
                            b.VEL -= 2



        if len(self.bricks) <= 0 or all(isinstance(sprite, MetalicaBrick) for sprite in self.bricks.sprites()):
            self.load_next_level()

        if self.LIVES <= 0:
            self.reset_game()

    def load_next_level(self):
        global LEVEL
        LEVEL += 1
        self.all_sprites.remove(self.paddle)
        self.paddle = Paddle((WIDTH, HEIGHT))
        self.all_sprites.add(self.paddle)
        self.mass_balls = [Ball(WIDTH / 2, HEIGHT - PADDLE_HEIGHT - 5 - BALL_RADIUS, BALL_RADIUS,
                                gameLevels[LEVEL]["ballColor"], 5)]
        self.bricks = self.generate_bricks()
        self.background_image = pygame.image.load(gameLevels[LEVEL]["bckImg"])
        self.background_image = pygame.transform.scale(self.background_image, (WIDTH, HEIGHT))
        self.LIVES = 3
        self.FORCE = False

    def reset_game(self):
        global LEVEL
        LEVEL = 1
        # saveCoordX = self.paddle.rect.centerx
        self.all_sprites.remove(self.paddle)
        self.paddle = Paddle((WIDTH, HEIGHT))
        # self.paddle.set_posX(saveCoordX)
        self.all_sprites.add(self.paddle)
        self.mass_balls = [Ball(WIDTH / 2, HEIGHT - PADDLE_HEIGHT - 5 - BALL_RADIUS, BALL_RADIUS,
                                gameLevels[LEVEL]["ballColor"], 5)]
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
                brick_type = bricksMatrix[row][col]
                if brick_type != 0:
                    brick = BrickFactory.create_brick(gap + col * (brick_width + gap), gap + row * (brick_height + gap),
                                                      brick_type)
                    brick_sprites.add(brick)
                    print(brick.rect.x, brick.rect.y)
        return brick_sprites

    def generate_ball(self):
        self.mass_balls.append(Ball(self.paddle.rect.x + self.paddle.rect.width // 2, self.paddle.rect.y - 5 - BALL_RADIUS, BALL_RADIUS,
                                gameLevels[LEVEL]["ballColor"], 5))

    def ballsX2(self, ball):
        newBall = Ball(ball.x, ball.y, ball.radius, ball.color, ball.VEL)
        newBall.set_vel(ball.x_vel * -1, ball.y_vel)
        self.mass_balls.append(newBall)
        print()


    def ball_collision(self, ball):
        if not self.FORCE:
            if ball.x + BALL_RADIUS <= BALL_RADIUS*2 or ball.x - BALL_RADIUS >= WIDTH - BALL_RADIUS*2:
                ball.set_vel(ball.x_vel * -1, ball.y_vel)

            if ball.y + BALL_RADIUS <= BALL_RADIUS*2:
                ball.set_vel(ball.x_vel, ball.y_vel * -1)
        else:
            if ball.x - BALL_RADIUS <= 0:
                ball.set_position(WIDTH - ball.radius * 2, ball.y)
            elif ball.x + BALL_RADIUS >= WIDTH:
                ball.set_position(0 + ball.radius * 2, ball.y)

            if ball.y - BALL_RADIUS <= 0:
                ball.set_vel(ball.x_vel, ball.y_vel * -1)

    def ball_flor_collision(self):
        for ball in self.mass_balls:
            if ball.y + BALL_RADIUS >= HEIGHT:
                self.mass_balls.remove(ball)
                if not self.mass_balls:
                    self.LIVES -= 1
                    self.FORCE = False
                    self.generate_ball()

    def ball_paddle_collision(self):
        for ball in self.mass_balls:
            if (self.paddle.rect.x <= ball.x <= self.paddle.rect.right) and (
                    ball.y + ball.radius >= self.paddle.rect.y):
                distance_to_center = ball.x - self.paddle.rect.centerx

                percent_width = distance_to_center / self.paddle.rect.width
                angle = percent_width * 90
                angle_radians = math.radians(angle)

                x_vel = math.sin(angle_radians)
                y_vel = math.cos(angle_radians)
                ball.set_vel(x_vel, y_vel * -1)
        # return

    def ball_brick_collision(self, brick):
        for ball in self.mass_balls:
            # Рассчитываем ближайшие точки на кирпиче к центру шара
            closest_x = max(brick.rect.x, min(ball.x, brick.rect.x + brick.rect.width))
            closest_y = max(brick.rect.y, min(ball.y, brick.rect.y + brick.rect.height))

            # Вычисляем расстояние между центром шара и ближайшей точкой на кирпиче
            distance_x = ball.x - closest_x
            distance_y = ball.y - closest_y

            # Проверяем, с какой стороны было столкновение
            if (distance_x ** 2 + distance_y ** 2) < ball.radius ** 2:
                if distance_y > 0:
                    print(" удар снизу")
                    brick.hit()
                    if brick.name == 'X2Ball':
                        return ball
                    ball.set_vel(ball.x_vel, ball.y_vel * -1)
                    ball.set_position(ball.x, ball.y + ball.VEL)
                    return ball
                elif distance_y < 0:
                    # Столкновение с верхней стороной кирпича
                    print(" удар сверху")
                    brick.hit()
                    if brick.name == 'X2Ball':
                        return ball
                    ball.set_vel(ball.x_vel, ball.y_vel * -1)
                    ball.set_position(ball.x, ball.y - ball.VEL)
                    return ball
                elif distance_x > 0:
                    # Столкновение с правой стороной кирпича
                    print(" удар справа")
                    brick.hit()
                    ball.set_vel(ball.x_vel * -1, ball.y_vel)
                    ball.set_position(ball.x + ball.VEL, ball.y)
                    return ball
                elif distance_x < 0:
                    # Столкновение с левой стороной кирпича
                    print(" удар слева")
                    brick.hit()
                    if brick.name == 'X2Ball':
                        return ball
                    ball.set_vel(ball.x_vel * -1, ball.y_vel)
                    ball.set_position(ball.x - ball.VEL, ball.y)
                    return ball

    def draw(self):
        self.win.blit(self.background_image, self.background_image.get_rect())
        self.all_sprites.update()
        self.all_sprites.draw(self.win)
        self.bricks.update()
        self.bricks.draw(self.win)
        for ball in self.mass_balls:
            ball.draw(self.win)
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


if __name__ == "__main__":
    game = Game()
    game.run()
