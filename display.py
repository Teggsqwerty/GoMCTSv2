from tkinter import *
import proccesingV3 as pro

class displayGrid():
    def __init__(self, parent, singlePlayer):
        self.blank = PhotoImage(file = "C:\\Users\\T Jackson\Documents\\school\\comp sci\\code\\schoolCode\\naughtsAndCrosses\\blank.png")
        self.cross = PhotoImage(file = "C:\\Users\\T Jackson\Documents\\school\\comp sci\\code\\schoolCode\\naughtsAndCrosses\\cross.png")
        self.naught = PhotoImage(file = "C:\\Users\\T Jackson\Documents\\school\\comp sci\\code\\schoolCode\\naughtsAndCrosses\\naught.png")

        self.x = 0
        self.y = 0
        self.value = ""

        self.singlePlayer = singlePlayer
        self.container = Frame(parent)
        self.container.pack()

        self.displayBoard = [[None for _ in range(3)] for _ in range(3)]
        self.header = Label(self.container, text = "naughts and crosses", font = ("Arial",25))
        self.header.grid(row = 0, column = 0, pady = 5, columnspan = 3)
        self.initBoard()

        self.infoBar = Label(self.container, text = "can player 1 (X) please play", font = ("Arial",18))
        self.infoBar.grid(row = 4, column = 0, pady = 5, columnspan = 3)
        self.board = pro.board(singlePlayer)

    def initBoard(self):
        for y in range(3):
            for x in range(1,4):
                self.displayBoard[y][x - 1] = Button(self.container, image = self.blank)
                self.displayBoard[y][x - 1].grid(row = x, column = y)
                self.displayBoard[y][x - 1].bind("<Button-1>", self.click)

    def click(self,event):
        widget = event.widget
        self.x = widget.grid_info()['row'] - 1
        self.y = widget.grid_info()["column"]
        text = self.proccess()
        self.infoBar.configure(text = text)
        self.updateGUI()
        
    def updateGUI(self):
        for y in range(3):
            for x in range(3):
                if self.board.board[y][x] == "o":
                    self.displayBoard[y][x].configure(image = self.naught)
                elif self.board.board[y][x] == "x":
                    self.displayBoard[y][x].configure(image = self.cross)
                else:
                    self.displayBoard[y][x].configure(image = self.blank)

    def proccess(self):
        if self.singlePlayer:
            message = self.board.singlePlayerTurn(self.x, self.y)
            return message
        else:
            message, valid = self.board.userTurn(self.x, self.y)
            return message

class mainMenu():
    def __init__(self,parent):
        self.container = Frame(parent)
        self.container.pack()

        self.title = Label(self.container, text = "naughts and crosses", font = ("Arial",25))
        self.title.pack(padx = 10, pady = 50)

        self.player1 = Button(self.container, text = "single player game", font = ("Arial",25), width = 20)
        self.player1.pack(padx = 10, pady = 10)

        self.player2 = Button(self.container, text = "two player game", font = ("Arial",25), width = 20)
        self.player2.pack(padx = 10, pady = 10)

        self.player1.bind("<Button-1>", self.singlePlayer)
        self.player2.bind("<Button-1>", self.twoPlayer)
    
    def singlePlayer(self,event):
        self.container.destroy()
        display = displayGrid(root, True)

    def twoPlayer(self,event):
        self.container.destroy()
        display = displayGrid(root, False) 

if __name__ == "__main__":
    root = Tk()
    root.resizable(0,0)
    root.geometry("400x500")
    root.title("naughts and crosses")
    main = mainMenu(root)
    root.mainloop()
    