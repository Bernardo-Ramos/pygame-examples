import pygame

WIDTH = 1280
HEIGHT = 720
FRAMES_PER_SECOND = 60
RADIUS = 30

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

x_position = [WIDTH/2]
y_position = [HEIGHT/4]

DELTA_TIME = 0

X_VELOCITY = 50
Y_VELOCITY = 70


running = True

index = 0

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("black")

    x_position.append(x_position[index] + DELTA_TIME * X_VELOCITY)
    y_position.append(y_position[index] + DELTA_TIME * Y_VELOCITY)

    pygame.draw.circle(screen, "white", (x_position[-1], y_position[-1]), RADIUS)
    
    pygame.display.flip()
    
    DELTA_TIME = clock.tick(FRAMES_PER_SECOND) / 1000

    index += 1

pygame.quit()