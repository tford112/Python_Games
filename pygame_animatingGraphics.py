''' again commands typed from Al Sweigarts book '''

import pygame, sys, time
from pygame.locals import *

pygame.init()

windowWidth = 400
windowHeight = 400
windowSurface = pygame.display.set_mode((windowWidth, windowHeight),0, 32)

pygame.display.set_caption("Bouncing Box Animation")

# Set up Direction and color variables
downleft = "downleft"
downright = "downright"
upleft = "upleft"
upright = "upright"

white = (255,255,255)
red = (255, 0 , 0)
green = (0, 255, 0)
blue = (0, 0, 255)
## tells program how many pixels each box should move on each iteration of game loop
movespeed = 4


# Box Data Structure
## b1 x coord = 300, ycoord = 80, width of 50 pixels, height of 100
b1 = {"rect": pygame.Rect(300,80, 50, 100),"color" : red, "dir": upright}
b2 = {"rect": pygame.Rect(200, 70, 20, 70), "color": green, "dir": upleft}
b3 = {"rect": pygame.Rect(100, 100, 45, 50), "color": blue, "dir": downleft}
boxes = [b1, b2, b3]


# RUNNING GAME LOOP
while True:
    # check for QUIT event
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        # draw white background -- essentially refreshes so won't have trailing boxes
    windowSurface.fill(white)

    for b in boxes:
        if b["dir"] == downleft:
            b["rect"].left -= movespeed
            b["rect"].top += movespeed
        ## so if box was going downleft, then coord = (96, 104, 45, 50)
        ## going left means a decrease in x coord
        ## going down means an increase in y coord
        if b["dir"] == downright:
            b["rect"].left += movespeed
            b["rect"].top += movespeed
        if b["dir"] == upright:
            b["rect"].left += movespeed
            b["rect"].top -= movespeed
        if b["dir"] == upleft:
            b["rect"].left -= movespeed
            b["rect"].top -= movespeed

        # Bouncing the box

        ## check whether box has moved out of the top of surface object
        if b["rect"].top <0:
            if b["dir"] == upright:
                b["dir"] = downright
            if b["dir"] == upleft:
                b["dir"] = downleft

        ## check whether box has moved out of bottom of surface object
        if b["rect"].bottom > windowHeight:
            if b["dir"] == downright:
                b["dir"] = upright
            if b["dir"] == downleft:
                b["dir"] = upleft

        ## check whether box has moved out of sides of surface object
        if b["rect"].left < 0:
            if b["dir"] == downleft:
                b["dir"] = downright
            if b["dir"] == upleft:
                b["dir"] = upright
        if b["rect"].right > windowWidth:
            if b["dir"] == upright:
                b["dir"] = upleft
            if b["dir"] == downright:
                b["dir"] = downleft

        ## after updating the positions, draw the box
        pygame.draw.rect(windowSurface, b["color"], b["rect"])

    pygame.display.update()
    time.sleep(0.02)
