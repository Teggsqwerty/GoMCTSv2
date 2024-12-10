from basicImports import *
from GoV6_1 import *
import mtalg.random as rand
import numpy as np

class rng():
    def __init__(self):
        self.__seeds = 0 
        self.__noSeeds = 0
        self.__noNewSeeds = 100000

        self.generateSeeds()

    def generateSeeds(self):
        self.__seeds = rand.random(self.__noNewSeeds)
        self.__noSeeds += self.__noNewSeeds
    
    def getRndNum(self,maxval):
        if self.__noSeeds == 0:
            self.generateSeeds() 
        seed = self.__seeds[-1]
        self.__seeds = self.__seeds[:-1]
        self.__noSeeds -= 1
        value = (seed*(maxval))//1
        return value + 1

# test code for above
'''
vals = [0,0,0,0]
test = rng()
for x in range(100000):
    vals[int(test.getRndNum(4)) - 1] += 1
print(vals)
'''
class MCTS():
    def __init__(self):
        self.__tree = node()


class node():
    def __init__(self):
        self.__board = board()
        self.__size = 9
        self.__children = []
        self.__player = stone()
        self.__rootPlayer = stone()
        self.__isMax = False
        self.__score = 0
        self.__move = [-1,-1]

    def getchildren(self):
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

if __name__ == "__main__":
    pass


