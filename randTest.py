import timeit
mysetup = """
import mtalg.random as rand
import numpy as np

class rng():
    def __init__(self):
        self.__seeds = 0 
        self.__noNewSeeds = 100000000

        self.generateSeeds()

    def generateSeeds(self):
        self.__seeds = rand.random(self.__noNewSeeds)

    
    # returns a value between 0 and maxval inclusive
    def getRndNum(self,maxval): 
        seed = self.__seeds[0]
        self.__seeds = self.__seeds[1:]
        return int(seed*(maxval))

rng = rng()
"""
slowSetup = """
import random
"""
getRand = """
for x in range(100000000):
    rng.getRndNum(x)"""

getSlow = """
for x in range(100000000):
    random.randint(0,x)"""
        
print(timeit.timeit(setup = mysetup  ,stmt = getRand, number = 1))
print(timeit.timeit(setup = slowSetup,stmt = getSlow, number = 1))
