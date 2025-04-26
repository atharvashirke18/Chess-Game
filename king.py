from pieces.piece import Piece

class King(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.has_moved = False  # For castling
    
    def get_valid_moves(self, board, check_castling=True, check_en_passant=True):
        valid_moves = []
        row, col = self.position
        
        # All eight surrounding squares
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                
                new_pos = (row + dr, col + dc)
                if self.can_move_to(new_pos, board):
                    valid_moves.append(new_pos)
        
        return valid_moves