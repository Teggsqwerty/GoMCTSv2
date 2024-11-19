BLANK = ""
class board():
    def __init__(self):
        self.__board = [[BLANK for _ in range(3)] for _ in range(3)]
        
    def resetGame(self):
        self.__board = [[BLANK for _ in range(3)] for _ in range(3)]

    def printBoard(self):
        print("+ = 1 = + = 2 = + = 3 = +")
        line1 = ""
        line2 = ""
        line3 = ""
        for y in range(len(self.__board)):
            line1 =  "|"
            line2 =  str(y+1)
            line3 =  "|"
            for x in range(len(self.__board[y])):  
                #print(self.__board[y][x])
                if self.__board[y][x] == "o":
                    line1 = line1 + " /¯¯¯\ |"
                    line2 = line2 + " |   | " +str(y+1)
                    line3 = line3 + " \___/ |"
                elif self.__board[y][x] == "x":
                    line1 = line1 + "  \ /  |"
                    line2 = line2 + "   \   " + str(y+1)
                    line3 = line3 + "  / \  |"
                else:
                    line1 = line1 + "       |"
                    line2 = line2 + "       " + str(y+1)
                    line3 = line3 + "       |"
            print(line1)
            print(line2)
            print(line3)
            print("+ = 1 = + = 2 = + = 3 = +")
        #print("\n\n\n\n")

    def checkIfWon(self):
        for i in self.__board:
            if i[0] == i[1] == i[2] != BLANK:
                return i[0]
        for i in range(len(self.__board[0])):
            if self.__board[0][i] == self.__board[1][i] == self.__board[2][i] != BLANK:
                return self.__board[0][i]
        if self.__board[0][0] == self.__board[1][1] == self.__board[2][2] != BLANK:
            return self.__board[0][0]
        if self.__board[0][2] == self.__board[1][1] == self.__board[2][0] != BLANK:
            return self.__board[0][2]
        return BLANK
    
    def getNoMoves(self):
        possibleMoves = 0
        for y in range(len(self.__board)):
            for x in range(len(self.__board[y])):
                if self.__board[y][x] == "":
                    possibleMoves +=1
        return possibleMoves
    
    def checkValidLocation(self,x,y):
        if self.__board[y][x] != "x" and self.__board[y][x] != "o":
            return True
        return False
    
    def makeMove(self, x, y, player):
        self.__board[y][x] = player

    # returns finshed, winner
    def playTurn(self,x,y,player):
        self.__board[y][x] = player
        winner = self.checkIfWon()
        if winner == BLANK:
            if self.getNoMoves() == 0:
                return True, BLANK
            return False, BLANK
        else:
            return True, winner

class game():
    def __init__(self):
        self.__board = board()
        self.__user = "x"
        self.__singlePlayer = False
        self.__score = [0,0] # [x,o]
    
    def userTurn(self,x,y):
        valid = self.__board.checkValidLocation(x,y)
        if valid:
            finished, winner = self.__board.playTurn(x,y,self.__user)
            if finished:
                self.__board.resetGame()
                if winner == "x":
                    message = "player 1 (X) has won!\nclick any button to reset"
                    self.__score[0] += 1
                elif winner == "o":
                    message = "player 2 (O) has won!\nclick any button to reset"
                    self.__score[1] += 1
                elif self.findAllMoves() == 0:
                    message = "draw! both sides win 1/2 a point\nclick any button to reset"
                    self.__score[0] += 0.5
                    self.__score[0] += 0.5
            elif self.__user == "o":
                message = "can player 1 (X) please play"
                self.__user = "x"
            else:
                message = "can player 2 (O) please play"
                self.__user = "o" 
            return message, valid, finished
        else:
            message = "invalid move, please try again"     
            return message, valid, False 
    
    def playTextGame(self):
        self.__user = "x"
        finished = False
        message = "can player 1 (X) please play"
        while not(finished):
            self.__board.printBoard()
            valid = False
            while not(valid):
                print(message)
                x = getValidInt(1,3,"enter x: ") - 1
                y = getValidInt(1,3,"enter y: ") - 1
                message, valid, finished = self.userTurn(x,y)

        print("\n\n" + message)

class node():
    def __init__(self):
        self.__board = [[BLANK for _ in range(3)] for _ in range(3)]
        self.__childeren = []
        self.__player = BLANK

    def setPlayer(self,player):
        self.__player = player

    def getInversePlayer(self):
        if self.__player == "x":
            return "o"
        elif self.__player == "o":
            return "x"
        else:
            return BLANK
        
    def setBoard(self,board):
        for x in range(3):
            for y in range(3):
                self.__board[y][x] = board[y][x]
    
    def getBoard(self):
        return self.__board
    
    def setLoc(self,x,y):
        self.__board[y][x] = self.__player
    
    def addChild(self,x,y):
        self.__childeren.append(node())
        self.__childeren[-1:][0].setBoard(self.__board)
        self.__childeren[-1:][0].setPlayer(self.getInversePlayer())
        self.__childeren[-1:][0].setLoc(x,y)

    def getAllMoves(self):
        possibleMoves = []
        count = 0
        for y in range(len(self.__board)):
            for x in range(len(self.__board[y])):
                if self.__board[y][x] == "":
                    possibleMoves.append([x,y])
                    count += 1
        return possibleMoves, count
    
    def checkIfWon(self):
        for i in self.__board:
            if i[0] == i[1] == i[2] != BLANK:
                return True
        for i in range(len(self.__board[0])):
            if self.__board[0][i] == self.__board[1][i] == self.__board[2][i] != BLANK:
                return True
        if self.__board[0][0] == self.__board[1][1] == self.__board[2][2] != BLANK:
            return True
        if self.__board[0][2] == self.__board[1][1] == self.__board[2][0] != BLANK:
            return True
        return False
    
    def fillTree(self):
        won = self.checkIfWon()
        if not(won):
            possibleMoves, count = self.getAllMoves()
            if count != 0:
                for move in possibleMoves:
                    self.addChild(move[0],move[1])
            for child in self.__childeren:
                child.fillTree()
    
        

# this is a general sub which returns a value inclusive of the two bounds entered
def getValidInt(mini,maxi,message, exceptions = []):
    while True:
        num = input(message)
        intNum = tryInt(num)
        if intNum in exceptions:
            return intNum
        elif not(num.isnumeric()):
            print("must be a number")
        elif not(int(num) in range(mini,(maxi+1))):
            print(f"must be in range {mini} to {maxi}")
        else:
            return int(num)

# this must be stored with the getValidInt sub
def tryInt(num):
    try:
        return int(num)
    except:
        return num

if __name__ == "__main__":
    test = node()
    test.setPlayer("x")
    test.fillTree()
    

