"""
Snake Eater
Made with PyGame
"""

import pygame, sys, time, random
from geneetiline_algoritm import Individuaal

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


# FPS (frames per second) controller
fps_controller = pygame.time.Clock()


# Game variables
snake_pos = [30, 30]
snake_body = [[30, 30], [30-10, 30], [30-(2*10), 30]]

food_pos = [random.randrange(1, (frame_size_x//10)) * 10, random.randrange(1, (frame_size_y//10)) * 10]
food_spawn = True

direction = 'RIGHT'
change_to = direction

score = 0

# Seina lisamine

block_size = 10
wall_length = 10 # Seina pikkus - 10 ühiku võrra suureneb
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
        value = i*block_size
        wall = [wall_pos+value, wall_pos]
        wall_body.append(wall)
else:
    for i in range(wall_length):
        value = i*block_size
        wall = [wall_pos, wall_pos+value]
        wall_body.append(wall)

# Populatsioon

population_size = 50  # Define the size of the population
population = []  # Initialize an empty list to hold the individuals

# Create the initial population
for _ in range(population_size):
    indiviid = Individuaal(["UP", "DOWN", "LEFT", "RIGHT"],
                           mutation_rate=0.2)  # Create a new instance of the Individual class
    population.append(indiviid)  # Add the individual to the population list

mang_labi = False


# Game Over
# def game_over():
#     my_font = pygame.font.SysFont('times new roman', 26)
#     game_over_surface = my_font.render('YOU DIED', True, red)
#     game_over_rect = game_over_surface.get_rect()
#     game_over_rect.midtop = (frame_size_x/2, frame_size_y/4)
#     game_window.fill(black)
#     game_window.blit(game_over_surface, game_over_rect)
#     show_score(0, red, 'times', 20)
#     pygame.display.flip()
#     time.sleep(3)
#     pygame.quit()
#     sys.exit()

# Score
def show_score(choice, color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render(str(score), True, color)
    score_rect = score_surface.get_rect()
    if choice == 1:
        score_rect.midtop = (frame_size_x/4, 5)
    else:
        score_rect.midtop = (frame_size_x/2, frame_size_y/1.25)
    game_window.blit(score_surface, score_rect)
    # pygame.display.flip()

def madu_algus():
    global snake_pos, snake_body, food_pos, food_spawn, direction, change_to, score
    snake_pos = [30, 30]
    snake_body = [[30, 30], [30 - 10, 30], [30 - (2 * 10), 30]]
    food_pos = [random.randrange(1, (frame_size_x // 10)) * 10, random.randrange(1, (frame_size_y // 10)) * 10]
    food_spawn = True
    direction = 'RIGHT'
    change_to = direction
    score = 0

def uus_populatsioon():
    global population
    # Sort the population based on fitness in descending order
    population.sort(key=lambda x: x.fitness, reverse=True)

    # Select the best individuals for reproduction (you can adjust the selection strategy according to your needs)
    parents = population[:int(0.2 * population_size)]

    # Reproduction: crossover and mutation
    offspring = []

    while len(offspring) < population_size:
        parent1 = random.choice(parents)
        parent2 = random.choice(parents)
        child = parent1.crossover(parent2)
        child.mutate()
        offspring.append(child)

    # Replace the old population with the new offspring
    population = offspring

def alusta():
    # Main logic
    global score, mang_labi, change_to, direction, food_pos, food_spawn
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Making sure the snake cannot move in the opposite direction instantaneously
        if change_to == 'UP' and direction != 'DOWN':
            direction = 'UP'
        if change_to == 'DOWN' and direction != 'UP':
            direction = 'DOWN'
        if change_to == 'LEFT' and direction != 'RIGHT':
            direction = 'LEFT'
        if change_to == 'RIGHT' and direction != 'LEFT':
            direction = 'RIGHT'

        # Calculate the Euclidean distance between snake head and food
        distance = ((snake_pos[0] - food_pos[0]) ** 2 + (snake_pos[1] - food_pos[1]) ** 2) ** 0.5

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
        snake_body.insert(0, list(snake_pos))
        if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
            score += 1 + (100 - distance)
            food_spawn = False
        else:
            snake_body.pop()

        # Spawning food on the screen
        # Ei lisa sööki seina sisse
        while not food_spawn:
            still_in_wall = False
            food_pos = [random.randrange(1, (frame_size_x // 10)) * 10, random.randrange(1, (frame_size_y // 10)) * 10]
            for pos in wall_body:
                if food_pos[0] == pos[0] and food_pos[1] == pos[1]:
                    still_in_wall = True
                    break
            if not still_in_wall:
                food_spawn = True

        # GFX
        game_window.fill(black)
        for pos in snake_body:
            # Snake body
            # .draw.rect(play_surface, color, xy-coordinate)
            # xy-coordinate -> .Rect(x, y, size_x, size_y)
            pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], 10, 10))

        # Snake food
        pygame.draw.rect(game_window, white, pygame.Rect(food_pos[0], food_pos[1], 10, 10))

        # Sein
        for pos in wall_body:
            pygame.draw.rect(game_window, red, pygame.Rect(pos[0], pos[1], 10, 10))

        ### Game Over conditions ###

        # Seina vastu
        for block in wall_body:
            if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
                mang_labi = True

        # Getting out of bounds
        if snake_pos[0] < 0 or snake_pos[0] > frame_size_x-10:
            mang_labi = True
            score -= 10
        if snake_pos[1] < 0 or snake_pos[1] > frame_size_y-10:
            mang_labi = True
            score -= 10
        # Touching the snake body
        for block in snake_body[1:]:
            if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
                mang_labi = True
                score -= 10


        if direction == 'UP' and snake_pos[1] > food_pos[1]:
            score += 7
        if direction == 'UP' and snake_pos[1] < food_pos[1]:
            score -= 5
        if direction == 'DOWN' and snake_pos[1] < food_pos[1]:
            score += 7
        if direction == 'DOWN' and snake_pos[1] > food_pos[1]:
            score -= 5
        if direction == 'LEFT' and snake_pos[0] > food_pos[0]:
            score += 7
        if direction == 'LEFT' and snake_pos[0] < food_pos[0]:
            score -= 5
        if direction == 'RIGHT' and snake_pos[0] < food_pos[0]:
            score += 7
        if direction == 'RIGHT' and snake_pos[0] > food_pos[0]:
            score -= 5

        show_score(1, white, 'consolas', 20)
        change_to = population[0].get_next_move(direction)

        if mang_labi:
            for indiviid in population:
                indiviid.evaluate_fitness(score)
            uus_populatsioon()
            madu_algus()
            mang_labi = False
        # Refresh game screen
        pygame.display.update()
        # Refresh rate
        fps_controller.tick(difficulty)

alusta()