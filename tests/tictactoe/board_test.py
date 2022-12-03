import unittest
import numpy as np

from src.tictactoe.board import Board

class BoardTest(unittest.TestCase):
    def setUp(self) -> None:
        self.empty_board_layout = np.zeros([3, 3], dtype = np.int32)
        self.centre_occupied_layout = np.zeros([3, 3], dtype = np.int32)
        self.centre_occupied_layout[1,1] = 1
        self.full_board_layout = np.ones([3, 3], dtype = np.int32)


    def test_get_valid_move(self):
        empty_board = Board(self.empty_board_layout)
        expected_result = np.ones((3,3), dtype = bool) # i.e. true everywhere
        self.assertTrue(np.array_equal(empty_board.get_valid_move(), expected_result))

        centre_occupied = Board(self.centre_occupied_layout)
        expected_result[1,1] = False
        self.assertTrue(np.array_equal(centre_occupied.get_valid_move(), expected_result))
        full_board = Board(self.full_board_layout)
        expected_result = np.zeros((3,3), dtype = bool) # i.e. false everywhere
        self.assertTrue(np.array_equal(full_board.get_valid_move(), expected_result))


    def test_place_piece(self):
        centre_occupied_board = Board(self.centre_occupied_layout)
        new_board = centre_occupied_board.place_piece(0, 0, -1)
        expected_result = np.zeros([3, 3], dtype = np.int32)
        expected_result[1,1] = 1
        expected_result[0,0] = -1
        self.assertTrue(np.array_equal(new_board.board_layout, expected_result))
        # confirm you cannot add to a piece if the [row, column] is already full
        self.assertRaises(ValueError, new_board.place_piece, 0, 0, -1)

    def test_is_strait_winner(self):
        board = Board()
        player = 1
        board = board.place_piece(0, 0, player)
        board = board.place_piece(0, 1, player)
        board = board.place_piece(0, 2, player)
        player_pieces = board.board_layout == player
        self.assertTrue(board._is_straight_winner(player_pieces))
        player_pieces = board.board_layout == -player
        self.assertFalse(board._is_straight_winner(player_pieces))

        # to test columns, we need to transpose the board layout
        board = Board()
        board = board.place_piece(0, 2, -player)
        board = board.place_piece(1, 2, -player)
        board = board.place_piece(2, 2, -player)
        player_pieces = board.board_layout == -player
        player_pieces = player_pieces.transpose()
        self.assertTrue(board._is_straight_winner(player_pieces))
        player_pieces = board.board_layout == player
        player_pieces = player_pieces.transpose()
        self.assertFalse(board._is_straight_winner(player_pieces))

    def test_is_diagonal_winner(self):
        board = Board()
        player = 1
        board = board.place_piece(0, 0, player)
        board = board.place_piece(1, 1, player)
        board = board.place_piece(2, 2, player)
        player_pieces = board.board_layout == player
        self.assertTrue(board._is_diagonal_winner(player_pieces))

        board = Board()
        player = -1
        board = board.place_piece(0, 2, player)
        board = board.place_piece(1, 1, player)
        board = board.place_piece(2, 0, player)
        player_pieces = board.board_layout == player
        self.assertTrue(board._is_diagonal_winner(player_pieces))

if __name__ == '__main__':
    unittest.main()