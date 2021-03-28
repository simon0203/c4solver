# Line class to represent a possible 4-in-line on a board of connect-four

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
            #line was possible for opponent or already not possible, now not possible for any player
            self.status = 3
        #print("line_add_update", self.line_index, self.line_coordinates, self.tokens, self.status)

    def remove_play(self, player):
        self.tokens[player-1] -= 1
        if self.tokens[0] == 0 and self.tokens[1] == 0:
            self.status = 0
        elif self.tokens[0] == 0:
            self.status = 2
        elif self.tokens[1] == 0:
            self.status = 1
        
        # note: the last case is tokens for both players still already present,
        # the line status is supposed to be 3 (not possible anymore) and remains 3

        #print("line_remove_update", self.line_index, self.line_coordinates, self.tokens, self.status)
