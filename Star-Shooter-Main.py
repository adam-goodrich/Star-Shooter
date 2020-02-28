import pygame
from pygame import mixer
import random
import math

pygame.init()

screen = pygame.display.set_mode((800, 600))

background = pygame.image.load('space.png')

mixer.music.load("Background.wav")
mixer.music.play(-1)


bullet = pygame.image.load("bullet.png")

pygame.display.set_caption("Star-Shooter")
icon = pygame.image.load("spaceship.png")
pygame.display.set_icon(icon)

player_img = pygame.image.load("spaceship_1.png")
player_x = 370
player_y = 480
player_x_change = 0
player_y_change = 0

enemy_img = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []
num_of_enemies = 2

enemy_x_change_increase = 1
enemy_y_change_increase = 6

bullet = pygame.image.load("bullet.png")
bullet_x = 0
bullet_y = 480
bullet_x_change = 0
bullet_y_change = 10
bullet_state = "ready"

score_value = 0
font = pygame.font.Font("Stars Fighters Upright.ttf", 16)

text_x = 10
text_y = 10

over = pygame.font.Font("Stars Fighters Upright.ttf", 32)

def show_score(x, y):
    score = font.render("Points: " + str(score_value * points), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over_text(x, y):
    over_text = over.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (x, y))

def player(x, y):
    screen.blit(player_img, (x, y))

def enemy(x, y, i):
    screen.blit(enemy_img[i], (x, y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet, (x + 16, y + 10))

def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt((math.pow(bullet_x - enemy_x,2)) + (math.pow(bullet_y - enemy_y, 2)))
    if distance < 32:
        return True
    else:
        return False
points = 10
dead = False
running = True
while running:
    screen.blit(background, (0,0))
    dead_counter = 0
    while dead:
        dead_counter += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                dead = False
                running = False
        if dead_counter < 100:
            game_over_text(200, 250)
            player_img = pygame.image.load("flame.png")
            player(player_x, player_y)
            show_score(275, 325)
            pygame.display.update()
        if dead_counter > 101:
            game_over_text(200, 250)
            player_img = pygame.image.load("skull.png")
            player(player_x, player_y)
            show_score(275, 325)
            pygame.display.update()

        
    
    if score_value > 100:
        enemy_y_change_increase += .05
        points = 500
    elif score_value > 75:
        enemy_y_change_increase += .012
        points = 200
    elif score_value > 50:
        enemy_y_change_increase += .008
        points = 150
    elif score_value > 25:
        enemy_x_change_increase += .0003
        enemy_y_change_increase += .005
        points = 100
    elif score_value > 5:
        enemy_x_change_increase += .0001
        enemy_y_change_increase += .003
        points = 50
    elif num_of_enemies > 5:
        num_of_enemies -= 1
    elif score_value > num_of_enemies:
        num_of_enemies += 1
        
    for i in range(num_of_enemies):
        enemy_img.append(pygame.image.load("alien.png"))
        enemy_x.append(random.randint(0, 735))
        enemy_y.append(0)
        enemy_x_change.append(enemy_x_change_increase)
        enemy_y_change.append(enemy_y_change_increase)
    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 
    
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -5
            if event.key == pygame.K_RIGHT:
                player_x_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    bullet_x = player_x
                    fire_bullet(bullet_x, bullet_y)

                    
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                player_y_change = 0
        
        

    player_x += player_x_change

    if player_x <= 0:
        player_x = 0
    elif player_x >= 736:
        player_x = 736

    for i in range(num_of_enemies):
     
        if enemy_y[i] > 440:
            explosion_sound = mixer.Sound("explosion.wav")
            explosion_sound.play()
            dead = True
            
        enemy_x[i] += enemy_x_change[i]

        if enemy_x[i] <= 0:
            enemy_x_change[i] = enemy_x_change_increase
            enemy_y[i] += enemy_y_change[i]
        elif enemy_x[i] >= 736:
            enemy_x_change[i] = -(enemy_x_change_increase)
            enemy_y[i] += enemy_y_change[i]

        collision = is_collision(enemy_x[i], enemy_y[i], bullet_x, bullet_y)
        if collision:
            explosion_sound = mixer.Sound("explosion.wav")
            explosion_sound.play()
            bullet_y = 480
            bullet_state = "ready"
            score_value += 1
            enemy_img[i] = pygame.image.load("alien.png")
            enemy_x[i] = random.randint(0, 735)
            enemy_y[i] = 0
            

        enemy(enemy_x[i], enemy_y[i], i)

        for i in range(num_of_enemies):
     
            if enemy_y[i] > 440:
                explosion_sound = mixer.Sound("explosion.wav")
                explosion_sound.play()
                dead = True
                
            enemy_x[i] += enemy_x_change[i]

            if enemy_x[i] <= 0:
                enemy_x_change[i] = enemy_x_change_increase
                enemy_y[i] += enemy_y_change_increase
            elif enemy_x[i] >= 736:
                enemy_x_change[i] = -(enemy_x_change_increase)
                enemy_y[i] += enemy_y_change_increase

            collision = is_collision(enemy_x[i], enemy_y[i], bullet_x, bullet_y)
            if collision:
                explosion_sound = mixer.Sound("explosion.wav")
                explosion_sound.play()
                bullet_y = 480
                bullet_state = "ready"
                score_value += 1
                enemy_img[i] = pygame.image.load("alien.png")
                enemy_x[i] = random.randint(0, 735)
                enemy_y[i] = 0
                

            enemy(enemy_x[i], enemy_y[i], i)
        

    
    if bullet_y <= 0:
        bullet_y = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_y_change


    player(player_x, player_y)
    show_score(text_x, text_y)
    pygame.display.update()



    