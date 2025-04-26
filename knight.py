from pieces.piece import Piece

class Knight(Piece):
    def get_valid_moves(self, board, check_castling=True, check_en_passant=True):
        valid_moves = []
        row, col = self.position
        
        # All possible knight moves
        moves = [
            (row - 2, col - 1), (row - 2, col + 1),
            (row - 1, col - 2), (row - 1, col + 2),
            (row + 1, col - 2), (row + 1, col + 2),
            (row + 2, col - 1), (row + 2, col + 1)
        ]
        
        for move in moves:
            if self.can_move_to(move, board):
                valid_moves.append(move)
        
        return valid_moves