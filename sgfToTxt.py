def sgfToTxt(filename):
    sgfname = "train\\0000\\" + filename + ".sgf"
    fin = open(sgfname)
    rawData = fin.read()
    fin.close()
    start = findStart(rawData)
    data = rawData[start:-2]
    data = parseTurns(data)
    txtname = "txtData\\" + filename + ".txt"
    fin = open(txtname, "w")
    fin.write(data)
    fin.close()

def parseTurns(data):
    newData = ""
    string = ""
    for char in data:
        if char == ";":
            newData += str(ord(string[2]) - ord("a") + 1) + ","
            newData += str(ord(string[3]) - ord("a") + 1) + ","
            if string[0] == "B":
                newData += "o\n"
            else:
                newData += "x\n"
            string = ""
        else:
            string += char
    return newData[:-1]

def findStart(data):
    count = 0
    semiCount = 0
    while count <= len(data) and semiCount != 2:
        if data[count] == ";":
            semiCount += 1
        count += 1
    return count
        

if __name__ == "__main__":
    for x in range(999):
        if x%10 == 0:
            print("*",end = "", flush = True)
        dir = str(x)
        while len(dir) < 8:
            dir = "0" + dir
        sgfToTxt(dir)