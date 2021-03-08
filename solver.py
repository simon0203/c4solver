# Python solver for connect-four

# for process_time()
import time

from board import Board

class Win_Loss:
    def __init__(self):
        self.total_calls = 0
        self.elapsed_time = 0

    def compute_is_win(self, board):
        self.total_calls = 0
        t_start = time.process_time()
        result = self.recursive_win_loss(board)
        t_stop = time.process_time()
        self.elapsed_time = t_stop - t_start
        return result

    def show_stats(self):
        print("Elapsed time:", self.elapsed_time)
        print("Total calls:", self.total_calls)

    # board is supposed to be a Board object
    # return True if the current player has a winning move
    def recursive_win_loss(self, board, depth=0):
        self.total_calls += 1
        for j in range(board.nb_cols):
            if depth<3:
                s = ""
                for k in range(depth+1):
                    s += "-"
                print(s, j)
            if board.play(j):
                if board.is_win:
                    board.remove_last_play()
                    return True
                else:
                    if board.is_finished():
                        # game is finished, it implies this was a player 2 board, and he wins
                        board.remove_last_play()
                        return True

                    result = self.recursive_win_loss(board, depth+1)
                    if result == False:
                        #opponent loses, so this is a win
                        board.remove_last_play()
                        return True
                board.remove_last_play()
        # all moves resulted in an opponent win, so this is a loss
        return False

if __name__ == "__main__":
    b = Board(nb_rows=4, nb_cols=5)
    b.show()
    
    compute = Win_Loss()
    result = compute.compute_is_win(b)
    print("is_win=", result)
    compute.show_stats()
