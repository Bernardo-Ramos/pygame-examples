import pygame
from pygame import gfxdraw
from objects.particle import Particle
from objects.link import Link

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
        # particle.apply_dynamic_color(max_velocity)
        # pygame.draw.circle(screen, particle.color, particle.position_current * SCALE, particle.radius * SCALE)
        gfxdraw.aacircle(screen, int(particle.position_current.x * SCALE), int(particle.position_current.y * SCALE), int(particle.radius * SCALE), particle.color)
        gfxdraw.filled_circle(screen, int(particle.position_current.x * SCALE), int(particle.position_current.y * SCALE), int(particle.radius * SCALE), (particle.color.r, particle.color.g, particle.color.b, 100))

def draw_lines(linkList: list[Link]):
    for link in linkList:
        pygame.draw.line(screen, pygame.Color(255, 255, 255, 255), link.particle_1.position_current, link.particle_2.position_current)

def apply_gravity(particleList: list[Particle]):
    GRAVITY = pygame.Vector2(0.0, 10.0)
    for particle in particleList:
        particle.accelerate(GRAVITY)

def update_positions(particleList: list[Particle], linkList: list[Link], dt):
    for particle in particleList:
        particle.update_position(dt)

    for link in linkList:
        link.apply_constrain()


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

def solve_collisions(particleList: list[Particle]):
    for i in range(len(particleList)):
        particle_1 = particleList[i]

        for k in range(i+1, len(particleList)):
            particle_2 = particleList[k]
            collision_axis = particle_1.position_current - particle_2.position_current
            distance_1_to_2 = collision_axis.magnitude()

            if distance_1_to_2 == 0:
                continue

            if distance_1_to_2 < particle_1.radius + particle_2.radius:
                normalized_collision_axis = collision_axis / distance_1_to_2
                correction_factor = (particle_1.radius + particle_2.radius) - distance_1_to_2

                if particle_1.is_fixed == False:
                    particle_1.position_current += 0.5 * correction_factor * normalized_collision_axis
                
                if particle_2.is_fixed == False:
                    particle_2.position_current -= 0.5 * correction_factor * normalized_collision_axis

def apply_mouse_force(particleList: list[Particle]):
    mouse_force = pygame.Vector2(pygame.mouse.get_pos())

    for particle in particleList:
        particle.accelerate(mouse_force)

# constants
FRAMES_PER_SECOND = 60
SUB_STEPS = 2

WIDTH = 1280
HEIGHT = 720

WORLD_WIDTH = 1280
WORLD_HEIGHT = 720

SCALE_X = WIDTH / WORLD_WIDTH
SCALE_Y = HEIGHT / WORLD_HEIGHT
SCALE = min(SCALE_X, SCALE_Y)


# pygame setup
pygame.init()
screen = pygame.display.set_mode((WORLD_WIDTH * SCALE, WORLD_HEIGHT * SCALE))
clock = pygame.time.Clock()

# particle initialization
particleList = []
linkList = []

p1 = Particle(pygame.Vector2(WORLD_WIDTH / 2, WORLD_HEIGHT / 4), 10, 30, pygame.Color(255, 255, 255, 255), True)
p2 = Particle(pygame.Vector2(WORLD_WIDTH / 5, WORLD_HEIGHT / 3), 10, 30, pygame.Color(255, 0, 0, 255))
p3 = Particle(pygame.Vector2(WORLD_WIDTH / 6, WORLD_HEIGHT / 3), 10, 30, pygame.Color(0, 0, 255, 255))
p4 = Particle(pygame.Vector2(WORLD_WIDTH / 7, WORLD_HEIGHT / 3), 10, 30, pygame.Color(255, 255, 100, 255))

particleList.append(p1)
particleList.append(p2)
particleList.append(p3)
particleList.append(p4)

l1 = Link(p1, p2, 100.0)
l2 = Link(p2, p3, 100.0)
l3 = Link(p3, p4, 100.0)


linkList.append(l1)
linkList.append(l2)
linkList.append(l3)





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
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            apply_mouse_force(particleList)

    # physics
    for _ in range(SUB_STEPS):
        apply_boundary_condition(particleList)
        apply_gravity(particleList)
        solve_collisions(particleList)
        update_positions(particleList, linkList, sub_dt)

    draw_lines(linkList)
    draw_particles(particleList)
    pygame.display.flip()

pygame.quit()