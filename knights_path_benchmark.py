#Thomas Walker, Adam Shaw, Elise Evans, Mason Humphrey
#Knights Path Benchmarking Refactor
#3/25/2021
#Design/Analysis Project 2
#This class benchmarks our two algorithms against each other and to ensure they are running in linear time.

import random, copy, time
from tkinter import Tk, Label, Button, Canvas, Entry, Checkbutton, Frame, IntVar, messagebox, OptionMenu, StringVar
import tkinter.font as f

class ChessBoard:
    #Constructor with size and starting row/column.
    #We represent squares in this class as tuples with row, column
    def __init__(self, size, row, column):

        #Setup our board with our initial parameters.
        self.board = [[False for i in range(size)] for j in range(size)]
        self.board[row][column] = True
        self.currentSquare = (row,column)

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
        # self.step(square[0], square[1])


#Warnsdorff's knights tour algorithm, uses a max unvisited neighbors to select our next move.
#https://www.geeksforgeeks.org/warnsdorffs-algorithm-knights-tour-problem/
def warnsdorff(size, chessboard):
    count = 1
    while count < size * size:
        #If there are no traversable squares from our location, we have failed.
        if not chessboard.attacks(chessboard.currentSquare):
            # print(f'Warnsdorff failed with {size*size-count} novel squares remaining')
            # print(chessboard)
            return False
        # if testing and count % 10 == 1 : print(chessboard)
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
    return True

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
        chessboard.moveKnight(square)
    return True

baseOne = [(4,0),(2,1),(0,0),(1,2),(0,4),(2,3),(4,4),(3,2),(2,4),(4,3),(3,1),(1,0),(0,2),(1,4),
(2,2),(0,3),(1,1),(3,0),(4,2),(3,4),(1,3),(0,1),(2,0),(4,1),(3,3)]
baseTwo = [(4,0),(3,2),(4,4),(2,3),(0,4),(1,2),(0,0),(2,1),(3,3),(4,1),(2,0),(0,1),(2,2),(1,4),
(0,2),(1,0),(3,1),(4,3),(2,4),(0,3),(1,1),(3,0),(4,2),(3,4),(1,3)]


print("Warnsdorff outputs: Size, Time(s), Success")
for i in range(1, 100):
    size = i * 5
    start = time.time()
    result = warnsdorff(size, ChessBoard(size, size-1, 0))
    end = time.time()
    print(str(size) + ", " + str(end-start) + ", " + str(result))


print("Cull outputs: Size, Time(s), Success")
for i in range(1, 100):
    size = i * 5
    start = time.time()
    result = cull(size, ChessBoard(size, size-1, 0))
    end = time.time()
    print(str(size) + ", " + str(end-start) + ", " + str(result))