from basicImports import *

class fileHandler():
    def __init__(self):
        self.__isSgf = True

    def setFileType(self,isSgf):
        self.__isSgf = isSgf

    def saveData(self,data,filename):
        if self.__isSgf:
            self.__saveDataSgf(data,(filename + ".sgf"))
        else:
            self.__saveDataTxt(data,(filename + ".txt"))

    def readData(self,filename):
        try:
            if self.__isSgf:
                data = self.__readSGF(filename + ".sgf")
            else:
                data = self.__readTxt(filename + ".txt")
            error = ""
        except:
            data = []
            error = "error loading file"
        return data, error
    
    def __saveDataSgf(self, data, filename):
        player = stone()
        player.setValue("x")
        rawData = "(;\n"
        for turn in data:
            if player.getValue() == "x":
                rawData += ";B["
            else:
                rawData += ";W["
            rawData += chr(97+ord(turn[0])) + chr(97+ord(turn[1])) + "]"
            player.invert()
        rawData += ")\n"
        fin = open(filename,"w")
        fin.write(rawData)
        fin.close()
    
    def __saveDataTxt(self, data, filename):
        player = stone()
        player.setValue("x")
        rawData = ""
        for turn in data:
            rawData += (str(turn[0]) + "," + str(turn[1]) + "," + player.getValue() + "\n")
            player.invert()
        fin = open(filename,"w")
        fin.write(rawData)
        fin.close()

    def __readTxt(self,filename):
        fin = open(filename)
        rawData = fin.readlines()
        fin.close()
        filesize = len(rawData)
        data = [[0,0,""] for x in range(filesize)]
        for index in range(filesize):
            offset = 0
            blank = ["","",""]
            for char in rawData[index]:
                if char != ",":   
                    blank[offset] += char
                else:
                    offset += 1
            print(blank[0])
            data[index][0] = int(blank[0])
            data[index][1] = int(blank[1])
            data[index][2] = blank[2].strip()
        return data

    def __readSGF(self,filename):
        fin = open(filename)
        data = fin.read()
        fin.close()
        start = self.__findStart(data)
        data = data[start:-2]
        data = self.__parseTurns(data)
        return data
    
    def __parseTurns(self,data):
        newData = [[0,0,""] for _ in range(data.count(";")+1)]
        string = ""
        index = 0
        for char in data:
            if char == ";":
                newData[index][0] = ord(string[2]) - ord("a") + 1
                newData[index][1] = ord(string[3]) - ord("a") + 1
                if string[0] == "B":
                    newData[index][2] = "o"
                else:
                    newData[index][2] = "x"
                string = ""
                index += 1
            else:
                string += char
        return newData
    
    def __findStart(self,data):
        count = 0
        semiCount = 0
        while count <= len(data) and semiCount != 2:
            if data[count] == ";":
                semiCount += 1
            count += 1
        return count

if __name__ == "__main__":
    test = fileHandler()