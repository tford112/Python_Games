# Final Chapter from Al Sweigart's book

import pygame, random, sys
from pygame.locals import *

windowwidth = 600
windowheight = 600
text_color = (0,0,0)
background_color = (255,255,255)
fps = 40
bad_minsize = 10
bad_maxsize = 40
bad_minspeed = 1
bad_maxspeed = 8
new_bad_rate = 6
baddie_add = 0
player_move_rate = 5

def terminate():
    pygame.quit()
    sys.exit()

def waitPlayerPress():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                return

def playerHitBaddie(player, baddies):
    for b in baddies:
        if player.colliderect(b["rect"]):
            return True
    return False

def drawText(text, font, surface, x, y):
    text_obj = font.render(text, 1, text_color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)

def generateBaddie():
    baddieSize = random.randint(bad_minsize, bad_maxsize)
    ## RECT -> left, top, width, height
    new_baddie = {"rect" : pygame.Rect(random.randint(
            0, windowwidth-baddieSize), 0-baddieSize, baddieSize,
    baddieSize),
                  "speed": random.randint(bad_minspeed, bad_maxspeed),
                  "surface": pygame.transform.scale(baddieImage, (baddieSize, baddieSize))}
    baddies.append(new_baddie)
    return baddies

## Set up pygame, window, and mouse cursor
pygame.init()
mainClock = pygame.time.Clock() ## used to speed or slow down the game with FPS
windowSurface = pygame.display.set_mode((windowwidth, windowheight), 0 , 32)
pygame.display.set_caption("Dodger")
pygame.mouse.set_visible(False)

# Set up fonts
font = pygame.font.SysFont(None, 48)

# Set up images
player = pygame.Rect(400, 200, 24,24)
playerImage = pygame.image.load("ninja.bmp")
playerStretched = pygame.transform.scale(playerImage,(24,24))
baddieImage = pygame.image.load("apple.bmp")


# Show start screen
windowSurface.fill(background_color)
drawText("Dodger", font, windowSurface, windowwidth/3, windowheight/3)
drawText("Press a key to start.", font, windowSurface, windowwidth/3 - 50, windowheight/3 +50)
pygame.display.update()
waitPlayerPress()

topscore = 0
while True:
    # set up start
    baddies = []
    score = 0
    moveLeft = moveRight = moveUp = moveDown = False  # set up the keys
    reverseCheat = slowCheat = False ## the cheats in the game
    difficulty = ""

    while True: # game loop runs while game is playing
        score += 1
        if score == 500: ## increasing difficulty level at this juncture
            difficulty = "Medium"
        elif score == 1000:
            difficulty = "High"
        else:
            difficulty = "Easy"
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            if event.type == KEYDOWN:
                if event.key == K_z:
                    reverseCheat = True
                if event.key == K_x:
                    slowCheat = True
                if event.key == K_LEFT or event.key == K_a:
                    moveRight = False
                    moveLeft = True
                if event.key == K_RIGHT or event.key == K_d:
                    moveLeft = False
                    moveRight = True
                if event.key == K_UP or event.key == K_w:
                    moveDown = False
                    moveUp = True
                if event.key == K_DOWN or event.key == K_s:
                    moveUp = False
                    moveDown = True

            if event.type == KEYUP:
                if event.key == K_z:
                    reverseCheat = False
                if event.key == K_x:
                    slowCheat = False
                if event.key == K_LEFT or event.key == K_a:
                    moveLeft = False
                if event.key == K_RIGHT or event.key == K_d:
                    moveRight = False
                if event.key == K_UP or event.key == K_w:
                    moveUp = False
                if event.key == K_DOWN or event.key == K_s:
                    moveDown = False

            if event.type == MOUSEMOTION:
                # if mouse moves, player moves
                player.centerx = event.pos[0]
                player.centery = event.pos[1]

        ## Add new baddies at the top of screen if needed
        if not reverseCheat and not slowCheat:
            baddie_add += 1

        if baddie_add == new_bad_rate:
            baddie_add = 0
            baddies = generateBaddie()



        if difficulty == "Medium":
            fps = 80
            drawText("Medium Difficulty", font, windowSurface, 10, 50)
        if difficulty == "High":
            new_bad_rate = 2
            drawText("High Difficulty", font, windowSurface, 10, 50)
        if difficulty == "Easy":
            drawText("Easy", font, windowSurface, 10, 50)

        # move player
        if moveLeft and player.left > 0:
            player.left -= player_move_rate
        if moveRight and player.right < windowwidth:
            player.left += player_move_rate
        if moveUp and player.top > 0 :
            player.top -= player_move_rate
        if moveDown and player.top < windowheight:
            player.top += player_move_rate

        # move baddie

        for b in baddies:
            if not reverseCheat and not slowCheat:
                b["rect"].move_ip(0, b["speed"]) # baddie moves down
            elif reverseCheat:
                b["rect"].move_ip(0, -5) # baddie reverse and moves up
            elif slowCheat:
                b["rect"].move_ip(0,1)

        # delete baddies that have fallen past bottom
        for b in baddies[:]:
            if b["rect"].top > windowheight:
                baddies.remove(b)

        # draw game world
        windowSurface.fill(background_color)

        # draw score and top score
        drawText("Score: %s" % (score), font, windowSurface, 10, 0)
        drawText("TopScore: %s" % (topscore), font, windowSurface, 10, 40)

        # draw player rectangle
        windowSurface.blit(playerStretched, player)

        # draw baddie
        for b in baddies:
            windowSurface.blit(b["surface"], b["rect"])

        pygame.display.update()

        # check if baddies hit
        if playerHitBaddie(player, baddies):
            if score > topscore:
                topscore = score # set new top score
            break

        mainClock.tick(fps)
    # stop game and show game over
    drawText("GAME OVER", font, windowSurface, (windowwidth/3), windowheight/3)
    waitPlayerPress()
