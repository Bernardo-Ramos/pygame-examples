import pygame
class Particle:
    def __init__(self, position: pygame.Vector2, mass: float, radius: float, color: str):
        self.position_current = position
        self.position_old = self.position_current.copy()
        self.mass = mass
        self.radius = radius
        self.acceleration = pygame.Vector2(0.0, 0.0)
        self.color = color

    def set_velocity(self, velocity: pygame.Vector2):
        """
        To set the velocity is the same thing as change position_old.
        """
        self.velocity = velocity
        self.position_old = self.position_current - self.velocity

    def accelerate(self, acceleration: pygame.Vector2):
        self.acceleration += acceleration

    def apply_force(self, force: pygame.Vector2):
        self.accelerate(force / self.mass)

    def update_position(self, dt: float):
        self.velocity = self.position_current - self.position_old
        self.position_old = self.position_current.copy()
        self.position_current = self.position_current + self.velocity + self.acceleration * dt * dt
        self.acceleration = pygame.Vector2(0.0, 0.0)


