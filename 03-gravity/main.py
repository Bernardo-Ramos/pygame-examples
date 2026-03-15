import pygame

WIDTH = 1280
HEIGHT = 720
FRAMES_PER_SECOND = 60
RADIUS = 30

x = [WIDTH / 2]
y = [HEIGHT / 4]

vx = [0.0]
vy = [0.0]

ax = 0.0
ay = 10.0

dt = 0

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

running = True
index = 0
while running:


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("black")

    pygame.draw.circle(screen, "white", (x[-1], y[-1]), RADIUS)
    pygame.display.flip()

    clock.tick(FRAMES_PER_SECOND)
    dt = clock.get_fps() / 1000.0

    x.append(x[index] + vx[index] * dt)
    y.append(y[index] + vy[index] * dt)

    vx.append(vx[index] + ax * dt)
    vy.append(vy[index] + ay * dt)

    index += 1


pygame.quit()