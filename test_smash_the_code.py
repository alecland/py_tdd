#!/usr/bin/python

from smash_the_code import BlockNature
from smash_the_code import Block
from smash_the_code import Board
import unittest

class TestBoardMethods(unittest.TestCase):

    ROWS_NUMBER = 12
    COLS_NUMBER = 6
    test_gravity = ['......',
                    '....4.',
                    '......', 
                    '..2...', 
                    '...3..', 
                    '...2..', 
                    '....2.', 
                    '.....5', 
                    '....45', 
                    '....35', 
                    '....4.', 
                    '.11.54']
    test_rows = ['......',
                '......', 
                '......', 
                '......', 
                '......', 
                '......', 
                '....4.', 
                '....2.', 
                '....45', 
                '....35', 
                '..2345', 
                '.11254']
    test_chains = ['......',
                '......', 
                '......', 
                '....4.', 
                '....2.', 
                '...030', 
                '...133', 
                '...133', 
                '...145', 
                '..0135', 
                '..2345', 
                '.11254']

    def setUp(self):
        self.board = Board()
        

    def test_can_use_block_nature_as_int(self):
        self.assertEqual(0, BlockNature.SKULL)
        self.assertEqual(1, BlockNature.BLUE)
        self.assertEqual(2, BlockNature.GREEN)
        self.assertEqual(3, BlockNature.PURPLE)
        self.assertEqual(4, BlockNature.RED)
        self.assertEqual(5, BlockNature.YELLOW)
        self.assertEqual(-2, BlockNature.EMPTY)
    
    def test_can_create_a_block(self):
        block = Block(BlockNature.GREEN)
        self.assertEqual(block.nature, BlockNature.GREEN)
        self.assertFalse(block.is_checked)
        self.assertTrue(block.is_colored())
        self.assertFalse(block.is_empty())

    def test_new_board_is_12x6(self):
        self.assertEqual(self.board.get_rows_count(), self.ROWS_NUMBER)
        self.assertEqual(self.board.get_cols_count(), self.COLS_NUMBER)
    
    def test_new_board_is_empty(self):
        self.assertTrue(self.board.is_empty())
    
    def test_board_fill_should_set_board(self):
        self.board.fill_with_rows(self.test_rows)
        self.assertEqual(BlockNature.RED, self.board.get_nature(11,5))
        self.assertEqual(BlockNature.YELLOW, self.board.get_nature(10,5))
        self.assertEqual(BlockNature.GREEN, self.board.get_nature(7,4))
        self.assertEqual(BlockNature.PURPLE, self.board.get_nature(9,4))
        self.assertEqual(BlockNature.BLUE, self.board.get_nature(11,2))
        self.assertEqual(BlockNature.EMPTY, self.board.get_nature(3,3))
    
    def test_given_board_before_appying_gravity_find_right_gravity_move_on_second_col(self):
        self.board.fill_with_rows(self.test_gravity)
        move = self.board.get_col_gravity_move(2)
        self.assertEqual(2, move.col_idx)
        self.assertEqual(3, move.start_idx)
        self.assertEqual(10, move.stop_idx)

    def test_given_board_before_appying_gravity_is_equal_to_ref_after_applying_gravity(self):
        self.board.fill_with_rows(self.test_gravity)
        self.board.apply_gravity()
        board = Board()
        board.fill_with_rows(self.test_rows)
        self.assertListEqual(board.grid, self.board.grid)
    
    def test_given_known_board_left_block_of_nature(self):
        self.board.fill_with_rows(self.test_rows)
        self.assertTrue(self.board.is_left_block_of_nature(11, 2, self.board.get_nature(11, 2)))
        self.assertFalse(self.board.is_left_block_of_nature(7, 0, self.board.get_nature(7, 0)))
        self.assertFalse(self.board.is_left_block_of_nature(11, 1, self.board.get_nature(11, 1)))
        self.assertFalse(self.board.is_left_block_of_nature(11, 5, self.board.get_nature(11, 5)))
    
    def test_block_chain_length(self):
        self.board.fill_with_rows(self.test_rows)
        self.assertEqual(0, self.board.search_chain_length(1, 1))
        self.assertEqual(1, self.board.search_chain_length(6, 4))
        self.assertEqual(2, self.board.search_chain_length(11, 1))
        self.assertEqual(3, self.board.search_chain_length(10, 5))
    
    def test_uncheck_board_should_remove_all_check_marks(self):
        self.board.fill_with_rows(self.test_rows)
        self.board.search_chain_length(1, 1)
        self.board.search_chain_length(10, 5)
        self.board.remove_check_marks()
        self.assertTrue(self.board.is_unchecked())
    
    def test_given_board_with_4_and_5_length_chains_remove_chains_should_return_4_and_5(self):
        self.board.fill_with_rows(self.test_chains)
        self.assertEqual(5, self.board.remove_chain(7, 4))
        self.assertEqual(4, self.board.remove_chain(7, 3))
      
    def test_given_board_with_chains_remove_chains_and_gravity_should_result_in_ref_board(self):
        self.board.fill_with_rows(self.test_chains)
        self.board.remove_chain(7, 4)
        self.board.remove_chain(7, 3)
        self.board.apply_gravity()
        board = Board()
        board.fill_with_rows(self.test_rows)
        self.assertListEqual(board.grid, self.board.grid)       

if __name__ == '__main__':
    unittest.main()