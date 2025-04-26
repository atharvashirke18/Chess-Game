import pygame
from utils import load_image

class Piece:
    def __init__(self, color, position):
        self.color = color  # "white" or "black"
        self.position = position  # (row, col)
        self.has_moved = False
        self.image = self._load_image()
    
    def _load_image(self):
        """Load the appropriate image for this piece"""
        filename = f"{self.color}_{self.__class__.__name__.lower()}.png"
        return load_image(filename)
    
    def get_valid_moves(self, board, check_castling=True, check_en_passant=True):
        """Return a list of valid moves for this piece"""
        # To be implemented by subclasses
        pass
    
    def can_move_to(self, position, board):
        """Check if the piece can move to the given position"""
        row, col = position
        
        # Check if the position is on the board
        if not (0 <= row < 8 and 0 <= col < 8):
            return False
        
        # Check if the position is occupied by a piece of the same color
        piece_at_pos = board.get_piece(position)
        if piece_at_pos and piece_at_pos.color == self.color:
            return False
        
        return True
