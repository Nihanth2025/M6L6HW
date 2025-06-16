import pygame
import random
import math
from pygame import mixer
mixer.init()
pygame.init()
screen = pygame.display.set_mode((800, 500))
pygame.display.set_caption("Space Invader Game")

bg = pygame.image.load("BACKGROUND.png")

mixer.music.load("e..mp3")
mixer.music.set_volume(0.5)
mixer.music.play()

playerimg = pygame.image.load("PLAYER.png")
playerX = 370
playerY = 400
playerX_change = 0


enemyimg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
n_of_enemy = 8

for i in range(n_of_enemy):
    enemyimg.append(pygame.image.load("ENEMY.png"))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(2)
    enemyY_change.append(40)
bulletimg = pygame.image.load("BULLET.png")
bulletX = 0
bulletY = 400
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"


score_value = 0
font = pygame.font.Font(None, 36)
textX = 10
textY = 10

over_font = pygame.font.Font(None, 64)

def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over_text():
    over = over_font.render("GAME OVER", True, (255, 0, 0))
    screen.blit(over, (250, 200))

def player(x, y):
    screen.blit(playerimg, (x, y))

def enemy(x, y, i):
    screen.blit(enemyimg[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletimg, (x + 16, y + 10))

def is_collision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    return distance < 27


running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(bg, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                playerX_change = 0

    
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    
    for i in range(n_of_enemy):
        
        if enemyY[i] > 350:
            for j in range(n_of_enemy):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 2
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -2
            enemyY[i] += enemyY_change[i]

        
        collision = is_collision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            
            bulletY = 400
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    
    if bulletY <= 0:
        bulletY = 400
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)

    pygame.display.update()