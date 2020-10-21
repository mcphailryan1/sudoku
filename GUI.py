# GUI.py
import pygame
from sudoku import solve, valid
import time
pygame.font.init()

#the window size is 540 by 600 (x,y)

#the Grid class holds a bunch of cubes in a row column structure
class Grid:
    # Nine rows
    R = 9
    #Nine columns
    C = 9

    # Initialize matrix 
    startingBoard = []
    print("Enter the numbers row by row: ")
    #When entering the entrries, read the sudoku puzzle like you would a book and enter the numbers in

    # For user input 
    for i in range(R):          # A for loop for row entries 
        a =[] 
        for j in range(C):      # A for loop for column entries 
            a.append(int(input())) 
        startingBoard.append(a) 
  
    # For printing the matrix 
    for i in range(R): 
        for j in range(C): 
            print(startingBoard[i][j], end = " ") 
        print() 

    def __init__(self, rows, cols, width, height):
        self.rows = rows
        self.cols = cols
        self.cubes = [[Cube(self.startingBoard[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]
        self.width = width
        self.height = height
       #again, the model is used for the solver to validate
        self.model = None
        self.selected = None

    def update_model(self):
        #the model board is the board that is sent to solver, ussed to attempt to solve
        #you only need to update this when we need to attempt to see if the solution can be solved
        #basically this is used because the solver check does not care about the penciled in answers
        self.model = [[self.cubes[i][j].value for j in range(self.cols)] for i in range(self.rows)]

    
    #setting the permanent value 
    def place(self, val):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set(val)
            self.update_model()

            #this is where the solve methods from the other python script are used
            if valid(self.model, val, (row,col)) and solve(self.model):
                return True
            else:
                self.cubes[row][col].set(0)
                self.cubes[row][col].set_temp(0)
                self.update_model()
                return False

    
    #setting the temporary value for the cube object that we click on
    def sketch(self, val):
        row, col = self.selected
        self.cubes[row][col].set_temp(val)

    def draw(self, win):
        # Draw Grid Lines
        gap = self.width / 9
        for i in range(self.rows+1):
            if i % 3 == 0 and i != 0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(win, (0,0,0), (0, i*gap), (self.width, i*gap), thick)
            pygame.draw.line(win, (0, 0, 0), (i * gap, 0), (i * gap, self.height), thick)

        # Draw Cubes
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw(win)

    def select(self, row, col):
        # Reset all other
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].selected = False

        self.cubes[row][col].selected = True
        self.selected = (row, col)

    def clear(self):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set_temp(0)

    def click(self, pos):
        """
        :param: pos
        :return: (row, col)
        """
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / 9
            x = pos[0] // gap
            y = pos[1] // gap
            return (int(y),int(x))
        else:
            return None

   #checks if there are any empty squares left in the board
    def is_finished(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cubes[i][j].value == 0:
                    return False
        return True


class Cube:
    rows = 9
    cols = 9

    def __init__(self, value, row, col, width ,height):
        self.value = value
       #the temp is the temporary penciled in value
        self.temp = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False

    def draw(self, win):
        fnt = pygame.font.SysFont("swiss721", 40)

        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        if self.temp != 0 and self.value == 0:
            text = fnt.render(str(self.temp), 1, (128,128,128))
            win.blit(text, (x+5, y+5))
        elif not(self.value == 0):
            text = fnt.render(str(self.value), 1, (0, 0, 0))
            win.blit(text, (x + (gap/2 - text.get_width()/2), y + (gap/2 - text.get_height()/2)))

        #selected will put a larger box around what you select to show that you have selected it
        if self.selected:
            pygame.draw.rect(win, (255,0,0), (x,y, gap ,gap), 3)

    def set(self, val):
        self.value = val

    def set_temp(self, val):
        self.temp = val


def redraw_window(win, board, time, strikes):
    win.fill((255,255,255))
    # Draw time
    fnt = pygame.font.SysFont("swiss721", 40)
    text = fnt.render("Time: " + format_time(time), 1, (0,0,0))
    win.blit(text, (540 - 200 , 550))
    # Draw Strikes
    text = fnt.render("X " * strikes, 1, (255, 0, 0))
    win.blit(text, (20, 560))
    # Draw grid and board
    board.draw(win)


def format_time(secs):
    sec = secs%60
    minute = secs//60
    hour = minute//60

    mat = " " + str(minute) + ":" + str(sec)
    return mat


def main():
    win = pygame.display.set_mode((540,600))
    pygame.display.set_caption("Sudoku GUI")
    board = Grid(9, 9, 540, 540)
    key = None
    run = True
    start = time.time()
    strikes = 0
    while run:

        play_time = round(time.time() - start)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            #the following is for all the different key strokes
            if event.type == pygame.KEYDOWN:
                #the K_1 is for "key one"
                #the K_KP1 is for "keypad one" so this code allows you to use both the keyboard and keypad
                
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_KP1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_KP2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_KP3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_KP4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_KP5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_KP6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_KP7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_KP8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9
                if event.key == pygame.K_KP9:
                    key = 9
                if event.key == pygame.K_DELETE:
                    board.clear()
                    key = None
               
               #the following "if" is for the enter key on the keyboard portion (K_RETURN)
               #it also makes sure that the answer is correct before letting you enter it into the puzzle
                if event.key == pygame.K_RETURN:
                    i, j = board.selected
                    if board.cubes[i][j].temp != 0:
                        if board.place(board.cubes[i][j].temp):
                            print("Correct!")
                        else:
                            print("Incorrect, try again!")
                            strikes += 1
                        key = None

                        if board.is_finished():
                            print("Game over!")
                            run = False

                #the following "if" is for the enter on the number pad of your keyboard (K_KP_ENTER)
                #it also makes sure that the answer is correct before letting you enter it into the puzzle
                if event.key == pygame.K_KP_ENTER:
                    i, j = board.selected
                    if board.cubes[i][j].temp != 0:
                        if board.place(board.cubes[i][j].temp):
                            print("Correct!")
                        else:
                            print("Incorrect, try again!")
                            strikes += 1
                        key = None

                        if board.is_finished():
                            print("Game over!")
                            run = False

            #the following is for when you click your mouse
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = board.click(pos)
                if clicked:
                    board.select(clicked[0], clicked[1])
                    key = None

        if board.selected and key != None:
            board.sketch(key)

        redraw_window(win, board, play_time, strikes)
        pygame.display.update()


main()
pygame.quit()