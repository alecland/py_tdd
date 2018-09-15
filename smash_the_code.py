#!/usr/bin/python

from enum import IntEnum
import sys
import math

class BlockNature(IntEnum):
    SKULL = 0
    BLUE = 1
    GREEN = 2
    PURPLE = 3
    RED = 4
    YELLOW = 5
    EMPTY = -2

class Block:
    def __init__(self, nature):
        self.nature = nature
        self.is_checked = False
    
    def __eq__(self, other):
        return self.nature == other.nature

class Board:
    ROWS_NUMBER = 12
    COLS_NUMBER = 6

    def __init__(self):
        self.grid = [[Block(BlockNature.EMPTY) for col_idx in range(self.COLS_NUMBER)] for row_idx in range(self.ROWS_NUMBER)]
    
    def get_nature(self, row_idx, col_idx):
        return self.grid[row_idx][col_idx].nature
    
    def fill_with_rows(self, rows):
        for row_idx, row in enumerate(rows):
            for col_idx in range(len(row)):
                self.grid[row_idx][col_idx].nature = ord(row[col_idx]) - ord('0')
    
    def apply_gravity(self):
        for col_idx in range(self.COLS_NUMBER):
            should_fall = True
            while(should_fall):
                should_fall = False
                for row_idx in range(self.ROWS_NUMBER - 1, 0, -1):
                    if self.grid[row_idx][col_idx].nature == BlockNature.EMPTY and self.grid[row_idx - 1][col_idx].nature != BlockNature.EMPTY:
                        should_fall = True
                        self.grid[row_idx][col_idx].nature = self.grid[row_idx - 1][col_idx].nature
                        self.grid[row_idx - 1][col_idx].nature = BlockNature.EMPTY