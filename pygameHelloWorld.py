'''The following is directly from the Al Sweigart book. I typed out the commands for practice on using pygame '''

import pygame, sys
from pygame.locals import *

## set up pygame
pygame.init()

# set up window
windowSurface = pygame.display.set_mode((500,400), 1, 8)
pygame.display.set_caption("Hello World!")

# Set up the colors
black = (0,0,0)
white = (255,255,255)
red = (255, 0 , 0 )
green = (0, 255, 0)
blue = (0, 0 , 255)

# Set up the fonts
basicFont = pygame.font.SysFont(None, 30)

# Set up text

## .render(text, aliasing, text color, background color)
text = basicFont.render("Hello World!", True, white, blue)
textRect = text.get_rect()
## assigning the overall surface's center coords to the text coords
textRect.centerx = windowSurface.get_rect().centerx
textRect.centery = windowSurface.get_rect().centery

# Draw white background onto surface
windowSurface.fill(white)

# Draw a green polygon onto surface

## .polygon(Surface object to draw on, color, tuple of tuples for coords,
## and optionally line width but if not filled, then polygon will be filled)
pygame.draw.polygon(windowSurface, green, ((146,0),
(291,106), (236,277), (56,277), (0,106)))

# Draw some blue lines onto surface
pygame.draw.line(windowSurface, blue, (60,60), (120,60), 4)
pygame.draw.line(windowSurface, blue, (120,60), (60,120), 3)

#Draw a blue circle

## .circle(surface object, color, center point, radius, line width)
### last arg can be 0 so can be filled in
pygame.draw.circle(windowSurface, blue, (300,50), 20,0)

#Draw a red ellipse
pygame.draw.ellipse(windowSurface, red, (300,250,40,80),1)

#draw text's background rectangle
pygame.draw.rect(windowSurface, red, (textRect.left-20,
textRect.top-20, textRect.width+40, textRect.height + 40))

# Get pixel array of surface
pixArray = pygame.PixelArray(windowSurface)
pixArray[480][380] = black
del pixArray

# draw text

## putting a surface object upon another
windowSurface.blit(text, textRect)

# draw window on screen
pygame.display.update()

# run game loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
