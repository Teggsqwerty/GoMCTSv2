import GoV6_1 as Go
import NandCV3_2 as NC
import GoMCTSV0_2 as MCTS

from tkinter import *

FONT = ("Segoe UI", 18) 


class rootWindow():
    def __init__(self, parent):
        self.__cont = Frame(parent)
        self.__cont.pack()

        self.__bar = topBar(self.__cont, TOP)

        self.__window = mainWindow(self.__cont, TOP)

    def proccess(self):
        self.__bar.proccess()
        self.__window.proccess()

class topBar():
    def __init__(self, parent, direction):
        self.__cont = Frame(parent, highlightbackground = "black", highlightthickness = 3)
        self.__cont.pack(side = direction, anchor = W, pady = 5)
    
        self.__fileOptions = ["Save game", "Load game (step through)","Load game (outcome)"]
        self.__selectedFileOption = StringVar(value = "File")

        self.__file = OptionMenu(self.__cont, self.__selectedFileOption, *self.__fileOptions, command = lambda option: self.fileMenuHandler(self.__selectedFileOption))
        self.__file.pack(side = LEFT)

        self.__gameOptions = ["Clear Board", "Player 1: Human", "Player 2: Computer","Computer delay: 30ms"]
        self.__selectedGameOption = StringVar(value = "Game")

        self.__game = OptionMenu(self.__cont, self.__selectedGameOption, *self.__gameOptions, command = lambda option: self.gameMenuHandler(self.__selectedGameOption))
        self.__game.pack(side = LEFT)

        self.__fill = Label(self.__cont, width = 70)
        self.__fill.pack(side = LEFT)

    def fileMenuHandler(self, option):
        print(option.get())
        option.set("File")
    
    def gameMenuHandler(self, option):
        print(option.get())
        option.set("Game")
    
    def proccess(self):
        pass


class mainWindow():
    def __init__(self, parent, direction):
        self.__cont = Frame(parent)
        self.__cont.pack(side = direction)

        self.__statsBar = stats(self.__cont, RIGHT)
        self.__gameWindow = game(self.__cont, RIGHT)
    
    def proccess(self):
        stats = self.__gameWindow.proccess()
        self.__statsBar.proccess(stats)
        

class stats():
    def __init__(self, parent, direction):
        self.__cont = Frame(parent, highlightbackground = "black", highlightthickness = 3)
        self.__cont.pack(side = direction)

        self.__width = 20
        self.__height = 3

        self.__numNodes = 0 
        self.__numNodesLab = Label(self.__cont, text = f"number of nodes:\n{self.__numNodes}", font = FONT, width = self.__width , height = self.__height)
        self.__numNodesLab.pack(side = TOP)

        self.__winProb = 0 
        self.__winProbLab = Label(self.__cont, text = f"last minimax score:\n{self.__winProb}", font = FONT, width = self.__width, height = self.__height)
        self.__winProbLab.pack(side = TOP)
        
        self.__maxDepth = 0 
        self.__maxDepthLab = Label(self.__cont, text = f"max search depth:\n{self.__maxDepth}", font = FONT, width = self.__width, height = self.__height)
        self.__maxDepthLab.pack(side = TOP)

        self.__maxBreadth = 0 
        self.__maxBreadthLab = Label(self.__cont, text = f"max search breadth:\n{self.__maxBreadth}", font = FONT, width = self.__width, height = self.__height)
        self.__maxBreadthLab.pack(side = TOP)

        self.__time = 0 
        self.__timeLab = Label(self.__cont, text = f"time taken:\n{self.__time} (ns)", font = FONT, width = self.__width, height = self.__height)
        self.__timeLab.pack(side = TOP)

        self.__winning = "player 1"
        self.__winningLab = Label(self.__cont, text = f"currently winning:\n{self.__winning}", font = FONT, width = self.__width, height = self.__height)
        self.__winningLab.pack(side = TOP)
    
    def proccess(self,stats):
        if stats != None:
            self.__maxBreadth, self.__maxDepth, self.__numNodes, self.__time, self.__winProb = stats
            self.__numNodesLab.configure(text = f"number of nodes:\n{self.__numNodes}")
            self.__winProbLab.configure(text = f"last minimax score:\n{self.__winProb}")
            self.__maxDepthLab.configure(text = f"max search depth:\n{self.__maxDepth}")
            self.__maxBreadthLab.configure(text = f"max search breadth:\n{self.__maxBreadth}")
            self.__timeLab.configure(text = f"time taken:\n{self.__time} (ns)")

    def setNumNodes(self,val):
        self.__numNodes = val

    def setWinProb(self,val):
        self.__winProb = val
    
    def setMaxDepth(self,val):
        self.__maxDepth = val

    def setMaxBreadth(self,val):
        self.__maxBreadth = val
    
    def setTime(self,val):
        self.__time = val

    def setWinning(self,val):
        self.__winning = val


class game():
    def __init__(self, parent, direction):
        self.__cont = Frame(parent, padx = 15)
        self.__cont.pack(side = direction)

        self.__test = NCBoard(self.__cont)
    
    def proccess(self):
        return self.__test.proccess()
        

class goBoard():
    def __init__(self, parent):
        self.__cont = Frame(parent)
        self.__cont.pack()

        self.__size = 9

        self.__initBoard()

    def __initBoard(self):
        if self.__size <= 10:
            self.__width = 70
        elif self.__size <= 13:
            self.__width = 60
        elif self.__size <= 16:
            self.__width = 50
        else:
            self.__width = 40

        self.__blank = PhotoImage(file = f"images\\goBlank{self.__width}.png")
        self.__white = PhotoImage(file = f"images\\goWhite{self.__width}.png")
        self.__black = PhotoImage(file = f"images\\goBlack{self.__width}.png")

        self.__displayBoard = [[Button(self.__cont, image = self.__blank, highlightthickness = 0, bd = 0) for x in range(self.__size)] for y in range(self.__size)]

        for y in range(self.__size):
            for x in range(self.__size):
                self.__displayBoard[y][x].grid(row = x, column = y)
                self.__displayBoard[y][x].bind("<Button-1>", self.__click)

    def __click(self,event):
        widget = event.widget
        x = widget.grid_info()['row']
        y = widget.grid_info()["column"]
        print(x,y)
        # text = self.proccess()
        # self.__updateGUI()
        
    
    # def __updateGUI(self):
    #     for y in range(3):
    #         for x in range(3):
    #             if self.board.board[y][x] == "o":
    #                 self.displayBoard[y][x].configure(image = self.__naught)
    #             elif self.board.board[y][x] == "x":
    #                 self.displayBoard[y][x].configure(image = self.__cross)
    #             else:
    #                 self.displayBoard[y][x].configure(image = self.__blank)

class NCBoard():
    def __init__(self, parent):
        self.__cont = Frame(parent)
        self.__cont.pack()

        self.__blank = PhotoImage(file = "images\\blank.png")
        self.__cross = PhotoImage(file = "images\\cross.png")
        self.__naught = PhotoImage(file = "images\\naught.png")
        
        self.__board = NC.NandC()

        self.__buff = ring()
        self.__initBoard()

    def __initBoard(self):
        self.__displayBoard = [[Button(self.__cont, image = self.__blank, highlightthickness = 0, bd = 0) for x in range(3)] for y in range(3)]
        for y in range(3):
            for x in range(3):
                self.__displayBoard[y][x].grid(row = x, column = y)
                self.__displayBoard[y][x].bind("<Button-1>", self.__click)
        
        self.__infoBar = Label(self.__cont, text = "can player 1 (X) please play", font = ("Arial",18))
        self.__infoBar.grid(row = 3, column = 0, pady = 5, columnspan = 3)

    def __click(self,event):
        widget = event.widget
        x = widget.grid_info()['row']
        y = widget.grid_info()["column"]
        success = self.__buff.push((x,y))
    
    def proccess(self):
        event = self.__buff.pop()
        if event != False:
            x,y = event
            text = self.__board.proccesing(x,y)
            self.__infoBar.configure(text = text)
            self.__updateGUI()
            return self.__board.getStats()
    
    def __updateGUI(self):
        board = self.__board.getBoard()
        for y in range(3):
            for x in range(3):
                if board[y][x] == "o":
                    self.__displayBoard[y][x].configure(image = self.__naught)
                elif board[y][x] == "x":
                    self.__displayBoard[y][x].configure(image = self.__cross)
                else:
                    self.__displayBoard[y][x].configure(image = self.__blank)
    

class ring():
    """ ring buffer for use with the ISRs"""
    def __init__(self):
        self.__buffer = [None for _ in range(256)]
        self.__rdptr = 0
        self.__wrptr = 0

    def push(self,val):
        if not(self.isFull()):
            self.__buffer[self.__wrptr] = val
            self.__wrptr += 1
            return True
        else:
            return False
    
    def pop(self):
        if not(self.isEmpty()):
            val = self.__buffer[self.__rdptr]
            self.__rdptr += 1
            return val
        else:
            return False

    def isEmpty(self):
        if self.__wrptr == self.__rdptr:
            return True
        return False
    
    def isFull(self):
        if self.__wrptr == (self.__rdptr - 1):
            return True
        if self.__wrptr == 255 and self.__rdptr == 0:
            return True
        return False

if __name__ == "__main__":
    width = 1200
    height = 900
    main = Tk()
    main.resizable(0,0)
    #main.geometry(f"{width}x{height}")
    main.title("Go Compare")
    test = mainWindow(main,TOP)
    exists = True
    while exists:
        test.proccess()
        main.update()
        try:
            main.winfo_exists()
        except:
            exists = False