# Python solver for connect-four

# correct size for real game is 6x7
nb_rows = 4
nb_cols = 5

class Board:
    def __init__(self):
        # board raw representation
        self.board = [[0 for j in range(nb_cols)] for i in range(nb_rows)]
        
        # current height of each board column
        self.heights = [0 for j in range(nb_cols)]

        # number of empty squares (used to know if the game is finished or not)
        self.total_empty = nb_rows * nb_cols

        # current player (1 = first player, 2=second player)
        self.player = 1

        # updated when after each play in a column (True if last play created 4-in-row)
        self.is_win = False

    def reverse_player(self):
        if self.player == 1:
            self.player = 2
        else:
            self.player = 1

    # play in column j
    # return True if play is valid
    def play(self, j):
        col_height = self.heights[j]
        if col_height < nb_rows:
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
        if j-2 >= 0 and j+1 < nb_cols:
            if self.board[i][j-2] == self.player and self.board[i][j-1] == self.player and self.board[i][j+1] == self.player:
                self.is_win = True
                #print("win 2")
                return
        if j-1 >= 0 and j+2 < nb_cols:
            if self.board[i][j-1] == self.player and self.board[i][j+1] == self.player and self.board[i][j+2] == self.player:
                self.is_win = True
                #print("win 3")
                return
        if j+3 < nb_cols:
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

        if j-2 >= 0 and i-2 >= 0 and j+1 < nb_cols and i+1 < nb_rows:
            if self.board[i-2][j-2] == self.player and self.board[i-1][j-1] == self.player and self.board[i+1][j+1] == self.player:
                self.is_win = True
                #print("win 6")
                return

        if j-1 >= 0 and i-1 >= 0 and j+2 < nb_cols and i+2 < nb_rows:
            if self.board[i-1][j-1] == self.player and self.board[i+1][j+1] == self.player and self.board[i+2][j+2] == self.player:
                self.is_win = True
                #print("win 7")
                return

        if j+3 < nb_cols and i+3 < nb_rows:
            if self.board[i+1][j+1] == self.player and self.board[i+2][j+2] == self.player and self.board[i+3][j+3] == self.player:
                self.is_win = True
                #print("win 8")
                return

        if j-3 >= 0 and i+3 < nb_rows:
            if self.board[i+3][j-3] == self.player and self.board[i+2][j-2] == self.player and self.board[i+1][j-1] == self.player:
                self.is_win = True
                #print("win 9")
                return

        if j-2 >= 0 and i+2 < nb_rows and j+1 < nb_cols and i-1 >= 0:
            if self.board[i+2][j-2] == self.player and self.board[i+1][j-1] == self.player and self.board[i-1][j+1] == self.player:
                self.is_win = True
                #print("win 10")
                return

        if j-1 >= 0 and i+1 < nb_rows and j+2 < nb_cols and i-2 >= 0:
            if self.board[i+1][j-1] == self.player and self.board[i-1][j+1] == self.player and self.board[i-2][j+2] == self.player:
                self.is_win = True
                #print("win 11")
                return

        if j+3 < nb_cols and i-3 >= 0:
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

class Win_Loss:
    #def __init__(self):
        # TODO: define here a table to store results

    # board is supposed to be a Board object
    # return True if the current player has a winning move
    def compute_is_win(self, board, depth=0):
        for j in range(nb_cols):
            if depth<3:
                s = ""
                for k in range(depth+1):
                    s += "-"
                print(s, j)
            if board.play(j):
                if board.is_win:
                    board.remove_last_play(j)
                    return True
                else:
                    if board.is_finished():
                        # game is finished, it implies this was a player 2 board, and he wins
                        board.remove_last_play(j)
                        return True

                    result = self.compute_is_win(board, depth+1)
                    if result == False:
                        #opponent loses, so this is a win
                        board.remove_last_play(j)
                        return True
                board.remove_last_play(j)
        # all moves resulted in an opponent win, so this is a loss
        return False

if __name__ == "__main__":
    b = Board()
    print(b.board)
    compute = Win_Loss()
    print(compute.compute_is_win(b))
