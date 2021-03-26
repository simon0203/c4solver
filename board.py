# Board class to represent a board of connect-four game

class Line:
    def __init__(self, line_index, line_coordinates):
        # line index in the list of lines (note : maybe not needed)
        self.line_index = line_index

        # list of (i,j) coordinates of the line in the board
        self.line_coordinates = line_coordinates

        # number of tokens of player 1 and player 2 in the line
        self.tokens = [0, 0]

        # line status: 0=open, 1=possible only for player 1, 2=possible only for player 2, 3=not possible anymore
        self.status = 0

    def add_play(self, player):
        self.tokens[player-1] += 1
        if self.status == 0:
            #line now only possible for current player 
            self.status = player
        elif self.status != player:
            #line was possible for opponent, now not possible for any player
            self. status = 3
        #print("line_add_update", self.line_index, self.line_coordinates, self.tokens, self.status)

    def remove_play(self, player):
        self.tokens[player-1] -= 1
        if self.tokens[0] == 0 and self.tokens[1] == 0:
            self.status = 0
        elif self.tokens[0] == 0:
            self.status = 2
        elif self.tokens[1] == 0:
            self.status = 1
        #print("line_remove_update", self.line_index, self.line_coordinates, self.tokens, self.status)

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

        # list of played moves (used to reverse a move)
        self.play_list = []

        # move ordering
        self.ordered_moves = []

        #------------------- Lines --------------
        # list of all lines on the board (storing coordinates and status)
        self.lines = []

        # dictionary to know the lines going through a given (i,j) cell
        # keys = (i,j) values =[line_index1, line_index2, ...], the line indexes going through (i,j)
        self.lines_lookup = {}

        # initialize the lines list and lookup table
        self.create_line_list()

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

    # string representation for storing in a transposition table
    def string_rep(self):
        str_rep = ""
        for i in range(self.nb_rows):
            for j in range(self.nb_cols):
                if self.board[i][j] == 1:
                    str_rep += "O"
                elif self.board[i][j] == 2:
                    str_rep += "X"
                else:
                    str_rep += "."
        return str_rep

    # init the board from a string representation
    # note : we allow useless characters (like space) for readability
    def init_from_string(self, str_rep):
        # check string representation length is compatible with board dimensions
        # if self.nb_rows*self.nb_cols != len(str_rep):
        #    return

        k = 0
        for i in range(self.nb_rows):
            for j in range(self.nb_cols):
                next_cell_found = False
                while not next_cell_found and k < len(str_rep):
                    cell = str_rep[k]
                    if cell == 'O':
                        self.board[i][j] = 1
                        next_cell_found = True
                    elif cell == 'X':
                        self.board[i][j] = 2
                        next_cell_found = True
                    elif cell == '.':
                        self.board[i][j] = 0
                        next_cell_found = True
                    k += 1

        self.init_board_variables()

    # function to init the internal board variables (like number of empty squares in each column)
    # should be called after an init of the board with a representation string
    def init_board_variables(self):
        self.total_empty = self.nb_rows * self.nb_cols

        for j in range(self.nb_cols):
            self.heights[j] = 0
            for i in range(self.nb_rows):
                if self.board[i][j] != 0:
                    self.heights[j] += 1
                    self.total_empty -= 1

        # player 1 to play if parity of empty squares is similar to empty board
        if self.total_empty % 2 == self.nb_rows*self.nb_cols % 2:
            self.player = 1
        else:
            self.player = 2

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
            self.play_list.append(j)
            self.update_line_status(i=col_height, j=j, is_remove=False)
            self.update_win(j)

            self.reverse_player()

            return True
        else:
            # this column is already full, not valid play
            return False

    # create a table with the list of possible lines in the board
    # this table is used to store the status of each line (possible for player 1, possible for player 2, not possible anymore)
    def create_line_list(self):        
        line_index = 0
        for j in range(self.nb_cols):
            for i in range(self.nb_rows):
                # possible vertical line starting at (i,j)
                if i + 3 < self.nb_rows:
                    t = ((i,j), (i+1,j), (i+2,j), (i+3,j))
                    line = Line(line_index, line_coordinates=t)
                    self.lines.append(line)
                    self.add_line_to_lookup(t, line_index)
                    line_index += 1

                # possible horizontal line starting at (i,j)
                if j+3 < self.nb_cols:
                    t = ((i,j), (i,j+1), (i,j+2), (i,j+3))
                    line = Line(line_index, line_coordinates=t)
                    self.lines.append(line)
                    self.add_line_to_lookup(t, line_index)
                    line_index += 1

                # possible diagonal lines starting at (i,j)
                if j+3 < self.nb_cols and i+3 < self.nb_rows:
                    t = ((i,j), (i+1,j+1), (i+2,j+2), (i+3,j+3))
                    line = Line(line_index, line_coordinates=t)
                    self.lines.append(line)
                    self.add_line_to_lookup(t, line_index)
                    line_index += 1

                if j+3 < self.nb_cols and i-3 >= 0:
                    t = ((i,j), (i-1,j+1), (i-2,j+2), (i-3,j+3))
                    line = Line(line_index, line_coordinates=t)
                    self.lines.append(line)
                    self.add_line_to_lookup(t, line_index)
                    line_index += 1

    def add_line_to_lookup(self, line_coordinates, line_index):
        for (i,j) in line_coordinates:
            dict_value = self.lines_lookup.setdefault((i,j), [])
            dict_value.append(line_index)
            self.lines_lookup[(i,j)] = dict_value

    # update the status of each line going through the cell (i,j)
    # if is_remove=True, a token was added by current player in (i, j)
    # if is_remove=False, a token was removed
    def update_line_status(self, i, j, is_remove = False):
        target_lines = self.lines_lookup[(i,j)]
        for line_index in target_lines:
            if is_remove:
                self.lines[line_index].remove_play(self.player)
            else:
                self.lines[line_index].add_play(self.player)

    def print_line_list(self):
        print("===number of lines:", len(self.lines))
        for line in self.lines:
            print("line", line.line_index, "coordinates:", line.line_coordinates)
        print("====lookup table:")
        for key in self.lines_lookup:
            print("cell", key, "  lines:", self.lines_lookup[key])

    # return a vector of 4 values indicating the number of lines going through cell (i, j)
    # with 0, 1, 2, 3 token still possible for player v
    #note 1 : seems a bit too slow to be effective (maybe effectiveness depends a lot on the position)
    #note 2 : code to go through the lines is very similar to codes to check if a win was reached
    def line_state(self, i, j, v):
        nb_lines = [0, 0, 0, 0]

        # possible vertical line
        if i >= 3:
            t = [self.board[i-1][j], self.board[i-2][j], self.board[i-3][j]]
            a = t.count(v)
            b = t.count('0')
            if a+b == 4:
               nb_lines[a] += 1

        # possible horizontal lines
        if j-3 >= 0:
            t = [self.board[i][j-3], self.board[i][j-2], self.board[i][j-1]]
            a = t.count(v)
            b = t.count('0')
            if a+b == 4:
               nb_lines[a] += 1

        if j-2 >= 0 and j+1 < self.nb_cols:
            t = [self.board[i][j-2], self.board[i][j-1], self.board[i][j+1]]
            a = t.count(v)
            b = t.count('0')
            if a+b == 4:
               nb_lines[a] += 1

        if j-1 >= 0 and j+2 < self.nb_cols:
            t = [self.board[i][j-1], self.board[i][j+1], self.board[i][j+2]]
            a = t.count(v)
            b = t.count('0')
            if a+b == 4:
               nb_lines[a] += 1

        if j+3 < self.nb_cols:
            t = [self.board[i][j+1], self.board[i][j+2], self.board[i][j+3]]
            a = t.count(v)
            b = t.count('0')
            if a+b == 4:
               nb_lines[a] += 1

        # possible diagonal lines
        if j-3 >= 0 and i-3 >= 0:
            t = [self.board[i-3][j-3], self.board[i-2][j-2], self.board[i-1][j-1]]
            a = t.count(v)
            b = t.count('0')
            if a+b == 4:
               nb_lines[a] += 1

        if j-2 >= 0 and i-2 >= 0 and j+1 < self.nb_cols and i+1 < self.nb_rows:
            t = [self.board[i-2][j-2], self.board[i-1][j-1], self.board[i+1][j+1]]
            a = t.count(v)
            b = t.count('0')
            if a+b == 4:
               nb_lines[a] += 1

        if j-1 >= 0 and i-1 >= 0 and j+2 < self.nb_cols and i+2 < self.nb_rows:
            t = [self.board[i-1][j-1], self.board[i+1][j+1], self.board[i+1][j+2]]
            a = t.count(v)
            b = t.count('0')
            if a+b == 4:
               nb_lines[a] += 1

        if j+3 < self.nb_cols and i+3 < self.nb_rows:
            t = [self.board[i+1][j+1], self.board[i+2][j+2], self.board[i+3][j+3]]
            a = t.count(v)
            b = t.count('0')
            if a+b == 4:
               nb_lines[a] += 1

        if j-3 >= 0 and i+3 < self.nb_rows:
            t = [self.board[i+3][j-3], self.board[i+2][j-2], self.board[i+1][j-1]]
            a = t.count(v)
            b = t.count('0')
            if a+b == 4:
               nb_lines[a] += 1

        if j-2 >= 0 and i+2 < self.nb_rows and j+1 < self.nb_cols and i-1 >= 0:
            t = [self.board[i+2][j-2], self.board[i+1][j-1], self.board[i-1][j+1]]
            a = t.count(v)
            b = t.count('0')
            if a+b == 4:
               nb_lines[a] += 1

        if j-1 >= 0 and i+1 < self.nb_rows and j+2 < self.nb_cols and i-2 >= 0:
            t = [self.board[i+1][j-1], self.board[i-1][j+1], self.board[i-1][j+2]]
            a = t.count(v)
            b = t.count('0')
            if a+b == 4:
               nb_lines[a] += 1

        if j+3 < self.nb_cols and i-3 >= 0:
            t = [self.board[i-1][j+1], self.board[i-2][j+2], self.board[i-3][j+3]]
            a = t.count(v)
            b = t.count('0')
            if a+b == 4:
               nb_lines[a] += 1

        return nb_lines

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
    
    def remove_last_play(self):
        # safe guard, nothing to do if the list of moves is empty
        if not self.play_list:
            return

        # get and remove the last move from the list of played moves
        j = self.play_list.pop()

        i = self.heights[j] - 1
        if i >= 0:
            self.board[i][j] = 0
            self.heights[j] = i
            self.total_empty = self.total_empty + 1
            self.is_win = False
            self.reverse_player()
            self.update_line_status(i=i, j=j, is_remove=True)

    def is_finished(self):
        if self.total_empty > 0:
            return False
        else:
            return True

    def order_moves(self):
        self.ordered_moves = []

        # simple order (available column order)
        for j in range(self.nb_cols):
            if self.heights[j] < self.nb_rows:
                self.ordered_moves.append(j)

        # priority to moves improving line completion
        # lines = [-1 for j in range(self.nb_cols)]
        # for j in range(self.nb_cols):
        #     if self.heights[j] < self.nb_rows:
        #         line_state_result = self.line_state(self.heights[j], j, self.player)
        #         if self.player == 1:
        #             opp = 2
        #         else:
        #             opp =1
        #         line_opp = self.line_state(self.heights[j], j, opp)

        #         #print(lines)
        #         #print(line_state_result)
        #         lines[j] = line_state_result[0]+ 20*line_state_result[1] + 400*line_state_result[2] + 8000*line_state_result[3]
        #         lines[j] += line_opp[0]+ 20*line_opp[1] + 400*line_opp[2] + 8000*line_opp[3]
        #         #self.ordered_moves.append(j)
        # while(lines.count(-1) < self.nb_cols):
        #     max_index = lines.index(max(lines))
        #     self.ordered_moves.append(max_index)
        #     lines[max_index] = -1

        # priority to follow-up moves
        # followup_j = -1
        # if self.play_list:
        #     followup_j=self.play_list[-1]
        #     if self.heights[followup_j] < self.nb_rows:
        #         self.ordered_moves.append(followup_j)
        # for j in range(self.nb_cols):
        #     if j !=  followup_j and self.heights[j] < self.nb_rows:
        #         self.ordered_moves.append(j)

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

    # check update_win
    b.play(3)
    b.play(4)
    b.play(4)
    print("No win after play at 5:")
    b.play(5)
    b.show()
    print("is_win=", b.is_win)
    print(" ")

    b.play(6)
    b.play(6)
    print("Win after play at 5:")
    b.play(5)
    b.show()
    print("is_win=", b.is_win)
    print(" ")

    # test of remove_last_play()
    print("Reverse one move:")
    b.remove_last_play()
    b.show()
    print("is_win=", b.is_win)
    print(" ")

    print("Reverse one more move:")
    b.remove_last_play()
    b.show()
    print("is_win=", b.is_win)
    print(" ")

    # test of string representation
    print("String representation:")
    print(b.string_rep())

    # test of init from string representation
    # should obtain the same string
    c = Board()
    c.init_from_string(b.string_rep())
    print("Init with above string representation")
    print(c.string_rep())

    # init from string representation
    print("")
    print("Init with allis_4_1:")
    allis_4_1 = "X.OOX.. ..XXX.. ..OO... ...O... ...O... ...X..."
    print(allis_4_1)
    c = Board()
    c.init_from_string(allis_4_1)
    c.show()

    # line list
    c.print_line_list()