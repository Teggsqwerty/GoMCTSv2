BLANK = ""

class measure():
    def __init__(self):
        self.__maxSpan = 0
        self.__maxDepth = 0
        self.__noNodes = 0
        self.__timeTaken = 0
        self.__depths = [0,0,0,0,0,0,0,0,0,0]
    
    def measureTree(self,node):
        self.__maxSpan = 0
        self.__maxDepth = 0
        self.__noNodes = 0
        self.__timeTaken = 0
        self.__score = 0
        self.__depths = [0,0,0,0,0,0,0,0,0,0]
        self.__measure(node,0)
        for x in self.__depths:
            if x > self.__maxSpan:
                self.__maxSpan = x
            if x != 0:
                self.__maxDepth += 1

    def __measure(self, node, depth):
        self.__noNodes += 1
        self.__depths[depth] += 1
        children = node.getChildren()
        for child in children:
            self.__measure(child,(depth + 1))
    
    def setScore(self,val):
        self.__score = val

    def setTime(self,val):
        self.__timeTaken = val
        
    def getStats(self):
        return self.__maxSpan, self.__maxDepth, self.__noNodes, self.__timeTaken, self.__score

class stone():
    def __init__(self):
        self.value = BLANK
    
    def setValue(self, value):
        self.value = value
    
    def getValue(self):
        return self.value
    
    def getInverse(self):
        if self.value == "x":
            return "o"
        elif self.value == "o":
            return "x"
        else:
            return BLANK
    
    def invert(self):
        self.value = self.getInverse()

# this is a general sub which returns a value inclusive of the two bounds entered
def getValidInt(mini,maxi,message, exceptions = []):
    while True:
        num = input(message)
        intNum = tryInt(num)
        if intNum in exceptions:
            return intNum
        elif not(num.isnumeric()):
            print("must be a number")
        elif not(int(num) in range(mini,(maxi+1))):
            print(f"must be in range {mini} to {maxi}")
        else:
            return int(num)

# this must be stored with the getValidInt sub
def tryInt(num):
    try:
        return int(num)
    except:
        return num