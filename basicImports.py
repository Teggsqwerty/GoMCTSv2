BLANK = ""

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