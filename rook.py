from pieces.piece import Piece

class Rook(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.has_moved = False  # For castling
    
    def get_valid_moves(self, board, check_castling=True, check_en_passant=True):
        valid_moves = []
        row, col = self.position
        
        # Horizontal and vertical directions
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        for dr, dc in directions:
            r, c = row + dr, col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                piece_at_pos = board.get_piece((r, c))
                if not piece_at_pos:
                    valid_moves.append((r, c))
                elif piece_at_pos.color != self.color:
                    valid_moves.append((r, c))
                    break
                else:
                    break
                r += dr
                c += dc
        
        return valid_moves