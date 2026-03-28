import pygame
class Particle:
    def __init__(self, position: pygame.Vector2, mass: float, radius: float, color: str, is_fixed: bool = False):
        self.position_current = position
        self.position_old = self.position_current.copy()
        self.mass = mass
        self.radius = radius
        self.acceleration = pygame.Vector2(0.0, 0.0)
        self.velocity = pygame.Vector2(0.0, 0.0)
        self.color = color
        self.is_fixed = is_fixed

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

    def apply_dynamic_color(self, max_velocity=0.06):
        if max_velocity < 0.002:
            max_velocity = 0.06
        
        value = 255 * self.velocity.magnitude() / max_velocity
        red = int(value)
        green = abs(int(255 - value) - 20)
        blue = int((255 - value))
        alpha = 255
        self.color = pygame.Color(red, green, blue, alpha)

    def update_position(self, dt: float):
        if self.is_fixed:
            return
        
        
        self.velocity = self.position_current - self.position_old
        self.position_old = self.position_current.copy()
        self.position_current = self.position_current + self.velocity + self.acceleration * dt * dt
        self.acceleration = pygame.Vector2(0.0, 0.0)
