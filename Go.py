import numpy as np
from basicImports import *
import matplotlib.pyplot as plt
import fileHandling as FH

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
        return self.playTurnIndex(index,player)

    def playTurnIndex(self, index, player): # returns wether or not the move was valid
        inverse = player.getInverse()
        playerVal = player.getValue()
        valid = self.checkValidMove(index)  
        if valid:
            self.__board[index].center.value = playerVal
            self.__removeDeadTiles(inverse,index)
            self.__removeSingleDeadTile(playerVal,index)
            if self.__checkSurounds(index,inverse):
                self.__board[index].center.value = BLANK
                return False
            if self.__board[index].center.value == player.value:
                return True
            return False
        return False
    
    def resetBoard(self):
        self.size = self.length * self.length
        self.__board = np.empty(self.size, object)
        for index in range(self.size):
            self.__board[index] = tile()
        self.__initPointer()

        self.xLoses = 0
        self.oLoses = 0
        self.oneDeadStone = False
        self.lastRemStoneLoc = -1

    def __initPointer(self):
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
    
    # remove dead tiles beloning to "player" surounding "location"
    def __removeDeadTiles(self,player,location):
        self.lastRemStoneLoc = -1
        self.oneDeadStone = False
        noDead = 0 
        tiles = self.__board[location].getSuroundLocations()
        for position in tiles:
            if position != "f":
                if self.__board[position].center.value == player:
                    if player in self.__board[position].getSurounds(self.__board):
                        noDead = self.removeDeadGroup(player,position)
                    else:
                        noDead = self.removeDeadTile(position)

        if player == "x":
            self.xLoses += noDead
        else:
            self.oLoses += noDead
    
    def __removeSingleDeadTile(self,player,location):
        if player in self.__board[location].getSurounds(self.__board):
            y,x = divmod(location,self.length)
            newGroup = group(self.__board, location, self.length)
            newGroup.checkIfGroupAlive(x, y, player, "checked")
            self.__floodFill(x,y,"checked",player)
            if not(newGroup.alive):
                self.__board[location].center.value = BLANK
    
    def removeDeadTile(self,position):
        if not(self.__board[position].isAlive(self.__board)):
            self.__board[position].center.value = BLANK
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
            
    def checkValidMove(self,position):
        return not(self.__board[position].center.value != BLANK or (self.oneDeadStone and position == self.lastRemStoneLoc))
    
    # returns False if it IS a valid move
    def __checkSurounds(self, position, inverse):
        for i in self.__board[position].getSuroundLocations():
            if i != "f" and self.__board[i].center.value != inverse:
                return False
        return True
    
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
        lValue = self.getLeft(board)
        return tValue,rValue,bValue,lValue

    # def isAlive(self,board):
    #     try:
    #         if board[self.right].center.value != (self.center.getInverse()):
    #             return True
    #     except:
    #         pass
    #     try:
    #         if board[self.left].center.value != (self.center.getInverse()):
    #             return True 
    #     except:
    #         pass
    #     try:
    #         if board[self.top].center.value != (self.center.getInverse()):
    #             return True
    #     except:
    #         pass
    #     try:
    #         if board[self.bottom].center.value != (self.center.getInverse()):
    #             return True
    #     except:
    #         pass
    #     return False
    
    def isAlive(self,board):
        if self.right != "f" and board[self.right].center.value != (self.center.getInverse()):
            return True
        elif self.left != "f" and board[self.left].center.value != (self.center.getInverse()):
            return True 
        elif self.top != "f" and board[self.top].center.value != (self.center.getInverse()):
            return True
        elif self.bottom != "f" and board[self.bottom].center.value != (self.center.getInverse()):
            return True
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