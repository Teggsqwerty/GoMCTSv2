from basicImports import *
from Go import *

from multiprocessing import *

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
        self.__simDepth =  (-(self.__size // -100))*100 # use 10 for tests
        
        self.__iterations = 1000

    def __startTree(self,board):
        if self.__player == "x":
            self.__tree = node(self.__size, "o", self.__player, False)
        else:
            self.__tree = node(self.__size, "x", self.__player, False)
        self.__tree.setBoard(board)

    def getBestMove(self,board,width,player):
        self.__size = width ** 2
        self.__player = player

        cpus = cpu_count()
        print('Number of cpu\'s to process WM: %d' % cpus)
        poolCount = cpus*2

        start = time.perf_counter_ns()
        self.__startTree(board)

        toDo = []
        roots = []

        moves, num = self.__tree.getAllMoves()
        for move in moves:
            roots.append(self.__tree.getNewChild(move))

        with Pool(processes = poolCount) as pool: 
            for subTree,subToDo in pool.map_async(self.expansion,roots).get():
                toDo.append(subToDo)
                self.__tree.setChild(subTree)

        with Pool(processes = poolCount) as pool: 
            results = pool.map(self.simulation,toDo)
            for x in results:
                pass

        move = self.__tree.getBestMove()
        stop = time.perf_counter_ns()
        self.__measure.measureTree(self.__tree)
        self.__measure.setTime(stop - start)
        self.__measure.setScore(self.__tree.getScore())
        
        #print(self.__tree.getScore(),self.__tree.getChildren()[0].getScore())

        del self.__tree
        del toDo
        print(self.__measure.getDepths())
        return move, self.__measure.getStats()

    def expansion(self,node):
        toDo = []
        for _ in range(self.__iterations):
            depth = 0
            current = node
            notDone = True
            while notDone:
                if depth > self.__maxSearchDepth:
                    notDone = False
                childNum = rnd.randint(0,self.__size)
                if childNum >= current.getNumChildren():
                    notDone = False
                else:
                    new = current.getChildren()[childNum]
                    current = new
                depth += 1

            moves, num = current.getAllMoves()

            move = moves[rnd.randint(0, num - 1)]
            child = current.addChild(move)

            toDo.append(child)

        return node,toDo
    
    def simulation(self, node):
        sim = node.addCopyChild()
        for x in range(self.__simDepth):
            moves, num = sim.getAllMoves()
            move = moves[rnd.randint(0, num - 1)]
            valid = sim.setLocation(move)
            if valid:
                sim.invertPlayer()

        sim.setScore(sim.getBoard().getScore(self.__player))
        
        return node
    
    def backpropogation(self,node):
        current = node
        while current.getParent() != None:
            children = current.getChildren()
            t = 0.01
            score = 0.01
            for child in children:
                t += 1
                score += child.getScore()
            val = (score/t) + ((math.sqrt((abs(2*math.log(t))/(abs(score)))))*(abs(score)/score))
            current.setScore(val)
            new = current.getParent()
            current = new

class node():
    def __init__(self, size, player, root, isMax, parent = None):
        self.__board = board()
        self.__size = size
        self.__player = stone()
        self.__player.setValue(player)

        self.__children = []
        self.__parent = parent
        self.__root = root # root player
        self.__isMax = isMax
        self.__score = 0
        self.__move = -1
        self.__isLeaf = False

    def getLeaf(self):
        return self.__isLeaf

    def getChildren(self):
        return self.__children
    
    def getParent(self):
        return self.__parent
    
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
        self.__children.append(node(self.__size,self.getInversePlayer(),self.__root,not(self.__isMax),self))
        child = self.__children[-1]
        child.setBoard(self.__board)
        child.setLocation(index)
        return child
        
    def addCopyChild(self):
        self.__children.append(node(self.__size,self.getInversePlayer(),self.__root,not(self.__isMax),self))
        child = self.__children[-1]
        child.setBoard(self.__board)
        child.setLeaf()
        return child
    
    def getNewChild(self,index):
        child = node(self.__size,self.getInversePlayer(),self.__root,not(self.__isMax),self)
        child.setBoard(self.__board)
        child.setLocation(index)
        return child
    
    def setChild(self,child):
        self.__children.append(child)
    
class GO():
    def __init__(self):
        self.__engine = MCTS()
        self.__board = board()
        self.__player = stone()
        self.__file = FH.fileHandler() 
        self.__Xhuman = True
        self.__Ohuman = True
        self.__stats = (0, 0, 0, 0, 0)
        self.__data = []
        self.__size = 19
        self.__init(self.__Xhuman, self.__Ohuman)

    def reset(self):
        self.__board.setLength(self.__size)
        self.__board.resetBoard()
        self.__player.setValue("x")
        self.__data = []
        
    def __init(self, X, O):
        self.__board.setLength(self.__size)
        self.__board.resetBoard()
        self.__Xhuman = X
        self.__Ohuman = O
        self.__player.setValue("x")
        self.__data = []
    
    def setPlayer1(self,val):
        self.__Xhuman = val
    
    def setPlayer2(self,val):
        self.__Ohuman = val

    def getStats(self):
        return self.__stats
    
    def setSize(self,size):
        self.__size = size

    def proccesing(self,x,y):
        if not(self.__Xhuman) and not(self.__Ohuman):
            return self.__GUIZeroPlayer()
        elif not(self.__Xhuman) and self.__Ohuman:
            return self.__GUIOnePlayerO(x,y)
        elif self.__Xhuman and not(self.__Ohuman):
            return self.__GUIOnePlayerX(x,y)
        elif self.__Xhuman and self.__Ohuman:
            return self.__GUITwoPlayer(x,y)
    
    def __GUITwoPlayer(self,x,y):
        message, valid = self.__userTurn(x,y)
        if valid:
            self.__data.append([x,y])
        return message
    
    def __GUIOnePlayerX(self,x,y): # X is human
        if self.__player.getValue() == "x":
            message, valid = self.__userTurn(x,y)
            if valid:
                self.__data.append([x,y])
                return "click for next move"
            return message
        else:
            move = self.__getComputerMove()
            self.__board.playTurnIndex(move,self.__player)
            message = "can player 1 (X) please play"
            self.__player.setValue("x")
            y,x = divmod(move,(self.__size**2))
            self.__data.append([x,y])
            return message
    
    def __GUIOnePlayerO(self,x,y): # O is human
        if self.__player.getValue() == "x":
            move = self.__getComputerMove()
            self.__board.playTurnIndex(move,self.__player)
            self.__player.setValue("o")
            message = "can player 2 (O) please play"
            y,x = divmod((self.__size**2),move)
            self.__data.append([x,y])
        else:
            message, valid = self.__userTurn(x,y)
            if valid:
                message = "click for next move"
                self.__data.append([x,y])
        return message
    
    def __GUIZeroPlayer(self):
        message = "click for next move"
        move = self.__getComputerMove()
        self.__board.playTurnIndex(move,self.__player)
        self.__player.invert()
        y,x = divmod((self.__size**2),move)
        self.__data.append([x,y])
        return message
    
    def getBoard(self):
        return self.__board.getBoard()
    
    def __userTurn(self,x,y):
        valid = self.__board.playTurn(x,y,self.__player)
        if valid:
            if self.__player.getValue() == "o":
                message = "can player 1 (X) please play"
                self.__player.setValue("x")
            else:
                message = "can player 2 (O) please play"
                self.__player.setValue("o") 
            return message, valid
        else:
            message = "invalid move, please try again"     
            return message, valid
    
    def loadGame(self, filePath):
        self.__player.setValue("x")
        self.__board.setLength(self.__size)
        self.__board.resetBoard()

        self.__data = []
        self.__file.setFileType(True) # currently only works with sgf
        fileData, error = self.__file.readData(filePath)

        if error != "":
            print("error")

        for turn in fileData:
            y = turn[1]
            x = turn[0] 
            self.__data.append([x,y])
            self.__board.playTurn(x,y,self.__player)
            
            self.__player.invert()
    
    def saveGame(self,filename):
        self.__file.saveData(self.__data,filename)
    
    def __getComputerMove(self):
        #print(self.__player.getValue())
        if self.__player.getValue() == "x":
            #self.__player.setValue("o")
            move, self.__stats = self.__engine.getBestMove(self.__board, self.__size,"o")
        else:
            #self.__player.setValue("x")
            move, self.__stats = self.__engine.getBestMove(self.__board, self.__size,"x")
        return move

    


if __name__ == "__main__":
    bla = stone()
    bla.setValue("x")
    printing = board()
    printing.resetBoard()
    test = MCTS()
    for abc in range(1):
        move, stats = test.getBestMove(printing,9,bla)
        maxSpan, maxDepth, noNodes, timeTaken, score, mode = stats
        print("time per loop", (timeTaken/(noNodes*1000000)))
        # print(move)
        # print("span",maxSpan,"depth", maxDepth,"nodes", noNodes,"time", timeTaken,"score", score, "time per loop", (timeTaken/noNodes))