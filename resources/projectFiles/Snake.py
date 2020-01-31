import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox


class Cube(object):
    rows = 20       #set the amount of rows and columns we wish to have in our Snake game
    w = 500         #set the pixel width and height of our game screen

    def __init__(self, start, dirnx=1, dirny=0, color=(200, 200, 200)):
        self.pos = start    #start our Snake where we want
        self.dirnx = 1      #make our Snake start facing right
        self.dirny = 0
        self.color = color  #give our Snake a color of our choosing (or the default white set in the function)

    def move(self, dirnx, dirny):
        self.dirnx = dirnx  #update the direction the Snake is moving
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny) #move the Snake according to it's direction

    def draw(self, surface, eyes=False):
        dis = self.w // self.rows   #take the width of the screen and divide by the rows in order to get the pixel length to each row
        i = self.pos[0] #get which row the Snake is in
        j = self.pos[1] #get which column the Snake is in

        pygame.draw.rect(surface, self.color, (i * dis + 1, j * dis + 1, dis - 2, dis - 2)) #draw a rectangle with the apporpriate math in order to put our Snake inside the boxes defined by our grid
        if eyes:    #for the head of the Snake this will draw the eyes on it
            centre = dis // 2
            radius = 3
            circleMiddle = (i * dis + centre - radius, j * dis + 8)
            circleMiddle2 = (i * dis + dis - radius * 2, j * dis + 8)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle, radius)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle2, radius)


class Snake(object):
    body = []   #an array to hold all the Cubes that make up the Snakes body
    turns = {}  #keep track of where and what direction our Snake has turned

    def __init__(self, color, pos):
        self.color = color          #set color
        self.head = Cube(pos)       #make Snakes head
        self.body.append(self.head) #attach the head to the Snake
        self.addCube()              #add 3 boxes to the Snake to start the game
        self.addCube()
        self.addCube()
        self.dirnx = 0              #make the starting direction facing down
        self.dirny = 1

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()       #exits out of pygame
                exit()              #always call exit() after pygame.quit() to keep away error about initializing video

            keys = pygame.key.get_pressed()     #grab keys pressed, check if wasd or up down left or right has been pressed then turn the Snake accordingly

            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.dirnx = -1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_a]:
                    self.dirnx = -1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_RIGHT]:
                    self.dirnx = 1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_d]:
                    self.dirnx = 1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_UP]:
                    self.dirnx = 0
                    self.dirny = -1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_w]:
                    self.dirnx = 0
                    self.dirny = -1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_DOWN]:
                    self.dirnx = 0
                    self.dirny = 1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_s]:
                    self.dirnx = 0
                    self.dirny = 1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        for i, c in enumerate(self.body):       #for each box(c) in our Snakes body(self.body)
            p = c.pos[:]                        #grab position of each Cube to see if it should be turned
            if p in self.turns:                 #if the postion of the current Cube(c) is on a position in our list of places that the Snake has turned(self.turns) then we should turn the Snake accordingly
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body) - 1:     #if this is the last Cube in the Snakes body going around a turn then we no longer need to know to turn here so we delete the info of the turn from our turn list
                    self.turns.pop(p)
            else:                               #if our Snake is moving off screen we want it to move out the other side of the screen
                if c.dirnx == -1 and c.pos[0] <= 0:
                    c.pos = (c.rows - 1, c.pos[1])
                elif c.dirnx == 1 and c.pos[0] >= c.rows - 1:
                    c.pos = (0, c.pos[1])
                elif c.dirny == 1 and c.pos[1] >= c.rows - 1:
                    c.pos = (c.pos[0], 0)
                elif c.dirny == -1 and c.pos[1] <= 0:
                    c.pos = (c.pos[0], c.rows - 1)
                else:
                    c.move(c.dirnx, c.dirny)

    def reset(self, pos):
        self.head = Cube(pos)       #when our Snake dies we reset it, basically the same function as the one to start the Snake
        self.body = []
        self.body.append(self.head)
        self.addCube()
        self.addCube()
        self.addCube()
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1

    def addCube(self):
        tail = self.body[-1]            #find the last Cube on the Snake
        dx, dy = tail.dirnx, tail.dirny #find the direction of the tail end of the Snake

        if dx == 1 and dy == 0:         #depending on the direction of the tail, add a new Cube in the correct location
            self.body.append(Cube((tail.pos[0] - 1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(Cube((tail.pos[0] + 1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(Cube((tail.pos[0], tail.pos[1] - 1)))
        elif dx == 0 and dy == -1:
            self.body.append(Cube((tail.pos[0], tail.pos[1] + 1)))

        self.body[-1].dirnx = dx    #make sure the new Cube that was added is moving in the right direction
        self.body[-1].dirny = dy

    def draw(self, surface):
        for i, c in enumerate(self.body):   #for each Cube(c) in our Snakes body (self.body)
            if i == 0:                      #if this is the head of the Snake(i==0) then we should draw the eyes on it
                c.draw(surface, True)
            else:
                c.draw(surface)             #if its not the head of the Snake then just draw a normal Cube


def drawGrid(w, rows, surface):
    sizeBtwn = w // rows    #take the width of the screen and divide it by the rows to get how much space should be between rows

    x = 0
    y = 0
    for l in range(rows):   #draw a horizontal and vertical line each iteration of the loop
        x += sizeBtwn
        y += sizeBtwn

        pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, w))  #draw a line at the current x position from the top the the bottom of the screen
        pygame.draw.line(surface, (255, 255, 255), (0, y), (w, y))  #draw a lind at the current y position from the left to the right of the screen


def redrawWindow(surface):
    global rows, width, s, snack
    surface.fill((0, 0, 0))
    s.draw(surface)                 #fill the back of the screen with black, then draw the Snake, snack, and grid, then update our display
    snack.draw(surface)
    drawGrid(width, rows, surface)
    pygame.display.update()


def randomSnack(rows, item):
    positions = item.body           #get the positions of the Snake to know where to not place snacks

    while True:                     #get a random position of the snack, if it happens to land on the Snake then try a new random position
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z: z.pos == (x, y), positions))) > 0:
            continue
        else:
            break

    return (x, y)


def messageBox(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()                         #fancy things to make the message box look nice
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass


def main():
    global width, rows, s, snack
    width = 500
    rows = 20
    win = pygame.display.set_mode((width, width))           #set pixel width and height of play area
    s = Snake((255, 0, 0), (10, 10))                        #create the Snake
    snack = Cube(randomSnack(rows, s), color=(255, 0, 0))   #make our first snack
    flag = True                                             #create a statement for our main loop to follow

    clock = pygame.time.Clock()                             #keep track of time so the Snake moves consistent speeds

    while flag:                                             #main game loop
        pygame.time.delay(50)                               #delay .5s inbetween Snake moves
        clock.tick(10)                                      #stop the game from moving at more than 10 fps, game will go faster when this is lower
        s.move()                                            #move the Snake
        if s.body[0].pos == snack.pos:                      #if the Snake moves over a snack, eat it and add a body part
            s.addCube()
            snack = Cube(randomSnack(rows, s), color=(255, 0, 0))

        for x in range(len(s.body)):                        #check to see if the Snake has hit itself and give the score and message box
            if s.body[x].pos in list(map(lambda z: z.pos, s.body[x + 1:])):
                print('Score: ', len(s.body))
                messageBox('You Lost!', 'Play again...')
                s.reset((10, 10))
                break

        redrawWindow(win)                                   #update the window each time the Snake moves

    pass


main()






























