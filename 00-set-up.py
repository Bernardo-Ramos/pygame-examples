import pygame

FRAMES_PER_SECOND = 60

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((860, 860))

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("purple")
    pygame.display.flip()

    clock.tick(FRAMES_PER_SECOND)


pygame.quit()