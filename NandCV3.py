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
        return ""
    
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

    def makeMImove(self):
        root = node(self.board,True,"o","x",0)
        self.board = root.bestMove


class node():
    def __init__(self, board, maximising, player, notPlayer, depth):
        self.player = player
        self.maximising = maximising
        self.board = board
        self.noMoves = self.getNoMoves()
        self.won = self.checkIfWon()
        if self.won == "" and self.noMoves != 0:
            self.childeren = [None for _ in range(self.noMoves)]
            self.moves = self.getAllMoves() 
            for x in range(self.noMoves):
                self.childeren[x] = node(self.moves[x], not(self.maximising), notPlayer, player,depth + 1)
            self.bestVal = 0 
            self.bestMove = [[None for _ in range(3)] for _ in range(3)]
            
            for child in self.childeren:
                if child.value >= self.bestVal and self.maximising:
                    self.bestVal = child.value
                    self.bestMove = child.board
                elif child.value <= self.bestVal and not(self.maximising):
                    self.bestVal = child.value
                    self.bestMove = child.board
            
            if self.bestMove[0][0] == None:
                self.bestVal = self.childeren[0].value
                self.bestMove = self.childeren[0].board
        else:
            if self.noMoves == 0:
                self.bestVal = 0
            elif (self.maximising and self.won == player) or (not(self.maximising) and self.won == notPlayer):
                self.bestVal = 1
            else:
                self.bestVal = -1

        self.value = self.bestVal


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
        return ""
    
    def getAllMoves(self):
        moves = [None for _ in range(self.noMoves)]
        count = 0
        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                if self.board[y][x] == "":
                    self.board[y][x] = self.player
                    moves[count] = [[x for x in y] for y in self.board]
                    self.board[y][x] = ""
                    count += 1
        return moves
    
    def getNoMoves(self):
        possibleMoves = 0
        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                if self.board[y][x] == "":
                    possibleMoves +=1
        return possibleMoves
    
class test:
    def __init__(self,board, player):
        self.board = board
        self.noMoves = self.getNoMoves()
        self.getAllMoves(player)

    def getAllMoves(self,player):
        moves = [None for _ in range(self.noMoves)]
        count = 0
        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                if self.board[y][x] == "":
                    self.board[y][x] = player
                    moves[count] = [[x for x in y] for y in self.board]
                    self.board[y][x] = ""
                    count += 1
        return moves
    
    def getNoMoves(self):
        possibleMoves = 0
        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                if self.board[y][x] == "":
                    possibleMoves +=1
        return possibleMoves
    
if __name__ == "__main__":
    main = [["" for _ in range(3)] for _ in range(3)]
    z = node(main,True,"x","o")
    main = z.bestMove
      