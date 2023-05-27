"""
Snake Eater
Made with PyGame
"""

import pygame, sys, time, random, argparse


parser = argparse.ArgumentParser(description='Arguments for Snake Game')

parser.add_argument('difficulty', type=int, help='Choose difficulty level -- (Easy: 10) (Medium: 25) (Hard: 40) (Harder: 60) (Impossible: 120)')

args = parser.parse_args()

clock = pygame.time.Clock()

# Difficulty settings
# Easy      ->  10
# Medium    ->  25
# Hard      ->  40
# Harder    ->  60
# Impossible->  120
difficulty = args.difficulty

# Window size
frame_size_x = 720
frame_size_y = 480

# Checks for errors encountered
check_errors = pygame.init()
# pygame.init() example output -> (6, 0)
# second number in tuple gives number of errors
if check_errors[1] > 0:
    print(f'[!] Had {check_errors[1]} errors when initialising game, exiting...')
    sys.exit(-1)
else:
    print('[+] Game successfully initialised')


# Initialise game window
pygame.display.set_caption('Snake Eater')
game_window = pygame.display.set_mode((frame_size_x, frame_size_y))


# Colors (R, G, B)
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)
yellow = pygame.Color(255, 255, 0)


# FPS (frames per second) controller
fps_controller = pygame.time.Clock()


# Game variables
snake_pos = [400, 200]
snake_body = [[0, 0], [0, 0], [0, 0]]

food_pos = [random.randrange(1, (frame_size_x//10)) * 10, random.randrange(1, (frame_size_y//10)) * 10]
food_spawn = True

bullet_pos = [-1, -1]
bullet_spawn = False

snake2_pos = [0, 0]
snake2_body = [[0, 0], [0, 0], [0, 0]]

bullet2_pos = [-1, -1]
bullet2_spawn = False

direction = 'RIGHT'
direction2 = 'RIGHT'
bullet_direction = ''
bullet2_direction = ''
change_to = direction
change_to2 = direction2

snake_1_score = 0
snake_2_score = 0


# Game Over
def game_over():
    my_font = pygame.font.SysFont('times new roman', 90)
    game_over_surface = my_font.render('GAME OVER', True, red)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (frame_size_x/2, frame_size_y/4)
    game_window.fill(black)
    game_window.blit(game_over_surface, game_over_rect)
    show_score(0, red, 'times', 20)
    pygame.display.flip()
    time.sleep(3)
    pygame.quit()
    sys.exit()

def pause():
    loop = 1
    my_font = pygame.font.SysFont('times new roman', 90)
    game_over_surface = my_font.render('PAUSED', True, blue)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (frame_size_x/2, frame_size_y/4)
    game_window.fill(black)
    game_window.blit(game_over_surface, game_over_rect)

    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = 0
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    loop = 0
                if event.key == pygame.K_SPACE:
                    game_window.fill((0, 0, 0))
                    loop = 0
        pygame.display.update()
        # screen.fill((0, 0, 0))
        clock.tick(60)

# Score
def show_score(choice, color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Snake 1 Score : ' + str(snake_1_score), True, color)
    score2_surface = score_font.render('Snake 2 Score : ' + str(snake_2_score), True, color)
    score_rect = score_surface.get_rect()
    score2_rect = score2_surface.get_rect()
    if choice == 1:
        score_rect.midtop = (frame_size_x/7, 15)
        score2_rect.midtop = (frame_size_x/7, 35)
    else:
        score_rect.midtop = (frame_size_x/2, (frame_size_y/1.25) - 20)
        score2_rect.midtop = (frame_size_x/2, frame_size_y/1.25)
    # game_window.blit(score2_surface, score2_rect)
    game_window.blit(score_surface, score_rect)
    game_window.blit(score2_surface, score2_rect)


# Main logic
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Whenever a key is pressed down
        elif event.type == pygame.KEYDOWN:
            # W -> Up; S -> Down; A -> Left; D -> Right
            if event.key == pygame.K_UP:
                change_to = 'UP'
            if event.key == pygame.K_DOWN:
                change_to = 'DOWN'
            if event.key == pygame.K_LEFT:
                change_to = 'LEFT'
            if event.key == pygame.K_RIGHT:
                change_to = 'RIGHT'
            if event.key == ord('w'):
                change_to2 = 'UP'
            if event.key == ord('s'):
                change_to2 = 'DOWN'
            if event.key == ord('a'):
                change_to2 = 'LEFT'
            if event.key == ord('d'):
                change_to2 = 'RIGHT'
            # Esc -> Create event to quit the game
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))

            if event.key == pygame.K_p:
                pause()

            if event.key == ord('/'):
                bullet_spawn = True
                if direction == 'UP':
                    bullet_pos[0] = snake_pos[0]
                    bullet_pos[1] = snake_pos[1] - 20
                    bullet_direction = 'UP'
                if direction == 'DOWN':
                    bullet_pos[0] = snake_pos[0]
                    bullet_pos[1] = snake_pos[1] + 20
                    bullet_direction = 'DOWN'
                if direction == 'LEFT':
                    bullet_pos[0] = snake_pos[0] - 20
                    bullet_pos[1] = snake_pos[1]
                    bullet_direction = 'LEFT'
                if direction == 'RIGHT':
                    bullet_pos[0] = snake_pos[0] + 20
                    bullet_pos[1] = snake_pos[1]    
                    bullet_direction = 'RIGHT'  

            if event.key == pygame.K_SPACE:
                bullet2_spawn = True
                if direction == 'UP':
                    bullet2_pos[0] = snake2_pos[0]
                    bullet2_pos[1] = snake2_pos[1] - 20
                    bullet2_direction = 'UP'
                if direction == 'DOWN':
                    bullet2_pos[0] = snake2_pos[0]
                    bullet2_pos[1] = snake2_pos[1] + 20
                    bullet2_direction = 'DOWN'
                if direction == 'LEFT':
                    bullet2_pos[0] = snake2_pos[0] - 20
                    bullet2_pos[1] = snake2_pos[1]
                    bullet2_direction = 'LEFT'
                if direction == 'RIGHT':
                    bullet2_pos[0] = snake2_pos[0] + 20
                    bullet2_pos[1] = snake2_pos[1]    
                    bullet2_direction = 'RIGHT'  

    # Making sure the snake cannot move in the opposite direction instantaneously
    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    if change_to2 == 'UP' and direction2 != 'DOWN':
        direction2 = 'UP'
    if change_to2 == 'DOWN' and direction2 != 'UP':
        direction2 = 'DOWN'
    if change_to2 == 'LEFT' and direction2 != 'RIGHT':
        direction2 = 'LEFT'
    if change_to2 == 'RIGHT' and direction2 != 'LEFT':
        direction2 = 'RIGHT'

    # Moving the first snake
    if direction == 'UP':
        snake_pos[1] -= 10
    if direction == 'DOWN':
        snake_pos[1] += 10
    if direction == 'LEFT':
        snake_pos[0] -= 10
    if direction == 'RIGHT':
        snake_pos[0] += 10

    # Moving the second snake
    if direction2 == 'UP':
        snake2_pos[1] -= 10
    if direction2 == 'DOWN':
        snake2_pos[1] += 10
    if direction2 == 'LEFT':
        snake2_pos[0] -= 10
    if direction2 == 'RIGHT':
        snake2_pos[0] += 10

    if bullet_direction == 'UP':
        bullet_pos[1] -= 10
    if bullet_direction == 'DOWN':
        bullet_pos[1] += 10
    if bullet_direction == 'LEFT':
        bullet_pos[0] -= 10
    if bullet_direction == 'RIGHT':
        bullet_pos[0] += 10

    if bullet2_direction == 'UP':
        bullet2_pos[1] -= 10
    if bullet2_direction == 'DOWN':
        bullet2_pos[1] += 10
    if bullet2_direction == 'LEFT':
        bullet2_pos[0] -= 10
    if bullet2_direction == 'RIGHT':
        bullet2_pos[0] += 10

    # Snake body growing mechanism
    snake_body.insert(0, list(snake_pos))
    snake2_body.insert(0, list(snake2_pos))

    if (snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]) or (bullet_pos[0] == food_pos[0] and bullet_pos[1] == food_pos[1]):
        snake_1_score += 1
        food_spawn = False
    else:
        snake_body.pop()

    if (snake2_pos[0] == food_pos[0] and snake2_pos[1] == food_pos[1]) or (bullet2_pos[0] == food_pos[0] and bullet2_pos[1] == food_pos[1]):
        snake_2_score += 1
        food_spawn = False
    else:
        snake2_body.pop()

    # Spawning food on the screen
    if not food_spawn:
        food_pos = [random.randrange(1, (frame_size_x//10)) * 10, random.randrange(1, (frame_size_y//10)) * 10]
    food_spawn = True

    # GFX
    game_window.fill(black)
    for pos in snake_body:
        # Snake body
        # .draw.rect(play_surface, color, xy-coordinate)
        # xy-coordinate -> .Rect(x, y, size_x, size_y)
        pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], 10, 10))

    for pos in snake2_body:
        # Snake body
        # .draw.rect(play_surface, color, xy-coordinate)
        # xy-coordinate -> .Rect(x, y, size_x, size_y)
        pygame.draw.rect(game_window, blue, pygame.Rect(pos[0], pos[1], 10, 10))

    # Snake food
    pygame.draw.rect(game_window, white, pygame.Rect(food_pos[0], food_pos[1], 10, 10))
    
    # Draw Bullet
    if bullet_spawn:
        pygame.draw.rect(game_window, red, pygame.Rect(bullet_pos[0], bullet_pos[1], 10, 10))

    if bullet2_spawn:
        pygame.draw.rect(game_window, yellow, pygame.Rect(bullet2_pos[0], bullet2_pos[1], 10, 10))

    # Game Over conditions
    # Getting out of bounds
    if snake_pos[0] < 0 or snake_pos[0] > frame_size_x-10:
        game_over()
    if snake_pos[1] < 0 or snake_pos[1] > frame_size_y-10:
        game_over()

    if snake2_pos[0] < 0 or snake2_pos[0] > frame_size_x-10:
        game_over()
    if snake2_pos[1] < 0 or snake2_pos[1] > frame_size_y-10:
        game_over()        

    if bullet_pos[0] < 0 or bullet_pos[0] > frame_size_x-10:
        bullet_spawn = False
    if bullet_pos[1] < 0 or bullet_pos[1] > frame_size_y-10:
        bullet_spawn = False

    # Touching the snake body
    for block in snake_body[1:]:
        if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
            game_over()

    for block in snake2_body[1:]:
        if snake2_pos[0] == block[0] and snake2_pos[1] == block[1]:
            game_over()
    show_score(1, white, 'consolas', 17)
    # Refresh game screen
    pygame.display.update()
    # Refresh rate
    fps_controller.tick(difficulty)