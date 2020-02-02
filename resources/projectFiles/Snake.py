import math
import random
import pygame
import tkinter
import tkinter.font as font
BOARDSIZE = 700
ROWS = 20


#A class for each individual cube in the snake
class Cube(object):
    #set rows and columns for game board
    rows = ROWS
    #set pixel width and height of game board
    width = BOARDSIZE         

    #start at a set position facing right with a set color
    def __init__(self, start, xDirec=1, yDirec=0, color=(200, 200, 200)):
        self.position = start    
        self.xDirec = 1      
        self.yDirec = 0
        self.color = color

    def move(self, xDirec, yDirec):
        #update the direction the snake is facing
        self.xDirec = xDirec  
        self.yDirec = yDirec
        #move in accordance to where the snake facing
        self.position = (self.position[0] + self.xDirec, self.position[1] + self.yDirec) 

    def draw(self, surface, eyes=False):
        #get the size the snake should be by finding how big each cube on the board is
        dis = self.width// self.rows
        #get the row and column the snake is at
        i = self.position[0] 
        j = self.position[1] 

        #draw a rectangle on the correct surface with the right color, size, and coordinates, plus some offset to place it correctly
        pygame.draw.rect(surface, self.color, (i * dis + 1, j * dis + 1, dis - 2, dis - 2))
        #if this is the head of the snake, draw eyes on it
        if eyes:
            center = dis // 2
            radius = self.width // 160
            if self.xDirec == 1:
                circleMiddle = (i * dis + center - radius, j * dis + self.width // 65)
                circleMiddle2 = (i * dis + dis - radius * 2, j * dis + self.width // 65)
                pygame.draw.circle(surface, (0, 0, 0), circleMiddle, radius)
                pygame.draw.circle(surface, (0, 0, 0), circleMiddle2, radius)
            if self.xDirec == -1:
                circleMiddle = (i * dis + center + radius, j * dis + self.width // 65)
                circleMiddle2 = (i * dis + dis - radius * 2 - self.width // 35, j * dis + self.width // 65)
                pygame.draw.circle(surface, (0, 0, 0), circleMiddle, radius)
                pygame.draw.circle(surface, (0, 0, 0), circleMiddle2, radius)
            if self.yDirec == 1:
                circleMiddle = (i * dis + center + radius + self.width // 160, j * dis + self.width // 65)
                circleMiddle2 = (i * dis + center + radius + self.width // 160, j * dis + dis - radius * 2)
                pygame.draw.circle(surface, (0, 0, 0), circleMiddle, radius)
                pygame.draw.circle(surface, (0, 0, 0), circleMiddle2, radius)
            if self.yDirec == -1:
                circleMiddle = (i * dis + center - radius - self.width // 160, j * dis + self.width // 65)
                circleMiddle2 = (i * dis + center - radius - self.width // 160, j * dis + dis - radius * 2)
                pygame.draw.circle(surface, (0, 0, 0), circleMiddle, radius)
                pygame.draw.circle(surface, (0, 0, 0), circleMiddle2, radius)
                


#take all the cube objects of the snake and put them together
class Snake(object):
    #array to hold all cube objects of the snake
    body = []
    #keep track of where and which direction every turn is at for the tail of the snake to follow
    turns = {}  

    #start the snake 4 cubes big facing right
    def __init__(self, color, position):
        self.color = color          
        self.head = Cube(position)       
        self.body.append(self.head)
        self.addCube()              
        self.addCube()
        self.addCube()
        self.xDirec = 0             
        self.yDirec = 1

    def move(self):
        for event in pygame.event.get():
            #quit the game when told to
            if event.type == pygame.QUIT:
                pygame.quit()
                #always call exit() when quitting to avoid an error
                exit()              

            #if we don't quit the game lets see if any keys are pressed and act accordingly
            keys = pygame.key.get_pressed()
            for key in keys:
                if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                    self.xDirec = -1
                    self.yDirec = 0
                    self.turns[self.head.position[:]] = [self.xDirec, self.yDirec]
                elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                    self.xDirec = 1
                    self.yDirec = 0
                    self.turns[self.head.position[:]] = [self.xDirec, self.yDirec]
                elif keys[pygame.K_UP] or keys[pygame.K_w]:
                    self.xDirec = 0
                    self.yDirec = -1
                    self.turns[self.head.position[:]] = [self.xDirec, self.yDirec]
                elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                    self.xDirec = 0
                    self.yDirec = 1
                    self.turns[self.head.position[:]] = [self.xDirec, self.yDirec]

        #move each cube in the snakes body and if we need to, move it
        for i, cube in enumerate(self.body):       
            p = cube.position[:]                      
            if p in self.turns:
                turn = self.turns[p]
                cube.move(turn[0], turn[1])
                #if a turn has reached the end of our snakes body, throw away the record of this turn
                #otherwise the next time the snake gets here it will automatically turn and we dont want that
                if i == len(self.body) - 1:
                    self.turns.pop(p)
            else:
                if cube.xDirec == -1 and cube.position[0] <= 0:
                    cube.position = (cube.rows - 1, cube.position[1])
                elif cube.xDirec == 1 and cube.position[0] >= cube.rows - 1:
                    cube.position = (0, cube.position[1])
                elif cube.yDirec == 1 and cube.position[1] >= cube.rows - 1:
                    cube.position = (cube.position[0], 0)
                elif cube.yDirec == -1 and cube.position[1] <= 0:
                    cube.position = (cube.position[0], cube.rows - 1)
                else:
                    cube.move(cube.xDirec, cube.yDirec)

    #put the snake back and remove extra cubes when it dies
    def reset(self, position):
        self.head = Cube(position)
        self.body = []
        self.body.append(self.head)
        self.addCube()
        self.addCube()
        self.addCube()
        self.turns = {}
        self.xDirec = 0
        self.yDirec = 1

    #add a cube on to the tail of the snake and facing the correct direction
    def addCube(self):
        tail = self.body[-1]            
        dx, dy = tail.xDirec, tail.yDirec
        if dx == 1 and dy == 0:
            self.body.append(Cube((tail.position[0] - 1, tail.position[1])))
        elif dx == -1 and dy == 0:
            self.body.append(Cube((tail.position[0] + 1, tail.position[1])))
        elif dx == 0 and dy == 1:
            self.body.append(Cube((tail.position[0], tail.position[1] - 1)))
        elif dx == 0 and dy == -1:
            self.body.append(Cube((tail.position[0], tail.position[1] + 1)))
        self.body[-1].xDirec = dx
        self.body[-1].yDirec = dy

    #draw all the cubes in the snake and if its the head give it eyes too
    def draw(self, surface):
        for i, cube in enumerate(self.body):
            if i == 0:
                cube.draw(surface, True)
            else:
                cube.draw(surface)
                

def drawGrid(width, rows, surface):
    sizeBtwn = width// rows    
    x = 0
    y = 0
    #draw the white lines on the board
    for l in range(rows):   
        x += sizeBtwn
        y += sizeBtwn
        pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, width))
        pygame.draw.line(surface, (255, 255, 255), (0, y), (width, y))


def redrawWindow(surface):
    global rows, width, snake, snack
    surface.fill((0, 0, 0))
    snake.draw(surface)
    snack.draw(surface)
    drawGrid(width, rows, surface)
    pygame.display.update()

#generate a random place for a snack
def randomSnack(rows, item):
    #grab all the positions of the body
    positionitions = item.body
    #keep finding random places to put a snack until we get one that isn't on top of the snake
    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z: z.position == (x, y), positionitions))) > 0:
            continue
        else:
            break
    return (x, y)


def messageBox(score):
    mainWindow = tkinter.Tk()
    mainWindow.title("You Lost!")
    mainWindow.geometry("300x180")
    scoreFrame = tkinter.Frame(mainWindow)
    scoreFrame.pack()
    buttonFrame = tkinter.Frame(mainWindow)
    buttonFrame.pack(fill='both')

    scoreLabel = tkinter.Label(scoreFrame, text = 'Score: ' + str(score),  anchor="w")
    scoreLabel['font'] = font.Font(size = 30)
    scoreLabel.pack()

    replayButton = tkinter.Button(buttonFrame, text='Play Again!', command=mainWindow.destroy)
    replayButton['font'] = font.Font(size = 30)
    replayButton.pack()

    scoreFrame.pack()
    buttonFrame.pack()
    tkinter.mainloop()

def main():
    global width, rows, snake, snack
    width = BOARDSIZE
    rows = ROWS
    win = pygame.display.set_mode((width, width))           
    snake = Snake((255, 0, 0), (10, 10))                        
    snack = Cube(randomSnack(rows, snake), color=(255, 0, 0))   
    flag = True                                             

    #keep time so the snake moves at a consistent rate
    clock = pygame.time.Clock()                             

    while flag:
        #0.5 second delay between moves
        pygame.time.delay(50)
        #stop the game from going more than 10 fps
        clock.tick(10)                                      
        snake.move()                                           
        if snake.body[0].position == snack.position:                      
            snake.addCube()
            snack = Cube(randomSnack(rows, snake), color=(255, 0, 0))

        for x in range(len(snake.body)):                        
            if snake.body[x].position in list(map(lambda z: z.position, snake.body[x + 1:])):
                print('Score: ', len(snake.body))
                messageBox(len(snake.body))
                snake.reset((10, 10))
                break

        redrawWindow(win)                                   


main()
