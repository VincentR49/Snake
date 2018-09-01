# Snake

import random, sys, pygame
from pygame.locals import *


# Set up colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GREY = (127, 127, 127)

# Global parameters
WINDOWWIDTH = 600
WINDOWHEIGHT = 600
GRIDSIZE = 50
BACKGROUNDCOLOR = BLACK
TEXTCOLOR = GREEN
FPS = 10


# Functions and classes definitions
def terminate():
    pygame.quit()
    sys.exit()


def newFood():
    x = random.randint(0, NXGRID - 1)
    y = random.randint(0, NYGRID - 1)
    return pygame.Rect(grid[x][y].left,
                       grid[x][y].top,
                       GRIDSIZE, GRIDSIZE)


def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


def waitForPlayerToContinue():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                if event.key == K_RETURN or event.key == K_SPACE:
                    return
    
class Player():
    ''' Classe du joueur'''
    def __init__(self):
        self.direction = [0, 0]
        self.score = 0
        self.x = random.randint(0, NXGRID - 1)
        self.y = random.randint(0, NYGRID - 1)
        self.rects = []
        self.isDead = False
        self.color = WHITE
        self.rects.append(pygame.Rect(grid[self.x][self.y].left,
                                      grid[self.x][self.y].top,
                                      GRIDSIZE, GRIDSIZE))

    def eatFood(self, food):
        self.score += 1
        del(food)
        xTail = - self.direction[0] * GRIDSIZE + self.rects[-1].left
        yTail = - self.direction[1] * GRIDSIZE + self.rects[-1].top
        self.rects.append(pygame.Rect(xTail,yTail,
                                      GRIDSIZE, GRIDSIZE))
        
    def update(self):
        # tail actualization
        self.rects[1:] = self.rects[0:-1]
        # new head position
        self.x += self.direction[0]
        self.y += self.direction[1]
        if self.x < 0:
            self.x = NXGRID - 1
        if self.x > NXGRID - 1:
            self.x = 0
        if self.y < 0:
            self.y = NYGRID - 1
        if self.y > NYGRID - 1:
            self.y = 0
        self.rects[0] = grid[self.x][self.y]
        # Check if the snake eats himslef
        for body in self.rects[1:]:
            if player.rects[0].colliderect(body):
                self.isDead = True
                self.color = RED

# Main

# set up the grid
grid = []
NXGRID = int(WINDOWHEIGHT / GRIDSIZE)
NYGRID = int(WINDOWWIDTH / GRIDSIZE)
for x in range(NXGRID):
    grid.append([])
    for y in range(NYGRID):
        grid[x].append(pygame.Rect( x * GRIDSIZE, y * GRIDSIZE, GRIDSIZE, GRIDSIZE))
        
# Initialisation
pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Snake')

# set up fonts
font = pygame.font.SysFont(None, 20)

# player initialisation
player = Player()
moveUp = moveDown = moveLeft = moveRight = False

# food initialisation
food = newFood()

while True: # game loop

    # check events
    for event in pygame.event.get():
        if event.type == QUIT:
            terminate()
        if event.type == KEYUP:
            if event.key == K_ESCAPE:
                terminate()
        if event.type == KEYDOWN:
            if event.key == K_UP:
                player.direction = [0, -1]
            if event.key == K_DOWN:
                player.direction = [0, 1]
            if event.key == K_LEFT:
                player.direction = [-1, 0]
            if event.key == K_RIGHT:
                player.direction = [1, 0]

    # check if the player eats the food
    if player.rects[0].colliderect(food):
        player.eatFood(food)
        food = newFood()
        
    # update player position  
    player.update()

    # reset screen
    windowSurface.fill(BACKGROUNDCOLOR)
    pygame.draw.rect(windowSurface, GREEN, food)
    # Draw player
    for playerRect in player.rects:
        pygame.draw.rect(windowSurface, player.color, playerRect)
        pygame.draw.rect(windowSurface, GREY, playerRect, 5)
    # Draw the score and other information
    drawText('Score: %s' %(player.score), font, windowSurface, 10, 0)
    drawText('x: %s' %(player.x), font, windowSurface, 10, 15)
    drawText('y: %s' %(player.y), font, windowSurface, 10, 30)
    drawText('FPS: %s' %(FPS), font, windowSurface, 10, 45)
    
    if player.isDead:
        drawText('GAME OVER !', font, windowSurface, WINDOWWIDTH / 2 - 100, WINDOWHEIGHT / 2 - 20)
        drawText('Score: %s' %(player.score), font, windowSurface, WINDOWWIDTH / 2 - 100, WINDOWHEIGHT / 2)
        drawText('Press enter to restart', font, windowSurface, WINDOWWIDTH / 2 - 100, WINDOWHEIGHT / 2 + 20 )
        drawText('Press escape to quit the game', font, windowSurface, WINDOWWIDTH / 2 - 100, WINDOWHEIGHT / 2 + 40)
        pygame.display.update()
        waitForPlayerToContinue()
        player = Player()
        food = newFood()
        
    pygame.display.update()
    mainClock.tick(FPS)
