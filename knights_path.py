import random, copy, time
from tkinter import Tk, Label, Button, Canvas, Entry, Checkbutton, Frame, IntVar, messagebox, OptionMenu, StringVar
import tkinter.font as f


testing = True

class ChessBoard:
    #Constructor with size and starting row/column.
    #We represent squares in this class as tuples with row, column
    def __init__(self, master):
        #Setup GUI
        self.master = master
        master.title("Knight's Tour")

        #Title Label
        self.label = Label(master, text="Knight's Tour")
        self.label.grid(row=0,column=1, sticky = "W", pady = 2)

        #Frame to hold options
        self.options_frame = Frame(master)
        self.options_frame.grid(row=1, column=0)

        #Size of board to draw
        self.size = 10
        self.board_size_label = Label(self.options_frame, text="Board Size")
        self.board_size_label.grid(row = 1, column = 0, sticky = "E", pady = 2)
        self.size_input = Entry(self.options_frame)
        self.size_input.grid(row = 1, column = 1, sticky = "W", pady = 2)
        self.size_input.insert(0, str(self.size))
    
        #Initial row, random starting location
        self.row = random.randint(0,self.size-1)
        self.knight_row_label = Label(self.options_frame, text="Row Location")
        self.knight_row_label.grid(row = 2, column = 0, sticky = "E", pady = 2)
        self.row_input = Entry(self.options_frame)
        self.row_input.grid(row = 2, column = 1, sticky = "W", pady = 2)
        self.row_input.insert(0, str(self.row))

        #Initial column, random starting location
        self.column = self.row = random.randint(0,self.size-1)
        self.knight_column_label = Label(self.options_frame, text="Column Location")
        self.knight_column_label.grid(row = 3, column = 0, sticky = "E", pady = 2)
        self.column_input = Entry(self.options_frame)
        self.column_input.grid(row = 3, column = 1, sticky = "W", pady = 2)
        self.column_input.insert(0, str(self.column))

        #Speed
        self.run_speed_label = Label(self.options_frame, text="Run Speed (ms)")
        self.run_speed_label.grid(row = 4, column = 0, sticky = "E", pady = 2)
        self.run_speed_input = Entry(self.options_frame)
        self.run_speed_input.grid(row = 4, column = 1, sticky = "W", pady = 2)
        self.run_speed_input.insert(0, "20")

        #Algorithm Selection
        self.option_label = Label(self.options_frame, text="Algorithm")
        self.option_label.grid(row = 5, column = 0, sticky = "E", pady = 2)
        self.algorithm_option = StringVar()
        self.algorithm_option.set("Warnsdorff")
        self.algorithm_menu = OptionMenu(self.options_frame, self.algorithm_option, "Warnsdorff", "Cull")
        self.algorithm_menu.grid(row = 5, column = 1, sticky = "W", pady = 2)

        #Draw path
        self.draw_path_label = Label(self.options_frame, text="Draw Path")
        self.draw_path_label.grid(row=6, column=0, sticky="E", pady=2)
        self.draw_path_state = IntVar()
        self.draw_path_check = Checkbutton(self.options_frame, variable=self.draw_path_state)
        self.draw_path_check.select()
        self.draw_path_check.grid(row=6, column=1, sticky="W", pady=2)

        # #Reset button
        # self.reset_button = Button(self.options_frame, text="Reset", command=self.restart)
        # self.reset_button.grid(row=7, column = 0, sticky = "E", pady=2)

        #Drawing canvas
        self.canvas = Canvas(master, width=751, height=751, bg="black", borderwidth=0, highlightthickness=0)
        self.canvas.grid(row=1, column=1, columnspan=5, rowspan=5, padx=8, pady=(0,8))

        # #Play button
        self.play_button = Button(self.options_frame, text="Run", command=self.run)
        self.play_button.grid(row=7, column = 1, pady=2, sticky="W")

        # #About button
        # self.reset_button = Button(self.options_frame, text="?", command=self.help)
        # self.reset_button.grid(row=10, column = 1, sticky = "W", pady=(50, 2))

        #Setup our board with our initial parameters.
        self.board = [[False for i in range(self.size)] for j in range(self.size)]
        self.board[self.row][self.column] = True
        self.currentSquare = (self.row,self.column)

        self.restart();

    def run(self):
        self.restart()
        self.stop = False
        if self.algorithm_option.get() == "Warnsdorff":
            warnsdorff(self.size, self)
        else:
            cull(self.size,self)


    def restart(self):
        self.stop = True
        #We get all the gui values and validate them.
        self.drawpath = int(self.draw_path_state.get())

        #Parse size
        try:
            self.size = int(self.size_input.get())
        except :
            self.size = 10;
            self.size_input.delete(0, 'end')
            self.size_input.insert(0, "10")
            messagebox.showinfo(title=None, message="Illegal board size, changed to " + str(self.size) + ".")
        if self.size < 0:
            self.size = abs(self.size)
            self.size_input.delete(0, 'end')
            self.size_input.insert(0, str(self.size))
            messagebox.showinfo(title=None, message="Board size cannot be negative, changed to " + str(self.size) + ".")
        if self.algorithm_option.get() == "Cull" and self.size % 5 != 0:
            self.size = int(self.size/5) * 5
            self.size_input.delete(0, 'end')
            self.size_input.insert(0, str(self.size))
            messagebox.showinfo(title=None, message=" For Cull's algorithm, size must be divisible by 5, changed board size to " + str(self.size) + ".")


        #Parse row entry

        if self.algorithm_option.get() == "Cull":
            try:
                self.row = int(self.row_input.get())
            except :
                self.row = random.randint(0, self.size-1);
                self.row_input.delete(0, 'end')
                self.row_input.insert(0, str(self.row))
                messagebox.showinfo(title=None, message=" Cull's algorithm starts on the lower left square, row updated to reflect that. " )
            if self.row != self.size-1:
                self.row = self.size-1;
                self.row_input.delete(0, 'end')
                self.row_input.insert(0, str(self.row))
                messagebox.showinfo(title=None, message=" Cull's algorithm starts on the lower left square, row updated to reflect that. " )

            #Parse column entry
            try:
                self.column = int(self.column_input.get())
            except :
                self.column = 0
                self.column_input.delete(0, 'end')
                self.column_input.insert(0, str(self.column))
                messagebox.showinfo(title=None, message=" Cull's algorithm starts on the lower left square, column updated to reflect that." )
            if self.column != 0:
                self.column = 0
                self.column_input.delete(0, 'end')
                self.column_input.insert(0, str(self.column))
                messagebox.showinfo(title=None, message=" Cull's algorithm starts on the lower left square, column updated to reflect that." )
        else:
            try:
                self.row = int(self.row_input.get())
            except :
                self.row = random.randint(0, self.size-1);
                self.row_input.delete(0, 'end')
                self.row_input.insert(0, str(self.row))
                messagebox.showinfo(title=None, message=" Illegal row, changed to " + str(self.row) + ".")
            if self.row < 0 or self.row >= self.size:
                self.row = random.randint(0, self.size-1);
                self.row_input.delete(0, 'end')
                self.row_input.insert(0, str(self.row))
                messagebox.showinfo(title=None, message=" Illegal row, changed to " + str(self.row) + ".")

            #Parse column entry
            try:
                self.column = int(self.column_input.get())
            except :
                self.column = random.randint(0, self.size-1)
                self.column_input.delete(0, 'end')
                self.column_input.insert(0, str(self.column))
                messagebox.showinfo(title=None, message=" Illegal column, changed to " + str(self.column) + ".")
            if self.column < 0 or self.column >= self.size:
                self.column = random.randint(0, self.size-1)
                self.column_input.delete(0, 'end')
                self.column_input.insert(0, str(self.column))
                messagebox.showinfo(title=None, message=" Illegal column, changed to " + str(self.column) + ".")


        #Parse run speed
        try:
            self.run_speed = int(self.run_speed_input.get())
        except :
            self.run_speed = 20;
            self.run_speed_input.delete(0, 'end')
            self.run_speed_input.insert(0, str(self.run_speed))
            messagebox.showinfo(title=None, message=" Illegal run speed, changed to " + str(self.run_speed) + ".")
        if self.run_speed < 0:
            self.run_speed = 20;
            self.run_speed_input.delete(0, 'end')
            self.run_speed_input.insert(0, str(self.run_speed))
            messagebox.showinfo(title=None, message=" Illegal run speed, changed to " + str(self.run_speed) + ".")
            
        #Setup board
        self.board = [[False for i in range(self.size)] for j in range(self.size)]
        self.board[self.row][self.column] = True
        self.currentSquare = (self.row,self.column)
        self.old = ()
        self.redraw()

    def redraw(self):
        #Calculate the size of the squares.
        dimension = len(self.board)
        square_size = (750)/dimension

        #Set the font size
        self.font = f.Font(size=(-int(0.25*square_size)))

        #Clear previous shapes from canvas, needed for performance
        self.canvas.delete("all")
        #Create array for the object id's for each tile to be stored
        self.rectangles = [[None for x in range(dimension)] for y in range(dimension)]
        #Calculate each tiles location and draw it as empty, storing its object id in the array.
        for y in range(dimension):
            for x in range(dimension):
                x1 = (x*square_size)
                y1 = (y*square_size)
                x2 = ((x+1)*square_size)
                y2 = ((y+1)*square_size)
                temp = self.canvas.create_rectangle(x1, y1, x2, y2, fill="white")
                self.rectangles[y][x] = temp

        #Generate a circle at the player location
        # print(self.row, self.column)
        self.knight = self.canvas.create_oval(self.column*square_size, self.row*square_size, (self.column + 1) * square_size, (self.row + 1) * square_size, fill="black")
        self.canvas.itemconfig(self.rectangles[self.row][self.column], fill="green")
        if self.algorithm_option.get() != "Cull":
            self.canvas.create_text((self.column+1)*square_size-15, (self.row+1)*square_size-10, text="1", font=self.font)
            self.count = 2
        else:
            self.count = 1
        #Keep track of what square we are on and our last position to draw a line from.
        self.old = (self.row, self.column)

    def step(self, row, column):
        time.sleep(self.run_speed/1000)

        #Move the knight to the new coords.
        square_size = (750)/len(self.board)
        self.canvas.coords(self.knight, column*square_size, row*square_size, (column + 1) * square_size, (row + 1) * square_size)
        #Color the new square in green

        self.canvas.itemconfig(self.rectangles[row][column], fill="green")

        #If in path draw mode, draw a line from the center of the old square, to the center of the new square.
        print(self.drawpath)
        if self.drawpath:
            self.canvas.create_line((self.old[1]*square_size)+(square_size/2), (self.old[0]*square_size)+(square_size/2), (column*square_size)+(square_size/2), (row*square_size)+(square_size/2))

        #Draw a number in the bottom left of the square for its visit order.
        self.canvas.create_text((column+1)*square_size-15, (row+1)*square_size-10, text=str(self.count), font=self.font)

        self.old = (row, column)
        self.count += 1
        self.master.update()

    #Prints the chessboard, K for the current location, 0 for a visited square and 1 for unvisited.
    def __str__(self):
        string = ''
        for row in range(len(self.board)):
            for column in range(len(self.board)):
                if row == self.currentSquare[0] and column == self.currentSquare[1] : string += 'K '
                elif self.board[row][column]: string += '0 '
                else: string += '1 '
            string += str(row) + '\n'
        return string

    #Returns a array of all possible moves from the square.
    def attacks(self, osquare):
        #Knights Location
        row = osquare[0]
        column = osquare[1]

        #All 8 possible moves from any position on a chessboard.
        unfiltered = [(row+2,column+1),(row-2,column+1),(row-2,column-1),(row+2,column-1),(row+1,column+2),(row-1,column+2),(row-1,column-2),(row+1,column-2)]

        #For every tuple representing a move in unfiltered, we check if the move is legal if so its included in the output array.
        return [square for square in unfiltered if -1 < square[0] < len(self.board) and -1 < square[1] < len(self.board) and not self.board[square[0]][square[1]]]

    #Called to move the current square to the new location and marks the location as visited.
    def moveKnight(self, square):
        self.currentSquare = (square[0],square[1])
        self.board[square[0]][square[1]] = True
        self.step(square[0], square[1])


#Warnsdorff's knights tour algorithm, uses a max unvisited neighbors to select our next move.
#https://www.geeksforgeeks.org/warnsdorffs-algorithm-knights-tour-problem/
def warnsdorff(size, chessboard):
    count = 1
    while count < size * size:
        #Poison pill if gui user restarts mid run
        if chessboard.stop:
            return

        #If there are no traversable squares from our location, we have failed.
        if not chessboard.attacks(chessboard.currentSquare):
            # print(f'Warnsdorff failed with {size*size-count} novel squares remaining')
            # print(chessboard)
            return f'Warnsdorff failed with {size*size-count} novel squares remaining'
        if testing and count % 10 == 1 : print(chessboard)
        #We select the unvisited traversable square with the lowest number of unvisited adjacent squares.
        current = chessboard.attacks(chessboard.currentSquare)[0]
        for square in chessboard.attacks(chessboard.currentSquare):
            if len(chessboard.attacks(square)) < len(chessboard.attacks(current)):
                current = square
        #We move to that best square
        chessboard.moveKnight(current)
        count += 1
    #If we make it to the end of the loop, we have successfully mapped a knights tour.
    # print('Success...')
    # print(chessboard)
    # return 'Warnsdorff worked'

def cull(size,chessboard):

    path = []
    for i in range(size // 5):
        if i % 2 == 0:
            vertOffset = size - (5 * (i + 1))
            for j in range(size // 5 - 1):
                horizonalOffset = j * 5
                path.extend([(n[0] + vertOffset,n[1] + horizonalOffset) for n in baseOne])
            path.extend([(n[0] + vertOffset,n[1] + size - 5)for n in baseTwo])
        else:
            vertOffset = size - (5 * (i + 1))
            for j in range(size // 5 - 1):
                horizonalOffset = j * 5
                path.extend([(n[0] + vertOffset, size - 1 - (n[1] + horizonalOffset)) for n in baseOne])
            path.extend([(n[0] + vertOffset, size - 1 - (n[1] + size - 5))for n in baseTwo])
    # print(path)
    for square in path:
        if chessboard.stop:
            return
        chessboard.moveKnight(square)
    # return 'hey'

baseOne = [(4,0),(2,1),(0,0),(1,2),(0,4),(2,3),(4,4),(3,2),(2,4),(4,3),(3,1),(1,0),(0,2),(1,4),
(2,2),(0,3),(1,1),(3,0),(4,2),(3,4),(1,3),(0,1),(2,0),(4,1),(3,3)]
baseTwo = [(4,0),(3,2),(4,4),(2,3),(0,4),(1,2),(0,0),(2,1),(3,3),(4,1),(2,0),(0,1),(2,2),(1,4),
(0,2),(1,0),(3,1),(4,3),(2,4),(0,3),(1,1),(3,0),(4,2),(3,4),(1,3)]
root = Tk()
#places the window at the top left corner.
root.geometry("+0+0")
my_gui = ChessBoard(root)
root.mainloop()
