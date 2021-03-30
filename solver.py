# Python solver for connect-four

# for process_time()
import time
import copy
from board import Board

class Win_Loss:
    def __init__(self):
        self.total_calls = 0
        self.elapsed_time = 0
        
        # transposition table of the current computation
        self.transpo_table = set()
        
        # transposition table of a previous computation used as an oracle
        self.oracle_table = set()

        # indicate if the current computation is a direct one or a check one
        # in check computation, moves are ordered with the oracle table
        self.is_check = False

    def clear_tranpo_table(self):
        self.transpo_table = set()

    def clear_oracle_table(self):
        self.check_table = set()

    def compute_is_win(self, board, is_check=False):
        self.total_calls = 0
        self.is_check = is_check
        if self.is_check:
            self.oracle_table = self.transpo_table
            self.transpo_table = set()
            print("Check computation")
            print("Oracle table:", len(self.oracle_table))

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

        ordered_moves = board.get_ordered_moves()

        # before anything else, check obvious wins, and existence of a known transposition
        for j in ordered_moves:
            if board.play(j):
                # obvious win by rules (4 in a row)
                if board.is_win:
                    board.remove_last_play()
                    return True
                
                if board.is_finished():
                    # game is finished, it implies this was a player 2 board, and he wins
                    board.remove_last_play()
                    return True

                # existence of transposition
                str_rep = board.string_rep()
                board.remove_last_play()
                if str_rep in self.transpo_table:
                    # loss for opponent, so this is an already known winning move, nothing to do
                    return True

        # for check computations, give priority to winning moves in the oracle table
        if self.is_check:
            winning_move = None
            for j in ordered_moves:
                if board.play(j):
                    str_rep = board.string_rep()
                    board.remove_last_play()
                    if str_rep in self.oracle_table:
                        # loss for opponent, so this is a winning move
                        winning_move = j
                        break
            if winning_move != None:
                # add the winning move in front of the list of moves
                # note : no need to delete the winning move from its original position in the list
                ordered_moves.insert(0, winning_move)

        # recursive step, compute the win-loss of each possible move until finding a winning one
        for j in ordered_moves:
            if depth<3:
                s = ""
                for k in range(depth+1):
                    s += "-"
                print(s, j)
            if board.play(j):
                result = self.recursive_win_loss(board, depth+1)
                if result == False:
                    str_rep = board.string_rep()
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
            ordered_moves = board.get_ordered_moves()
            for j in ordered_moves:
                if board.play(j):
                    return ordered_moves[0]
        else:
            # this is a Win, find the winning move in the transpo table
            ordered_moves = board.get_ordered_moves()
            for j in ordered_moves:
                if board.play(j):
                    str_rep = board.string_rep()
                    if str_rep in self.transpo_table:
                        return j
                    else:
                        board.remove_last_play()


if __name__ == "__main__":
    #b = Board(nb_rows=4, nb_cols=5)
    #b.show()
    
    b = Board()
    
    # diagram 3.10, player 1, win
    allis_3_10 = "...OXO. ...XOX. ...OOO. ...XXX. ....... ......."
    
    # diagram 3.14, player 2, loss
    allis_3_14 = "OXOOX.. .OXXX.. .OOOX.. ...XO.. ....... ......."

    # diagram 4.1, player 1, loss
    allis_4_1 = "X.OOX.. ..XXX.. ..OO... ...O... ...O... ...X..."

    # diagram 4.2, player 1, loss
    allis_4_2 = "X.OOX.. X.XXX.. ..OO... ..OO... ...O... ...X..."

    # diagram 4.5, player 1, win
    allis_4_5 = "OXOOX.. .OXXX.. .OOOX.. ..XXO.. ...O... ...X..."

    # diagram 4.7, player 1, loss
    allis_4_7 = "X.OOX.X ..XXX.. ..OOO.. ...O... ...O... ...X..."

    # diagram 5.4, player 1, loss
    allis_5_4 = "..OOX.X ..OXX.O ..XO..X ..OX..O ..XX..X ..OO..O"

    # diagram 11.1, player 1, win
    allis_11_1 = "..OOX.. ..XXX.. ..OO... ....... ....... ......."

    # diagram 11.1 after move5, player 1, win
    allis_11_1_move5 = "OXOOX.. ..XXX.. ..OO... ....... ....... ......."

    # diagram 11.1 after move 5 and 6, player 1, win
    allis_11_1_move6 = "OXOOX.. .OXXX.. ..OO... ...X... ....... ......."

    # diagram 11.1 after move 5, 6 and 7, player 1, win
    allis_11_1_move7 = "OXOOX.. .OXXX.. .OOOX.. ...X... ....... ......."

    b.init_from_string(allis_3_14)
    b.show()

    compute = Win_Loss()
    result = compute.compute_is_win(b)
    print("is_win=", result)
    compute.show_stats()

    result = compute.compute_is_win(b, is_check=True)
    print("is_win=", result)
    compute.show_stats()

    # check a short sequence of best moves
    # compute.best_move(b)
    # b.show()
    # compute.best_move(b)
    # b.show()
    # compute.best_move(b)
    # b.show()
    # compute.best_move(b)
    # b.show()
    # compute.best_move(b)
    # b.show()
    # compute.best_move(b)
    # b.show()
    # compute.best_move(b)
    # b.show()
    # compute.best_move(b)
    # b.show()
    # compute.best_move(b)
    # b.show()
    # compute.best_move(b)
    # b.show()
    
