import pygame
import random
import math
from pygame import mixer

pygame.init()
# SURFACE
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Invader")
icon = pygame.image.load("spacecraft.png")
pygame.display.set_icon(icon)
background_image = pygame.image.load("background.png")
fired = 0
collision_value = 0
collision_value1 = 0

#Background_sound
mixer.music.load("background.wav")
mixer.music.play(-1)

# PLAYER
playerImage = pygame.image.load("spaceship.png")
playerX = 370
playerY = 450
playerX_change = 0

# enemy spawn
enemyImage = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemy = 6

enemyImage1 = pygame.image.load("alien.png")
enemy1X = random.randint(0,735)
enemy1Y = random.randint(0,200)
enemy1X_change = 1
enemy1Y_change = 50

for i in range(num_of_enemy):
    enemyImage.append(pygame.image.load("enemy.png"))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(0, 150))
    enemyX_change.append(5)
    enemyY_change.append(50)
# BULLET
bulletImage = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 450
bulletX_change = 10
bulletY_change = 20
bullet_state = "ready"
# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
font1 = pygame.font.Font('freesansbold.ttf', 62)
textX = 10
textY = 10

def game_over():
    global num_of_enemy
    gameOver = font1.render("GAME OVER",True,(255,255,255))
    screen.blit(gameOver, (200,200))
    for j in range(num_of_enemy):
        enemyY[j] = 2000
    enemy1Y = 1200

def show_score(x,y):
    score = font.render("Score:" + str(score_value),True,(255,255,255))
    screen.blit(score, (x,y))


def player(x, y):
    screen.blit(playerImage, (x, y))


def enemy(x, y,i):
    screen.blit(enemyImage[i], (x, y))

def enemy1(x, y):
    screen.blit(enemyImage1, (x, y))



def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImage, (x + 16, y + 10))


def is_collision(x1, y1, x2, y2):
    global collision_value
    distance = math.sqrt((math.pow((x1 - x2), 2)) + (math.pow((y1 - y2), 2)))
    if distance < 27:
        collision_value += 1
        return True
    else:
        return False

def is_collision1(x1, y1, x2, y2):
    global collision_value1
    distance = math.sqrt((math.pow((x1 - x2), 2)) + (math.pow((y1 - y2), 2)))
    if distance < 27:
        collision_value1 += 1
        return True
    else:
        return False


running = True
# GAME LOOP
while running:
    screen.fill((0, 0, 0))
    screen.blit(background_image,(0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -10
            if event.key == pygame.K_RIGHT:
                playerX_change = 10
            if event.key == pygame.K_SPACE:
                fired += 1
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                playerX_change = 0

    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    if bulletY <= 0:
        bulletY = 450
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    for i in range(num_of_enemy):
        #GAME_OVER
        if enemyY[i] >= 400:
            for j in range(num_of_enemy):
                enemyY[j] = 2000
            game_over()
            break
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 5
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -5
            enemyY[i] += enemyY_change[i]

        if score_value >= 20:
            enemy1(enemy1X, enemy1Y)
            enemy1X += enemy1X_change
            if enemy1X <= 0:
                enemy1X_change = 2
                enemy1Y += enemy1Y_change
            elif enemy1X >= 736:
                enemy1X_change = -2
                enemy1Y += enemy1Y_change

        collision_value = is_collision1(bulletX, bulletY, enemy1X, enemy1Y)
        if collision_value:
            collision_sound = mixer.Sound("explosion.wav")
            collision_sound.play()
            bulletY = 450
            bullet_state = "ready"
            score_value += 1
            enemy1X = random.randint(0, 736)
            enemy1Y= random.randint(0, 150)

        if enemy1Y >= 400:
            #enemy1Y = 2000
            game_over()
            break



        collision = is_collision(bulletX, bulletY, enemyX[i], enemyY[i])
        if collision:
            collision_sound = mixer.Sound("explosion.wav")
            collision_sound.play()
            bulletY = 450
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(0, 150)
        enemy(enemyX[i], enemyY[i],i)
        #print(fired - (collision_value + collision_value1))
        #if (fired - (collision_value + collision_value1)) >= 10:
           # game_over()
            # break


    player(playerX, playerY)
    show_score(textX,textY)
    pygame.display.update()
