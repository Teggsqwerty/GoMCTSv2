BLANK = ""
class board():
    def __init__(self):
        self.__board = [[BLANK for _ in range(3)] for _ in range(3)]
        
    def resetGame(self):
        self.__board = [[BLANK for _ in range(3)] for _ in range(3)]

    def drawBoard(self):
        print("+ = A = + = B = + = C = +")
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
                    line1 = line1 + " /   \ "
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
            print("+ = A = + = B = + = C = +")
        print("\n\n\n\n")

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

    # returns finshed, winner
    def playTurn(self,x,y,player):
        self.__baord[y][x] = player
        winner = self.checkIfWon()
        if winner == BLANK:
            if self.getNoMoves() == 0:
                return True, BLANK
            return False, BLANK
        else:
            return True, winner

        
    
class game():
    def __init__(self):
        self.user = "x"
        self.won = False
        self.singlePlayer = False
    
    def userTurn(self,x,y):
        if self.won:
            for y in range(3):
                for x in range(3):
                    self.__board[y][x] = ""
            self.won = False
            message = "can player 1 (X) please play"
            valid = True
        else:
            valid = self.checkValidLocation(x,y)
            if valid:
                self.__board[y][x] = self.user
                winner = self.checkIfWon()

                if self.user == "o":
                    message = "can player 1 (X) please play"
                    self.user = "x"
                else:
                    message = "can player 2 (O) please play"
                    self.user = "o"

                if winner == "x":
                    message = "player 1 (X) has won!\nclick any button to reset"
                    self.won = True
                elif winner == "o":
                    message = "player 2 (O) has won!\nclick any button to reset"
                    self.won = True
                elif self.findAllMoves() == 0:
                    message = "draw! both sides win 1/2 a point\nclick any button to reset"
                    self.won = True
            else:
                message = "invalid move, please try again"
                
        return message, valid
    
    def singlePlayerTurn(self, x, y):
        if self.won:
            for y in range(3):
                for x in range(3):
                    self.__board[y][x] = ""
            self.won = False
            message = "can player 1 (X) please play"
            valid = True
        else:
            valid = self.checkValidLocation(x,y)
            if valid:
                self.board[y][x] = self.user
                winner = self.checkIfWon()
                message = "can player 1 (X) please play"
                if winner == "x":
                    message = "player 1 (X) has won!\nclick any button to reset"
                    self.won = True
                elif winner == "o":
                    message = "player 2 (O) has won!\nclick any button to reset"
                    self.won = True
                elif self.findAllMoves() == 0:
                    message = "draw! both sides win 1/2 a point\nclick any button to reset"
                    self.won = True
            else:
                message = "invalid move, please try again"
            if not(self.won):
                self.makeMImove()
                winner = self.checkIfWon()
                if winner == "x":
                    message = "player 1 (X) has won!\nclick any button to reset"
                    self.won = True
                elif winner == "o":
                    message = "player 2 (O) has won!\nclick any button to reset"
                    self.won = True
                elif self.findAllMoves() == 0:
                    message = "draw! both sides win 1/2 a point\nclick any button to reset"
                    self.won = True
        return message
    
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