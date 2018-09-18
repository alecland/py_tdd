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
    
    def is_colored(self):
        return self.nature >= BlockNature.BLUE
    
    def check(self):
        self.is_checked = True
    
    def uncheck(self):
        self.is_checked = False

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
    
    def is_empty(self):
        for row_idx in range(self.ROWS_NUMBER):
            for col_idx in range(self.COLS_NUMBER):
                if self.grid[row_idx][col_idx].nature != BlockNature.EMPTY:
                    return False
        return True

    def get_nature(self, row_idx, col_idx):
        return self.grid[row_idx][col_idx].nature
    
    def get_rows_count(self):
        return len(self.grid)
    
    def get_cols_count(self):
        return len(self.grid[self.get_rows_count() - 1])

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
    
    def is_above_block_of_nature(self, row_idx, col_idx, nature):
        return row_idx > 0 and self.grid[row_idx - 1][col_idx].nature == nature

    def is_below_block_of_nature(self, row_idx, col_idx, nature):
        return row_idx < self.ROWS_NUMBER - 1 and self.grid[row_idx + 1][col_idx].nature == nature
    
    def is_left_block_of_nature(self, row_idx, col_idx, nature):
        return col_idx > 0 and self.grid[row_idx][col_idx - 1].nature == nature
    
    def is_right_block_of_nature(self, row_idx, col_idx, nature):
        return col_idx < self.COLS_NUMBER - 1 and self.grid[row_idx][col_idx + 1].nature == nature
    
    def is_search_necessary(self, row_idx, col_idx):
        is_necessary = True
        if self.grid[row_idx][col_idx].is_checked or not self.grid[row_idx][col_idx].is_colored():
            is_necessary = False
            
        self.grid[row_idx][col_idx].is_checked = True
        return is_necessary

    def search_chain_length(self, row_idx, col_idx):
        if not self.is_search_necessary(row_idx, col_idx):
            return 0
               
        chain_length = 1
        if self.is_below_block_of_nature(row_idx, col_idx, self.grid[row_idx][col_idx].nature):
            chain_length += self.search_chain_length(row_idx + 1, col_idx)
        if self.is_above_block_of_nature(row_idx, col_idx, self.grid[row_idx][col_idx].nature):
            chain_length += self.search_chain_length(row_idx - 1, col_idx)
        if self.is_left_block_of_nature(row_idx, col_idx, self.grid[row_idx][col_idx].nature):
            chain_length += self.search_chain_length(row_idx, col_idx - 1)
        if self.is_right_block_of_nature(row_idx, col_idx, self.grid[row_idx][col_idx].nature):
            chain_length += self.search_chain_length(row_idx, col_idx + 1)

        return chain_length
    
    def remove_check_marks(self):
        for row_idx in range(self.ROWS_NUMBER):
            for col_idx in range(self.COLS_NUMBER):
                self.grid[row_idx][col_idx].uncheck()
    
    def is_unchecked(self):
        for row_idx in range(self.ROWS_NUMBER):
            for col_idx in range(self.COLS_NUMBER):
                if self.grid[row_idx][col_idx].is_checked:
                    return False
        return True
        
    def remove_chain(self, row_idx, col_idx):
        chain_nature = self.grid[row_idx][col_idx].nature
        self.grid[row_idx][col_idx].nature = BlockNature.EMPTY
        remove_count = 1
        
        if self.is_below_block_of_nature(row_idx, col_idx, chain_nature):
            remove_count += self.remove_chain(row_idx + 1, col_idx)
        elif self.is_below_block_of_nature(row_idx, col_idx, BlockNature.SKULL):
            self.grid[row_idx + 1][col_idx].nature = BlockNature.EMPTY
        
        if self.is_above_block_of_nature(row_idx, col_idx, chain_nature):
            remove_count += self.remove_chain(row_idx - 1, col_idx)
        elif self.is_above_block_of_nature(row_idx, col_idx, BlockNature.SKULL):
            self.grid[row_idx - 1][col_idx].nature = BlockNature.EMPTY
        
        if self.is_left_block_of_nature(row_idx, col_idx, chain_nature):
            remove_count += self.remove_chain(row_idx, col_idx - 1)
        elif self.is_left_block_of_nature(row_idx, col_idx, BlockNature.SKULL):
            self.grid[row_idx][col_idx - 1].nature = BlockNature.EMPTY
        
        if self.is_right_block_of_nature(row_idx, col_idx, chain_nature):
            remove_count += self.remove_chain(row_idx, col_idx + 1)
        elif self.is_right_block_of_nature(row_idx, col_idx, BlockNature.SKULL):
            self.grid[row_idx][col_idx + 1].nature = BlockNature.EMPTY
        
        return remove_count



    
    
