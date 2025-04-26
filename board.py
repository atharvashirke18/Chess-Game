import pygame
from pieces.pawn import Pawn
from pieces.rook import Rook
from pieces.knight import Knight
from pieces.bishop import Bishop
from pieces.queen import Queen
from pieces.king import King
from utils import load_image

class Board:
    def __init__(self):
        # Initialize an 8x8 board with None values
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.setup_pieces()
        
    def setup_pieces(self):
        # Place pawns
        for col in range(8):
            self.board[1][col] = Pawn("black", (1, col))
            self.board[6][col] = Pawn("white", (6, col))
        
        # Place rooks
        self.board[0][0] = Rook("black", (0, 0))
        self.board[0][7] = Rook("black", (0, 7))
        self.board[7][0] = Rook("white", (7, 0))
        self.board[7][7] = Rook("white", (7, 7))
        
        # Place knights
        self.board[0][1] = Knight("black", (0, 1))
        self.board[0][6] = Knight("black", (0, 6))
        self.board[7][1] = Knight("white", (7, 1))
        self.board[7][6] = Knight("white", (7, 6))
        
        # Place bishops
        self.board[0][2] = Bishop("black", (0, 2))
        self.board[0][5] = Bishop("black", (0, 5))
        self.board[7][2] = Bishop("white", (7, 2))
        self.board[7][5] = Bishop("white", (7, 5))
        
        # Place queens
        self.board[0][3] = Queen("black", (0, 3))
        self.board[7][3] = Queen("white", (7, 3))
        
        # Place kings
        self.board[0][4] = King("black", (0, 4))
        self.board[7][4] = King("white", (7, 4))
    
    def get_piece(self, position):
        row, col = position
        if 0 <= row < 8 and 0 <= col < 8:
            return self.board[row][col]
        return None
    
    def set_piece(self, position, piece):
        row, col = position
        if 0 <= row < 8 and 0 <= col < 8:
            self.board[row][col] = piece
            if piece:
                piece.position = position
    
    def move_piece(self, from_pos, to_pos):
        piece = self.get_piece(from_pos)
        if piece:
            # Handle captures
            captured_piece = self.get_piece(to_pos)
            
            # Update piece position
            self.set_piece(to_pos, piece)
            self.set_piece(from_pos, None)
            
            # Handle special moves
            
            # Pawn promotion
            if isinstance(piece, Pawn):
                if (piece.color == "white" and to_pos[0] == 0) or (piece.color == "black" and to_pos[0] == 7):
                    # Automatically promote to queen for simplicity
                    self.set_piece(to_pos, Queen(piece.color, to_pos))
            
            return True
        return False
    
    def find_king(self, color):
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if isinstance(piece, King) and piece.color == color:
                    return (row, col)
        return None
    
    def clone(self):
        """Create a deep copy of the board for move validation"""
        new_board = Board()
        new_board.board = [[None for _ in range(8)] for _ in range(8)]
        
        for row in range(8):
            for col in range(8):
                piece = self.get_piece((row, col))
                if piece:
                    # Create a new piece of the same type
                    if isinstance(piece, Pawn):
                        new_board.board[row][col] = Pawn(piece.color, (row, col))
                    elif isinstance(piece, Rook):
                        new_piece = Rook(piece.color, (row, col))
                        new_piece.has_moved = piece.has_moved
                        new_board.board[row][col] = new_piece
                    elif isinstance(piece, Knight):
                        new_board.board[row][col] = Knight(piece.color, (row, col))
                    elif isinstance(piece, Bishop):
                        new_board.board[row][col] = Bishop(piece.color, (row, col))
                    elif isinstance(piece, Queen):
                        new_board.board[row][col] = Queen(piece.color, (row, col))
                    elif isinstance(piece, King):
                        new_piece = King(piece.color, (row, col))
                        new_piece.has_moved = piece.has_moved
                        new_board.board[row][col] = new_piece
        
        return new_board