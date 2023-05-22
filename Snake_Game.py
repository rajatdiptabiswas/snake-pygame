"""
Snake Eater
Made with PyGame
"""
import math

import pygame, sys, time, random, numpy as np

# # Checks for errors encountered
#     check_errors = pygame.init()
#     # pygame.init() example output -> (6, 0)
#     # second number in tuple gives number of errors
#     if check_errors[1] > 0:
#         print(f'[!] Had {check_errors[1]} errors when initialising game, exiting...')
#         sys.exit(-1)
#     else:
#         print('[+] Game successfully initialised')

# Difficulty settings
# Easy      ->  10
# Medium    ->  25
# Hard      ->  40
# Harder    ->  60
# Impossible->  120
difficulty = 80

# Window size
frame_size_x = 200
frame_size_y = 200

# Seina parameetrid
wall_length = 10  # Seina pikkus - 10 ühiku võrra suureneb

# Ruudu ühik
block_size = 10

# Colors (R, G, B)
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

# Initialise game window
pygame.display.set_caption('Snake Eater') # Pealkiri
game_window = pygame.display.set_mode((frame_size_x, frame_size_y)) # Aken
fps_controller = pygame.time.Clock() # Akna kaadrisagedus

def naita_ussi(snake_body, game_window):
    for body_pos in snake_body:
        # Snake body
        # .draw.rect(play_surface, color, xy-coordinate)
        # xy-coordinate -> .Rect(x, y, size_x, size_y)
        pygame.draw.rect(game_window, green, pygame.Rect(body_pos[0], body_pos[1], 10, 10))

def naita_toitu(food_pos, game_window):
    # Snake food
    pygame.draw.rect(game_window, white, pygame.Rect(food_pos[0], food_pos[1], 10, 10))

def alustamispositsioonid():
    global block_size, wall_length
    # Game variables
    snake_pos = [30, 30]
    snake_body = [[30, 30], [30-10, 30], [30-(2*10), 30]]

    food_pos = [random.randrange(1, (frame_size_x//10)) * 10, random.randrange(1, (frame_size_y//10)) * 10]
    # food_spawn = True

    # direction = 'RIGHT'
    # change_to = direction

    score = 0

    #wall_body = koosta_sein(snake_body)

    return snake_pos, snake_body, food_pos, score #direction#, wall_body

def kaugus_toidust(food_pos, snake_pos):
    return np.linalg.norm(np.array(food_pos) - np.array(snake_pos))

def koosta_sein(snake_body):
    global frame_size_x, frame_size_y, wall_length
    # Seina lisamine
    wall_body = []
    wall_in_snake = True

    while wall_in_snake:
        still_wall_in_snake = False
        wall_pos = random.randrange(50, frame_size_x - (wall_length * 10) + 1, 10)
        for pos in snake_body:
            if wall_pos == pos[0] or wall_pos == pos[1]:
                still_wall_in_snake = True
                break
        if not still_wall_in_snake:
            wall_in_snake = False

    wall_direction = random.choice(["row", "column"])
    if wall_direction == "row":
        for i in range(wall_length):
            value = i * block_size
            wall = [wall_pos + value, wall_pos]
            wall_body.append(wall)
    else:
        for i in range(wall_length):
            value = i * block_size
            wall = [wall_pos, wall_pos + value]
            wall_body.append(wall)

    return wall_body

def ussi_funktsioonid(snake_pos, snake_body, food_pos, score, direction):
    # Moving the snake
    if direction == 'UP':
        snake_pos[1] -= 10
    if direction == 'DOWN':
        snake_pos[1] += 10
    if direction == 'LEFT':
        snake_pos[0] -= 10
    if direction == 'RIGHT':
        snake_pos[0] += 10

    # Snake body growing mechanism
    # Toidu kättesaamine
    if snake_pos == food_pos:
        food_pos, score = toidu_puutumine(food_pos, score)
        # food_spawn = False
    else:
        snake_body.insert(0, list(snake_pos))
        snake_body.pop()

    return snake_body, food_pos, score

def toidu_puutumine(food_pos, score):
    food_pos = [random.randrange(1, (frame_size_x//10)) * 10, random.randrange(1, (frame_size_y//10)) * 10]
    score += 1
    return food_pos, score

def aare_puutumine(snake_pos):
    global frame_size_x, frame_size_y
    # Getting out of bounds
    if snake_pos[0] < 0 or snake_pos[0] > frame_size_x - 10:
        return True
    if snake_pos[1] < 0 or snake_pos[1] > frame_size_y - 10:
        return True
    return False

def enda_puutumine(snake_pos, snake_body):
    # Touching the snake body
    if snake_pos in snake_body[1:]: # [1:] - alates peast
        return True
    return False

def seina_puutumine(snake_pos, wall_body):
    # Seina vastu
    for block in wall_body:
        if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
            return True
    return False

def suund_blokeeritud(snake_body, hetke_suuna_siht):
    print(snake_body[0], hetke_suuna_siht)
    jargmine_samm = snake_body[0] + hetke_suuna_siht
    snake_pos = snake_body[0]
    if aare_puutumine(jargmine_samm) or enda_puutumine(jargmine_samm.tolist(), snake_body): # TODO: Seina puutumine
        return True
    else:
        return False

def blokeeritud_suunad(snake_body):
    hetke_suuna_siht = np.array(snake_body[0]) - np.array(snake_body[1])
    vasak_suuna_siht = np.array([hetke_suuna_siht[1], -hetke_suuna_siht[0]])
    parem_suuna_siht = np.array([-hetke_suuna_siht[1], hetke_suuna_siht[0]])

    on_ees_blokk = suund_blokeeritud(snake_body, hetke_suuna_siht)
    on_vasakul_blokk = suund_blokeeritud(snake_body, vasak_suuna_siht)
    on_paremal_blokk = suund_blokeeritud(snake_body, parem_suuna_siht)

    return hetke_suuna_siht, on_ees_blokk, on_vasakul_blokk, on_paremal_blokk


def genereeri_liikumissuund(uus_suund):
    liikumissuund = "LEFT"
    if uus_suund.tolist() == [10, 0]:
        liikumissuund = "RIGHT"
    elif uus_suund.tolist() == [-10, 0]:
        liikumissuund = "LEFT"
    elif uus_suund.tolist() == [0, 10]:
        liikumissuund = "DOWN"
    else:
        liikumissuund = "UP"

    return liikumissuund

def get_nurk_toiduga(snake_body, food_pos):
    toidu_suuna_siht = np.array(food_pos) - np.array(snake_body[0])
    ussi_suuna_siht = np.array(snake_body[0]) - np.array(snake_body[1])

    norm_toidu_suuna_siht = np.linalg.norm(toidu_suuna_siht)
    norm_ussi_suuna_siht = np.linalg.norm(ussi_suuna_siht)
    if norm_toidu_suuna_siht == 0:
        norm_toidu_suuna_siht = 10
    if norm_ussi_suuna_siht == 0:
        norm_ussi_suuna_siht = 10

    toidu_suuna_siht_normaliseeritud = toidu_suuna_siht / norm_toidu_suuna_siht
    ussi_suuna_siht_normaliseeritud = ussi_suuna_siht / norm_ussi_suuna_siht
    nurk = math.atan2(
        toidu_suuna_siht_normaliseeritud[1] * ussi_suuna_siht_normaliseeritud[0] -
        toidu_suuna_siht_normaliseeritud[0] * ussi_suuna_siht_normaliseeritud[1],
        toidu_suuna_siht_normaliseeritud[1] * ussi_suuna_siht_normaliseeritud[1] +
        toidu_suuna_siht_normaliseeritud[0] * ussi_suuna_siht_normaliseeritud[0] /
        math.pi
    )
    return nurk, ussi_suuna_siht, toidu_suuna_siht_normaliseeritud, ussi_suuna_siht_normaliseeritud

def suuna_siht(snake_body, nurk_toiduga, suund):
    hetke_suuna_siht = np.array(snake_body[0]) - np.array(snake_body[1])
    vasak_suuna_siht = np.array([hetke_suuna_siht[1], -hetke_suuna_siht[0]])
    parem_suuna_siht = np.array([-hetke_suuna_siht[1], hetke_suuna_siht[0]])

    uus_suund = hetke_suuna_siht

    if suund == -1:
        uus_suund = vasak_suuna_siht
    if suund == 1:
        uus_suund = parem_suuna_siht

    liikumissuund = genereeri_liikumissuund(uus_suund)

    return suund, liikumissuund

def genereeri_suvaline_siht(snake_body, nurk_toiduga):
    suund = 0
    if nurk_toiduga > 0:
        suund = 1
    elif nurk_toiduga < 0:
        suund = -1
    else:
        suund = 0

    return suuna_siht(snake_body, nurk_toiduga, suund)

def mangi(snake_pos, snake_body, food_pos, liikumissuund, score, game_window, fps_controller): # TODO: SEIN
    crashed = False
    while crashed is not True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True
        game_window.fill(black)

        naita_toitu(food_pos, game_window)
        naita_ussi(snake_body, game_window)

        snake_body, food_pos, score = ussi_funktsioonid(snake_pos, snake_body, food_pos, score, liikumissuund)
        pygame.display.set_caption("SCORE: " + str(score))
        pygame.display.update()
        fps_controller.tick(difficulty)

        return snake_body, food_pos, score


# Score
# def show_score(choice, color, font, size, score):
#     score_font = pygame.font.SysFont(font, size)
#     score_surface = score_font.render(str(score), True, color)
#     score_rect = score_surface.get_rect()
#     if choice == 1:
#         score_rect.midtop = (frame_size_x/4, 5)
#     else:
#         score_rect.midtop = (frame_size_x/2, frame_size_y/1.25)
#     game_window.blit(score_surface, score_rect)
#     # pygame.display.flip()