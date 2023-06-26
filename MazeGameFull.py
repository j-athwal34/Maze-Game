import pygame, sys, random
from pygame.locals import *

pygame.init()
clock = pygame.time.Clock()

width = 750
height = 750


screen = pygame.display.set_mode((width+250,height+2))
pygame.display.set_caption('Maze Game')

BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0,255,0)
BLUE = (0,0,255)
RED = (255,0,0)
YELLOW = (255,255,0)
TEAL = (0,150,150)

font = pygame.font.Font(None, 50)
font_hints = pygame.font.Font(None, 30)
font_color = pygame.Color('springgreen')
font_white = pygame.Color(WHITE)
font_blue = pygame.Color(BLUE)
font_red = pygame.Color(RED)
font_yellow = pygame.Color(YELLOW)

solve_title = pygame.image.load(r'Default_Solve.jpg')
solve_menu = pygame.image.load(r'Default_Solve_Menu.jpg')

create_logo = pygame.image.load(r'Default_Create.jpg')
create_menu = pygame.image.load(r'Default_Create_Menu.jpg')
create_decision = pygame.image.load(r'Default_Create_Decision.jpg')
create_dTitle = pygame.image.load(r'Default_Create_Choose.jpg')

title = pygame.image.load(r'Default_Logo.jpg')
menu = pygame.image.load(r'Default_Menu.jpg')

global timer #used in solveMaze
global passed_time #used in solveMaze
timer = 0
passed_time = 0

def Main():
    while True:
        clock.tick(60)
        for event in pygame.event.get():    
                if event.type == pygame.QUIT:  
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        sys.exit()
                    if event.key == K_1:
                        SolvingInit()
                    if event.key == K_2:
                        CreationInit()
                   
        screen.fill(BLACK)
        
        screen.blit(title, (150,20))
        screen.blit(menu, (100,330))
        
        pygame.display.update()
        
#MAZE SOLVING CODE
        
class Block:#includes information for the player to navigate the grid
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def draw(self, colour):
        pygame.draw.rect(screen, colour, (self.x+1, self.y+1, p_width-2, p_width-2))    
player = Block(0,0)


class Grid: #one instance of this = one node
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.neighbours_near = []
        self.wall = [True, True, True, True]
        self.is_visited = False
        
    def draw(self, colour): #draws individual grids
        if self.wall[0]: #top
            pygame.draw.line(screen, colour, (self.x*p_width, self.y*p_height), (self.x*p_width+p_width, self.y*p_height), 3)
        if self.wall[1]: #left
            pygame.draw.line(screen, colour, (self.x*p_width, self.y*p_height+p_height), (self.x*p_width, self.y*p_height), 3)
        if self.wall[2]: #right
            pygame.draw.line(screen, colour, (self.x*p_width+p_width, self.y*p_height), (self.x*p_width+p_width, self.y*p_height+p_height), 3)
        if self.wall[3]: #bottom
            pygame.draw.line(screen, colour, (self.x*p_width+p_width, self.y*p_height+p_height), (self.x*p_width, self.y*p_height+p_height), 3)
            
    def get_neighbours(self, node_list):
        for node in node_list: #checking to see whether it has the same coordinates
            if self.y > 0: #up node
                if self.y - 1 == node.y and self.x == node.x:
                    self.neighbours_near.append(node)
            if self.x > 0: #left node
                if self.y == node.y and self.x - 1 == node.x:
                    self.neighbours_near.append(node)
            if self.x < rows - 1: #right node
                if self.y == node.y and self.x + 1 == node.x:
                    self.neighbours_near.append(node)
            if self.y < columns - 1: #down node
                if self.y + 1 == node.y and self.x == node.x:
                    self.neighbours_near.append(node)


def breakWall(node, neighbour):
    if neighbour.x > node.x: #meaning is the neighbour on the right of node
        node.wall[2] = False
        neighbour.wall[1] = False #double break wall because there are 2 walls over each other covering different sides of the wall
    if neighbour.x < node.x: #left wall
        node.wall[1] = False
        neighbour.wall[2] = False
    if neighbour.y > node.y: #down wall
        node.wall[3] = False
        neighbour.wall[0] = False
    if neighbour.y < node.y: #up wall
        node.wall[0] = False
        neighbour.wall[3] = False


def recursiveBacktrack(node, node_list):
    node.is_visited = True
    node.get_neighbours(node_list)
    neighbours_list = node.neighbours_near
    random.shuffle(neighbours_list)
    #neighbour list is now shuffled
    for neighbour in neighbours_list:
        if neighbour.is_visited == False:
            breakWall(node, neighbour)
            recursiveBacktrack(neighbour, node_list) #recursion
            

def depthFirstSearch(start, end, node_list, visited):
    node = getNode(node_list, int(start.x//p_width), int(start.y//p_width))
    if node.x == end.x and node.y == end.y:
        return True
    visited.append(node)
    neighbours = node.neighbours_near
    for n in neighbours:
        if n not in visited and solvecreateCheckWall(start, node_list, getDirection(node,n)) == False:
            new = Block(n.x*p_width, n.y*p_width)
            depthFirstSearch(new, end, node_list, visited) 
    return visited
                                

def mazeGenerator(): 
    node_list = []        
    for i in range(rows):
        for j in range(columns):
            grid = Grid(i, j)
            node_list.append(grid)

    starting_node = node_list[0] #has (x,y) of (0,0)     
    recursiveBacktrack(starting_node, node_list)
    return node_list #put this in a for loop and .draw the objects will draw maze


def points(start_x, start_y, end_x, end_y): #start point and endpoint in one function
    Block(start_x, start_y).draw(BLUE)
    Block(end_x, end_y).draw(RED)
    

def markBlock(x, y, colour):
    Block(x,y).draw(colour)


def solvecreateCheckWall(block, node_list, direction): #only works if you place a Block as a parameter NOT a node 
    (x, y) = block.x, block.y 
    x, y = int(x//p_width), int(y//p_width) #this is a FLOAT cannot use this data type for anything so int() will convert to int! divides by pixel per square to find my standard coordinates not the pixel coordinates
    
    if direction == 'r':
        x += 1
        check_node = getNode(node_list, x,y) #node_list[20] for (1,0)
        if check_node.wall[1] == True:
            return True
        else:
            return False
    if direction == 'l':
        check_node = getNode(node_list, x,y)
        if check_node.wall[1] == True:
            return True
        else:
            return False
    if direction == 'u':
        check_node = getNode(node_list, x,y)
        if check_node.wall[0] == True:
            return True
        else:
            return False
    if direction == 'd':
        y += 1
        check_node = getNode(node_list, x,y)
        if check_node.wall[0] == True:
            return True
        else:
            return False
       

def getNode(node_list, x, y): #position of the node corresponding to the position of the block
    for node in node_list:                
        if (node.x, node.y) == (x, y):
            return node
        

def getDirection(currentCell, n):
    if currentCell.x > n.x:
        return 'l'
    if currentCell.x < n.x:
        return 'r'
    if currentCell.y > n.y:
        return 'u'
    if currentCell.y < n.y:
        return 'd'
    

def difficultyVerification(path): #algorithm works by getting a path of the maximum nodes needed to traverse
    numberOfnode = len(path)
    percentage = (numberOfnode*100)//(rows*columns) #the maximum percentage of the maze that
    if percentage >= 90:
        return True
    else:
        return False


def solveMaze(pack, start_time, passed_time):
    while True:
        global timer
        
        node_list = pack[0]
        start_x = pack[1]
        start_y = pack[2]
        end_x = pack[3]
        end_y = pack[4]
        
        clock.tick(60)
        
        for event in pygame.event.get():    
            if event.type == pygame.QUIT:  
                sys.exit()               
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:       
                    SolvingInit()
                #player movement
                if event.key == K_RIGHT and player.x < width-p_width:
                    if solvecreateCheckWall(player, node_list, 'r') == False: #solvecreateCheckWall returning false means no wall
                        player.x += p_width
                if event.key == K_LEFT and player.x > 0:
                    if solvecreateCheckWall(player, node_list, 'l') == False:
                        player.x -= p_width
                if event.key == K_DOWN and player.y < height-p_width:
                    if solvecreateCheckWall(player, node_list, 'd') == False:
                        player.y += p_width
                if event.key == K_UP and player.y > 0:
                    if solvecreateCheckWall(player, node_list, 'u') == False:
                        player.y -= p_width
        
        screen.fill(BLACK)
        
        text1 = font_hints.render('Use Directional Keys to', True, font_white) 
        text2 = font_hints.render('navigate the maze', True, font_white)
        text3 = font_hints.render('Press ESC key to', True, font_white)
        text4 = font_hints.render('Return to Menu', True, font_white)
        text5 = font_hints.render('Get Stuck?', True, font_yellow)
        text6 = font_hints.render('Follow the wall on the', True, font_yellow)
        text7 = font_hints.render('left around the maze :)', True, font_yellow)
        screen.blit(text1, (width+20, 200))
        screen.blit(text2, (width+20, 230))
        screen.blit(text3, (width+20, 300))
        screen.blit(text4, (width+20, 330))
        screen.blit(text5, (width+20, 400))
        screen.blit(text6, (width+20, 430))
        screen.blit(text7, (width+20, 460))
        
        
        points(start_x, start_y, end_x, end_y)
        
        player.draw(GREEN)
            
        for line in node_list: #draws maze
            line.draw(WHITE)
        
        if int(player.x) == int(end_x) and int(player.y) == int(end_y):
            return True
        
        else:
            passed_time = pygame.time.get_ticks() - start_time #in milliseconds
            timer = passed_time
            time = str(passed_time/1000)
            text = font.render(f'Time: {time}', True, font_color) 
            
        screen.blit(text,(770, 100))
            
        pygame.display.update()


def mazeVerification():
    accepted = False
    while accepted == False:
        node_list = mazeGenerator() #very important contains all information to draw the maze (loop for item in list and .draw)
        #note: node_list is a tree data structure, it contains no cycles!
        end_x = int(random.randint(rows-5,rows-1) * p_width)
        end_y = int(random.randint(columns-5,columns-1) * p_width)
        start_x = 0
        start_y = 0

        endCell = getNode(node_list, int(end_x//p_width), int(end_y//p_width))
        start = Block(0,0)
        visited = []
        path = depthFirstSearch(start, endCell, node_list, visited)

        diff = difficultyVerification(path)

        if diff == False:
            pass
        elif diff == True:
            accepted = True
            return node_list, start_x, start_y, end_x, end_y       


def winScreen(time_taken):
    while True:
        clock.tick(60)
        
        for event in pygame.event.get():    
            if event.type == pygame.QUIT:  
                sys.exit()               
            if event.type == KEYDOWN:
                if event.key == K_r:       
                    SolvingInit()
                if event.key == K_ESCAPE:
                    Main()
        
        screen.fill(BLACK)
        message = f'Maze Solved in time: {time_taken} seconds'
        restart = 'R to Return to Menu'
        leave = 'ESC to exit to Main Menu' #as of right now, this closes the application however in a alpha build this will return back to the menu
        
        textM = font.render(message, True, font_color)
        textR = font.render(restart, True, font_color)
        textL = font.render(leave, True, font_color)
        
        screen.blit(textM, (200, 200))
        screen.blit(textR, (200, 300))
        screen.blit(textL, (200, 400))
        
        pygame.display.update()
    

def solveMenu():
    while True:
        clock.tick(60)
        
        for event in pygame.event.get():    
            if event.type == pygame.QUIT:  
                sys.exit()               
            if event.type == KEYDOWN:      
                if event.key == K_ESCAPE:       
                    Main()
                if event.key == K_1:
                    return 10
                if event.key == K_2:
                    return 20
                if event.key == K_3:
                    return 40
        
        screen.fill(BLACK)
        
        screen.blit(solve_title, (150,100))
        screen.blit(solve_menu, (150, 300))
        
        pygame.display.update()
        

def mainSolve():
    pack = mazeVerification()
    player.x, player.y = 0,0

    start_time = pygame.time.get_ticks()
    if solveMaze(pack, start_time, passed_time=0) == True:
        time_taken = timer/1000
        winScreen(time_taken)
        

def SolvingInit():
    size = solveMenu()
    
    global rows, columns, p_width, p_height
    
    rows = size
    columns = size
    p_width = width/rows
    p_height = height/columns
    
    mainSolve()
    
#MAZE CREATION CODE
     
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def draw(self, colour=GREEN):
        pygame.draw.rect(screen, colour, (self.x*p_width+2, self.y*p_width+2, p_width-2, p_width-2))

class grid:
    def __init__(self, x, y):
        self.x = x #in the form of rows and columns NOT the pygame pixels (have to *p_width to get pixel position) 
        self.y = y
        self.wall = True #true if this node is a wall
        self.neighbours = []
        self.hx = 0 #Heuristic
        self.gx = float("inf") #weight of edge
        self.fx = float("inf") #Heuristic + Weight of Edge
    def draw(self, colour):
        #pygame.draw.rect(screen, outline, (self.x*p_width, self.y*p_width, p_width, p_width))
        pygame.draw.rect(screen, colour, (self.x*p_width+2, self.y*p_width+2, p_width-2, p_width-2))
    def get_neighbours(self, node_list):
        if self.wall == False:
            for node in node_list: #checking to see whether it has the same coordinates
                if node.wall == False:
                    if self.y > 0: #up node
                        if self.y - 1 == node.y and self.x == node.x:
                            self.neighbours.append(node)
                    if self.x > 0: #left node
                        if self.y == node.y and self.x - 1 == node.x:
                            self.neighbours.append(node)
                    if self.x < rows - 1: #right node
                        if self.y == node.y and self.x + 1 == node.x:
                            self.neighbours.append(node)
                    if self.y < columns - 1: #down node
                        if self.y + 1 == node.y and self.x == node.x:
                            self.neighbours.append(node)
    def heuristic(self, goal):
        g_x, g_y = goal.x, goal.y
        hsquared = (self.x - g_x)**2 + (self.y - g_y)**2
        h = (hsquared)**0.5
        self.hx = h
        #working out the euclidian distance
        

def createMenu():
    while True:
        clock.tick(60)
        for event in pygame.event.get():    
                if event.type == pygame.QUIT:  
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        Main()
                    if event.key == K_1:
                        return 10
                    if event.key == K_2:
                        return 15
                    if event.key == K_3:
                        return 20
                   
        screen.fill(BLACK)
        
        screen.blit(create_logo, (150,100))
        screen.blit(create_menu, (150,300))
        
        pygame.display.update()


def nodeInit():
    node_list = []
    walls = []
    for i in range(rows):
        for j in range(columns):
            block = grid(i, j)
            node_list.append(block)
            walls.append(block)
            
    return node_list, walls


def createMaze(node_list, walls):
    count = 0
    while True:
        clock.tick(60)
        for event in pygame.event.get():    
                if event.type == pygame.QUIT:  
                    sys.exit()
                    
                if event.type == MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()
                        mx, my = pos
                        mx, my = int(mx//p_width), int(my//p_width)
                        
                        if mx < rows and my < columns:
                            for i in node_list:
                                if i.x == mx and i.y == my:
                                    node = i

                            if event.button == 1: #click to remove wall, click again to add wall
                                if node.wall == True:
                                    node.wall = False
                                    walls.remove(node)
                                    count += 1
                                elif node.wall == False:
                                    node.wall = True
                                    walls.append(node)
                                    count -= 1
                        #print(node)     
                if event.type == KEYDOWN:      
                    if event.key == K_ESCAPE:       
                        CreationInit() 
                    if event.key == K_c:  
                        if count >= 2:
                            return True
                    
        screen.fill(BLACK)
        
        text1 = font_hints.render('Use Mouse Clicks to', True, font_white) 
        text2 = font_hints.render('interact with the walls', True, font_white)
        text3 = font_hints.render('Press ESC key to', True, font_white)
        text4 = font_hints.render('Return to Menu', True, font_white)
        text5 = font_hints.render('Press C key to', True, font_white)
        text6 = font_hints.render('Confirm/Continue', True, font_white)
        screen.blit(text1, (width+20, 100)) 
        screen.blit(text2, (width+20, 130))
        screen.blit(text3, (width+20, 200))
        screen.blit(text4, (width+20, 230))
        screen.blit(text5, (width+20, 300))
        screen.blit(text6, (width+20, 330))
        
        for i in walls:
            i.draw(WHITE)
        
        pygame.display.update()
  
  
def addStartEnd(node_list, walls, List):
    while True:
        clock.tick(60)
        for event in pygame.event.get():    
                if event.type == pygame.QUIT:  
                    sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()
                        mx, my = pos
                        mx, my = int(mx//p_width), int(my//p_width)
                        
                        if mx < rows and my < columns:
                            for i in node_list:
                                if i.x == mx and i.y == my:
                                    node = i
                            if node.wall == False and node not in Start: #if the block chosen is not a wall and it is not the starting node
                                if len(List) != 0:
                                    List.remove(List[0])
                                List.append(node)
                                node.wall = False
                            
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        CreationInit() 
                    if event.key == K_c and len(List) == 1:
                        return True
                        #return True              
        
        screen.fill(BLACK)
        
        text1 = font_hints.render('Use Mouse Clicks to', True, font_white) 
        text2 = font_hints.render('add a Start/End Square', True, font_white)
        text3 = font_hints.render('Blue is the Start', True, font_blue)
        text4 = font_hints.render('Red is the Goal', True, font_red)
        text5 = font_hints.render('Press ESC key to', True, font_white)
        text6 = font_hints.render('Return to Menu', True, font_white)
        text7 = font_hints.render('Press C key to', True, font_white)
        text8 = font_hints.render('Confirm/Continue', True, font_white)
        screen.blit(text1, (width+20, 100))
        screen.blit(text2, (width+20, 130))
        screen.blit(text3, (width+20, 160))
        screen.blit(text4, (width+20, 190))
        screen.blit(text5, (width+20, 260))
        screen.blit(text6, (width+20, 290))
        screen.blit(text7, (width+20, 360))
        screen.blit(text8, (width+20, 390))
        
        
        for i in walls:
            i.draw(WHITE)
        
        if len(Start) > 0:
            Start[0].draw(BLUE)
            
        if len(End) > 0:
            End[0].draw(RED)
            
        pygame.display.update()


def aStar(node_list, start_node, goal_node):
    graph = {}
    
    for node in node_list:
        node.heuristic(goal_node)
        node.get_neighbours(node_list)
        if node.wall == False:
            graph[node] = node.neighbours
    
    shortest_path = []
    
    path = {}
    start_node.fx = 0
    start_node.gx = 0
    
    while len(graph) > 0:
        
        smallestfx = [node for node in graph]
        smallestfx.sort(key=lambda x: x.fx, reverse=False)
        smallest = smallestfx[0] #the node with the smallest fx value
                
        for neighbour in graph[smallest]: #for the neighbours of the smallest node
            if neighbour in graph and neighbour.fx > 1 + smallest.gx + neighbour.hx:
                neighbour.gx = 1 + smallest.gx
                neighbour.fx = neighbour.gx + neighbour.hx
                path[neighbour] = smallest
        graph.pop(smallest)

    node = goal_node
    while node != start_node:
        shortest_path.insert(0, node)
        node = path[node]
        
    shortest_path.insert(0, start_node)
    
    return shortest_path


def createCheckWall(node_list, node, direction):
    for i in node_list:
        if direction == 'u':
            if i.x == node.x and i.y == node.y-1:
                if i.wall == False:
                    return False #no wall in the intended direction
                else:
                    return True
        elif direction == 'd':
            if i.x == node.x and i.y == node.y+1:
                if i.wall == False:
                    return False #no wall in the intended direction
                else:
                    return True
        elif direction == 'l':
            if i.x == node.x-1 and i.y == node.y:
                if i.wall == False:
                    return False #no wall in the intended direction
                else:
                    return True
        elif direction == 'r':
            if i.x == node.x+1 and i.y == node.y:
                if i.wall == False:
                    return False #no wall in the intended direction
                else:
                    return True
    
    
def solveComputer(walls, node_list, start_node, goal_node):
    try:
        path = aStar(node_list, start_node, goal_node)
        while True:
            clock.tick(60)
            for event in pygame.event.get():    
                    if event.type == pygame.QUIT:  
                        sys.exit()
                    if event.type == KEYDOWN:
                        if event.key == K_ESCAPE:
                            CreationInit() 
                        if event.key == K_RETURN:
                            return True
                            
            screen.fill(BLACK)
            
            text1 = font_hints.render('Press RETURN Key to', True, font_white) 
            text2 = font_hints.render('finish viewing the maze', True, font_white)
            text3 = font_hints.render('Press ESC key to', True, font_white)
            text4 = font_hints.render('Return to Menu', True, font_white)
            screen.blit(text1, (width+15, 200))
            screen.blit(text2, (width+15, 230))
            screen.blit(text3, (width+15, 300))
            screen.blit(text4, (width+15, 330))
            
            for i in walls:
                i.draw(WHITE)
            for j in path:
                j.draw(YELLOW)
                
            pygame.display.update()
            
    except KeyError:
        print("no path exists -- error, restarting application...")
        CreationInit()


def solveUser(walls, node_list, start_node, goal_node, start_time):
    player = Player(start_node.x, start_node.y)
    while True:
        global timer
        
        clock.tick(60)
        for event in pygame.event.get():    
                if event.type == pygame.QUIT:  
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        CreationInit()
                        
                    if event.key == K_UP:
                        if createCheckWall(node_list, player, 'u') == False:
                            player.y -= 1
                    if event.key == K_LEFT:
                        if createCheckWall(node_list, player, 'l') == False:
                            player.x -= 1
                    if event.key == K_RIGHT:
                        if createCheckWall(node_list, player, 'r') == False:
                            player.x += 1
                    if event.key == K_DOWN:
                        if createCheckWall(node_list, player, 'd') == False:
                            player.y += 1
                    
        screen.fill(BLACK)
        
        text1 = font_hints.render('Use Directional Keys to', True, font_white) 
        text2 = font_hints.render('navigate the maze', True, font_white)
        text3 = font_hints.render('Press ESC key to', True, font_white)
        text4 = font_hints.render('Return to Menu', True, font_white)
        screen.blit(text1, (width+20, 200))
        screen.blit(text2, (width+20, 230))
        screen.blit(text3, (width+20, 300))
        screen.blit(text4, (width+20, 330))
        
        for i in walls:
            i.draw(WHITE)
        Start[0].draw(BLUE)
        End[0].draw(RED)
        
        player.draw()
        
        if int(player.x) == int(goal_node.x) and int(player.y) == int(goal_node.y):
            return True
            
        else:
            passed_time = pygame.time.get_ticks() - start_time #in milliseconds
            timer = passed_time
            time = str(passed_time/1000)
            text = font.render(f'Time: {time}', True, font_color) 
            
        screen.blit(text,(width+20, 100))

        pygame.display.update()
    
    
def UserOrComputer():
    while True:
        clock.tick(60)
        for event in pygame.event.get():    
                if event.type == pygame.QUIT:  
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        CreationInit() 
                    if event.key == K_1:
                        return True #Computer
                    if event.key == K_2:
                        return False #User
        screen.fill(BLACK)
        screen.blit(create_dTitle, (150, 100))
        screen.blit(create_decision, (150, 300))
        pygame.display.update()


def winScreenUser(time_taken):
    while True:
        clock.tick(60)
        
        for event in pygame.event.get():    
            if event.type == pygame.QUIT:  
                sys.exit()               
            if event.type == KEYDOWN:
                if event.key == K_r:       
                    CreationInit() 
                if event.key == K_ESCAPE:
                    Main()
        
        screen.fill(BLACK)
        message = f'Maze Solved in time: {time_taken} seconds'
        restart = 'R to Return to Menu'
        leave = 'ESC to exit to Main Menu' #as of right now, this closes the application however in a alpha build this will return back to the menu
        
        textM = font.render(message, True, font_color)
        textR = font.render(restart, True, font_color)
        textL = font.render(leave, True, font_color)
        
        screen.blit(textM, (200, 200))
        screen.blit(textR, (200, 300))
        screen.blit(textL, (200, 400))

        pygame.display.update()


def winScreenComputer():
     while True:
        clock.tick(60)
        
        for event in pygame.event.get():    
            if event.type == pygame.QUIT:  
                sys.exit()               
            if event.type == KEYDOWN:
                if event.key == K_r:       
                    CreationInit() 
                if event.key == K_ESCAPE:
                    Main()
        
        screen.fill(BLACK)
        restart = 'R to Return to Menu'
        leave = 'ESC to exit to Main Menu' #as of right now, this closes the application however in a alpha build this will return back to the menu
        
        textR = font.render(restart, True, font_color)
        textL = font.render(leave, True, font_color)
        
        screen.blit(textR, (300, 300))
        screen.blit(textL, (300, 400))
        
        pygame.display.update()


def Computer(walls, node_list, start_node, goal_node):
    if solveComputer(walls, node_list, start_node, goal_node) == True:
        winScreenComputer()


def User(walls, node_list, start_node, goal_node):
    start_time = pygame.time.get_ticks()
    if solveUser(walls, node_list, start_node, goal_node, start_time) == True:
        time_taken = timer/1000
        winScreenUser(time_taken)
   
   
def mainCreate():
    pack = nodeInit()
    node_list = pack[0]
    walls = pack[1]
    if createMaze(node_list, walls) == True:
        if addStartEnd(node_list, walls, Start) == True:
            if addStartEnd(node_list, walls, End) == True:
                start_node = Start[0] #this is the global variable that contains the info for the start node
                goal_node = End[0] #same as above
                if UserOrComputer() == True:
                    Computer(walls, node_list, start_node, goal_node)
                else:
                    User(walls, node_list, start_node, goal_node)
        
        
def CreationInit():
    size = createMenu()
    global rows, columns, p_width, walls, Start, End
    
    walls = []
    Start = []
    End = []
    rows = size
    columns = size
    p_width = width//rows

    mainCreate()


if __name__ == '__main__':
    Main()