import pygame
from simulation.particle import Particle


def applyGravity(particles):
    # apply gravity
    for particle in particles:
        GRAVITY = pygame.Vector2(0.0, 10.0)
        particle.accelerate(GRAVITY)

def applyConstrain(particles):
    # apply constrain
    CONSTRAIN_RADIUS = 300.0
    constrain_position = pygame.Vector2(WIDTH / 2, HEIGHT / 2)
    for particle in particles:
        constrain_to_particle = particle.position_current - constrain_position
        distance_magnitude = constrain_to_particle.magnitude()

        if distance_magnitude + particle.radius > CONSTRAIN_RADIUS:
            normalized_constrain_to_particle = constrain_to_particle / distance_magnitude
            particle.position_current = constrain_position + normalized_constrain_to_particle * (CONSTRAIN_RADIUS - particle.radius)
            
    pygame.draw.circle(screen, "black", constrain_position, CONSTRAIN_RADIUS)

def updatePosition(particles, _dt):
    # update positions
    for particle in particles:
        particle.updatePosition(_dt)

def drawParticles(particles):
    # draw particles
    for particle in particles:
        pygame.draw.circle(screen, "white", particle.position_current, particle.radius)

def solveCollisions(particles: Particle):
    for i in range(len(particles)):
        particle_1 = particles[i]
        for k in range(i+1, len(particles)):
            particle_2 = particles[k]
            collision_axis = particle_1.position_current - particle_2.position_current
            distance_1_to_2 = collision_axis.magnitude()

            if distance_1_to_2 == 0:
                continue

            if distance_1_to_2 < particle_1.radius + particle_2.radius:
                normalized_collision_axis = collision_axis / distance_1_to_2
                correction_factor = (particle_1.radius + particle_2.radius) - distance_1_to_2
                particle_1.position_current += 0.5 * correction_factor * normalized_collision_axis
                particle_2.position_current -= 0.5 * correction_factor * normalized_collision_axis

def createParticle(particleList):
    PARTICLE_RADIUS = 10
    babyParticle = Particle(pygame.Vector2(230 + WIDTH / 2, HEIGHT / 2 - 70), PARTICLE_RADIUS)
    babyParticle.position_old.y -= 1.0
    babyParticle.position_old.x += 2.0
    particleList.append(babyParticle)

# constants
WIDTH = 1280
HEIGHT = 720
FRAMES_PER_SECOND = 60
MAX_PARTICLES = 200
SUB_STEPS = 2

# initialization
dt = 0
particles = []

# initializing pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# custom event
SPAWN_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_EVENT, 100)

# render loop
running = True
while running:

    screen.fill("gray")
    clock.tick(FRAMES_PER_SECOND)
    dt = clock.get_fps() / 1000.0
    sub_dt = dt / SUB_STEPS

    print(f"---------")
    print(f"dt: {dt}")
    print(f"sub_dt: {sub_dt}")


    # scan for quit event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == SPAWN_EVENT and len(particles) < MAX_PARTICLES:
            createParticle(particles)


    # physics
    for i in range(SUB_STEPS):    
        applyGravity(particles)
        applyConstrain(particles)
        solveCollisions(particles)
        updatePosition(particles, sub_dt)

    # render particles
    drawParticles(particles)


    pygame.display.flip()


pygame.quit()