'''
Eliza Wallace
Tetris!
'''

import pygame
import random

#rgb codes for the tetris blocks
colours = [
    (255,153,200),
    (252, 246, 189),
    (208,244,222),
    (169,222,249),
    (228,193,249),
    (241,256,121),
    (215,219,221)
]

#multiple shapes
class Figure:
    x = 0
    y = 0

    figures = [
        [[1, 5, 9, 13], [4, 5, 6, 7]],
        [[4, 5, 9, 10], [2, 6, 5, 9]],
        [[6, 7, 9, 10], [1, 5, 6, 10]],
        [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],
        [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],  
        [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],
        [[1, 2, 5, 6]],
    ]

    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.type = random.randint(0, len(self.figures) - 1)
        self.colour = random.randint(1, len(colours) - 1)
        self.rotation = 0

    def image(self):
        return self.figures[self.type][self.rotation]

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.figures[self.length])

class Tetris:
    #set base conditions
    level = 2
    score = 0
    state = "start"
    field = []
    height = 0
    width = 0
    x = 100
    y = 60
    zoom = 20
    figure = None

    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.field = []
        self.score = 0
        self.state = "start"
        for i in range(height):
            newLine = []
            for j in range(width):
                newLine.append(0)
            self.field.append(newLine)

    def newFigure(self):
        self.figure = Figure(3, 0)

#logic for the game
#can we move or rotate the tetris block

    def intersects(self):
        intersection = False
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    if i + self.figure.y > self.height - 1 or \
                            j + self.figure.x > self.width - 1 or \
                            j + self.figure.x < 0 or \
                            self.field[i + self.figure.y][j + self.figure.x] > 0:
                        intersection = True
        return intersection

    def breakLines(self):
        lines = 0
        for i in range(1, self.height):
            zeroes = 0
            for j in range(self.width):
                if self.field[i][j] == 0:
                    zeroes +=1
            if zeroes == 0:
                lines +=1
                for i in ranfe(i,1,-1):
                    for j in range(self.width):
                        self.field[i][j] = self.field[i - 1][j]
        self.score += lines ** 2

    def goSpace(self):
        while not self.intersects():
            self.figure.y +=1
        self.figure.y -= 1
        self.freeze()

    def goDown(self):
        self.figure.y +=1
        if self.intersects():
            self.figure.y -=1
            self.freeze()
    
    def freeze(self):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    self.field[i + self.figure.y][j + self.figure.x] = self.figure.colour

        self.breakLines()
        self.newFigure()
        if self.intersects():
            self.state = 'gameover'

    def goSide(self,dx):
        old_x = self.figure.x 
        self.figure.x += dx
        if self.intersects():
            self.figure.x = old_x

    def rotate(self):
        old_rotation = self.figure.rotation
        self.figure.rotate()
        if self.intersects():
            self.figure.rotation = old_rotation

    #initialize

pygame.init()
GREEN = (0, 51, 0)

NAVY = (0,0,102)
GREY = (102,153,153)

size = (400,500)
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Aesthetic Tetris')

done = False
clock = pygame.time.Clock()
fps = 25
game = Tetris(20,10)
counter = 0
pressingDown = False

while not done:
    if game.figure is None:
        game.newFigure()
    counter +=1
    if counter > 100000:
        counter = 0
    if counter % (fps // game.level // 2) == 0 or pressingDown:
        if game.state == 'start':
            game.goDown()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                game.rotate()
            if event.key == pygame.K_DOWN:
                pressingDown = True
            if event.key == pygame.K_LEFT:
                game.goSide(-1)
            if event.key == pygame.K_RIGHT:
                game.goSide(1)
            if event.key == pygame.K_SPACE:
                game.goSpace()
            if event.key == pygame.K_ESCAPE:
                game.__init__(20,10)

    if event.type == pygame.KEYUP:
        if event.key == pygame.K_DOWN:
            pressingDown = False

    screen.fill(GREY)

    for i in range(game.height):
        for j in range(game.width):
            pygame.draw.rect(screen, NAVY, [game.x + game.zoom * j, game.y + game.zoom * i, game.zoom, game.zoom], 1)
            if game.field[i][j] > 0:
                pygame.draw.rect(screen, colours[game.field[i][j]],[game.x + game.zoom * j + 1, game.y + game.zoom * i + 1, game.zoom -2, game.zoom -1])
    if game.figure is not None:
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in game.figure.image():
                    pygame.draw.rect(screen, colours[game.figure.colour], 
                    [game.x + game.zoom * (j + game.figure.x) + 1,
                    game.y + game.zoom * (i + game.figure.y) + 1, game.zoom -2, game.zoom -2])

        font = pygame.font.SysFont('Calibri', 25, True, False)
        font1 = pygame.font.SysFont('Calibri', 65, True, False)
        text = font.render("Score: " + str(game.score), True, GREEN)
        text_game_over = font1.render("Game Over", True, (255, 125, 0))
        text_game_over1 = font1.render("Press ESC", True, (255, 215, 0))

        screen.blit(text, [0, 0])
        if game.state == "gameover":
            screen.blit(text_game_over, [20, 200])
            screen.blit(text_game_over1, [25, 265])

        pygame.display.flip()
        clock.tick(fps)

pygame.quit()




