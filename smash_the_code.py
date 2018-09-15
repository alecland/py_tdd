#!/usr/bin/python

from enum import IntEnum
#import sys
#import math

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
    
    def is_empty(self):
        return self.nature == BlockNature.EMPTY

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
            gravity_candidates = self.get_col_gravity_candidates(col_idx)
            while(gravity_candidates[1] is not None):
                self.grid[gravity_candidates[0]][col_idx].nature = self.grid[gravity_candidates[1]][col_idx].nature
                self.grid[gravity_candidates[1]][col_idx].nature = BlockNature.EMPTY
                gravity_candidates = self.get_col_gravity_candidates(col_idx)
    
    def get_col_gravity_candidates(self, col_idx):
        empty_row_idx, not_empty_row_idx = None, None
        for row_idx in range(self.ROWS_NUMBER - 1, 0, -1):
            if empty_row_idx is None and self.grid[row_idx][col_idx].is_empty():
                empty_row_idx = row_idx
            elif not_empty_row_idx is None and empty_row_idx is not None and not self.grid[row_idx][col_idx].is_empty():
                not_empty_row_idx = row_idx
        return [empty_row_idx, not_empty_row_idx]
    
    
