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

class GravityMove:
    def __init__(self, col_idx, start_idx, stop_idx):
        self.col_idx = col_idx
        self.start_idx = start_idx
        self.stop_idx = stop_idx

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
            gravity_move = self.get_col_gravity_move(col_idx)
            while(gravity_move.start_idx is not None):
                self.make_block_fall(gravity_move)                
                gravity_move = self.get_col_gravity_move(col_idx)
    
    def get_col_gravity_move(self, col_idx):
        stop_idx, start_idx = None, None
        for row_idx in range(self.ROWS_NUMBER - 1, 0, -1):
            if stop_idx is None and self.grid[row_idx][col_idx].is_empty():
                stop_idx = row_idx
            elif start_idx is None and stop_idx is not None and not self.grid[row_idx][col_idx].is_empty():
                start_idx = row_idx
        return GravityMove(col_idx, start_idx, stop_idx)
    
    def make_block_fall(self, gravity_move):
        self.grid[gravity_move.stop_idx][gravity_move.col_idx].nature = self.grid[gravity_move.start_idx][gravity_move.col_idx].nature
        self.grid[gravity_move.start_idx][gravity_move.col_idx].nature = BlockNature.EMPTY
    
    
