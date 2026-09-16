import pygame

pygame.init()

# Window
WIDTH = 900
HEIGHT = 700

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PIKO - Filipino Traditional Game")

clock = pygame.time.Clock()

# Colors
BACKGROUND = (245, 235, 215)
BLACK = (40, 40, 40)
WHITE = (255, 255, 255)
PINK = (255, 105, 160)
DARK_PINK = (220, 70, 125)

# Fonts
title_font = pygame.font.Font(None, 70)
font = pygame.font.Font(None, 35)

# Player
player_x = 450
player_y = 610
player_radius = 18
player_speed = 5

# Piko boxes
boxes = {
    1: (405, 580, 90, 55),

    2: (350, 515, 90, 55),
    3: (460, 515, 90, 55),

    4: (405, 450, 90, 55),

    5: (350, 385, 90, 55),
    6: (460, 385, 90, 55),

    7: (405, 320, 90, 55),

    8: (350, 255, 90, 55),
    9: (460, 255, 90, 55),

    10: (405, 190, 90, 55)
}

running = True

while running:

    clock.tick(60)

    # Events
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

    # Keyboard
    keys = pygame.key.get_pressed()

    if keys[pygame.K_a]:
        player_x -= player_speed

    if keys[pygame.K_d]:
        player_x += player_speed

    # Keep player inside screen
    if player_x < 250:
        player_x = 250

    if player_x > 650:
        player_x = 650

    # Background
    screen.fill(BACKGROUND)

    # Title
    title = title_font.render(
        "PIKO",
        True,
        DARK_PINK
    )

    screen.blit(
        title,
        (
            (WIDTH - title.get_width()) // 2,
            30
        )
    )

    # Draw Piko board
    for number in range(1, 11):

        x, y, width, height = boxes[number]

        pygame.draw.rect(
            screen,
            WHITE,
            (x, y, width, height)
        )

        pygame.draw.rect(
            screen,
            BLACK,
            (x, y, width, height),
            3
        )

        number_text = font.render(
            str(number),
            True,
            BLACK
        )

        text_x = x + (
            width - number_text.get_width()
        ) // 2

        text_y = y + (
            height - number_text.get_height()
        ) // 2

        screen.blit(
            number_text,
            (text_x, text_y)
        )

    # Player
    pygame.draw.circle(
        screen,
        PINK,
        (player_x, player_y),
        player_radius
    )

    pygame.draw.circle(
        screen,
        BLACK,
        (player_x, player_y),
        player_radius,
        2
    )

    # Controls
    controls = font.render(
        "A / D = Move",
        True,
        BLACK
    )

    screen.blit(
        controls,
        (
            (WIDTH - controls.get_width()) // 2,
            660
        )
    )

    pygame.display.flip()

pygame.quit()            screen,
            BLACK,
            (x, y, width, height),
            3
        )

        number_text = font.render(
            str(number),
            True,
            BLACK
        )

        text_x = x + (
            width - number_text.get_width()
        ) // 2

        text_y = y + (
            height - number_text.get_height()
        ) // 2

        screen.blit(
            number_text,
            (text_x, text_y)
        )

    # Player
    pygame.draw.circle(
        screen,
        PINK,
        (player_x, player_y),
        player_radius
    )

    pygame.draw.circle(
        screen,
        BLACK,
        (player_x, player_y),
        player_radius,
        2
    )

    # Controls
    controls = font.render(
        "A / D = Move",
        True,
        BLACK
    )

    screen.blit(
        controls,
        (
            (WIDTH - controls.get_width()) // 2,
            660
        )
    )

    pygame.display.flip()

pygame.quit()
