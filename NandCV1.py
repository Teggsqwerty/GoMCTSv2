class board():
    def __init__(self,singlePlayer):
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.user = "x"
        self.won = False
        self.singlePlayer = singlePlayer
        
    def checkIfWon(self):
        for i in self.board:
            if i[0] == i[1] == i[2] != "":
                return i[0]
        for i in range(len(self.board[0])):
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != "":
                return self.board[0][i]
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != "":
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != "":
            return self.board[0][2]
        
    def findAllMoves(self):
        possibleMoves = 0
        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                if self.board[y][x] == "":
                    possibleMoves +=1
        return possibleMoves
    
    def checkValidLocation(self,x,y):
        if self.board[y][x] != "x" and self.board[y][x] != "o":
            return True
        return False

    def userTurn(self,x,y):
        if self.won:
            for y in range(3):
                for x in range(3):
                    self.board[y][x] = ""
            self.won = False
            message = "can player 1 (X) please play"
            valid = True
        else:
            valid = self.checkValidLocation(x,y)
            if valid:
                self.board[y][x] = self.user
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
                    self.board[y][x] = ""
            self.won = False
            message = "can player 1 (X) please play"
            valid = True
        else:
            valid = self.checkValidLocation(x,y)
            if valid:
                self.board[y][x] = self.user
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

    def makeMImove(self):
        pass
    
if __name__ == "__main__":
    pass




       