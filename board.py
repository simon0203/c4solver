# Board class to represent a board of connect-four game

class Board:
    # default board size is 6x7
    def __init__(self, nb_rows=6, nb_cols=7):
        self.nb_rows = nb_rows
        self.nb_cols = nb_cols
        
        # board raw representation
        self.board = [[0 for j in range(self.nb_cols)] for i in range(self.nb_rows)]
        
        # current height of each board column
        self.heights = [0 for j in range(self.nb_cols)]

        # number of empty squares (used to know if the game is finished or not)
        self.total_empty = self.nb_rows * self.nb_cols

        # current player (1 = first player, 2=second player)
        self.player = 1

        # updated when after each play in a column (True if last play created 4-in-row)
        self.is_win = False

    # print a readable board representation
    def show(self):
        for i in range(self.nb_rows):
            row_str = ""
            for j in range(self.nb_cols):
                if self.board[self.nb_rows-1-i][j] == 1:
                    row_str += "O"
                elif self.board[self.nb_rows-1-i][j] == 2:
                    row_str += "X"
                else:
                    row_str += "."
            print(row_str)
        print(" ")

    def reverse_player(self):
        if self.player == 1:
            self.player = 2
        else:
            self.player = 1

    # play in column j
    # return True if play is valid
    def play(self, j):
        col_height = self.heights[j]
        if col_height < self.nb_rows:
            self.board[col_height][j] = self.player
            self.heights[j] = col_height + 1
            self.total_empty = self.total_empty -1

            self.update_win(j)

            self.reverse_player()

            return True
        else:
            # this column is already full, not valid play
            return False

    def update_win(self, j):
        # note : [i][j] is supposed to be equal to self.player (so not tested below)
        i = self.heights[j] -1
        #print(i, j)

        # possible vertical win
        if i >= 3:
            if self.board[i-1][j] == self.player and self.board[i-2][j] == self.player and self.board[i-3][j] == self.player:
                self.is_win = True
                #print("win 0")
                return

        # possible horizontal wins
        if j-3 >= 0:
            if self.board[i][j-3] == self.player and self.board[i][j-2] == self.player and self.board[i][j-1] == self.player:
                self.is_win = True
                #print("win 1")
                return
        if j-2 >= 0 and j+1 < self.nb_cols:
            if self.board[i][j-2] == self.player and self.board[i][j-1] == self.player and self.board[i][j+1] == self.player:
                self.is_win = True
                #print("win 2")
                return
        if j-1 >= 0 and j+2 < self.nb_cols:
            if self.board[i][j-1] == self.player and self.board[i][j+1] == self.player and self.board[i][j+2] == self.player:
                self.is_win = True
                #print("win 3")
                return
        if j+3 < self.nb_cols:
            if self.board[i][j+1] == self.player and self.board[i][j+2] == self.player and self.board[i][j+3] == self.player:
                self.is_win = True
                #print("win 4")
                return

        # possible diagonal wins
        if j-3 >= 0 and i-3 >= 0:
            if self.board[i-3][j-3] == self.player and self.board[i-2][j-2] == self.player and self.board[i-1][j-1] == self.player:
                self.is_win = True
                #print("win 5")
                return

        if j-2 >= 0 and i-2 >= 0 and j+1 < self.nb_cols and i+1 < self.nb_rows:
            if self.board[i-2][j-2] == self.player and self.board[i-1][j-1] == self.player and self.board[i+1][j+1] == self.player:
                self.is_win = True
                #print("win 6")
                return

        if j-1 >= 0 and i-1 >= 0 and j+2 < self.nb_cols and i+2 < self.nb_rows:
            if self.board[i-1][j-1] == self.player and self.board[i+1][j+1] == self.player and self.board[i+2][j+2] == self.player:
                self.is_win = True
                #print("win 7")
                return

        if j+3 < self.nb_cols and i+3 < self.nb_rows:
            if self.board[i+1][j+1] == self.player and self.board[i+2][j+2] == self.player and self.board[i+3][j+3] == self.player:
                self.is_win = True
                #print("win 8")
                return

        if j-3 >= 0 and i+3 < self.nb_rows:
            if self.board[i+3][j-3] == self.player and self.board[i+2][j-2] == self.player and self.board[i+1][j-1] == self.player:
                self.is_win = True
                #print("win 9")
                return

        if j-2 >= 0 and i+2 < self.nb_rows and j+1 < self.nb_cols and i-1 >= 0:
            if self.board[i+2][j-2] == self.player and self.board[i+1][j-1] == self.player and self.board[i-1][j+1] == self.player:
                self.is_win = True
                #print("win 10")
                return

        if j-1 >= 0 and i+1 < self.nb_rows and j+2 < self.nb_cols and i-2 >= 0:
            if self.board[i+1][j-1] == self.player and self.board[i-1][j+1] == self.player and self.board[i-2][j+2] == self.player:
                self.is_win = True
                #print("win 11")
                return

        if j+3 < self.nb_cols and i-3 >= 0:
            if self.board[i-1][j+1] == self.player and self.board[i-2][j+2] == self.player and self.board[i-3][j+3] == self.player:
                self.is_win = True
                #print("win 12")
                return
    
    def remove_last_play(self, j):
        i = self.heights[j] - 1
        if i >= 0:
            self.board[i][j] = 0
            self.heights[j] = i
            self.total_empty = self.total_empty + 1
            self.is_win = False
            self.reverse_player()

    def is_finished(self):
        if self.total_empty > 0:
            return False
        else:
            return True

# unit tests for Board class, can be checked with python board.py
if __name__ == "__main__":
    # simple tests of play() and show()
    b = Board()
    print("Empty default size board:")
    b.show()
    b.play(2)
    b.play(3)
    b.play(2)
    b.play(2)
    print("Board after play at 2, 3, 2, 2:")
    b.show()
