import pygame
from pygame import gfxdraw
from objects.particle import Particle

def create_particle(particleList: list[Particle]):
    position = pygame.Vector2(WIDTH / 2, HEIGHT / 2)
    mass = 10.0
    radius = 50.0
    babyParticle = Particle(position, mass, radius)
    particleList.append(babyParticle)

def draw_particles(particleList: list[Particle]):
    velocities = [i.velocity.magnitude() for i in particleList]
    max_velocity = max(velocities)
    for particle in particleList:
        particle.apply_dynamic_color(max_velocity)
        # pygame.draw.circle(screen, particle.color, particle.position_current * SCALE, particle.radius * SCALE)
        gfxdraw.aacircle(screen, int(particle.position_current.x * SCALE), int(particle.position_current.y * SCALE), int(particle.radius * SCALE), particle.color)
        gfxdraw.filled_circle(screen, int(particle.position_current.x * SCALE), int(particle.position_current.y * SCALE), int(particle.radius * SCALE), (particle.color.r, particle.color.g, particle.color.b, 100))

def apply_gravity(particleList: list[Particle]):
    GRAVITY = pygame.Vector2(0.0, 10.0)
    for particle in particleList:
        particle.accelerate(GRAVITY)

def update_positions(particleList: list[Particle], dt):
    for particle in particleList:
        particle.update_position(dt)

def apply_gravitational_force(particleList: list[Particle]):
    GRAVITATIONAL_CONSTANT = 1
    for i in range(len(particleList)):
        particle_1 = particleList[i]
        for k in range(i + 1, len(particleList)):
            particle_2 = particleList[k]

            separation_axis = particle_1.position_current - particle_2.position_current
            distance = separation_axis.magnitude()

            force = (GRAVITATIONAL_CONSTANT * particle_1.mass * particle_2.mass / (distance * distance * distance)) * separation_axis

            particle_1.apply_force(-force)
            particle_2.apply_force(force)

def calculate_gravitational_energy(particleList: list[Particle]):
    GRAVITATIONAL_CONSTANT = 1
    gravitational_energy = 0.0
    for i in range(len(particleList)):
        particle_1 = particleList[i]
        for k in range(i + 1, len(particleList)):
            particle_2 = particleList[k]
            separation_axis = particle_1.position_current - particle_2.position_current
            distance = separation_axis.magnitude()
            gravitational_energy -= particle_1.mass * particle_2.mass / distance

    return gravitational_energy

def calculate_knetic_energy(particleList: list[Particle]):
    knetic_energy = 0.0
    for particle in particleList:
        knetic_energy += 0.5 * particle.mass * particle.velocity.magnitude()**2
    
    return knetic_energy
    
def apply_lennard_jhones(particleList: list[Particle]):
    EPSILON = 1.5
    SIGMA = 0.9
    for i in range(len(particleList)):
        particle_1 = particleList[i]
        for k in range(i+1, len(particleList)):
            particle_2 = particleList[k]
            
            separation_axis = particle_1.position_current - particle_2.position_current
            normalized_separation_axis = separation_axis.normalize()
            distance = separation_axis.magnitude()
            
            force = 48 * EPSILON * ((SIGMA**12 / distance**13) - (SIGMA**6 / distance**7)) * normalized_separation_axis
            particle_1.apply_force(force)
            particle_2.apply_force(-force)


def apply_boundary_condition(particleList: list[Particle]):
    WALL_LEFT = 0
    WALL_RIGHT = WORLD_WIDTH
    WALL_TOP = 0
    WALL_BOTTOM = WORLD_HEIGHT

    for particle in particleList:
        if particle.position_current.x - particle.radius < WALL_LEFT:
            particle.position_current.x = WALL_LEFT + particle.radius
            x_velocity = particle.velocity.x
            y_velocity = particle.velocity.y
            new_velocity = pygame.Vector2(-x_velocity, y_velocity)
            particle.set_velocity(new_velocity)

        if particle.position_current.x + particle.radius > WALL_RIGHT:
            particle.position_current.x = WALL_RIGHT - particle.radius
            x_velocity = particle.velocity.x
            y_velocity = particle.velocity.y
            new_velocity = pygame.Vector2(-x_velocity, y_velocity)
            particle.set_velocity(new_velocity)

        if particle.position_current.y - particle.radius < WALL_TOP:
            particle.position_current.y = WALL_TOP + particle.radius
            x_velocity = particle.velocity.x
            y_velocity = particle.velocity.y
            new_velocity = pygame.Vector2(x_velocity, -y_velocity)
            particle.set_velocity(new_velocity)

        if particle.position_current.y + particle.radius > WALL_BOTTOM:
            particle.position_current.y = WALL_BOTTOM - particle.radius
            x_velocity = particle.velocity.x
            y_velocity = particle.velocity.y
            new_velocity = pygame.Vector2(x_velocity, -y_velocity)
            particle.set_velocity(new_velocity)
            



# constants
FRAMES_PER_SECOND = 60
SUB_STEPS = 1

WIDTH = 1280
HEIGHT = 720


WORLD_WIDTH = 20
WORLD_HEIGHT = 11.25

SCALE_X = WIDTH / WORLD_WIDTH
SCALE_Y = HEIGHT / WORLD_HEIGHT

SCALE = min(SCALE_X, SCALE_Y)


# pygame setup
pygame.init()
screen = pygame.display.set_mode((WORLD_WIDTH * SCALE, WORLD_HEIGHT * SCALE))
clock = pygame.time.Clock()

# particle initialization
particleList = []

NUMBER_OF_PARTICLES_PER_ROW = 10
SPACING = 1.14

for i in range(NUMBER_OF_PARTICLES_PER_ROW - 1):
    for j in range(NUMBER_OF_PARTICLES_PER_ROW - 1):
        babyParticle = Particle(pygame.Vector2( SPACING * i, + SPACING * j), 100, 10.0 / SCALE, "white")
        particleList.append(babyParticle)

# EXEMPLO DE ESTADO INICIAL LIGADO
# p1 = Particle(pygame.Vector2(5, 5), 100, 10.0 / SCALE, "white")
# p1.set_velocity(pygame.Vector2(0.0, 0.001))

# p2 = Particle(pygame.Vector2(6.12, 5), 100, 10.0 / SCALE, "white")
# p2.set_velocity(pygame.Vector2(0.01, -0.001))

# p3 = Particle(pygame.Vector2(5, 6.12), 100, 10.0 / SCALE, "white")
# p3.set_velocity(pygame.Vector2(0.0, -0.001))

# p4 = Particle(pygame.Vector2(6.12, 6.12), 100, 10.0 / SCALE, "white")
# p4.set_velocity(pygame.Vector2(-0.01, -0.001))

# particleList.append(p1)
# particleList.append(p2)
# particleList.append(p3)
# particleList.append(p4)

# game loop
running = True
while running:

    # basic setup
    screen.fill("black")
    clock.tick(FRAMES_PER_SECOND)
    
    # delta time
    # dt = clock.get_fps() / 1000.0
    dt = 0.05
    sub_dt = dt / SUB_STEPS
    
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    # physics
    for _ in range(SUB_STEPS):
        apply_lennard_jhones(particleList)
        apply_boundary_condition(particleList)
        update_positions(particleList, sub_dt)
        draw_particles(particleList)

    pygame.display.flip()

pygame.quit()