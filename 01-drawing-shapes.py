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

    screen.fill("black")

    # rectangles
    RECTANGLE_COLOR = pygame.Color(63, 63, 63, 255)
    RECTANGLE_VERTICES = pygame.Rect(100, 200, 300, 400)
    rectangle_1 = pygame.draw.rect(screen, RECTANGLE_COLOR, RECTANGLE_VERTICES)
    rectangle_2 = pygame.draw.rect(screen, "blue", (100, 100, 100, 100))

    # polygon
    polygon_1 = pygame.draw.polygon(screen, "green", [(800, 850), (600, 650), (50, 300)])
    polygon_2 = pygame.draw.polygon(screen, "red", [(80, 850), (600, 350), (10, 840)], 1)

    # circle
    CIRCLE_CENTER = pygame.Vector2(700, 700)
    CIRCLE_RADIUS = 150
    CIRCLE_WIDTH = 0
    circle_1 = pygame.draw.circle(screen, "yellow", CIRCLE_CENTER, CIRCLE_RADIUS, CIRCLE_WIDTH)
    circle_2 = pygame.draw.circle(screen, "yellow", (300, 200), 100, 5)



    pygame.display.flip()
    clock.tick(FRAMES_PER_SECOND)


pygame.quit()