import pygame
import sys
from board import Board
from game import Game

# Initialize pygame
pygame.init()
pygame.mixer.init()  # Initialize sound mixer

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
BOARD_SIZE = 8
SQUARE_SIZE = SCREEN_WIDTH // BOARD_SIZE
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
HIGHLIGHT_COLOR = (100, 249, 83, 180)  # Semi-transparent green
LAST_MOVE_COLOR = (250, 240, 80, 180)  # Semi-transparent yellow

# Create window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Chess Game")
clock = pygame.time.Clock()

# Font for messages
font = pygame.font.SysFont("Arial", 36)

# Load move sound
move_sound = pygame.mixer.Sound('assets/move.wav')

def draw_board(board, selected_piece, valid_moves, last_move):
    # Draw squares
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            color = WHITE if (row + col) % 2 == 0 else (120, 120, 120)
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            
            # Highlight last move
            if last_move and ((row, col) == last_move[0] or (row, col) == last_move[1]):
                highlight = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                highlight.fill(LAST_MOVE_COLOR)
                screen.blit(highlight, (col * SQUARE_SIZE, row * SQUARE_SIZE))
                
    # Highlight selected piece and valid moves
    if selected_piece:
        row, col = selected_piece
        highlight = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
        highlight.fill(HIGHLIGHT_COLOR)
        screen.blit(highlight, (col * SQUARE_SIZE, row * SQUARE_SIZE))
        
        # Highlight valid moves
        for move in valid_moves:
            move_row, move_col = move
            highlight = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
            highlight.fill(HIGHLIGHT_COLOR)
            screen.blit(highlight, (move_col * SQUARE_SIZE, move_row * SQUARE_SIZE))
    
    # Draw pieces
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            piece = board.get_piece((row, col))
            if piece:
                piece_image = piece.image
                # Center the piece in the square
                image_rect = piece_image.get_rect()
                image_rect.center = (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2)
                screen.blit(piece_image, image_rect)

def show_message(message):
    # Create semi-transparent overlay
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))
    screen.blit(overlay, (0, 0))
    
    # Render message
    text = font.render(message, True, WHITE)
    text_rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
    screen.blit(text, text_rect)
    
    # Add instruction to restart
    restart_text = font.render("Press R to restart game", True, WHITE)
    restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50))
    screen.blit(restart_text, restart_rect)
    
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True  # Restart the game
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
    return False

def main():
    board = Board()
    game = Game(board)
    selected_piece = None
    valid_moves = []
    game_over = False
    last_move = None
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if not game_over:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    col = event.pos[0] // SQUARE_SIZE
                    row = event.pos[1] // SQUARE_SIZE
                    
                    # If a piece is already selected
                    if selected_piece:
                        # Check if the clicked position is a valid move
                        if (row, col) in valid_moves:
                            # Move the piece
                            piece = board.get_piece(selected_piece)
                            old_pos = selected_piece
                            new_pos = (row, col)
                            
                            move_result = game.make_move(old_pos, new_pos)
                            
                            if move_result:
                                # Play move sound
                                move_sound.play()
                                last_move = (old_pos, new_pos)
                                
                                # Check for game over conditions
                                if game.is_checkmate(game.current_turn):
                                    game_over = True
                                    winner = "White" if game.current_turn == "black" else "Black"
                                    restart = show_message(f"Checkmate! {winner} wins!")
                                    if restart:
                                        board = Board()
                                        game = Game(board)
                                        selected_piece = None
                                        valid_moves = []
                                        game_over = False
                                        last_move = None
                                elif game.is_stalemate(game.current_turn):
                                    game_over = True
                                    restart = show_message("Stalemate! The game is a draw.")
                                    if restart:
                                        board = Board()
                                        game = Game(board)
                                        selected_piece = None
                                        valid_moves = []
                                        game_over = False
                                        last_move = None
                        
                        # Reset selection
                        selected_piece = None
                        valid_moves = []
                    else:
                        # Select a piece
                        piece = board.get_piece((row, col))
                        if piece and piece.color == game.current_turn:
                            selected_piece = (row, col)
                            valid_moves = game.get_valid_moves(selected_piece)
            
            # Allow restart with 'r' key anytime
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                board = Board()
                game = Game(board)
                selected_piece = None
                valid_moves = []
                game_over = False
                last_move = None
        
        # Draw everything
        screen.fill(BLACK)
        draw_board(board, selected_piece, valid_moves, last_move)
        
        # Display whose turn it is
        turn_text = font.render(f"{game.current_turn.capitalize()}'s Turn", True, WHITE)
        screen.blit(turn_text, (10, 10))
        
        # Display check status
        if game.is_in_check(game.current_turn) and not game_over:
            check_text = font.render("CHECK!", True, (255, 0, 0))
            screen.blit(check_text, (SCREEN_WIDTH - 150, 10))
        
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()