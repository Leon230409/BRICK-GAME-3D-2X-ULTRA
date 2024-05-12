import pygame


class Ball:
    def __init__(self, x, y, radius, color, speed):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.VEL = speed
        self.x_vel = 0
        self.y_vel = -1

    def move(self):
        self.x += self.x_vel * self.VEL
        self.y += self.y_vel * self.VEL

    def set_vel(self, x_vel, y_vel):
        self.x_vel = x_vel
        self.y_vel = y_vel

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)

    def set_position(self, x, y):
        self.x = x
        self.y = y