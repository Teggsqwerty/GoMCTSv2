BLANK = ""
class board():
    def __init__(self):
        self.__board = [[BLANK for _ in range(3)] for _ in range(3)]
        
    def resetGame(self):
        self.__board = [[BLANK for _ in range(3)] for _ in range(3)]

    def getBoard(self):
        return self.__board

    def printBoard(self):
        print("+ = 1 = + = 2 = + = 3 = +")
        line1 = ""
        line2 = ""
        line3 = ""
        for y in range(len(self.__board)):
            line1 =  "|"
            line2 =  str(y+1)
            line3 =  "|"
            for x in self.__board[y]:  
                if x == "o":
                    line1 = line1 + " /¯¯¯\ |"
                    line2 = line2 + " |   | " +str(y+1)
                    line3 = line3 + " \___/ |"
                elif x == "x":
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

    # returns finished, winner
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
                
                if winner == "x":
                    message = "player 1 (X) has won!\nclick any button to reset"
                    self.__score[0] += 1
                elif winner == "o":
                    message = "player 2 (O) has won!\nclick any button to reset"
                    self.__score[1] += 1
                elif winner == BLANK:
                    message = "draw! both sides win 1/2 a point\nclick any button to reset"
                    self.__score[0] += 0.5
                    self.__score[1] += 0.5
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
        self.__board.resetGame()    
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
        self.__board.printBoard()
        print("\n\n" + message)
        self.__board.resetGame()

    def playAIGame(self):
        self.__user = "x"
        finished = False
        while not(finished):
            self.__board.printBoard()
            test = node()
            if self.__user == "x":
                test.setPlayer("x")
                test.setRoot("o")
            else:
                test.setPlayer("o")
                test.setRoot("x")
            test.setBoard(self.__board.getBoard())
            test.fillTree()
            x,y = test.getBestMove()
            finished, winner = self.__board.playTurn(x,y,self.__user)
            if self.__user == "x":
                self.__user = "o"
            else:
                self.__user = "x"
            print()
        self.__board.printBoard()
        


class node():
    def __init__(self):
        self.__board = [[BLANK for _ in range(3)] for _ in range(3)]
        self.__childeren = []
        self.__player = self.__rootPlayer = BLANK
        self.__score = -1
        self.__move = [-1,-1]

    def getBestMove(self):
        for child in self.__childeren:
            if child.__score == self.__score:
                move = child.getMove()
                return move[0], move[1]

    def getMove(self):
        return self.__move

    def getScore(self):
        return self.__score

    def getBoard(self):
        return self.__board

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
    
    def setLoc(self,x,y):
        self.__board[y][x] = self.__player
    
    def setMove(self,x,y):
        self.__move = [x,y]

    def setPlayer(self,player):
        self.__player = player
    
    def setRoot(self,val):
        self.__rootPlayer = val

    def addChild(self,x,y):
        self.__childeren.append(node())
        self.__childeren[-1:][0].setBoard(self.__board)
        self.__childeren[-1:][0].setPlayer(self.getInversePlayer())
        self.__childeren[-1:][0].setRoot(self.__rootPlayer)
        self.__childeren[-1:][0].setLoc(x,y)
        self.__childeren[-1:][0].setMove(x,y)

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
                return True, i[0]
        for i in range(len(self.__board[0])):
            if self.__board[0][i] == self.__board[1][i] == self.__board[2][i] != BLANK:
                return True, self.__board[0][i]
        if self.__board[0][0] == self.__board[1][1] == self.__board[2][2] != BLANK:
            return True, self.__board[0][0]
        if self.__board[0][2] == self.__board[1][1] == self.__board[2][0] != BLANK:
            return True, self.__board[0][2]
        return False, BLANK
    
    def fillTree(self):
        won, winner = self.checkIfWon()
        if not(won):
            possibleMoves, count = self.getAllMoves()
            if count != 0:
                for move in possibleMoves:
                    self.addChild(move[0],move[1])
                scores = []
                for child in self.__childeren:
                    child.fillTree()
                    scores.append(child.getScore())
                if self.__player == self.__rootPlayer:
                    self.__score = max(scores)
                else:
                    self.__score = min(scores)
                
            else:
                self.__score = 0
        else:
            if winner == self.__rootPlayer:
                self.__score = 1
            else:
                self.__score = -1
    

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
    test = game()
    test.playTextGame()

