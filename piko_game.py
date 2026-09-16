
import pygame
import os

pygame.init()

# =========================
# WINDOW
# =========================
WIDTH = 900
HEIGHT = 700

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PIKO - Filipino Traditional Game")

clock = pygame.time.Clock()

# =========================
# COLORS
# =========================
BACKGROUND = (245, 235, 215)
BLACK = (40, 40, 40)
WHITE = (255, 255, 255)
PINK = (255, 105, 160)
DARK_PINK = (220, 70, 125)
YELLOW = (245, 200, 70)
GREEN = (80, 180, 100)
RED = (220, 70, 70)
GRAY = (120, 120, 120)
LIGHT_GRAY = (220, 220, 220)

# =========================
# FONTS
# =========================
title_font = pygame.font.Font(None, 80)
big_font = pygame.font.Font(None, 55)
font = pygame.font.Font(None, 38)
small_font = pygame.font.Font(None, 28)

# =========================
# GAME STATES
# =========================
MENU = "menu"
INSTRUCTIONS = "instructions"
GAME = "game"
PAUSE = "pause"
RESULT = "result"
LEADERBOARD = "leaderboard"

game_state = MENU

# =========================
# PLAYER
# =========================
player_x = 350
player_y = 570

player_radius = 22
player_speed = 5

jumping = False
jump_speed = 0
gravity = 1

# =========================
# GAME VARIABLES
# =========================
score = 0
lives = 3
stage = 1

start_time = 0
final_time = 0

# =========================
# LEADERBOARD
# =========================
leaderboard_file = "leaderboard.txt"

leaderboard = []


def load_leaderboard():

    global leaderboard

    leaderboard = []

    if os.path.exists(leaderboard_file):

        with open(leaderboard_file, "r") as file:

            for line in file:

                parts = line.strip().split(",")

                if len(parts) == 2:

                    name = parts[0]

                    try:
                        score_value = int(parts[1])
                        leaderboard.append((name, score_value))
                    except:
                        pass

    leaderboard.sort(key=lambda x: x[1], reverse=True)


def save_score(name, score_value):

    leaderboard.append((name, score_value))

    leaderboard.sort(key=lambda x: x[1], reverse=True)

    leaderboard[:] = leaderboard[:10]

    with open(leaderboard_file, "w") as file:

        for player_name, player_score in leaderboard:

            file.write(player_name + "," + str(player_score) + "\n")


load_leaderboard()

# =========================
# PIKO BOARD
# =========================

# Each box:
# x, y, width, height

boxes = [
    (300, 100, 100, 60),
    (400, 100, 100, 60),

    (300, 165, 200, 60),

    (300, 230, 100, 60),
    (400, 230, 100, 60),

    (300, 295, 200, 60),

    (300, 360, 100, 60),
    (400, 360, 100, 60),

    (300, 425, 200, 60)
]

# =========================
# RESET GAME
# =========================

def reset_game():

    global player_x
    global player_y
    global score
    global lives
    global stage
    global jumping
    global jump_speed
    global start_time
    global final_time

    player_x = 350
    player_y = 570

    score = 0
    lives = 3
    stage = 1

    jumping = False
    jump_speed = 0

    start_time = pygame.time.get_ticks()

    final_time = 0


# =========================
# BUTTON
# =========================

def draw_button(text, x, y, width, height):

    pygame.draw.rect(
        screen,
        PINK,
        (x, y, width, height),
        border_radius=15
    )

    pygame.draw.rect(
        screen,
        DARK_PINK,
        (x, y, width, height),
        3,
        border_radius=15
    )

    text_surface = font.render(
        text,
        True,
        WHITE
    )

    text_x = x + (width - text_surface.get_width()) // 2
    text_y = y + (height - text_surface.get_height()) // 2

    screen.blit(
        text_surface,
        (text_x, text_y)
    )


# =========================
# DRAW BOARD
# =========================

def draw_board():

    number = 1

    for box in boxes:

        pygame.draw.rect(
            screen,
            WHITE,
            box
        )

        pygame.draw.rect(
            screen,
            BLACK,
            box,
            3
        )

        text = font.render(
            str(number),
            True,
            BLACK
        )

        text_x = box[0] + (box[2] - text.get_width()) // 2
        text_y = box[1] + (box[3] - text.get_height()) // 2

        screen.blit(
            text,
            (text_x, text_y)
        )

        number += 1


# =========================
# CHECK LINE
# =========================

def touching_line():

    # Player circle boundaries

    left = player_x - player_radius
    right = player_x + player_radius
    top = player_y - player_radius
    bottom = player_y + player_radius

    for box in boxes:

        x, y, w, h = box

        # Check if player overlaps the border of a box

        near_left = abs(right - x) < 5
        near_right = abs(left - (x + w)) < 5
        near_top = abs(bottom - y) < 5
        near_bottom = abs(top - (y + h)) < 5

        vertical_overlap = (
            bottom > y and
            top < y + h
        )

        horizontal_overlap = (
            right > x and
            left < x + w
        )

        if (near_left or near_right) and vertical_overlap:
            return True

        if (near_top or near_bottom) and horizontal_overlap:
            return True

    return False


# =========================
# LOSE LIFE
# =========================

def lose_life():

    global lives
    global player_x
    global player_y
    global stage
    global jumping
    global jump_speed

    lives -= 1

    player_x = 350
    player_y = 570

    jumping = False
    jump_speed = 0

    if lives <= 0:

        game_over()


# =========================
# GAME OVER
# =========================

def game_over():

    global game_state
    global final_time

    final_time = (
        pygame.time.get_ticks() - start_time
    ) / 1000

    game_state = RESULT


# =========================
# WIN
# =========================

def win_game():

    global game_state
    global final_time
    global score

    final_time = (
        pygame.time.get_ticks() - start_time
    ) / 1000

    # Faster time = higher score

    time_bonus = max(
        0,
        int(1000 - final_time * 10)
    )

    score += time_bonus

    game_state = RESULT


# =========================
# PLAYER NAME
# =========================

player_name = ""
typing_name = False


# =========================
# MAIN LOOP
# =========================

running = True

while running:

    clock.tick(60)

    # =========================
    # EVENTS
    # =========================

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False

        if event.type == pygame.KEYDOWN:

            # =========================
            # MENU
            # =========================

            if game_state == MENU:

                if event.key == pygame.K_RETURN:

                    reset_game()
                    player_name = ""
                    typing_name = True

                    game_state = GAME

                elif event.key == pygame.K_i:

                    game_state = INSTRUCTIONS

                elif event.key == pygame.K_l:

                    load_leaderboard()
                    game_state = LEADERBOARD

                elif event.key == pygame.K_ESCAPE:

                    running = False

            # =========================
            # INSTRUCTIONS
            # =========================

            elif game_state == INSTRUCTIONS:

                if event.key == pygame.K_RETURN:

                    reset_game()
                    player_name = ""
                    typing_name = True

                    game_state = GAME

                elif event.key == pygame.K_ESCAPE:

                    game_state = MENU

            # =========================
            # LEADERBOARD
            # =========================

            elif game_state == LEADERBOARD:

                if event.key == pygame.K_ESCAPE:

                    game_state = MENU

            # =========================
            # GAME
            # =========================

            elif game_state == GAME:

                # Type player name first

                if typing_name:

                    if event.key == pygame.K_RETURN:

                        if player_name.strip() == "":
                            player_name = "Player"

                        typing_name = False

                    elif event.key == pygame.K_BACKSPACE:

                        player_name = player_name[:-1]

                    else:

                        if len(player_name) < 12:

                            if event.unicode.isprintable():

                                player_name += event.unicode

                else:

                    if event.key == pygame.K_SPACE:

                        if not jumping:

                            jumping = True
                            jump_speed = -15

                    elif event.key == pygame.K_p:

                        game_state = PAUSE

                    elif event.key == pygame.K_ESCAPE:

                        game_state = MENU

            # =========================
            # PAUSE
            # =========================

            elif game_state == PAUSE:

                if event.key == pygame.K_p:

                    game_state = GAME

                elif event.key == pygame.K_r:

                    reset_game()
                    game_state = GAME

                elif event.key == pygame.K_ESCAPE:

                    game_state = MENU

            # =========================
            # RESULT
            # =========================

            elif game_state == RESULT:

                if event.key == pygame.K_r:

                    save_score(
                        player_name,
                        score
                    )

                    reset_game()

                    player_name = ""
                    typing_name = True

                    game_state = GAME

                elif event.key == pygame.K_l:

                    save_score(
                        player_name,
                        score
                    )

                    load_leaderboard()

                    game_state = LEADERBOARD

                elif event.key == pygame.K_ESCAPE:

                    save_score(
                        player_name,
                        score
                    )

                    load_leaderboard()

                    game_state = MENU

    # =========================
    # GAMEPLAY
    # =========================

    if game_state == GAME and not typing_name:

        keys = pygame.key.get_pressed()

        # A = LEFT

        if keys[pygame.K_a]:

            player_x -= player_speed

        # D = RIGHT

        if keys[pygame.K_d]:

            player_x += player_speed

        # Keep player inside play area

        if player_x < 270:

            player_x = 270

        if player_x > 630:

            player_x = 630

        # =========================
        # JUMP
        # =========================

        if jumping:

            player_y += jump_speed

            jump_speed += gravity

            # Successful landing

            if player_y >= 570:

                player_y = 570

                jumping = False
                jump_speed = 0

                # Check if player touched a line

                if touching_line():

                    lose_life()

                else:

                    score += 10

                    stage += 1

                    # Complete all stages

                    if stage > len(boxes):

                        win_game()

    # =========================
    # BACKGROUND
    # =========================

    screen.fill(BACKGROUND)

    # =========================
    # MENU
    # =========================

    if game_state == MENU:

        title = title_font.render(
            "PIKO",
            True,
            DARK_PINK
        )

        subtitle = big_font.render(
            "Filipino Traditional Game",
            True,
            BLACK
        )

        screen.blit(
            title,
            (
                (WIDTH - title.get_width()) // 2,
                90
            )
        )

        screen.blit(
            subtitle,
            (
                (WIDTH - subtitle.get_width()) // 2,
                170
            )
        )

        draw_button(
            "PLAY",
            300,
            270,
            300,
            60
        )

        draw_button(
            "INSTRUCTIONS",
            300,
            345,
            300,
            60
        )

        draw_button(
            "LEADERBOARD",
            300,
            420,
            300,
            60
        )

        info = small_font.render(
            "ENTER = Play    I = Instructions    L = Leaderboard",
            True,
            GRAY
        )

        screen.blit(
            info,
            (
                (WIDTH - info.get_width()) // 2,
                520
            )
        )

        info2 = small_font.render(
            "ESC = Exit",
            True,
            GRAY
        )

        screen.blit(
            info2,
            (
                (WIDTH - info2.get_width()) // 2,
                550
            )
        )

    # =========================
    # INSTRUCTIONS
    # =========================

    elif game_state == INSTRUCTIONS:

        title = big_font.render(
            "HOW TO PLAY",
            True,
            DARK_PINK
        )

        screen.blit(
            title,
            (325, 50)
        )

        instructions = [
            "A / D - Move Left / Right",
            "SPACE - Jump",
            "P - Pause",
            "",
            "Avoid stepping on the Piko lines.",
            "Stepping on a line costs 1 life.",
            "You have 3 lives.",
            "",
            "Complete all stages to win.",
            "The faster you finish, the higher your score!"
        ]

        y = 120

        for instruction in instructions:

            text = small_font.render(
                instruction,
                True,
                BLACK
            )

            screen.blit(
                text,
                (180, y)
            )

            y += 42

        draw_button(
            "PLAY",
            300,
            570,
            300,
            60
        )

    # =========================
    # GAME
    # =========================

    elif game_state == GAME:

        title = big_font.render(
            "PIKO",
            True,
            DARK_PINK
        )

        screen.blit(
            title,
            (40, 20)
        )

        # Timer

        if typing_name:

            elapsed_time = 0

        else:

            elapsed_time = (
                pygame.time.get_ticks() - start_time
            ) / 1000

        timer_text = small_font.render(
            "Time: " + str(round(elapsed_time, 1)) + "s",
            True,
            BLACK
        )

        screen.blit(
            timer_text,
            (650, 25)
        )

        score_text = small_font.render(
            "Score: " + str(score),
            True,
            BLACK
        )

        screen.blit(
            score_text,
            (650, 60)
        )

        lives_text = small_font.render(
            "Lives: " + str(lives),
            True,
            BLACK
        )

        screen.blit(
            lives_text,
            (650, 95)
        )

        stage_text = small_font.render(
            "Stage: " + str(stage),
            True,
            BLACK
        )

        screen.blit(
            stage_text,
            (650, 130)
        )

        # =========================
        # NAME INPUT
        # =========================

        if typing_name:

            name_title = big_font.render(
                "ENTER YOUR NAME",
                True,
                DARK_PINK
            )

            screen.blit(
                name_title,
                (
                    (WIDTH - name_title.get_width()) // 2,
                    210
                )
            )

            name_box = pygame.Rect(
                250,
                290,
                400,
                60
            )

            pygame.draw.rect(
                screen,
                WHITE,
                name_box,
                border_radius=10
            )

            pygame.draw.rect(
                screen,
                DARK_PINK,
                name_box,
                3,
                border_radius=10
            )

            name_text = font.render(
                player_name,
                True,
                BLACK
            )

            screen.blit(
                name_text,
                (
                    name_box.x + 15,
                    name_box.y + 12
                )
            )

            enter_text = small_font.render(
                "Press ENTER when ready",
                True,
                GRAY
            )

            screen.blit(
                enter_text,
                (
                    (WIDTH - enter_text.get_width()) // 2,
                    380
                )
            )

        else:

            # Board

            draw_board()

            # Pamato

            # Current target box

            if stage <= len(boxes):

                target = boxes[stage - 1]

                target_x = target[0] + target[2] // 2
                target_y = target[1] + target[3] // 2

                pygame.draw.circle(
                    screen,
                    YELLOW,
                    (target_x, target_y),
                    12
                )

                pygame.draw.circle(
                    screen,
                    BLACK,
                    (target_x, target_y),
                    12,
                    2
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

            controls = small_font.render(
                "A / D = Move    SPACE = Jump    P = Pause",
                True,
                GRAY
            )

            screen.blit(
                controls,
                (235, 640)
            )

    # =========================
    # PAUSE
    # =========================

    elif game_state == PAUSE:

        title = title_font.render(
            "PAUSED",
            True,
            DARK_PINK
        )

        screen.blit(
            title,
            (
                (WIDTH - title.get_width()) // 2,
                150
            )
        )

        draw_button(
            "RESUME",
            300,
            280,
            300,
            65
        )

        draw_button(
            "RESTART",
            300,
            365,
            300,
            65
        )

        info = small_font.render(
            "P = Resume    R = Restart    ESC = Menu",
            True,
            GRAY
        )

        screen.blit(
            info,
            (
                (WIDTH - info.get_width()) // 2,
                480
            )
        )

    # =========================
    # RESULT
    # =========================

    elif game_state == RESULT:

        if lives > 0:

            title = title_font.render(
                "YOU WIN!",
                True,
                GREEN
            )

        else:

            title = title_font.render(
                "GAME OVER",
                
