import pygame
from .particle import Particle


class Link:
    def __init__(self, particle_1: Particle, particle_2: Particle, link_length: float):
        self.particle_1 = particle_1
        self.particle_2 = particle_2
        self.link_length = link_length

    def apply_constrain(self):
        separation_axis = self.particle_1.position_current - self.particle_2.position_current
        distance_1_to_2 = separation_axis.magnitude()

        if distance_1_to_2 != self.link_length:
            separation_axis_normalized = separation_axis.normalize()
            correction_factor = distance_1_to_2 - self.link_length

            if self.particle_1.is_fixed == False:
                self.particle_1.position_current += -0.5 * correction_factor * separation_axis_normalized

            if self.particle_2.is_fixed == False:
                self.particle_2.position_current += 0.5 * correction_factor * separation_axis_normalized




