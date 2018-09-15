#!/usr/bin/python

from enum import IntEnum
from smash_the_code import BlockNature
from smash_the_code import Block
from smash_the_code import Board
import sys
import math
import unittest

class TestBoardMethods(unittest.TestCase):

    ROWS_NUMBER = 12
    COLS_NUMBER = 6

    def setUp(self):
        self.board = Board()
        self.test_gravity = ['......',
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
                             '..1.54']
        self.test_rows = ['......',
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
                          '..1254']

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

    def test_new_board_is_12x6(self):
        self.assertEqual(len(self.board.grid), self.ROWS_NUMBER)
        self.assertEqual(len(self.board.grid[self.ROWS_NUMBER - 1]), self.COLS_NUMBER)
    
    def test_new_board_is_empty(self):
        for row_idx in range(self.ROWS_NUMBER):
            for col_idx in range(self.COLS_NUMBER):
                self.assertEqual(self.board.get_nature(row_idx, col_idx), BlockNature.EMPTY)
    
    def test_board_fill_should_set_board(self):
        self.board.fill_with_rows(self.test_rows)
        self.assertEqual(BlockNature.RED, self.board.get_nature(11,5))
        self.assertEqual(BlockNature.YELLOW, self.board.get_nature(10,5))
        self.assertEqual(BlockNature.GREEN, self.board.get_nature(7,4))
        self.assertEqual(BlockNature.PURPLE, self.board.get_nature(9,4))
        self.assertEqual(BlockNature.BLUE, self.board.get_nature(11,2))
        self.assertEqual(BlockNature.EMPTY, self.board.get_nature(3,3))
    
    def test_board_after_applying_gravity(self):
        self.board.fill_with_rows(self.test_gravity)
        self.board.apply_gravity()
        board = Board()
        board.fill_with_rows(self.test_rows)
        self.assertEqual(BlockNature.RED, self.board.get_nature(11,5))
        self.assertEqual(BlockNature.YELLOW, self.board.get_nature(10,5))
        self.assertEqual(BlockNature.GREEN, self.board.get_nature(7,4))
        self.assertEqual(BlockNature.PURPLE, self.board.get_nature(9,4))
        self.assertEqual(BlockNature.BLUE, self.board.get_nature(11,2))
        self.assertEqual(BlockNature.EMPTY, self.board.get_nature(3,3))
        self.assertListEqual(board.grid, self.board.grid)
        

if __name__ == '__main__':
    unittest.main()