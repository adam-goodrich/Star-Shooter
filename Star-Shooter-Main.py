import pygame
from pygame import mixer
import random
import math

pygame.init()

screen = pygame.display.set_mode((800, 600))

background = pygame.image.load('Desktop/Star-Shooter/space.png')

mixer.music.load("Desktop/Star-Shooter/Background.wav")
mixer.music.play(-1)


bullet = pygame.image.load("Desktop/Star-Shooter/bullet.png")

pygame.display.set_caption("Star-Shooter")
icon = pygame.image.load("Desktop/Star-Shooter/spaceship.png")
pygame.display.set_icon(icon)

player_img = pygame.image.load("Desktop/Star-Shooter/spaceship_1.png")
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

enemy_x_change_increase = 3
enemy_y_change_increase = 10

bullet = pygame.image.load("Desktop/Star-Shooter/bullet.png")
bullet_x = 0
bullet_y = 480
bullet_x_change = 0
bullet_y_change = 10
bullet_state = "ready"

score_value = 0
font = pygame.font.Font("Desktop/Star-Shooter/Stars Fighters Upright.ttf", 20)

text_x = 10
text_y = 10

over = pygame.font.Font("Desktop/Star-Shooter/Stars Fighters Upright.ttf", 32)

def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
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
            player_img = pygame.image.load("Desktop/Star-Shooter/flame.png")
            player(player_x, player_y)
            show_score(275, 325)
            pygame.display.update()
        if dead_counter > 101:
            game_over_text(200, 250)
            player_img = pygame.image.load("Desktop/Star-Shooter/skull.png")
            player(player_x, player_y)
            show_score(275, 325)
            pygame.display.update()

        
    
    if score_value > 75:
        enemy_x_change_increase += .009
        enemy_y_change_increase += .009
    elif score_value > 50:
        enemy_x_change_increase += .005
        enemy_y_change_increase += .005
    elif score_value > 25:
        enemy_x_change_increase += .003
        enemy_y_change_increase += .003
    elif score_value > 8:
        enemy_x_change_increase += .001
        enemy_y_change_increase += .001
    elif num_of_enemies > 8:
        num_of_enemies -= 1
        enemy_x_change_increase -= 1
        enemy_y_change_increase -= 1
    elif score_value > num_of_enemies:
        num_of_enemies += 1
        enemy_x_change_increase += 1
        enemy_y_change_increase += 1
    for i in range(num_of_enemies):
        enemy_img.append(pygame.image.load("Desktop/Star-Shooter/alien.png"))
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
                    bullet_sound = mixer.Sound("Desktop/Star-Shooter/laser.wav")
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
            explosion_sound = mixer.Sound("Desktop/Star-Shooter/explosion.wav")
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
            explosion_sound = mixer.Sound("Desktop/Star-Shooter/explosion.wav")
            explosion_sound.play()
            bullet_y = 480
            bullet_state = "ready"
            score_value += 1
            enemy_img[i] = pygame.image.load("Desktop/Star-Shooter/alien.png")
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



    