import random
class ChessBoard:
    def __init__(self, size, row, column):
        self.board = [[False for i in range(size)] for j in range(size)]
        self.board[row][column] = True
        self.currentSquare = (row,column)

    def __str__(self):
        string = ''
        for row in range(len(self.board)):
            for column in range(len(self.board)):
                if row == self.currentSquare[0] and column == self.currentSquare[1] : string += 'K '
                elif self.board[row][column]: string += '0 '
                else: string += '1 '
            string += str(row) + '\n'
        return string

    def attacks(self, osquare):
        row = osquare[0]
        column = osquare[1]
        unfiltered = [(row+2,column+1),(row-2,column+1),(row-2,column-1),(row+2,column-1),(row+1,column+2),(row-1,column+2),(row-1,column-2),(row+1,column-2)]
        return [square for square in unfiltered if -1 < square[0] < len(self.board) and -1 < square[1] < len(self.board) and not self.board[square[0]][square[1]]]

    def moveKnight(self, square):
        self.currentSquare = (square[0],square[1])
        self.board[square[0]][square[1]] = True


size = int(input("Enter the size of the chess board: "))
copy = chessboard = ChessBoard(size,random.randint(0,size-1),random.randint(0,size-1))
count = 1

while count < size * size:
    if not chessboard.attacks(chessboard.currentSquare):
        print(f'The algorithm failed with {size*size-count} novel squares remaining')
        print(chessboard)
        exit()
    if count % 10 == 1 : print(chessboard)
    current = chessboard.attacks(chessboard.currentSquare)[0]
    for square in chessboard.attacks(chessboard.currentSquare):
        if len(chessboard.attacks(square)) < len(chessboard.attacks(current)):
            current = square
    chessboard.moveKnight(current)
    count += 1
print('Success...')
print(chessboard)
