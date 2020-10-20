import pygame                                           #importing package
import random
import math
from pygame import mixer
pygame.init()                                           #initializing pygame

screen = pygame.display.set_mode((800,600))             #create the game screen (width,height)

pygame.display.set_caption("Space Invaders by Writtik") #Setting title
icon = pygame.image.load("ufo.png")                     #Loading Icon
pygame.display.set_icon(icon)                           #Setting Icon

#Backgroung
backimg = pygame.image.load("background.png")           #Game in Background

#Player
img = pygame.image.load("spaceship.png")                #Game in Image
xcor = 370                                              #xcoordinate of Player 
ycor = 480                                              #ycoordinate of Player
position_change = 0   

#Enemy
enemyimg = []
enemyxcor = []        
enemyycor = []
enemyposition_xchange = []             
enemyposition_ychange = []
no_of_enemies = 6
for enemies in range (no_of_enemies):
    enemyimg.append(pygame.image.load("enemy32.png"))                #Game in Image
    enemyxcor.append(random.randint(0, 736))                         #xcoordinate of Enemy
    enemyycor.append(random.randint(50, 130))                        #ycoordinate of Enemy
    enemyposition_xchange.append(4.5)                                #change in x coordinates
    enemyposition_ychange.append(60)                                 #change in y coordinates

#Bullet
bulletimg = pygame.image.load("bullet.png")                 #Game in Image
bulletxcor = 0                                              #xcoordinate of Enemy
bulletycor = 480                                            #ycoordinate of Enemy
bulletposition_xchange = 0                                  #change in x coordinates
bulletposition_ychange = 10                                 #change in y coordinates
bullet_state = "ready"                                      #'Ready'-You cant see the bullet on screen and 'Fire'-The bullet currently moving

#Score
score = 0
font = pygame.font.Font("freesansbold.ttf", 30)
textxcor = 10
textycor = 10

#Game_over
over_font = pygame.font.Font("freesansbold.ttf", 80)

#Music
mixer.music.load("background.mp3")
mixer.music.play(-1)


#functions
def player(x, y):
    screen.blit(img,(x, y))

def enemy(x, y, enemies):
    screen.blit(enemyimg[enemies],(x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletimg,(x+20, y+5))

def collision_happened(enemyxcor, enemyycor, bulletxcor, bulletycor):
    distance = math.sqrt(math.pow(enemyxcor - bulletxcor,2) + math.pow(enemyycor - bulletycor,2))
    if distance < 20: return True
    else: return False

def show_score(x, y):
    score_now = font.render("Score : " + str(score), True, (255,255,255))
    screen.blit(score_now, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER" , True, (255,255,255))
    screen.blit(over_text, (165, 250))


#Game Loop
running = True
while running:
    screen.fill((0,0,0))                                #Setting Whole Screen Colour(filling)
    screen.blit(backimg, (0,0))

    for event in pygame.event.get():                    #checking for keyboard and mouse input
        if event.type == pygame.QUIT:
            running = False
        #KEY MANAGEMENT
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                position_change = -3
            if event.key == pygame.K_RIGHT:
                position_change = 3
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    bulletxcor = xcor
                    fire_bullet(bulletxcor, bulletycor)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                position_change = 0
        #KEY MANAGEMENT
    xcor += position_change                                       #Change in Coordinates
    #Boundary Cond.
    if xcor <= 0:
        xcor = 0
    elif xcor >= 736:
        xcor = 736
    #Boundary Cond.
    player(xcor, ycor)                                             #Player fuction for spaceship img
    #All enemy movement
    for enemies in range (no_of_enemies):
        if enemyycor[enemies] > 430:
            for i in range (no_of_enemies):
                enemyycor[i] = 2000
            game_over_text()
            break

        #Boundary cond.
        enemyxcor[enemies] += enemyposition_xchange[enemies]                             #Change in coordinates
        if enemyxcor[enemies] <= 0:
            enemyposition_xchange[enemies] = 4.5
            enemyycor[enemies] += enemyposition_ychange[enemies]                         #increasing y coordinates
        elif enemyxcor[enemies] >= 768:
            enemyposition_xchange[enemies] = -4.5
            enemyycor[enemies] += enemyposition_ychange[enemies]                         #increasing y coordinates
        #Boundary cond.

        #Collision
        collision = collision_happened(enemyxcor[enemies], enemyycor[enemies], bulletxcor, bulletycor)
        if collision:
            collision_sound = mixer.Sound("explosion.wav")
            collision_sound.play()
            bulletycor = 480
            bullet_state ="ready"
            score += 1
            enemyxcor[enemies] = random.randint(0, 736)
            enemyycor[enemies] = random.randint(50, 130)

        enemy(enemyxcor[enemies], enemyycor[enemies], enemies)                                    #Enemy fuction for enemy img

    #Bullet Movement
    if bullet_state == "fire":
        fire_bullet(bulletxcor, bulletycor)
        bulletycor -= bulletposition_ychange

    if bulletycor <= 0:
        bulletycor = 480
        bullet_state = "ready"

    show_score(textxcor, textycor)

    pygame.display.update() 