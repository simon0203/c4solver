# Python solver for connect-four

# for process_time()
import time
import copy
from board import Board

class Win_Loss:
    def __init__(self):
        self.total_calls = 0
        self.elapsed_time = 0
        self.transpo_table = set()

    def clear_tranpo_table(self):
        self.transpo_table = set()

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
        print("Transpo table:", len(self.transpo_table))

    # board is supposed to be a Board object
    # return True if the current player has a winning move
    def recursive_win_loss(self, board, depth=0):
        self.total_calls += 1

        board.order_moves()
        #note: deep copy needed because board can be changed in further recursive calls
        ordered_moves = copy.deepcopy(board.ordered_moves)

        for j in ordered_moves:
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

                    str_rep = board.string_rep()
                    if str_rep in self.transpo_table:
                        result = False
                    else:
                        result = self.recursive_win_loss(board, depth+1)
                        if result == False:
                            self.transpo_table.add(str_rep)

                    if result == False:
                        #opponent loses, so this is a win
                        board.remove_last_play()
                        return True
                board.remove_last_play()
        # all moves resulted in an opponent win, so this is a loss
        return False

    # return a winning move (if there is one) for the given position
    # board is modified with the winning move
    # mainly for use against a testing human player
    def best_move(self, board):
        result = self.recursive_win_loss(board)
        if result == False:
            # Loss position, any move is ok, play randomly
            board.order_moves()
            for j in board.ordered_moves:
                if board.play(j):
                    return board.ordered_moves[0]
        else:
            # this is a Win, find the winning move in the transpo table
            board.order_moves()
            for j in board.ordered_moves:
                if board.play(j):
                    str_rep = board.string_rep()
                    if str_rep in self.transpo_table:
                        return j
                    else:
                        board.remove_last_play()


if __name__ == "__main__":
    b = Board(nb_rows=4, nb_cols=5)
    b.show()
    
    compute = Win_Loss()
    result = compute.compute_is_win(b)
    print("is_win=", result)
    compute.show_stats()

    # check a short sequence of best moves
    compute.best_move(b)
    b.show()
    compute.best_move(b)
    b.show()
    compute.best_move(b)
    b.show()
    compute.best_move(b)
    b.show()
    compute.best_move(b)
    b.show()
    compute.best_move(b)
    b.show()
    compute.best_move(b)
    b.show()
    compute.best_move(b)
    b.show()
    compute.best_move(b)
    b.show()
    compute.best_move(b)
    b.show()
    
