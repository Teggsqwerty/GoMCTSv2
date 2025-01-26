import GoV6_1 as Go
import NandCV3_2 as NC
import GoMCTSV0_2 as MCTS

from tkinter import *

FONT = ("Segoe UI", 18) 

class rootWindow():
    def __init__(self, parent):
        self.__cont = Frame(parent)
        self.__cont.pack()

        self.__bar = topBar(self.__cont)

        self.__window = mainWindow(self.__cont)

class topBar():
    def __init__(self, parent):
        self.__cont = Frame(parent)
        self.__cont.pack()

class mainWindow():
    def __init__(self, parent):
        self.__cont = Frame(parent)
        self.__cont.pack()

        self.__gameWindow = game(self.__cont, LEFT)
        self.__statsBar = stats(self.__cont, LEFT)

class stats():
    def __init__(self, parent, direction):
        self.__cont = Frame(parent)
        self.__cont.pack(side = direction)

        self.__width = 20
        self.__height = 2

        self.__numNodes = 0 
        self.__numNodesLab = Label(self.__cont, text = f"number of nodes:\n{self.__numNodes}", font = FONT, width = self.__width , height = self.__height)
        self.__numNodesLab.pack(side = TOP)

        self.__winProb = 0 
        self.__winProbLab = Label(self.__cont, text = f"probibility of winning:\n{self.__winProb}", font = FONT, width = self.__width, height = self.__height)
        self.__winProbLab.pack(side = TOP)
        
        self.__maxDepth = 0 
        self.__maxDepthLab = Label(self.__cont, text = f"max search depth:\n{self.__maxDepth}", font = FONT, width = self.__width, height = self.__height)
        self.__maxDepthLab.pack(side = TOP)

        self.__maxBreadth = 0 
        self.__maxBreadthLab = Label(self.__cont, text = f"max search breadth:\n{self.__maxBreadth}", font = FONT, width = self.__width, height = self.__height)
        self.__maxBreadthLab.pack(side = TOP)

        self.__time = 0 
        self.__timeLab = Label(self.__cont, text = f"time taken:\n{self.__maxBreadth}", font = FONT, width = self.__width, height = self.__height)
        self.__timeLab.pack(side = TOP)


class game():
    def __init__(self, parent, direction):
        self.__cont = Frame(parent)
        self.__cont.pack(side = direction)

        

class goBoard():
    def __init__(self, parent):
        self.__cont = Frame(parent)
        self.__cont.pack()

class NCBoard():
    def __init__(self, parent):
        self.__cont = Frame(parent)
        self.__cont.pack()

        self.__blank = PhotoImage(file = "blank.png")
        self.__cross = PhotoImage(file = "cross.png")
        self.__naught = PhotoImage(file = "naught.png")

        self.__displayBoard = [[None for x in range(3)] for y in range(3)]
        

    def __initBoard(self):
        for y in range(3):
            for x in range(3):
                self.__displayBoard[y][x] = Button(self.__cont, image = self.blank)
                self.__displayBoard[y][x].grid(row = x, column = y)
                self.__displayBoard[y][x].bind("<Button-1>", self.__click)

    def __click(self,event):
        widget = event.widget
        self.x = widget.grid_info()['row']
        self.y = widget.grid_info()["column"]
        text = self.proccess()
        self.__updateGUI()
        
    def __updateGUI(self):
        for y in range(3):
            for x in range(3):
                if self.board.board[y][x] == "o":
                    self.displayBoard[y][x].configure(image = self.__naught)
                elif self.board.board[y][x] == "x":
                    self.displayBoard[y][x].configure(image = self.__cross)
                else:
                    self.displayBoard[y][x].configure(image = self.__blank)


if __name__ == "__main__":
    main = Tk()
    test = mainWindow(main)
    while 1:
        main.update()