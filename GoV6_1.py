import numpy as np
from basicImports import *
import matplotlib.pyplot as plt
import fileHandlingV1 as FH

class board():
    # length is the length/width of the board 
    # size is the no. of tiles in the board
    # the board is a numpy array of tiles
    # DO NOT edit blank copy, this is used to hopefully speed up the group detection algorithm
    # group detection is for use with the group detection algorithm, it will be reset by copying
    # blankCopy into it
    def __init__(self):
        # basic game variables
        self.length = 9
        self.size = self.length * self.length
        self.__board = 0

        # no of stones removed for each player
        self.xLoses = 0
        self.oLoses = 0

        # used to check ko rule
        self.oneDeadStone = False
        self.lastRemStoneLoc = -1 # index position rather than cartesian

        # used to count no of changed tiles in the flood fill 
        self.__noChangedTiles = 0

        # reset before a game
        self.resetBoard()
    
    def setLength(self,length):
        self.length = length

    def getLength(self):
        return self.length
    
    def getBoard(self):
        return self.__board
    
    def setBoard(self,new):
        newBoard = new.getBoard()
        for x in range(self.size):
            if newBoard[x].center.value == "x":
                self.__board[x].center.value = "x"
            elif newBoard[x].center.value == "o":
                self.__board[x].center.value = "o"
            else:
                self.__board[x].center.value = BLANK

    def playTurn(self, x, y, player): # returns wether or not the move was valid
        index = (y*self.length) + x
        inverse = player.getInverse()
        playerVal = player.getValue()
        valid = self.checkValidMove(index, inverse)  
        if valid:
            self.editTile(index,playerVal)
            self.removeDeadTiles(inverse,index)
            self.removeSingleDeadTile(playerVal,index)
            if self.__board[index].center.value == player.value:
                return True
            return False
        return False

    def playTurnIndex(self, index, player): # returns wether or not the move was valid
        inverse = player.getInverse()
        playerVal = player.getValue()
        valid = self.checkValidMove(index, inverse)  
        if valid:
            self.editTile(index,playerVal)
            self.removeDeadTiles(inverse,index)
            self.removeSingleDeadTile(playerVal,index)
            if self.__board[index].center.value == player.value:
                return True
            return False
        return False
    
    def resetBoard(self):
        self.size = self.length * self.length
        self.__board = np.empty(self.size, object)
        for index in range(self.size):
            self.__board[index] = tile()
        self.initPointer()

        self.xLoses = 0
        self.oLoses = 0
        self.oneDeadStone = False
        self.lastRemStoneLoc = -1

    def initPointer(self):
        for index in range(self.size):
            y,x = divmod(index,self.length)
            topX,topY = x,(y-1)
            rigX,rigY = (x+1),y
            botX,botY = x,(y+1)
            lefX,lefY = (x-1),y
            if topY < 0:
                self.__board[index].top = "f"
            else:
                topInd = topX+topY*self.length
                self.__board[index].top = topInd
            if rigX == self.length:
                self.__board[index].right = "f" 
            else:
                rigInd = rigX+rigY*self.length
                self.__board[index].right = rigInd
            if botY == self.length:
                self.__board[index].bottom = "f"
            else:
                botInd = botX+botY*self.length
                self.__board[index].bottom = botInd
            if lefX < 0:
                self.__board[index].left = "f"
            else:
                lefInd = lefX+lefY*self.length
                self.__board[index].left = lefInd
                
    def __makePrintable(self):
        printable = [[BLANK for _ in range(self.length)] for _ in range(self.length)]
        for index in range(self.size):
            y,x = divmod(index,self.length)
            printable[y][x] = self.__board[index].center.value
        return printable
    
    def __printXIndex(self):
        print(" ", end = "")
        for n in range(1,self.length+1):
            if n > 9:
                print(f"  {n}",end = "")
            else:
                print(f"  {n}",end = " ")
        print()
        
    def __processRow(self,board,y):
        string = BLANK
        for x in range(self.length):
            if (board[y][x] == "x"):
                string += "X"
            elif (board[y][x] == "o"):
                string += "O"
            elif (board[y][x] == BLANK):
                string += " "
            else:
                string += "b"
            string += "---"
        return string[:-3]
    
    def printBoard(self):
        board = self.__makePrintable()
        self.__printXIndex()
        for y in range(self.length):
            string = self.__processRow(board,y)
            printedY = (self.length - y)
            if printedY < 10:
                print(printedY,"  ", string,"  ",printedY,sep = "")
            else:
                print(printedY," ",string," ",printedY,sep = "")
            string = BLANK
            if y != (self.length-1):
                for _ in range(self.length):
                    string += " |  "
                print(" ",string)
        self.__printXIndex()
        print("\n\n")
        
    def editTile(self,position,char):
        self.__board[position].center.value = char
    
    # remove dead tiles beloning to "player" surounding "location"
    def removeDeadTiles(self,player,location):
        self.lastRemStoneLoc = -1
        self.oneDeadStone = False
        deadStones = 0 
        tiles = self.__board[location].getSuroundLocations()
        #tiles += (location,) # i dont think this is needed 
        for position in tiles:
            if position != "f":
                if self.__board[position].center.value == player:
                    isGroup = self.checkIfGroup(position,player)
                    if isGroup:
                        deadStones = self.removeDeadGroup(player,position)
                    else:
                        deadStones = self.removeDeadTile(position)

        self.__updateDeadStones(player,deadStones)
    
    def removeSingleDeadTile(self,player,location):
        isGroup = self.checkIfGroup(location,player)
        if isGroup:
            y,x = divmod(location,self.length)
            newGroup = group(self.__board, location, self.length)
            newGroup.checkIfGroupAlive(x, y, player, "checked")
            self.__floodFill(x,y,"checked",player)
            if not(newGroup.alive):
                self.__board[location].center.value = BLANK

    def __updateDeadStones(self,player,noDead):
        if player == "x":
            self.xLoses += noDead
        else:
            self.oLoses += noDead

    def checkIfGroup(self,position,player):
        if player in self.__board[position].getSurounds(self.__board):
            return True
        return False
    
    def removeDeadTile(self,position):
        if not(self.__board[position].isAlive(self.__board)):
            self.editTile(position,BLANK)
            self.lastRemStoneLoc = position
            self.oneDeadStone = True
            return 1
        return 0
    
    def removeDeadGroup(self,player,position):
        self.__noChangedTiles = 0
        y,x = divmod(position,self.length)
        newGroup = group(self.__board, position, self.length)
        newGroup.checkIfGroupAlive(x, y, player, "checked")
        if newGroup.alive:
            self.__floodFill(x,y,"checked",player)
            self.__noChangedTiles = 0
        else:
            self.__floodFill(x,y,"checked",BLANK)
        return self.__noChangedTiles
            
    def checkValidMove(self,position,inverse):
        if self.__checkSurounds(position, inverse):
            return False
        if self.__board[position].center.value != BLANK:
            return False
        if self.__checkKo(position):
            return False
        return True
    
    # returns False if it IS a valid move
    def __checkSurounds(self, position, inverse):
        for i in self.__board[position].getSuroundLocations():
            if i != "f" and self.__board[i].center.value != inverse:
                return False
        return True
    
    def __checkKo(self, position):
        if self.oneDeadStone and position == self.lastRemStoneLoc:
            return True
        return False
        """
        if the last go removed one of your stones 
        then you are not allowed to play where your stone was removed from on the next move
        """
    
    def getScore(self,player):
        xScore = 0
        oScore = 0
        for tiles in self.__board:
            if tiles.center.value == BLANK:
                surounds = tiles.getSurounds(self.__board)
                xCount = surounds.count("x")
                oCount = surounds.count("o")
                if xCount > oCount:
                    xScore += 1
                elif xCount < oCount:
                    oScore += 1
            elif tiles.center.value == "x":
                xScore += 1
            else:
                oScore += 1
        if player == "x":
            return (xScore - oScore) + self.oLoses
        else:
            return (oScore - xScore) + self.xLoses
        
    # found this pseudocode on freeCodeCamp (basicaly c++ not pseudocode)
    # it was fairly bad so this is it improved (i hope)
    def __floodFill(self,x, y, targetCounter, replacmentCounter):
        currentValue = self.__board[(x+(y*self.length))].center.value
        if currentValue != targetCounter:
            return
        
        self.__board[(x+(y*self.length))].center.value = replacmentCounter
        self.__noChangedTiles += 1

        if (x+1) < self.length:
            self.__floodFill((x+1),y,targetCounter,replacmentCounter) # go right
        if x != 0:
            self.__floodFill((x-1),y,targetCounter,replacmentCounter) # go left
        if (y+1) < self.length:
            self.__floodFill(x,(y+1),targetCounter,replacmentCounter) # go up
        if y != 0:
            self.__floodFill(x,(y-1),targetCounter,replacmentCounter) # go down

class tile():
    def __init__(self):
        self.center  = stone()
        self.right  = 0
        self.left   = 0
        self.top    = 0
        self.bottom = 0
        
    def getRightLocation(self):
        return self.right

    def getRight(self,board):
        if self.right == "f":
            return self.center.getInverse()
        else:
            return board[self.right].center.value
    
    def getTopLocation(self):
        return self.Top

    def getTop(self,board):
        if self.top == "f":
            return self.center.getInverse()
        else:
            return board[self.top].center.value
    
    def getLeftLocation(self):
        return self.left

    def getLeft(self,board):
        if self.left == "f":
            return self.center.getInverse()
        else:
            return board[self.left].center.value
        
    def getBottomLocation(self):
        return self.bottom

    def getBottom(self,board):
        if self.bottom == "f":
            return self.center.getInverse()
        else:
            return board[self.bottom].center.value
    
    def getSuroundLocations(self):
        return self.top, self.right, self.bottom, self.left

    def getSurounds(self,board):
        tValue = self.getTop(board)
        rValue = self.getRight(board)
        bValue = self.getBottom(board)
        # not changed in previous versions from 
        # lValue = self.getRight(board)
        # may be the cause of some major errors in previous version
        lValue = self.getLeft(board)
        return tValue,rValue,bValue,lValue

    def isAlive(self,board):
        try:
            if board[self.right].center.value != (self.center.getInverse()):
                return True
        except:
            pass
        try:
            if board[self.left].center.value != (self.center.getInverse()):
                return True 
        except:
            pass
        try:
            if board[self.top].center.value != (self.center.getInverse()):
                return True
        except:
            pass
        try:
            if board[self.bottom].center.value != (self.center.getInverse()):
                return True
        except:
            pass
        return False
      
  
class group():
    def __init__(self,board,position,length):
        self.board = board
        self.position = position
        self.length = length

        self.alive = False
        
    # group detection algorithm to check if a group is alive
    # based on the flood fill algorithm.
    # a single counter in a group is only dead if
    # it has no free adjacent tiles.
    # a group is only dead if all the tiles in it are dead.
    def checkIfGroupAlive(self,x, y, targetCounter, replacmentCounter):
        currentValue = self.board[(x+(y*self.length))].center.value
        if currentValue != targetCounter or self.alive:
            return
    
        surounds = self.board[(x+(y*self.length))].getSurounds(self.board) # previous versions had this 

        self.board[(x+(y*self.length))].center.value = replacmentCounter   # and this line the other way round which caused an error when checking tiles on the edge of the board

        if BLANK in surounds:
            self.alive = True
        if (x+1) < self.length:
            self.checkIfGroupAlive((x+1),y,targetCounter,replacmentCounter) # go right
        if x != 0:    
            self.checkIfGroupAlive((x-1),y,targetCounter,replacmentCounter) # go left
        if (y+1) < self.length:
            self.checkIfGroupAlive(x,(y+1),targetCounter,replacmentCounter) # go up
        if y != 0:
            self.checkIfGroupAlive(x,(y-1),targetCounter,replacmentCounter) # go down

class game(): # used only for text based testing
    def __init__(self):
        self.__mainBoard = board()
        self.__player = stone()
        self.__file = FH.fileHandler() 
            
    def __printMenu(self):
        print("\n=========================")
        print("S: save game")
        print("Q: quit game")
        print("P: print game")
        print("D: Display Score Graph")
        print("Enter: continue")
        print("=========================\n")
        print("enter your Choice: ", end = "")

    def __getValidMove(self):
        length = self.__mainBoard.getLength()
        valid = False
        while not(valid):
            x = getValidInt(1,length,"enter x: ",["M"]) 
            if x != "M":
                x -= 1
                y = getValidInt(1,length,"enter y: ") 
                y = length - y
                print()
                index = (y*length) + x
                valid = self.__mainBoard.checkValidMove(index)
                if not(valid):
                    print("must be a valid move!")
                else:
                    return x,y
            else:
                return x,0
        
    def __playGameTxt(self, boardWidth):
        test = stone() # used for testing
        test.setValue("x") # used for testing
        self.__player.setValue("x")
        self.__mainBoard.setLength(boardWidth)
        self.__mainBoard.resetBoard()
        won = False
        turnCounter = 0
        scores = [0]
        data = []
        while not(won):
            self.__mainBoard.printBoard()
            #print("current score is " + str(self.__mainBoard.getScore(test))) # "test" used just for testing
            print(f"it is player {self.__player.getValue()}'s turn.\n")
            x = "M"
            while x == "M":
                x,y = self.__getValidMove()
                if x == "M":
                    self.__printMenu()
                    Choice = input()
                    if Choice == "S":
                        filename = input("enter save game name: ")
                        self.__file.saveData(data,filename)
                    elif Choice == "Q": # hello world
                        won = True
                        x == -1
                    elif Choice == "P":
                        print(data)
                    elif Choice == "D":
                        self.__graphScore(scores)
                    print(won)
            if x != -1:
                self.__mainBoard.playTurn(x,y,self.__player)
                turnCounter += 1
                data.append([x,y])
                self.__player.setValue(self.__player.getInverse())
                scores.append(self.__mainBoard.getScore(test))

    def __loadExampleGame(self, filename, sgf, boardWidth):
        test = stone() # used for testing
        test.setValue("x") # used for testing

        self.__player.setValue("x")
        self.__mainBoard.setLength(boardWidth)
        self.__mainBoard.resetBoard()

        won = False
        turnCounter = 0
        scores = [0]
        data = []

        self.__file.setFileType(sgf)
        fileData, error = self.__file.readData(filename)

        if error != "":
            raise Exception(error)

        for turn in fileData:
            y = boardWidth - turn[1]
            x = turn[0] - 1
            data.append([x,y])
            self.__mainBoard.playTurn(x,y,self.__player)
            
            self.__player.invert()
            scores.append(self.__mainBoard.getScore(test))
            # self.__mainBoard.printBoard()
            # print("current score is " + str(self.__mainBoard.getScore(test)))

        while not(won):
            self.__mainBoard.printBoard()
            print("current score is " + str(self.__mainBoard.getScore(test))) # "test" used just for testing
            print(f"it is player {self.__player.getValue()}'s turn.\n")
            x = "M"
            while x == "M":
                x,y = self.__getValidMove()
                if x == "M":
                    self.__printMenu()
                    Choice = input()
                    if Choice == "S":
                        filename = input("enter save game name: ")
                        self.__file.saveData(data,filename)
                    elif Choice == "Q": # hello world
                        won = True
                        x == -1
                    elif Choice == "P":
                        print(data)
                    elif Choice == "D":
                        self.__graphScore(scores)
            if x != -1:
                self.__mainBoard.playTurn(x,y,self.__player)
                scores[turnCounter] = self.__mainBoard.getScore(test)
                turnCounter += 1
                data.append([x,y])
                self.__player.setValue(self.__player.getInverse())
            

        
    def __getMainMenuChoice(self):
        while True:
            print("=============================")
            print("My GO game!")
            print("1: play 2 player game")
            print("2: load an example game(.txt)")
            print("3: load an example game(.sgf)")
            print("9: quit")
            print("==============================\n")
            return getValidInt(1,3,"enter your choice: ",[9])
    
    def __graphScore(self,scores):
        y = np.array(scores)
        i = 2
        z = []
        for x in range(i,len(scores)):
            z.append(np.std(y[(x-i):x]))
        n = 0.
        for x in range(len(z)):
            if z[x] < n:
                print("done",x)
        #plt.plot(y)
        plt.plot(z)
        plt.show()

    def main(self):
        playing = True
        while playing:
            mainChoice = self.__getMainMenuChoice()
            if mainChoice == 1:
                boardSize = getValidInt(1,19,"Enter the board size (1,19): ")
                self.__playGameTxt(boardSize)
            elif mainChoice in [2,3]:
                boardSize = getValidInt(1,19,"Enter the board size for the file(1,19): ")
                invalid = True
                while invalid:
                    fName = input("Enter a valid file name: ")
                    try:
                        self.__loadExampleGame(fName, (mainChoice==3), boardSize)
                        invalid = False
                    except:
                        print("Must be a valid file name.")
            elif mainChoice == 9:
                playing = False
    

    
if __name__ == "__main__":
    main = game()
    main.main()
    play = stone()
    play.setValue("x")
    test = board()
    test.resetBoard()

    test.playTurnIndex(1,play)
    test.playTurnIndex(10,play)
    test.playTurnIndex(18,play)

    play.invert()

    test.playTurnIndex(9,play)
    test.printBoard()
    print(test.playTurnIndex(0,play))
    test.printBoard()             # for testing stone validation on the edge

