# game.py
from pieces.pawn import Pawn
from pieces.rook import Rook
from pieces.knight import Knight
from pieces.bishop import Bishop
from pieces.queen import Queen
from pieces.king import King

class Game:
    def __init__(self, board):
        self.board = board
        self.current_turn = "white"
        self.move_history = []
        self.last_move = None  # Track last move for en passant
    
    def toggle_turn(self):
        self.current_turn = "black" if self.current_turn == "white" else "white"
    
    def make_move(self, from_pos, to_pos):
        piece = self.board.get_piece(from_pos)
        if not piece or piece.color != self.current_turn:
            return False
        
        # Handle special moves
        
        # Castling
        if self._is_castling_move(from_pos, to_pos):
            return self._handle_castling(from_pos, to_pos)
        
        # En passant
        if self._is_en_passant_move(from_pos, to_pos):
            return self._handle_en_passant(from_pos, to_pos)
        
        # Validate the move is legal
        valid_moves = self.get_valid_moves(from_pos)
        if to_pos not in valid_moves:
            return False
        
        # Move the piece
        self.board.move_piece(from_pos, to_pos)
        
        # Update last move for en passant
        self.last_move = (from_pos, to_pos, piece)
        
        # Switch turns
        self.toggle_turn()
        
        return True
    
    def _is_castling_move(self, from_pos, to_pos):
        piece = self.board.get_piece(from_pos)
        if not isinstance(piece, King):
            return False
        
        # Check if king is moving two squares horizontally
        return abs(to_pos[1] - from_pos[1]) == 2 and from_pos[0] == to_pos[0]
    
    def _handle_castling(self, from_pos, to_pos):
        row, from_col = from_pos
        _, to_col = to_pos
        
        # Determine if it's kingside or queenside castling
        is_kingside = to_col > from_col
        
        # Get the rook position
        rook_col = 7 if is_kingside else 0
        rook_pos = (row, rook_col)
        
        # Move the king
        king = self.board.get_piece(from_pos)
        self.board.set_piece(to_pos, king)
        self.board.set_piece(from_pos, None)
        king.has_moved = True
        
        # Move the rook
        rook = self.board.get_piece(rook_pos)
        new_rook_col = 5 if is_kingside else 3
        self.board.set_piece((row, new_rook_col), rook)
        self.board.set_piece(rook_pos, None)
        rook.has_moved = True
        
        # Update last move
        self.last_move = (from_pos, to_pos, king)
        
        # Switch turns
        self.toggle_turn()
        
        return True
    
    def _is_en_passant_move(self, from_pos, to_pos):
        piece = self.board.get_piece(from_pos)
        if not isinstance(piece, Pawn):
            return False
        
        # Check if pawn is moving diagonally to an empty square
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        if abs(from_col - to_col) == 1 and ((piece.color == "white" and from_row - to_row == 1) or 
                                            (piece.color == "black" and to_row - from_row == 1)):
            # Check if the destination is empty
            if not self.board.get_piece(to_pos):
                # Check if there's an enemy pawn that just made a double move
                if self.last_move:
                    last_from, last_to, last_piece = self.last_move
                    if isinstance(last_piece, Pawn) and abs(last_to[0] - last_from[0]) == 2:
                        # The pawn is adjacent to the moving pawn
                        if last_to[0] == from_row and last_to[1] == to_col:
                            return True
        return False
    
    def _handle_en_passant(self, from_pos, to_pos):
        pawn = self.board.get_piece(from_pos)
        to_row, to_col = to_pos
        
        # Remove the captured pawn
        captured_row = from_pos[0]  # The row of the capturing pawn
        self.board.set_piece((captured_row, to_col), None)
        
        # Move the pawn
        self.board.move_piece(from_pos, to_pos)
        
        # Update last move
        self.last_move = (from_pos, to_pos, pawn)
        
        # Switch turns
        self.toggle_turn()
        
        return True
    
    def get_valid_moves(self, position):
        piece = self.board.get_piece(position)
        if not piece:
            return []
        
        potential_moves = piece.get_valid_moves(self.board)
        valid_moves = []
        
        # Filter moves that would put/leave the king in check
        for move in potential_moves:
            # Create a temporary board to simulate the move
            temp_board = self.board.clone()
            temp_board.move_piece(position, move)
            
            # Check if the king is in check after the move
            king_pos = temp_board.find_king(piece.color)
            if not king_pos or not self._is_position_under_attack(king_pos, piece.color, temp_board):
                valid_moves.append(move)
        
        # Add special moves
        
        # Castling
        if isinstance(piece, King) and not piece.has_moved:
            valid_moves.extend(self._get_castling_moves(position))
        
        # En passant
        if isinstance(piece, Pawn):
            en_passant_moves = self._get_en_passant_moves(position)
            for move in en_passant_moves:
                # Create a temporary board to simulate the move
                temp_board = self.board.clone()
                # Need to handle en passant specially in simulation
                from_row, from_col = position
                to_row, to_col = move
                
                # Move the pawn
                temp_board.move_piece(position, move)
                
                # Remove the captured pawn
                temp_board.set_piece((from_row, to_col), None)
                
                # Check if the king is in check after the move
                king_pos = temp_board.find_king(piece.color)
                if not king_pos or not self._is_position_under_attack(king_pos, piece.color, temp_board):
                    valid_moves.append(move)
        
        return valid_moves
    
    def _get_castling_moves(self, king_pos):
        king = self.board.get_piece(king_pos)
        if not isinstance(king, King) or king.has_moved or self.is_in_check(king.color):
            return []
        
        castling_moves = []
        row, col = king_pos
        
        # Check kingside castling
        if self._can_castle_kingside(king_pos):
            castling_moves.append((row, col + 2))
        
        # Check queenside castling
        if self._can_castle_queenside(king_pos):
            castling_moves.append((row, col - 2))
        
        return castling_moves
    
    def _can_castle_kingside(self, king_pos):
        row, col = king_pos
        king = self.board.get_piece(king_pos)
        
        # Check if the squares between king and rook are empty
        if self.board.get_piece((row, col + 1)) or self.board.get_piece((row, col + 2)):
            return False
        
        # Check if the rook is in place and hasn't moved
        rook_pos = (row, 7)
        rook = self.board.get_piece(rook_pos)
        if not isinstance(rook, Rook) or rook.color != king.color or rook.has_moved:
            return False
        
        # Check if the king passes through or ends up in check
        for c in range(col, col + 3):
            if self._is_position_under_attack((row, c), king.color, self.board):
                return False
        
        return True
    
    def _can_castle_queenside(self, king_pos):
        row, col = king_pos
        king = self.board.get_piece(king_pos)
        
        # Check if the squares between king and rook are empty
        if (self.board.get_piece((row, col - 1)) or 
            self.board.get_piece((row, col - 2)) or 
            self.board.get_piece((row, col - 3))):
            return False
        
        # Check if the rook is in place and hasn't moved
        rook_pos = (row, 0)
        rook = self.board.get_piece(rook_pos)
        if not isinstance(rook, Rook) or rook.color != king.color or rook.has_moved:
            return False
        
        # Check if the king passes through or ends up in check
        for c in range(col, col - 3, -1):
            if self._is_position_under_attack((row, c), king.color, self.board):
                return False
        
        return True
    
    def _get_en_passant_moves(self, pawn_pos):
        pawn = self.board.get_piece(pawn_pos)
        if not isinstance(pawn, Pawn) or not self.last_move:
            return []
        
        last_from, last_to, last_piece = self.last_move
        if not isinstance(last_piece, Pawn) or last_piece.color == pawn.color:
            return []
        
        # Check if the last move was a double pawn move
        last_from_row, last_from_col = last_from
        last_to_row, last_to_col = last_to
        if abs(last_to_row - last_from_row) != 2:
            return []
        
        # Check if the pawns are adjacent
        row, col = pawn_pos
        if abs(col - last_to_col) != 1 or row != last_to_row:
            return []
        
        # Determine the capture direction based on pawn color
        capture_row = row - 1 if pawn.color == "white" else row + 1
        
        return [(capture_row, last_to_col)]
    
    def _is_position_under_attack(self, position, color, board=None):
        """Check if a position is under attack by any enemy piece"""
        if board is None:
            board = self.board
        
        enemy_color = "black" if color == "white" else "white"
        
        # Check for attacks from all enemy pieces
        for row in range(8):
            for col in range(8):
                piece = board.get_piece((row, col))
                if piece and piece.color == enemy_color:
                    # Don't check for castling or en passant here to avoid recursion
                    moves = piece.get_valid_moves(board, check_castling=False, check_en_passant=False)
                    if position in moves:
                        return True
        
        return False
    
    def is_in_check(self, color):
        """Check if the king of the given color is in check"""
        king_pos = self.board.find_king(color)
        if not king_pos:
            return False
        
        return self._is_position_under_attack(king_pos, color)
    
    def is_checkmate(self, color):
        """Check if the given color is in checkmate"""
        if not self.is_in_check(color):
            return False
        
        # Check if any piece can make a move that gets out of check
        for row in range(8):
            for col in range(8):
                piece = self.board.get_piece((row, col))
                if piece and piece.color == color:
                    valid_moves = self.get_valid_moves((row, col))
                    if valid_moves:
                        return False
        
        return True
    
    def is_stalemate(self, color):
        """Check if the given color is in stalemate"""
        if self.is_in_check(color):
            return False
        
        # Check if any piece can make a valid move
        for row in range(8):
            for col in range(8):
                piece = self.board.get_piece((row, col))
                if piece and piece.color == color:
                    valid_moves = self.get_valid_moves((row, col))
                    if valid_moves:
                        return False
        
        return True