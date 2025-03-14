import NandCV5_0 as NC
import GoMCTSV2_0 as GO

from tkinter import *
from tkinter import filedialog

FONT   = ("Segoe UI", 18) 
WIDTH  = 1100
HEIGHT = 870

class rootWindow():
    def __init__(self, parent):
        self.__cont = Frame(parent)
        self.__cont.pack()

        self.__bar = topBar(self.__cont, TOP)

        self.__window = mainWindow(self.__cont, TOP)

    def proccess(self):
        topBarChoice = self.__bar.proccess()
        options, changed = self.__window.proccess(topBarChoice)
        if changed:
            self.__bar.setGameOptions(options)

class topBar():
    def __init__(self, parent, direction):
        self.__cont = Frame(parent, highlightbackground = "black", highlightthickness = 3)
        self.__cont.pack(side = direction, anchor = W, pady = 5)
    
        self.__fileOptions = ["Save game", "Load game (outcome)"]
        self.__selectedFileOption = StringVar(value = "File")

        self.__file = OptionMenu(self.__cont, self.__selectedFileOption, *self.__fileOptions, command = lambda option: self.fileMenuHandler(self.__selectedFileOption))
        self.__file.pack(side = LEFT)

        self.__gameOptions = ["Clear Board", "Player 1: Human", "Player 2: Computer","Switch Game", "Toggle Board Size"]
        self.__selectedGameOption = StringVar(value = "Game")

        self.__initGameOptions()
        self.__buff = ring()

    def __initGameOptions(self):
        self.__game = OptionMenu(self.__cont, self.__selectedGameOption, *self.__gameOptions, command = lambda option: self.gameMenuHandler(self.__selectedGameOption))
        self.__game.pack(side = LEFT)

        self.__fill = Label(self.__cont, width = 950)
        self.__fill.pack(side = LEFT)

    def setGameOptions(self,options):
        self.__gameOptions = options
        self.__game.destroy()
        self.__fill.destroy()
        self.__initGameOptions()

    def fileMenuHandler(self, option):
        #print(option.get())
        self.__buff.push(option.get())
        option.set("File")
    
    def gameMenuHandler(self, option):
        #print(option.get())
        self.__buff.push(option.get())
        option.set("Game")
    
    def proccess(self):
        return self.__buff.pop()
        
class mainWindow():
    def __init__(self, parent, direction):
        self.__cont = Frame(parent)
        self.__cont.pack(side = direction)

        self.__statsBar = stats(self.__cont, RIGHT)
        self.__gameWindow = game(self.__cont, RIGHT)
    
    def proccess(self, topBarChoice):
        stats, options, changed = self.__gameWindow.proccess(topBarChoice)
        self.__statsBar.proccess(stats)
        return options, changed

class stats():
    def __init__(self, parent, direction):
        self.__cont = Frame(parent, highlightbackground = "black", highlightthickness = 3)
        self.__cont.pack(side = direction)

        self.__width = 20
        self.__height = 5

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

        # self.__winning = "player 1"
        # self.__winningLab = Label(self.__cont, text = f"currently winning:\n{self.__winning}", font = FONT, width = self.__width, height = self.__height)
        # self.__winningLab.pack(side = TOP)
    
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

        self.__isGo = True
        self.__game = goBoard(self.__cont,9)

        self.__gameOptions = ["Clear Board", "Player 1: Human", "Player 2: Computer","Switch Game", "Toggle Board Size"]

        self.__allowedSizes = [9,13,15,17,19]
        self.__sizeCount = 0

    def proccess(self,topBarChoice):
        changed = False
        if topBarChoice == False:
            pass
        elif topBarChoice == "Toggle Board Size" and self.__isGo:
            self.__toggleSize()
            changed = True
        elif topBarChoice == "Save game":
            self.__saveGame()
        elif topBarChoice == "Load game (outcome)":
            self.__loadGame()
        elif topBarChoice == "Player 1: Human":
            self.__game.setPlayer1(False)
            self.__gameOptions[1] = "Player 1: Computer"
            changed = True
        elif topBarChoice == "Player 1: Computer":
            self.__game.setPlayer1(True)
            self.__gameOptions[1] = "Player 1: Human"
            changed = True
        elif topBarChoice == "Player 2: Human":
            self.__game.setPlayer2(False)
            self.__gameOptions[2] = "Player 2: Computer"
            changed = True
        elif topBarChoice == "Player 2: Computer":
            self.__game.setPlayer2(True)
            self.__gameOptions[2] = "Player 2: Human"
            changed = True
        elif topBarChoice == "Switch Game" and self.__isGo:
            self.__game.destroy()
            self.__isGo = False
            self.__game = NCBoard(self.__cont)
            self.__gameOptions[1] = "Player 1: Human"
            self.__gameOptions[2] = "Player 2: Computer"
            changed = True
        elif topBarChoice == "Switch Game":
            self.__game.destroy()
            self.__isGo = True
            self.__game = goBoard(self.__cont,self.__allowedSizes[self.__sizeCount])
            self.__gameOptions[1] = "Player 1: Human"
            self.__gameOptions[2] = "Player 2: Computer"
            changed = True
        return self.__game.proccess(topBarChoice), self.__gameOptions, changed
    
    def __toggleSize(self):
        self.__sizeCount += 1
        if self.__sizeCount == len(self.__allowedSizes):
            self.__sizeCount = 0
        self.__game.destroy()
        self.__game = goBoard(self.__cont,self.__allowedSizes[self.__sizeCount])
        self.__gameOptions[1] = "Player 1: Human"
        self.__gameOptions[2] = "Player 2: Computer"

    def __saveGame(self):
        filePath = filedialog.asksaveasfilename(title = "Save As", filetypes = [ ("Smart Game Format", "*.sgf")]) # maybe could be extended to use my txt file format. ("Text files", "*.txt"),
        self.__game.saveGame(filePath)
    
    def __loadGame(self):
        filePath = filedialog.askopenfilename(title = "Select File", filetypes = [ ("Smart Game Format", "*.sgf")]) # maybe could be extended to use my txt file format. ("Text files", "*.txt"),
        try:
            self.__game.loadGame(filePath)
        except:
            pass

class goBoard():
    def __init__(self, parent, size):
        self.__cont = Frame(parent)
        self.__cont.pack()

        self.__parent = parent

        self.__size = size
        
        self.__board = GO.GO()

        self.__buff = ring()
        
        self.init()
        
    def init(self):
        self.__board.setSize(self.__size)
        self.__board.reset()
        if self.__size == 9:
            self.__width = 70
            self.__cont.configure(padx = 83)
        elif self.__size == 13:
            self.__width = 60
            self.__cont.configure(padx = 15)
        elif self.__size == 15:
            self.__width = 50
            self.__cont.configure(padx = 27)
        elif self.__size == 17:
            self.__width = 45
            self.__cont.configure(padx = 15)
        else:
            self.__width = 40
            self.__cont.configure(padx = 15)

        self.__blank = PhotoImage(file = f"images\\goBlank{self.__width}.png")
        self.__white = PhotoImage(file = f"images\\goWhite{self.__width}.png")
        self.__black = PhotoImage(file = f"images\\goBlack{self.__width}.png")

        self.__displayBoard = [[Button(self.__cont, image = self.__blank, highlightthickness = 0, bd = 0) for x in range(self.__size)] for y in range(self.__size)]

        for y in range(self.__size):
            for x in range(self.__size):
                self.__displayBoard[y][x].grid(row = x, column = y)
                self.__displayBoard[y][x].bind("<Button-1>", self.__click)

        self.__infoBar = Label(self.__cont, text = "can player 1 (X) please play", font = ("Arial",18))
        self.__infoBar.grid(row = (self.__size + 1), column = 0, pady = 5, columnspan = self.__size)

        

    def setPlayer1(self,val):
        self.__board.setPlayer1(val)

    def setPlayer2(self,val):
        self.__board.setPlayer2(val)

    def __click(self,event):
        widget = event.widget
        x = widget.grid_info()['row']
        y = widget.grid_info()["column"]
        success = self.__buff.push((x,y))
    
    def __clear(self):
        self.__board.reset()
        self.__infoBar.configure(text = "can player 1 (X) please play")
        for y in range(self.__size):
            for x in range(self.__size):
                self.__displayBoard[y][x].configure(image = self.__blank)

    def proccess(self,topOpt):
        if topOpt != False:
            if topOpt == "Clear Board":
                self.__clear()
        event = self.__buff.pop()
        if event != False:
            x,y = event
            text = self.__board.proccesing(x,y)
            self.__infoBar.configure(text = text)
            self.__updateGUI()
            return self.__board.getStats()
    
    def __updateGUI(self):
        board = self.__board.getBoard()
    
        for y in range(self.__size):
            for x in range(self.__size):
                index = (y*self.__size) + x
                if board[index].center.getValue() == "o":
                    self.__displayBoard[y][x].configure(image = self.__black)
                elif board[index].center.getValue() == "x":
                    self.__displayBoard[y][x].configure(image = self.__white)
                else:
                    self.__displayBoard[y][x].configure(image = self.__blank)

    def saveGame(self,filename):
        self.__board.saveGame(filename)
    
    def loadGame(self,filename):
        self.__board.loadGame(filename)
        self.__updateGUI()

    def destroy(self):
        self.__cont.destroy()
        self.__infoBar.destroy()

class NCBoard():
    def __init__(self, parent):
        self.__cont = Frame(parent, padx = 180)
        self.__cont.pack()

        self.__blank = PhotoImage(file = "images\\blank.png")
        self.__cross = PhotoImage(file = "images\\cross.png")
        self.__naught = PhotoImage(file = "images\\naught.png")
        
        self.__board = NC.NandC()

        self.__buff = ring()
        self.__initBoard()

    def __initBoard(self):
        self.__board.reset()
        self.__displayBoard = [[Button(self.__cont, image = self.__blank, highlightthickness = 0, bd = 0) for x in range(3)] for y in range(3)]
        for y in range(3):
            for x in range(3):
                self.__displayBoard[y][x].grid(row = x, column = y)
                self.__displayBoard[y][x].bind("<Button-1>", self.__click)
        
        self.__infoBar = Label(self.__cont, text = "can player 1 (X) please play", font = ("Arial",18))
        self.__infoBar.grid(row = 3, column = 0, pady = 5, columnspan = 3)
    
    def setPlayer1(self,val):
        self.__board.setPlayer1(val)

    def setPlayer2(self,val):
        self.__board.setPlayer2(val)

    def __clear(self):
        self.__board.reset()
        self.__infoBar.configure(text = "can player 1 (X) please play")
        for y in range(3):
            for x in range(3):
                self.__displayBoard[y][x].configure(image = self.__blank)

    def __click(self,event):
        widget = event.widget
        x = widget.grid_info()['row']
        y = widget.grid_info()["column"]
        success = self.__buff.push((x,y))
    
    def proccess(self,topOpt):
        if topOpt != False:
            if topOpt == "Clear Board":
                self.__clear()
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
    
    def destroy(self):
        self.__cont.destroy()
        self.__infoBar.destroy()

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
            if self.__wrptr > 255:
                self.__wrptr = 0
            return True
        else:
            return False
    
    def pop(self):
        if not(self.isEmpty()):
            val = self.__buffer[self.__rdptr]
            self.__rdptr += 1
            if self.__rdptr > 255:
                self.__rdptr = 0
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
    main = Tk()
    main.resizable(0,0)
    main.geometry(f"{WIDTH}x{HEIGHT}")
    main.title("Go Compare")
    test = rootWindow(main)
    exists = True
    while exists:
        test.proccess()
        main.update()
        try:
            main.winfo_exists()
        except:
            exists = False

    