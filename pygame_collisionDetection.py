''' following code is typed from Al Sweigart's book as practice'''
import pygame, sys, random, os
from pygame.locals import *


# Set up pygame
pygame.init()
## function to make program run same speed on all computers
mainClock = pygame.time.Clock()

# Set up window
windowWidth = 400
windowHeight = 400
windowSurface = pygame.display.set_mode((windowWidth, windowHeight),
0, 32)
pygame.display.set_caption("Collision Detection")

# Set up colors
black =(0,0,0)
green = (0,255,0)
white = (255,255,255)

# Set up player and food data structures
foodCounter = 0
newFood = 40
foodSize = 20
## player location
player = pygame.Rect(300,100,50,50)
## 20 food square locations
foods = []
for i in range(20):
    foods.append(pygame.Rect(random.randint(0, windowWidth-foodSize),
    random.randint(0, windowHeight-foodSize), foodSize, foodSize))

# Set up Movement Variables -- keyboard
moveLeft = False
moveRight = False
moveUp = False
moveDown = False
movespeed = 6
''' Event Handling
1. "pygame module can generate events in response to user input from mouse/keyboard"
2. pygame.event.get() retrieves the following events
3. quit, keydown, keyup, mousemotion, mousebuttondown, mousebuttonup
'''

# Handling Keydown Event
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            # change keyboard variables when a key is pressed
            ## can be the arrow keys or the WASD
            if event.key == K_LEFT or event.key == K_a:
                moveRight = False
                moveLeft = True
            elif event.key == K_RIGHT or event.key == K_d:
                moveLeft = False
                moveRight = True
            elif event.key == K_UP or event.key == K_w:
                moveDown = False
                moveUp = True
            elif event.key == K_DOWN or event.key == K_s:
                moveUp = False
                moveDown = True
            elif event.key == K_1:
                print("this does work!")

        # Handling KeyUp Event -- closing out the event
        if event.type == KEYUP:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.key == K_RIGHT or event.key == K_d:
                moveRight = False
            elif event.key == K_LEFT or event.key == K_a:
                moveLeft = False
            elif event.key == K_UP or event.key == K_w:
                moveUp = False
            elif event.key == K_DOWN or event.key == K_s:
                moveUp = False
            ## Teleportation
            elif event.key == K_x:
                player.top = random.randint(0, windowHeight-player.height)
                player.left = random.randint(0, windowWidth - player.width)

    ## Adding new Food
        if event.type == MOUSEBUTTONUP:
            foods.append(pygame.Rect(event.pos[0], event.pos[1], foodSize, foodSize))

    ## Draw white background
    windowSurface.fill(white)

    ## Moving player
    if moveDown and player.bottom < windowHeight:
        player.top += movespeed
    elif moveUp and player.top > 0:
        player.top -= movespeed
    elif moveLeft and player.left > 0:
        player.left -= movespeed
    elif moveRight and player.right < windowWidth:
        player.left += movespeed
    # draw player
    pygame.draw.rect(windowSurface, black, player)

## Collision Detection
    ### foods[:] is a copy of the foods list
    ## this is important as if we are removing at the same time of iterating the actual
    ## food list, it would be confusing and ill-advised
    for food in foods[:]:
        if player.colliderect(food):
            foods.remove(food)
    ## Draw food
    for i in range(len(foods)):
        pygame.draw.rect(windowSurface,green, foods[i])
    ## draw window on screen
    pygame.display.update()
    mainClock.tick(40)
