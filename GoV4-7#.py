import numpy as np
import fileHandlingV1 as FH
BLANK = ""

class board():
    # length is the length/width of the board 
    # size is the no. of tiles in the board
    # the board is a numpy array of tiles
    # DO NOT edit blank copy, this is used to hopefully speed up the group detection algorithm
    # group detection is for use with the group detection algorithm, it will be reset by copying
    # blankCopy into it
    def __init__(self):
        self.length = 9
        self.size = self.length * self.length
        self.board = 0
        self.resetBoard()
        self.blankCopy = np.copy(self.board)
        self.groupDetection = np.copy(self.board)
    
    def setLength(self,length):
        self.length = length

    def getLength(self):
        return self.length
    
    def playTurn(self, x, y, player):
        index = (y*self.length) + x
        self.editTile(index,player.getValue())
        self.removeDeadTiles(player.invert())

    def resetBoard(self):
        self.board = np.empty(self.size, object)
        for index in range(self.size):
            self.board[index] = tile()
        self.initPointer(self.board)
        
    def initPointer(self,blank):
        for index in range(self.size):
            y,x = divmod(index,self.length)
            topX,topY = x,(y-1)
            rigX,rigY = (x+1),y
            botX,botY = x,(y+1)
            lefX,lefY = (x-1),y
            if topY < 0:
                blank[index].top = "f"
            else:
                topInd = topX+topY*self.length
                blank[index].top = topInd
            if rigX == self.length:
                blank[index].right = "f" 
            else:
                rigInd = rigX+rigY*self.length
                blank[index].right = rigInd
            if botY == self.length:
                blank[index].bottom = "f"
            else:
                botInd = botX+botY*self.length
                blank[index].bottom = botInd
            if lefX < 0:
                blank[index].left = "f"
            else:
                lefInd = lefX+lefY*self.length
                blank[index].left = lefInd
                
    def makePrintable(self):
        printable = [[BLANK for _ in range(self.length)] for _ in range(self.length)]
        for index in range(self.size):
            y,x = divmod(index,self.length)
            printable[y][x] = self.board[index].center.value
        return printable
    
    def printXIndex(self):
        print(" ", end = "")
        for n in range(1,self.length+1):
            if n > 9:
                print(f"  {n}",end = "")
            else:
                print(f"  {n}",end = " ")
        print()
        
    def processRow(self,board,y):
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
        board = self.makePrintable()
        self.printXIndex()
        for y in range(self.length):
            string = self.processRow(board,y)
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
        self.printXIndex()
        print("\n\n")
        
    def editTile(self,position,char):
        self.board[position].center.value = char
    
    # remove dead tiles beloning to player "player"
    def removeDeadTiles(self,player):
        for position in range(self.size):
            isGroup = self.checkIfGroup(position,player)
            if isGroup and self.board[position].center.value == player:
                self.removeDeadGroup(player,position)
            elif self.board[position].center.value == player:
                self.removeDeadTile(position)
       
    def checkIfGroup(self,position,player):
        surounds = self.board[position].getSurounds(self.board)
        if player in surounds:
            return True
        return False
    
    def removeDeadTile(self,position):
        if not(self.board[position].isAlive(self.board)):
            self.editTile(position,BLANK)
    
    def removeDeadGroup(self,player,position):
        y,x = divmod(position,self.length)
        newGroup = group(self.board,position,self.length)
        newGroup.checkIfGroupAlive(x, y, player, "checked")
        if newGroup.alive:
            self.floodFill(x,y,"checked",player)
        else:
            self.floodFill(x,y,"checked",BLANK)
            
    def checkValidMove(self,position):
        # must be improved for use with the AI
        if self.board[position].center.value != BLANK:
            return False
        elif self.__checkKo():
            return False
        return True
    
    def __checkKo(self):
        return False
        """
        if the last go removed one of your stones 
        then you are not allowd to play where your stone was removed from on the next move
        """
    
    def getScore(self,player):
        xScore = 0
        oScore = 0
        for tiles in self.board:
            if tiles.center.value == BLANK:
                surounds = tiles.getSurounds(self.board)
                xCount = surounds.count("x")
                oCount = surounds.count("o")
                if xCount > oCount:
                    xScore += 1
                elif xCount < oCount:
                    oScore += 1
        if player == "x":
            return xScore - oScore
        else:
            return oScore - xScore
        
    # found this pseudocode on freeCodeCamp (basicaly c++ not pseudocode)
    # it was fairly bad so this is it improved (i hope)
    def floodFill(self,x, y, targetCounter, replacmentCounter):
        currentValue = self.board[(x+(y*self.length))].center.value
        if currentValue != targetCounter:
            return
        
        self.board[(x+(y*self.length))].center.value = replacmentCounter
        
        if (x+1) < self.length:
            self.floodFill((x+1),y,targetCounter,replacmentCounter) # go right
        if x != 0:
            self.floodFill((x-1),y,targetCounter,replacmentCounter) # go left
        if (y+1) < self.length:
            self.floodFill(x,(y+1),targetCounter,replacmentCounter) # go up
        if y != 0:
            self.floodFill(x,(y-1),targetCounter,replacmentCounter) # go down

class tile():
    def __init__(self):
        self.center  = stone()
        self.right  = 0
        self.left   = 0
        self.top    = 0
        self.bottom = 0
           
    def getRight(self,board):
        if self.right == "f":
            return self.center.invert()
        else:
            return board[self.right].center.value
    
    def getTop(self,board):
        if self.top == "f":
            return self.center.invert()
        else:
            return board[self.top].center.value
    
    def getLeft(self,board):
        if self.left == "f":
            return self.center.invert()
        else:
            return board[self.left].center.value
        
    def getBottom(self,board):
        if self.bottom == "f":
            return self.center.invert()
        else:
            #print(self.bottom)
            return board[self.bottom].center.value
        
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
            if board[self.right].center.value != (self.center.invert()):
                return True
        except:
            pass
        try:
            if board[self.left].center.value != (self.center.invert()):
                return True 
        except:
            pass
        try:
            if board[self.top].center.value != (self.center.invert()):
                return True
        except:
            pass
        try:
            if board[self.bottom].center.value != (self.center.invert()):
                return True
        except:
            pass
        return False
      
class stone():
    def __init__(self):
        self.value = BLANK
    
    def setValue(self, value):
        self.value = value
    
    def getValue(self):
        return self.value
    
    def invert(self):
        if self.value == "x":
            return "o"
        elif self.value == "o":
            return "x"
        else:
            return -1
  
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
        
        self.board[(x+(y*self.length))].center.value = replacmentCounter
        
        surounds = self.board[(x+(y*self.length))].getSurounds(self.board)
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

# blank
class AI():
    def __init__(self):
        pass
        # blank ???


class game():
    def __init__(self):
        self.__mainBoard = board()
        self.__player = stone()
        self.__file = FH.fileHandler()
        
            
    def __printMenu(self):
        print("\n===================")
        print("S: save game")
        print("Q: quit game")
        print("P: print game")
        print("Enter: continue")
        print("===================\n")
        print("enter your Choice: ", end = "")

    def __getValidMove(self):
        length = self.__mainBoard.getLength()
        valid = False
        while not(valid):
            x = getValidInt(1,length,"enter M for menu or\nenter x: ",["M"]) 
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
        self.__player.setValue("x")
        self.__mainBoard.setLength(boardWidth)
        self.__mainBoard.resetBoard()
        won = False
        turnCounter = 0
        data = []
        while not(won):
            self.__mainBoard.printBoard()
            print("current score is " + str(self.__mainBoard.getScore(self.__player)))
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
            if x != -1:
                self.__mainBoard.playTurn(x,y,self.__player)
                turnCounter += 1
                data.append([x,y])
                self.__player.setValue(self.__player.invert())


    def __playExampleGame(self, filename, sgf, length):
        file = FH.fileHandler(sgf)
        data = file.readData(filename)
        mainBoard = board(length)
        player = stone()
        player.value = "x"
        print(data)
        for turn in data:
            index = int(((length - turn[1])*length) + (turn[0]-1))
            player.value = turn[2]
            mainBoard.editTile(index,player.value)
            player.value = player.invert()
            mainBoard.removeDeadTiles(player.value)
            mainBoard.removeDeadTiles(player.invert())
            mainBoard.printBoard()
            print(mainBoard.scoreBoard())

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
                        self.__playExampleGame(fName, (mainChoice==3), boardSize)
                        invalid = False
                    except:
                        print("Must be a valid file name.")
            elif mainChoice == 9:
                playing = False
    
# this is a general sub which returns a value inclusive of the two bounds entered
def getValidInt(mini,maxi,message, exceptions = []):
    while True:
        num = input(message)
        if num in exceptions:
            return num
        elif not(num.isnumeric()):
            print("must be a number")
        elif not(int(num) in range(mini,(maxi+1))):
            print(f"must be in range {mini} to {maxi}")
        else:
            return int(num)

if __name__ == "__main__":
    main = game()
    main.main()