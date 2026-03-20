import pygame

class Particle:
    def __init__(self, position, radius):
        self.position_current = position
        self.position_old = self.position_current.copy()
        self.acceleration = pygame.Vector2(0.0, 0.0)
        self.radius = radius

    def updatePosition(self, dt):
        self.velocity = self.position_current - self.position_old
        self.position_old = self.position_current
        self.position_current = self.position_current + self.velocity + self.acceleration * dt * dt
        self.acceleration = pygame.Vector2(0.0, 0.0)

    def accelerate(self, acceleration):
        self.acceleration += acceleration



