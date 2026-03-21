import pygame
from objects.particle import Particle

def create_particle(particleList: list[Particle]):
    position = pygame.Vector2(WIDTH / 2, HEIGHT / 2)
    mass = 10.0
    radius = 50.0
    babyParticle = Particle(position, mass, radius)
    particleList.append(babyParticle)

def draw_particles(particleList: list[Particle]):
    for particle in particleList:
        pygame.draw.circle(screen, particle.color, particle.position_current, particle.radius)

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
    



# constants
WIDTH = 1280
HEIGHT = 720
FRAMES_PER_SECOND = 60
SUB_STEPS = 1

# pygame setup
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# particle initialization
particleList = []

SEPARATION = 100
p1 = Particle(pygame.Vector2( SEPARATION + WIDTH / 2,  SEPARATION + HEIGHT / 2), 9000.0, 20.0, "blue")
p2 = Particle(pygame.Vector2(-SEPARATION + WIDTH / 2, -SEPARATION + HEIGHT / 2), 9000.0, 20.0, "yellow")
p3 = Particle(pygame.Vector2(              WIDTH / 2,               HEIGHT / 2), 9000.0, 20.0, "red")

p1.set_velocity(pygame.Vector2(-0.5, 0.0))
p2.set_velocity(pygame.Vector2(0.4, -0.2))
p3.set_velocity(pygame.Vector2(-0.2, -0.0))

particleList.append(p1)
particleList.append(p2)
particleList.append(p3)


# game loop
running = True
while running:

    # basic setup
    screen.fill("black")
    clock.tick(FRAMES_PER_SECOND)
    
    # delta time
    dt = clock.get_fps() / 1000.0
    sub_dt = dt / SUB_STEPS
    
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    # physics
    for _ in range(SUB_STEPS):
        # apply_gravity(particleList)
        apply_gravitational_force(particleList)
        update_positions(particleList, sub_dt)
        draw_particles(particleList)

    potential_energy = calculate_gravitational_energy(particleList)
    knetic_energy = calculate_knetic_energy(particleList)
    total = potential_energy + knetic_energy

    energy = "U: {0} | K: {1} | Total: {2}".format(potential_energy, knetic_energy, total)
    print(energy)
    



    
    pygame.display.flip()

pygame.quit()