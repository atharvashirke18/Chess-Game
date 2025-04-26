from pieces.piece import Piece

class Pawn(Piece):
    def get_valid_moves(self, board, check_castling=True, check_en_passant=True):
        valid_moves = []
        row, col = self.position
        
        # Determine direction based on color
        direction = -1 if self.color == "white" else 1
        
        # One square forward
        new_pos = (row + direction, col)
        if 0 <= new_pos[0] < 8 and not board.get_piece(new_pos):
            valid_moves.append(new_pos)
            
            # Two squares forward from starting position
            if ((self.color == "white" and row == 6) or 
                (self.color == "black" and row == 1)):
                new_pos = (row + 2 * direction, col)
                if not board.get_piece(new_pos):
                    valid_moves.append(new_pos)
        
        # Captures
        for capture_col in [col - 1, col + 1]:
            new_pos = (row + direction, capture_col)
            if 0 <= new_pos[0] < 8 and 0 <= new_pos[1] < 8:
                piece_at_pos = board.get_piece(new_pos)
                if piece_at_pos and piece_at_pos.color != self.color:
                    valid_moves.append(new_pos)
        
        return valid_moves
