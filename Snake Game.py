"""
Snake Eater
Made with PyGame
"""

import pygame, sys, time, random


# Difficulty settings
# Easy      ->  10
# Medium    ->  25
# Hard      ->  40
# Harder    ->  60
# Impossible->  120
difficulty = 25

# Window size
frame_size_x = 720
frame_size_y = 480

# Checks for errors encountered
check_errors = pygame.init()
# pygame.init() example output -> (6, 0)
# second number in tuple gives number of errors
if check_errors[1] > 0:
    print(f"[!] Had {check_errors[1]} errors when initialising game, exiting...")
    sys.exit(-1)
else:
    print("[+] Game successfully initialised")


# Initialise game window
pygame.display.set_caption("Snake Eater")
game_window = pygame.display.set_mode((frame_size_x, frame_size_y))


# Colors (R, G, B)
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)


# a list that stors all buttons
buttons = []

# FPS (frames per second) controller
fps_controller = pygame.time.Clock()


# Game variables
snake_pos = [100, 50]
snake_body = [[100, 50], [100 - 10, 50], [100 - (2 * 10), 50]]

food_pos = [
    random.randrange(1, (frame_size_x // 10)) * 10,
    random.randrange(1, (frame_size_y // 10)) * 10,
]
food_spawn = True

direction = "RIGHT"
change_to = direction

score = 0


class Button:
    """
    propertes:
    buttons: a List of all buttons
    react: the button hitbox (a pygame.rect)
    coolDown: button coldown to stop instantanus clicking
    func: function given to the button to exacute
    window: which menu window the button is in
    name: the text that is displayed on the button
    mouse_on: boolen that shows if the mous is on the button
    show: shows the button

    methods:
    render(self) -> None: Renders the button whith text placed on the button
    update(self) -> None: checks if the button is clicked
    """

    def __init__(self, x, y, width, height, window, func, name="Button") -> None:
        buttons.append(self)
        self.react = pygame.Rect(x, y, width, height)
        self.coolDown = 0
        self.func = func
        self.window = window
        self.name = name
        self.mouse_on = False
        self.show = False

    def render(self) -> None:
        if self.show:
            textRect = pygame.Rect(
                self.react.x + 8,
                self.react.y + 8,
                self.react.width - 16,
                self.react.height - 16,
            )
            font = pygame.font.SysFont("times new roman", 16)
            text = font.render(self.name, True, green)
            if self.mouse_on:
                pygame.draw.rect(game_window, white, self.react, border_radius=10)
                game_window.blit(text, textRect)
            else:
                pygame.draw.rect(game_window, blue, self.react, border_radius=10)
                game_window.blit(text, textRect)

    def update(self) -> None:
        if self.coolDown > 0:
            self.coolDown -= 1
        elif self.show:
            self.mouse_on = False
            if self.react.collidepoint(pygame.mouse.get_pos()):
                self.mouse_on = True
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.coolDown = 15
                    self.func(self)


def show_main_menu():
    """
    shows all buttons that are on the main menu and hides the rest
    """
    for button in buttons:
        button.show = False
        if button.window == "main":
            button.show = True


def start_game(which_button):
    """
    starts the game
    """
    global run_game
    run_game = True

def change_difficulty(which_button):
    """
    changes the difficulty of the game
    """
    global difficulty
    if which_button.name == "easy":
        difficulty = 25
        which_button.name = "medium"
    elif which_button.name == "medium":
        difficulty = 40
        which_button.name = "hard"
    elif which_button.name == "hard":
        difficulty = 60
        which_button.name = "harder"
    elif which_button.name == "harder":
        difficulty = 120
        which_button.name = "impossible"
    elif which_button.name == "impossible":
        difficulty = 120
        which_button.name = "easy"
    print(difficulty)


# Game Over
def game_over():
    my_font = pygame.font.SysFont("times new roman", 90)
    game_over_surface = my_font.render("YOU DIED", True, red)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (frame_size_x / 2, frame_size_y / 4)
    game_window.fill(black)
    game_window.blit(game_over_surface, game_over_rect)
    show_score(0, red, "times", 20)
    pygame.display.flip()
    time.sleep(3)
    pygame.quit()
    sys.exit()


# Score
def show_score(choice, color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render("Score : " + str(score), True, color)
    score_rect = score_surface.get_rect()
    if choice == 1:
        score_rect.midtop = (frame_size_x / 10, 15)
    else:
        score_rect.midtop = (frame_size_x / 2, frame_size_y / 1.25)
    game_window.blit(score_surface, score_rect)
    # pygame.display.flip()


def main():
    global change_to, direction, food_pos, food_spawn, score
    # Main logic
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Whenever a key is pressed down
            elif event.type == pygame.KEYDOWN:
                # W -> Up; S -> Down; A -> Left; D -> Right
                if event.key == pygame.K_UP or event.key == ord("w"):
                    change_to = "UP"
                if event.key == pygame.K_DOWN or event.key == ord("s"):
                    change_to = "DOWN"
                if event.key == pygame.K_LEFT or event.key == ord("a"):
                    change_to = "LEFT"
                if event.key == pygame.K_RIGHT or event.key == ord("d"):
                    change_to = "RIGHT"
                # Esc -> Create event to quit the game
                if event.key == pygame.K_ESCAPE:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))

        # Making sure the snake cannot move in the opposite direction instantaneously
        if change_to == "UP" and direction != "DOWN":
            direction = "UP"
        if change_to == "DOWN" and direction != "UP":
            direction = "DOWN"
        if change_to == "LEFT" and direction != "RIGHT":
            direction = "LEFT"
        if change_to == "RIGHT" and direction != "LEFT":
            direction = "RIGHT"

        # Moving the snake
        if direction == "UP":
            snake_pos[1] -= 10
        if direction == "DOWN":
            snake_pos[1] += 10
        if direction == "LEFT":
            snake_pos[0] -= 10
        if direction == "RIGHT":
            snake_pos[0] += 10

        # Snake body growing mechanism
        snake_body.insert(0, list(snake_pos))
        if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
            score += 1
            food_spawn = False
        else:
            snake_body.pop()

        # Spawning food on the screen
        if not food_spawn:
            food_pos = [
                random.randrange(1, (frame_size_x // 10)) * 10,
                random.randrange(1, (frame_size_y // 10)) * 10,
            ]
        food_spawn = True

        # GFX
        game_window.fill(black)
        for pos in snake_body:
            # Snake body
            # .draw.rect(play_surface, color, xy-coordinate)
            # xy-coordinate -> .Rect(x, y, size_x, size_y)
            pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], 10, 10))

        # Snake food
        pygame.draw.rect(
            game_window, white, pygame.Rect(food_pos[0], food_pos[1], 10, 10)
        )

        # Game Over conditions
        # Getting out of bounds
        if snake_pos[0] < 0 or snake_pos[0] > frame_size_x - 10:
            game_over()
        if snake_pos[1] < 0 or snake_pos[1] > frame_size_y - 10:
            game_over()
        # Touching the snake body
        for block in snake_body[1:]:
            if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
                game_over()

        show_score(1, white, "consolas", 20)
        # Refresh game screen
        pygame.display.update()
        # Refresh rate
        fps_controller.tick(difficulty)


# intoduce buttons here
Button((frame_size_x / 2) - 38, (frame_size_y / 4) -16, 76, 32, "main", start_game, name="play")
Button((frame_size_x / 2) - 38, 2 * (frame_size_y / 4) -16, 76, 32, "main", change_difficulty, name="easy")
show_main_menu()

# turn run_game to true to start the game
run_game = False

while True:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # updates the player (location)

    # fill the screen with a color to wipe away anything from last frame
    game_window.fill(black)

    # RENDER GAME HERE

    for button in buttons:
        button.update()
        button.render()

    # flip() the display to put your work on screen
    pygame.display.flip()
    if run_game:
        main()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    fps_controller.tick(60)
