from basicImports import *
from GoV6_1 import *
import numpy as np
import random as rnd


class MCTS():
    def __init__(self):
        self.__size = 81
        self.__player = "x"
        # still gives approx. 10 trillion possible games
        self.__maxSearchDepth = 5 
        # this is an arbitary value, size rounded up to the nearest 100 
        self.__simDepth = (-(self.__size // -100))*100 
        self.__path = []

    def __startTree(self):
        self.__tree = node(self.__size, self.__player, self.__player, False)

    def getBestMove(self):
        self.__startTree()
        for x in range(40):
            self.__tree.addChild(x)
        print(len(self.__tree.getChildren()))
        end = self.selection()
        end.printBoard()

    def selection(self):
        depth = 0
        current = self.__tree
        while True:
            self.__path.append(current)
            if depth > self.__maxSearchDepth:
                return current
            childNum = rnd.randint(0,self.__size)
            if childNum >= current.getNumChildren():
                return current
            else:
                new = current.getChildren()[childNum]
                current = new
            depth += 1
    
    def simulation(self,node):
        node.addCopyChild()
        for x in range(self.__simDepth):
            moves, num = node.getAllMoves()
            move = moves[rnd.randint(0, (len(moves) - 1))]
            node.setLocation(move)
        node.setScore(node.getBoard().getScore(self.__player))


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

    def setLeaf(self, val):
        self.__isLeaf = val

    def setPlayer(self,player):
        self.__player.setValue(player)
    
    def setBoard(self,new):
        self.__board.setBoard(new)

    def setLocation(self, loc):
        self.__board.playTurnIndex(loc, self.__player)
        self.__move = loc

    def setScore(self,val):
        self.__score = val

    def addChild(self,index):
        self.__children.append(node(self.__size,self.getInversePlayer(),self.__root,not(self.__isMax)))
        self.__children[-1].setBoard(self.__board)
        self.__children[-1].setLocation(index)
        
    def addCopyChild(self):
        self.__children.append(node(self.__size,self.getInversePlayer(),self.__root,not(self.__isMax)))
        self.__children[-1].setBoard(self.__board)

if __name__ == "__main__":
    test = MCTS()
    for x in range(10):
        test.getBestMove()
    '''
    vals = [0,0,0,0]
    test = rng()
    for x in range(10000000):
        vals[int(test.getRndNum(4)) - 1] += 1
    print(vals)
    '''