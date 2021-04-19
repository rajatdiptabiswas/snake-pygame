#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  2 23:28:23 2021

@author: nassim
"""


import pygame, sys, time, random
from pygame.locals import *


pygame.init() # Initialisation du jeu 

difficulty = 25

# Window size
frame_size_x = 810
frame_size_y = 580


check_errors = pygame.init()

# Initialise game window
pygame.display.set_caption('MoSEF Snake Game')
game_window = pygame.display.set_mode((frame_size_x, frame_size_y))

# Colors (R, G, B)
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

# FPS (frames per second) controller
fps_controller = pygame.time.Clock()


# Textes pour les settings 
font=pygame.font.SysFont('garamond', 36)
lvl1 = font.render("level 1",True,(0,0,0))
lvl2 = font.render("level 2",True,(0,0,0))
lvl3 = font.render("level 3",True,(0,0,0))
lvl4 = font.render("level 4",True,(0,0,0))
choice = font.render("Choose your level... I know you won't click on level 4.",True,(255,255,255))
start_txt = font.render('Start',True,(0,0,0))

font=pygame.font.SysFont('garamond', 46)
title = font.render('Snake Game',True,(255,255,255))

# Importation de l'image Snake 
image = pygame.image.load('/Users/papillon/Desktop/Now-You-Can-Play-The-Nokia-3310s-Iconic-Snake-Game-On-Facebook-Messenger.png').convert()


if check_errors[1] > 0:
    print(f'[!] Had {check_errors[1]} errors when initialising game, exiting...')
    sys.exit(-1)
else:
    print('[+] Game successfully initialised')


# Score
def show_score(choice, color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Score : ' + str(score), True, color)
    score_rect = score_surface.get_rect()
    if choice == 1:
        score_rect.midtop = (frame_size_x/10, 15)
    else:
        score_rect.midtop = (frame_size_x/2, frame_size_y/1.25)
    game_window.blit(score_surface, score_rect)
    pygame.display.flip()



settings = True #On veut que les settings s'affichent

#Boucle de jeu
while True:
    
    # Game variables
    snake_pos = [100, 50]
    snake_body = [[100, 50], [100 - 10, 50], [100 - (2 * 10), 50]]
    food_pos = [random.randrange(1, (frame_size_x // 10)) * 10, random.randrange(1, (frame_size_y // 10)) * 10]
    food_spawn = True
    direction = 'RIGHT'
    change_to = direction
    score = 0

    
    snake_is_alive = True
    
    #Boucle pour jouer plusieurs fois 
    while snake_is_alive:
        
        #Boucle pour afficher les paramètres
        while settings :
        
            game_window.fill(black)
            pygame.draw.rect(game_window, [0,255,0], [50,300,100,100])
            pygame.draw.rect(game_window, [255,230,0], [250,300,100,100])
            pygame.draw.rect(game_window, [255,172,0], [450,300,100,100])
            pygame.draw.rect(game_window, [255,0,0], [650,300,100,100])
            pygame.draw.rect(game_window, [0,100,70], [350,500,70,30])
    
            #pygame.display.update()
            clic1 = pygame.Rect([50,300,100,100])
            clic2 = pygame.Rect([250,300,100,100])
            clic3 = pygame.Rect([450,300,100,100])
            clic4 = pygame.Rect([650,300,100,100])
            start = pygame.Rect([350,500,70,30])
            
            game_window.blit(title,(300,100))
            game_window.blit(choice,(80,200))
            game_window.blit(lvl1, (60, 320))
            game_window.blit(lvl2, (260, 320))
            game_window.blit(lvl3, (460, 320))
            game_window.blit(lvl4, (660, 320))
            game_window.blit(start_txt,(350,500))
            game_window.blit(pygame.transform.scale(image, (150, 75)), (100,100))
            game_window.blit(pygame.transform.scale(image, (150, 75)), (550,100))
            pygame.display.update()
            
            
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        
                        #Réglage des difficultés
                        if clic1.collidepoint(event.pos):
                            difficulty = 10
    
                            pygame.draw.rect(game_window, [0,0,0], [250,300,100,100])
                            pygame.draw.rect(game_window, [0,0,0], [450,300,100,100])
                            pygame.draw.rect(game_window, [0,0,0], [650,300,100,100])
                            pygame.display.update()
                            #settings = False
                        elif clic2.collidepoint(event.pos):
                            difficulty = 25
                            pygame.draw.rect(game_window, [0,0,0], [50,300,100,100])
    
                            pygame.draw.rect(game_window, [0,0,0], [450,300,100,100])
                            pygame.draw.rect(game_window, [0,0,0], [650,300,100,100])
                            pygame.display.update()
                            #settings = False
                        elif clic3.collidepoint(event.pos):
                            difficulty = 50
                            pygame.draw.rect(game_window, [0,0,0], [50,300,100,100])
                            pygame.draw.rect(game_window, [0,0,0], [250,300,100,100])
    
                            pygame.draw.rect(game_window, [0,0,0], [650,300,100,100])
                            pygame.display.update()
                            #settings = False
                        elif clic4.collidepoint(event.pos):
                            difficulty = 100
                            pygame.draw.rect(game_window, [0,0,0], [50,300,100,100])
                            pygame.draw.rect(game_window, [0,0,0], [250,300,100,100])
                            pygame.draw.rect(game_window, [0,0,0], [450,300,100,100])
                            pygame.display.update()
                            #settings = False
                        
                        #Start Game
                        if start.collidepoint(event.pos):
                            settings = False 
                        
                #Quitter le jeu avant de jouer        
                if event.type == pygame.QUIT:                   
                    #sys.exit()
                    settings = False
                    snake_is_alive = False
                    sys.exit()
                    #game = False
                    
                    
                    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    change_to = 'RIGHT'
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    change_to = 'LEFT'
                if event.key == pygame.K_UP or event.key == ord('w'):
                    change_to = 'UP'
                if event.key == pygame.K_DOWN or event.key == ord('s'):
                    change_to = 'DOWN'
                if event.key == pygame.K_ESCAPE:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))
               # if event.key == pygame.K_SPACE:
                #    snake_is_alive = True
                    
        # Making sure the snake cannot move in the opposite direction instantaneously
        if change_to == 'UP' and direction != 'DOWN':
            direction = 'UP'
        if change_to == 'DOWN' and direction != 'UP':
            direction = 'DOWN'
        if change_to == 'LEFT' and direction != 'RIGHT':
            direction = 'LEFT'
        if change_to == 'RIGHT' and direction != 'LEFT':
            direction = 'RIGHT'
    
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
            score += 1
            food_spawn = False
        else:
            snake_body.pop()
    
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
    
        # Snake food
        pygame.draw.rect(game_window, white, pygame.Rect(food_pos[0], food_pos[1], 10, 10))
        pygame.display.flip()

        # Game Over conditions
        # Getting out of bounds
        if snake_pos[0] < 0 or snake_pos[0] > frame_size_x-10:
            snake_is_alive = False
        if snake_pos[1] < 0 or snake_pos[1] > frame_size_y-10:
            snake_is_alive = False
        # Touching the snake body
        for block in snake_body[1:]:
            if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
                snake_is_alive = False
        fps_controller.tick(difficulty) 
        # Refresh game screen
        pygame.display.update()
        
    settings = True            
    my_font = pygame.font.SysFont('times new roman', 90)
    game_over_surface = my_font.render('Game Over', True, red)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (frame_size_x/2, frame_size_y/4)
    game_window.fill(black)
    game_window.blit(game_over_surface, game_over_rect)
    show_score(0, red, 'times', 20)
    pygame.display.flip()
    time.sleep(5)
   
    
   
    #mettre autre part le code ci dessous pour le faire manuellement
    
    # if event.key == pygame.K_SPACE:
                #    snake_is_alive = True
                
                
                
                
                