import numpy as np
from collections import namedtuple

WinState = namedtuple('WinState', 'is_ended winner')

class Board():
    """
    Each Board is its own instance. When a piece is added to a board, a new board is created. This is to 
    make the Monte Carlo Tree Search implementation efficient

    Pieces on the board are persisted as 
    - +1 for a piece belonging to the current player
    - -1 for a piece belonging to the opponent
    """

    # TODO: Is this from the perspective of a player? If so that player should always be +1
    def __init__(self, board_layout = None):
        self.height = 3
        self.width = 3
        self.win_length = 3

        if board_layout is None:
            self.board_layout = np.zeros([self.height, self.width], dtype = np.int32)
            # TODO: Will changing dtype = np.int32 to something like dtype = np.int8 make any impact
        else:
            assert board_layout.shape == (3, 3)
            self.board_layout = board_layout

    def get_valid_move(self):
        "If the top row of a column contains 0, that column is a valid move"
        return self.board_layout == 0

    def place_piece(self, row, column, player):
        "Create copy of board containing new piece."
        #available_idx, = np.where(self.board_layout[row, column] == 0)
        if self.board_layout[row, column] != 0:
            raise ValueError("Can't play row %s, column %s on board %s" % (row, column, self))

        # TODO: At what stage do I revers the signs to show it is the opponent's move
        new_board_layout = np.copy(self.board_layout)
        new_board_layout[row][column] = player
        return Board(new_board_layout)

    def get_win_state(self):
        for player in [-1, 1]:
            player_pieces = self.board_layout == -player
            # Check rows & columns for win
            if (self._is_straight_winner(player_pieces) or
                self._is_straight_winner(player_pieces.transpose()) or
                self._is_diagonal_winner(player_pieces)):
                return WinState(True, -player)

        # draw has very little value.
        if not self.get_valid_moves().any():
            return WinState(True, None)

        # Game is not ended yet.
        return WinState(False, None)

    def _is_diagonal_winner(self, player_pieces):
        """Checks if player_pieces contains a diagonal win."""
        win_length = self.win_length
        for i in range(len(player_pieces) - win_length + 1):
            for j in range(len(player_pieces[0]) - win_length + 1):
                if all(player_pieces[i + x][j + x] for x in range(win_length)):
                    return True
            for j in range(win_length - 1, len(player_pieces[0])):
                if all(player_pieces[i + x][j - x] for x in range(win_length)):
                    return True
        return False

    def _is_straight_winner(self, player_pieces):
        """player_pieces is a boolean mask of the board_layout from the perspective of one of the players.
        
        This method tests rows. To test columns, use a transpose of the board_layout
        """        
        run_lengths = [player_pieces[:, i:i + self.win_length].sum(axis=1) for i in range(len(player_pieces) - self.win_length + 2)]
        return max([x.max() for x in run_lengths]) >= self.win_length 

    def __str__(self):
        return str(self.board_layout)