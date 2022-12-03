import unittest
import numpy as np

from src.connect4.board import Board

class BoardTest(unittest.TestCase):
    def setUp(self) -> None:
        self.empty_board_layout = np.zeros([6, 7], dtype = np.int32)
        self.column_one_full_board_layout = np.zeros([6, 7], dtype = np.int32)
        self.column_one_full_board_layout[:,0] = 1
        self.full_board_layout = np.ones([6, 7], dtype = np.int32)

    def test_get_valid_move(self):
        empty_board = Board(self.empty_board_layout)
        expected_result = np.ones((7,), dtype = bool)
        self.assertTrue(np.array_equal(empty_board.get_valid_move(), expected_result))
        column_one_full_board = Board(self.column_one_full_board_layout)
        expected_result[0] = False
        self.assertTrue(np.array_equal(column_one_full_board.get_valid_move(), expected_result))
        full_board = Board(self.full_board_layout)
        expected_result = np.zeros((7,), dtype = bool)
        self.assertTrue(np.array_equal(full_board.get_valid_move(), expected_result))


    def test_place_piece(self):
        column_one_full_board = Board(self.column_one_full_board_layout)
        new_board = column_one_full_board.place_piece(6, -1)
        expected_result = np.zeros([6, 7], dtype = np.int32)
        expected_result[:,0] = 1
        expected_result[5,6] = -1
        self.assertTrue(np.array_equal(new_board.board_layout, expected_result))
        # confirm you cannot add to a column that is already full
        self.assertRaises(ValueError, column_one_full_board.place_piece, 0, -1)

    def test_is_strait_winner(self):
        board = Board()
        player = 1
        board = board.place_piece(6, player)
        board = board.place_piece(5, player)
        board = board.place_piece(4, player)
        board = board.place_piece(3, player)
        player_pieces = board.board_layout == player
        self.assertTrue(board._is_straight_winner(player_pieces))
        player_pieces = board.board_layout == -player
        self.assertFalse(board._is_straight_winner(player_pieces))

        board = Board()
        player = 1
        board = board.place_piece(0, player)
        board = board.place_piece(1, player)
        board = board.place_piece(2, player)
        board = board.place_piece(3, player)
        player_pieces = board.board_layout == player
        self.assertTrue(board._is_straight_winner(player_pieces))
        player_pieces = board.board_layout == -player
        self.assertFalse(board._is_straight_winner(player_pieces))

        # to test columns, we need to transpose the board layout
        board = board.place_piece(0, -player)
        board = board.place_piece(0, -player)
        board = board.place_piece(0, -player)
        board = board.place_piece(0, -player)
        player_pieces = board.board_layout == -player
        player_pieces = player_pieces.transpose()
        self.assertTrue(board._is_straight_winner(player_pieces))
        player_pieces = board.board_layout == player
        player_pieces = player_pieces.transpose()
        self.assertFalse(board._is_straight_winner(player_pieces))

    def test_is_diagonal_winner(self):
        board = Board()
        player = 1
        board = board.place_piece(0, player)
        board = board.place_piece(1, -player)
        board = board.place_piece(1, player)
        board = board.place_piece(2, -player)
        board = board.place_piece(2, -player)
        board = board.place_piece(2, player)
        board = board.place_piece(3, -player)
        board = board.place_piece(3, -player)
        board = board.place_piece(3, -player)
        board = board.place_piece(3, player)
        player_pieces = board.board_layout == player
        self.assertTrue(board._is_diagonal_winner(player_pieces))

        board = Board()
        player = -1
        board = board.place_piece(6, player)
        board = board.place_piece(5, -player)
        board = board.place_piece(5, player)
        board = board.place_piece(4, -player)
        board = board.place_piece(4, -player)
        board = board.place_piece(4, player)
        board = board.place_piece(3, -player)
        board = board.place_piece(3, -player)
        board = board.place_piece(3, -player)
        board = board.place_piece(3, player)
        player_pieces = board.board_layout == player
        self.assertTrue(board._is_diagonal_winner(player_pieces))

if __name__ == '__main__':
    unittest.main()