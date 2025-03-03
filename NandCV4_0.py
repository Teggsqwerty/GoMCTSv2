from basicImports import *
import time

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

class node():
    def __init__(self, player, isMax, rootPlayer, move = [-1,-1]):
        self.__board = [[BLANK for _ in range(3)] for _ in range(3)]
        self.__children = []
        self.__player = player
        self.__rootPlayer = rootPlayer
        self.__isMax = isMax
        self.__score = 0
        self.__move = move

    def getChildren(self):
        return self.__children
    
    def getBestMove(self):
        for child in self.__children:
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

    def addChild(self,x,y):
        self.__children.append(node(self.getInversePlayer(),not(self.__isMax),self.__rootPlayer, [x,y]))
        self.__children[-1].setBoard(self.__board)
        self.__children[-1].setLoc(x,y)

    def getAllMoves(self):
        possibleMoves = []
        count = 0
        for y in range(len(self.__board)):
            for x in range(len(self.__board[y])):
                if self.__board[y][x] == "":
                    possibleMoves.append([x,y])
                    count += 1
        return possibleMoves, count
    
    # returns finished, winner
    def __checkIfWon(self):
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
    
    def minimax(self):
        finished, winner = self.__checkIfWon()
        if finished:
            if winner == self.__rootPlayer:
                self.__score = 1
            else:
                self.__score = -1
            return self.__score
        
        moves, noMoves = self.getAllMoves()
        if noMoves == 0:
            return 0

        if self.__isMax:
            self.__score = -1
            for i in range(noMoves):
                self.addChild(moves[i][0],moves[i][1])
                score = self.__children[i].minimax()
                self.__score = max(score,self.__score)
            return self.__score
        else:
            self.__score = 1
            for i in range(noMoves):
                self.addChild(moves[i][0],moves[i][1])
                score = self.__children[i].minimax()
                self.__score = min(score,self.__score)
            return self.__score
            
class NandC():
    def __init__(self):
        self.__board = board()
        self.__measure = measure()

        self.__init(True,False)

    def __init(self, X,O):
        self.__board.resetGame()
        self.__Xhuman = X
        self.__Ohuman = O
        self.__user = "x"
        self.__finished = False
        self.__score = [0,0] # [x,o]

    def reset(self):
        self.__board.resetGame()
        self.__finished = False
        self.__user = "x"

    def setPlayer1(self,val):
        self.__Xhuman = val
        print(self.__Xhuman, self.__Ohuman)

    def setPlayer2(self,val):
        self.__Ohuman = val
        print(self.__Xhuman, self.__Ohuman)

    def getStats(self):
        return self.__measure.getStats()

    def proccesing(self,x,y):
        if self.__finished:
            self.__init(self.__Xhuman, self.__Ohuman)
            if not(self.__Xhuman) and not(self.__Ohuman):
                message =  "click for next move"
            else:
                message = "can player 1 (X) please play"
        
        elif not(self.__Xhuman) and not(self.__Ohuman):
            message = self.__GUIZeroPlayer()
        elif not(self.__Xhuman) and self.__Ohuman:
            message = self.__GUIOnePlayerO(x,y)
        elif self.__Xhuman and not(self.__Ohuman):
            message = self.__GUIOnePlayerX(x,y)
        elif self.__Xhuman and self.__Ohuman:
            message = self.__GUITwoPlayer(x,y)
            
        
        return message

    def __GUITwoPlayer(self,x,y):
        message, valid, self.__finished = self.__userTurn(x,y)
        return message
    
    def __GUIOnePlayerX(self,x,y): # X is human
        message, valid, self.__finished = self.__userTurn(x,y)
        if not(valid):
            return message
        elif self.__finished:
            return message
        else:
            x,y = self.__getComputerMove()
            self.__finished, winner = self.__board.playTurn(x,y,"o")
            if self.__finished:
                if winner == "x":
                    message = "player 1 (X) has won!\nclick any button to reset"
                    self.__score[0] += 1
                elif winner == "o":
                    message = "player 2 (O) has won!\nclick any button to reset"
                    self.__score[1] += 1
                elif winner == BLANK:
                    message = "draw! both sides win 1/2 a point\nclick any tile to reset"
                    self.__score[0] += 0.5
                    self.__score[1] += 0.5
            else:
                message = "can player 1 (X) please play"
                self.__user = "x"
            return message
    
    def __GUIOnePlayerO(self,x,y): # O is human
        if self.__user == "x":
            x,y = self.__getComputerMove()
            self.__finished, winner = self.__board.playTurn(x,y,"x")
            if self.__finished:
                if winner == BLANK:
                    message = "draw! both sides win 1/2 a point\nclick any tile to reset"
                    self.__score[0] += 0.5
                    self.__score[1] += 0.5
                else:
                    message = "player 1 (X) has won!\nclick any button to reset"
                    self.__score[0] += 1
            else:
                message = "can player 2 (O) please play"
        else:
            message, valid, self.__finished = self.__userTurn(x,y)
            if valid:
                message = "click for next move"
        return message
    
    def __GUIZeroPlayer(self):
        message = "click for next move"
        x,y = self.__getComputerMove()
        if self.__user == "x":
            self.__finished, winner = self.__board.playTurn(x,y,"o")
        else:
            self.__finished, winner = self.__board.playTurn(x,y,"x")
        if self.__finished:
            if winner == "x":
                message = "player 1 (X) has won!\nclick any button to reset"
                self.__score[0] += 1
            elif winner == "o":
                message = "player 2 (O) has won!\nclick any button to reset"
                self.__score[1] += 1
            elif winner == BLANK:
                message = "draw! both sides win 1/2 a point\nclick any tile to reset"
                self.__score[0] += 0.5
                self.__score[1] += 0.5
        return message
    
    def getBoard(self):
        return self.__board.getBoard()
    
    def __userTurn(self,x,y):
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
                    message = "draw! both sides win 1/2 a point\nclick any tile to reset"
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
                message, valid, finished = self.__userTurn(x,y)
        self.__board.printBoard()
        print("\n\n" + message)
        self.__board.resetGame()

    def __getComputerMove(self):
        if self.__user == "x":
            self.__user = "o"
        else:
            self.__user = "x"
        test = node(self.__user,False,self.__user)
        test.setBoard(self.__board.getBoard())
        start = time.perf_counter_ns()
        self.__measure.setScore(test.minimax())
        end   = time.perf_counter_ns()
        x,y = test.getBestMove()
        self.__measure.measureTree(test)
        self.__measure.setTime(end - start)
        return x,y
    
    def playAIGame(self):
        self.__board.resetGame()
        self.__user = "x"
        finished = False
        while not(finished):
            self.__board.printBoard()
            x,y = self.__getComputerMove()
            if self.__user == "x":
                finished, winner = self.__board.playTurn(x,y,"o")
            else:
                finished, winner = self.__board.playTurn(x,y,"x")
            print()
        self.__board.printBoard()
    
    def playOnePlayerGame(self):
        self.__board.resetGame()    
        self.__user = "x"
        finished = False
        
        while not(finished):
            self.__board.printBoard()
            print(self.__user)
            valid = False
            message = "can player 1 (X) please play"
            while not(valid):
                print(message)
                x = getValidInt(1,3,"enter x: ") - 1
                y = getValidInt(1,3,"enter y: ") - 1
                message, valid, finished = self.__userTurn(x,y)
            self.__board.printBoard()
            print(self.__user)
            if not(finished):
                x,y = self.__getAiMove()
                if self.__user == "x":
                    finished, winner = self.__board.playTurn(x,y,"o")
                else:
                    finished, winner = self.__board.playTurn(x,y,"x")
        self.__board.printBoard()
        print("\n\n" + message)
        self.__board.resetGame()

if __name__ == "__main__":
   
    # test = node("x",True,"x")
    # test.setBoard([["x","o","x"],["o","x","o"],["x","o","x"]])
    # print(test.getBoard())
    
    
    test = NandC()
    #while True:
    test.playOnePlayerGame()
    
    
    # test = node("x",True,"x")
    # currentChild = test
    # won = False
    # i = 0
    # while not(won):
    #     z,m = divmod(i,3)
    #     currentChild.addChild(z,m)
    #     nextChild = currentChild.getchildren()[0]
    #     print(nextChild.getAllMoves())
    #     currentChild = nextChild
    #     moves,num = nextChild.getAllMoves()
    #     if num == 0:
    #         won = True
    #     i += 1
    # print(test.getchildren()[-1].getAllMoves())
    
