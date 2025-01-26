from basicImports import *
from GoV6_1 import *
import numpy as np
import random as rnd
import math

class MCTS():
    def __init__(self):
        self.__size = 81
        self.__player = "x"
        # still gives approx. 10 trillion possible games
        self.__maxSearchDepth = 5 
        # this is an arbitary value, size rounded up to the nearest 100 
        self.__simDepth = (-(self.__size // -100))*100 # use 10 for tests
        self.__path = []
        self.__depth = 0

    def setDepth(self,depth):
        self.__depth = depth

    def __startTree(self):
        self.__tree = node(self.__size, self.__player, self.__player, False)

    def getBestMove(self):
        self.__startTree()
        for x in range(10):
            end = self.selection()
            moves, num = end.getAllMoves()
            move = moves[rnd.randint(0, (len(moves) - 1))]
            end.addChild(move)
            self.__path.append(end.getChildren()[-1])

            self.simulation(self.__path[-1])

            self.backpropogation()
        
        print(self.__tree.getBestMove())

        # self.__startTree()
        # for x in range(40):
        #     self.__tree.addChild(x)
        # end = self.selection()
        # self.simulation(end)
        # print(end.getLastChild().getScore())
        # print(end.getLastChild().getBoard().printBoard())
        # print(end.getChildren()[0].getScore())

    def selection(self):
        self.__depth = 0
        current = self.__tree
        while True:
            self.__path.append(current)
            if self.__depth > self.__maxSearchDepth:
                return current
            childNum = rnd.randint(0,self.__size)
            if childNum >= current.getNumChildren():
                return current
            else:
                new = current.getChildren()[childNum]
                current = new
            self.__depth += 1
    
    def simulation(self,node):
        node.addCopyChild()
        sim = node.getLastChild()
        for x in range(self.__simDepth):
            moves, num = sim.getAllMoves() # this was node.bla in v0-1
            move = moves[rnd.randint(0, num - 1)]
            valid = sim.setLocation(move)
            if valid:
                sim.invertPlayer()
            input()
            sim.printBoard()
        sim.setScore(sim.getBoard().getScore(self.__player))
    
    def backpropogation(self):
        for count in range((self.__depth - 1),-1,-1):
            current = self.__path[count]
            children = current.getChildren()
            t = 0
            score = 0
            for child in children:
                t += 1
                score += child.getScore()
            
            current.setScore((score/t) + (math.sqrt((2*math.log(t))/score)))

    def calculateUCB(self,node):
        children = node.getChildren()
        t = 0
        score = 0
        for child in children:
            t += 1
            score += child.getScore()
        
        node.setScore((score/t) + (math.sqrt((2*math.log(t))/score)))

class node():
    def __init__(self, size, player, root, isMax):
        self.__board = board()
        self.__size = size
        self.__children = []
        self.__player = stone()
        self.__player.setValue(player)
        self.__root = root # root player
        self.__isMax = isMax
        self.__score = 0
        self.__move = -1
        self.__isLeaf = False

    def getLeaf(self):
        return self.__isLeaf

    def getChildren(self):
        return self.__children
    
    def getLastChild(self):
        return self.__children[-1]
    
    def getNumChildren(self):
        return len(self.__children)

    def getBestMove(self):
        for child in self.__children:
            if child.__score == self.__score:
                move = child.getMove()
                return move

    def getMove(self):
        return self.__move

    def getScore(self):
        return self.__score

    def getBoard(self):
        return self.__board

    def getInversePlayer(self):
        return self.__player.getInverse()
    
    def getPlayer(self):
        return self.__player
    
    def getAllMoves(self):
        moves = []
        count = 0
        for (index,loc) in enumerate(self.__board.getBoard()):
            if loc.center.value == BLANK:
                moves.append(index)
                count += 1
        return moves, count

    def printBoard(self):
        self.__board.printBoard()

    def setPlayer(self,player):
        self.__player.setValue(player)
    
    def setBoard(self,new):
        self.__board.setBoard(new)

    def setLocation(self, loc):
        valid = self.__board.playTurnIndex(loc, self.__player)
        self.__move = loc
        if not(valid):
            print("invalid", loc)
        return valid

    def setScore(self,val):
        self.__score = val

    def setLeaf(self):
        self.__isLeaf = True

    def invertPlayer(self):
        return self.__player.invert()

    def addChild(self,index):
        self.__children.append(node(self.__size,self.getInversePlayer(),self.__root,not(self.__isMax)))
        self.__children[-1].setBoard(self.__board)
        self.__children[-1].setLocation(index)
        
    def addCopyChild(self):
        self.__children.append(node(self.__size,self.getInversePlayer(),self.__root,not(self.__isMax)))
        self.__children[-1].setBoard(self.__board)
        self.__children[-1].setLeaf()

if __name__ == "__main__":
    test = MCTS()
    test.getBestMove()