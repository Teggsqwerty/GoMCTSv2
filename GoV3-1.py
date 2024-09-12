BLANK = ""

class game():
    def __init__(self,length):
        self.length = length
        self.size = length * length
        self.board = [tile() for _ in range(self.size)]
        self.resetBoard()
        
    def resetBoard(self):
        for index in range(self.size):
            y,x = divmod(index,self.length)
            topX,topY = x,(y-1)
            rigX,rigY = (x+1),y
            botX,botY = x,(y+1)
            lefX,lefY = (x-1),y
            if topY < 0:
                self.board[index].top = "f"
            else:
                topInd = topX+topY*self.length
                self.board[index].top = topInd
            if rigX == self.length:
                self.board[index].right = "f" 
            else:
                rigInd = rigX+rigY*self.length
                self.board[index].right = rigInd
            if botY == self.length:
                self.board[index].bottom = "f"
            else:
                botInd = botX+botY*self.length
                self.board[index].bottom = botInd
            if lefX < 0:
                self.board[index].left = "f"
            else:
                lefInd = lefX+lefY*self.length
                self.board[index].left = lefInd
                
    def makePrintable(self):
        printable = [[BLANK for _ in range(self.length)] for _ in range(self.length)]
        for index in range(self.size):
            y,x = divmod(index,self.length)
            #print(x,y)
            #print(self.board[index].center.value,",")
            printable[y][x] = self.board[index].center.value
        #print(printable)
        return printable
    
    def printXIndex(self):
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
            if y < 10:
                print((self.length - y)," ", string," ", (self.length - y),sep = "")
            else:
                print((self.length - y),string,(self.length - y),sep = "")
            string = BLANK
            if y != (self.length-1):
                for _ in range(self.length):
                    string += "|   "
                print(" ",string)
        self.printXIndex()
        print("\n\n")
        
    def editTile(self,position,char):
        #print(position)
        self.board[position].center.value = char
        #print(self.board[position].center.invert())
        
    def editBoard(self,char):
        valid = False
        while not(valid):
            y = getValidInt(1,self.length+1,"enter x: ") - 1
            x = self.length - getValidInt(0,self.length,"enter y: ") 
            print()
            #print(x,y)
            index = (x*self.length) + y
            valid = self.checkValidMove(index)
            if not(valid):
                print("must not already contain a counter")
        self.editTile(index,char) 
        
    # remove dead tiles beloning to player "player"
    def removeDeadTiles(self,player):
        for position in range(self.size):
            isGroup = self.checkIfGroup(position,player)
            if isGroup and self.board[position].center.value == player:
                self.removeDeadGroup(player,position)
                #pass
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
        return True
        
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

class counter():
    def __init__(self):
        self.value = BLANK
    
    def invert(self):
        if self.value == "x":
            return "o"
        elif self.value == "o":
            return "x"
        else:
            return -1
        
class tile():
    def __init__(self):
        self.center  = counter()
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
        lValue = self.getRight(board)
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
    
def getValidInt(mini,maxi,message):
    while True:
        num = input(message)
        if not(num.isnumeric()):
            print("must be a number")
        elif num in range(mini,(maxi+1)):
            print(f"must be in range {mini} to {maxi}")
        else:
            return int(num)
        

def playGame():
    boardWidth = 9
    mainBoard = game(boardWidth)
    player = counter()
    player.value = "x"
    won = False
    turnCounter = 0
    
    while not(won):
        print(f"it is player {player.value}'s turn.\n")
        mainBoard.printBoard()
        mainBoard.editBoard(player.value)
        player.value = player.invert()
        mainBoard.removeDeadTiles(player.value)
        mainBoard.removeDeadTiles(player.invert())
        turnCounter += 1
        '''
        if turnCounter == 18:
            won = True
        '''
   
if __name__ == "__main__":
    playGame()
