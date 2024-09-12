import numpy as np

BLANK = ""

class board():
    # length is the length/width of the board 
    # size is the no. of tiles in the board
    # the board is a numpy array of tiles
    # DO NOT edit blank copy, this is used to hopefully speed up the group detection algorithm
    # group detection is for use with the group detection algorithm, it will be rest by copying
    # blankCopy into it
    def __init__(self,length):
        self.length = length
        self.size = length * length
        self.board = self.createBlankBoard()
        self.blankCopy = np.copy(self.board)
        self.groupDetection = np.copy(self.board)
        
    def createBlankBoard(self):
        blank = np.empty(self.size, object)
        for index in range(self.size):
            blank[index] = tile()
        self.initPointer(blank)
        return blank
        
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
        #print(position)
        self.board[position].center.value = char
        #print(self.board[position].center.invert())
        
    def editBoard(self,char):
        valid = False
        while not(valid):
            y = getValidInt(1,self.length,"enter M for menu or\nenter x: ",["M"]) 
            if y != "M":
                OY = y
                y -= 1
                x = getValidInt(1,self.length,"enter y: ") 
                OX = x
                x = self.length - x
                print()
                index = (x*self.length) + y
                valid = self.checkValidMove(index)
                if not(valid):
                    print("must not already contain a counter")
                else:
                    self.editTile(index,char)
            else:
                valid = True
                OY = y
                OX = 0
        return OX, OY
    
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
        
class AI():
    def __init__(self):
        pass
        # blank ???
        
class game():
    def __init__(self, size, isTest, name = "", sgf = True):
        if isTest:
            self.playExampleGame(name, sgf, size)
        else:
            self.playGame(size)
            
    def printMenu(self):
        print("\n===================")
        print("S: save game")
        print("Q: quit game")
        print("P: print game")
        print("Enter: continue")
        print("===================\n")
        print("enter your Choice: ", end = "")

    def playGame(self, boardWidth):
        mainBoard = board(boardWidth)
        player = counter()
        file = fileHandler()
        player.value = "x"
        won = False
        turnCounter = 0
        data = []
        while not(won):
            print(f"it is player {player.value}'s turn.\n")
            mainBoard.printBoard()
            x,y = mainBoard.editBoard(player.value)
            while y == "M":
                if y == "M":
                    self.printMenu()
                    Choice = input()
                    if Choice == "S":
                        filename = input("enter save game name: ")
                        filename += ".txt"
                        file.saveData(data,filename)
                    elif Choice == "Q":
                        won = True
                        y = 0
                    elif Choice == "P":
                        print(data)
                if not(won):
                    x,y = mainBoard.editBoard(player.value)
            player.value = player.invert()
            mainBoard.removeDeadTiles(player.value)
            mainBoard.removeDeadTiles(player.invert())
            turnCounter += 1
            data.append([x,y])


    def playExampleGame(self, name, sgf, length):
        file = fileHandler()
        if sgf:
            filename = name + ".sgf"
            data = file.readSGF(filename)
            print(data)
        else:
            filename = name + ".txt"
            data = file.readData(filename)
        mainBoard = board(length)
        player = counter()
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

class fileHandler():
    def saveData(self, data, filename):
        rawData = ""
        for turn in data:
            rawData += (str(turn[0]) + "," + str(turn[1]) + "\n")
        fin = open(filename,"w")
        fin.write(rawData)
        fin.close()

    def readData(self,filename):
        fin = open(filename)
        rawData = fin.readlines()
        fin.close()
        filesize = len(rawData)
        data = [[0,0,""] for x in range(filesize)]
        for index in range(filesize):
            offset = 0
            blank = ["","",""]
            for char in rawData[index]:
                if char != ",":   
                    blank[offset] += char
                else:
                    offset += 1
            print(blank[0])
            data[index][0] = int(blank[0])
            data[index][1] = int(blank[1])
            data[index][2] = blank[2].strip()
        return data

    def sgfToTxt(self,filename):
        sgfname = filename + ".sgf"
        fin = open(sgfname)
        rawData = fin.read()
        fin.close()
        start = self.findStart(rawData)
        data = rawData[start:-2]
        data = self.parseTurns(data)
        txtname = filename + ".txt"
        fin = open(txtname, "w")
        fin.write(data)
        fin.close()

    def readSGF(self,filename):
        fin = open(filename)
        data = fin.read()
        fin.close()
        start = self.findStart(data)
        data = data[start:-2]
        newData = [[0,0,""] for _ in range(data.count(";")+1)]
        string = ""
        index = 0
        for char in data:
            if char == ";":
                newData[index][0] = ord(string[2]) - ord("a") + 1
                newData[index][1] = ord(string[3]) - ord("a") + 1
                if string[0] == "B":
                    newData[index][2] = "o"
                else:
                    newData[index][2] = "x"
                string = ""
                index += 1
            else:
                string += char
        return newData
    
    def parseTurns(self,data):
        newData = ""
        string = ""
        for char in data:
            if char == ";":
                newData += str(ord(string[2]) - ord("a") + 1) + ","
                newData += str(ord(string[3]) - ord("a") + 1) + ","
                if string[0] == "B":
                    newData += "o\n"
                else:
                    newData += "x\n"
                string = ""
            else:
                string += char
        return newData[:-1]

    def findStart(self,data):
        count = 0
        semiCount = 0
        while count <= len(data) and semiCount != 2:
            if data[count] == ";":
                semiCount += 1
            count += 1
        return count
    
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
        
def getMainMenuChoice():
    while True:
        print("=============================")
        print("My GO game!")
        print("1: play 2 player game")
        print("2: load an example game(.txt)")
        print("3: load an example game(.sgf)")
        print("9: quit")
        print("==============================\n")
        choice = input("enter your choice: ")
        if not(choice in ["1","2","3","9"]):
            print("must be a valid choice.\n")
        else:
            return int(choice)
        
if __name__ == "__main__":
    for x in range(50):
        print("\n\n")
    playing = True
    while playing:
        mainChoice = getMainMenuChoice()
        if mainChoice == 1:
            boardSize = getValidInt(1,19,"Enter the board size (1,19): ")
            main = game(boardSize,False)
        elif mainChoice == 2:
            boardSize = getValidInt(1,19,"Enter the board size for the file(1,19): ")
            invalid = True
            while invalid:
                fName = input("Enter a valid file name: ")
                try:
                    main = game(boardSize, True, fName)
                    invalid = False
                except:
                    print("Must be a valid file name.")
        elif mainChoice == 3:
            boardSize = getValidInt(1,19,"Enter the board size for the file(1,19): ")
            invalid = True
            while invalid:
                fName = input("Enter a valid file name: ")
                try:
                    main = game(boardSize, True, fName, True)
                    invalid = False
                except:
                    print("Must be a valid file name.")
        elif mainChoice == 9:
            playing = False