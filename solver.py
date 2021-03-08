# Python solver for connect-four

from board import Board

class Win_Loss:
    #def __init__(self):
        # TODO: define here a table to store results

    # board is supposed to be a Board object
    # return True if the current player has a winning move
    def compute_is_win(self, board, depth=0):
        for j in range(board.nb_cols):
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
    b = Board(nb_rows=4, nb_cols=5)
    b.show()
    compute = Win_Loss()
    print(compute.compute_is_win(b))
