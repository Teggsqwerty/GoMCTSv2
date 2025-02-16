from basicImports import *
from GoV6_1 import *
import numpy as np
import random as rnd
import math
import time

class MCTS():
    def __init__(self):
        self.__measure = measure()
        self.__size = 81
        self.__player = "x"
        # still gives approx. 10 trillion possible games
        self.__maxSearchDepth = 5 
        # this is an arbitary value, size rounded up to the nearest 100 
        self.__simDepth =  20# (-(self.__size // -100))*100 # use 10 for tests
        self.__path = []
        self.__depth = 0

    def setDepth(self,depth):
        self.__depth = depth

    def __startTree(self):
        self.__tree = node(self.__size, self.__player, self.__player, False)
    
    def getBestMove(self):
        start = time.perf_counter_ns()
        self.__startTree()
        for _ in range(50000):
            end = self.selection()
            #print(self.__path)
            moves, num = end.getAllMoves()
            move = moves[rnd.randint(0, (len(moves) - 1))]
            end.addChild(move)
            self.__path.append(end.getChildren()[-1])

            self.simulation(self.__path[-1])
            #print(self.__path[-1].getChildren())
            self.backpropogation()

            self.__path = []
            self.__depth = 0
        move = self.__tree.getBestMove()
        stop = time.perf_counter_ns()
        self.__measure.measureTree(self.__tree)
        self.__measure.setTime(stop - start)
        self.__measure.setScore(self.__tree.getScore())
        print("root node score", self.__tree.getScore())
        print("best move", move)

        # self.__startTree()
        # for x in range(40):
        #     self.__tree.addChild(x)
        # end = self.selection()
        # self.simulation(end)
        # print(end.getLastChild().getScore())
        # print(end.getLastChild().getBoard().printBoard())
        # print(end.getChildren()[0].getScore())

        return move, self.__measure.getStats()
    
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
            #input() # used for bug testing to allow for the program to be steped through
            #sim.printBoard() # used for bug testing

        score = sim.getBoard().getScore(self.__player)
        #print("set score", score)
        sim.setScore(score)
        #print("get score", sim.getScore())

    def backpropogation(self):
        for count in range((self.__depth+1),-1,-1):
            #print("count",count)
            current = self.__path[count]
            children = current.getChildren()
            t = 0
            score = 0.01
            for child in children:
                t += 1
                score += child.getScore()
                #print("score", child.getScore())
            val = (score/t) + ((math.sqrt(((2*math.log(t))/(abs(score)))))*(abs(score)/score))
            #print("value",val)
            current.setScore(val)

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
        best = -9999999999
        for child in self.__children:
            #print(child.__score)
            if child.__score > best:
                move = child.getMove()
                best = child.__score
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
        # if not(valid):
            # print("invalid", loc) # used for bug testing
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
    bla = stone()
    bla.setValue("x")
    printing = board()
    printing.resetBoard()
    test = MCTS()
    for abc in range(1):
        move, stats = test.getBestMove()
        maxSpan, maxDepth, noNodes, timeTaken, score = stats
        print(move)
        printing.playTurnIndex(move,bla)
        printing.printBoard()
        print("span",maxSpan,"depth", maxDepth,"nodes", noNodes,"time", timeTaken,"score", score, "time per loop", (timeTaken/50000))