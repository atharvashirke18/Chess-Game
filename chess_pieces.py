# create_chess_pieces.py
import pygame
import os

# Initialize pygame
pygame.init()

# Create assets directory if it doesn't exist
if not os.path.exists('assets'):
    os.makedirs('assets')

piece_size = (80, 80)
colors = ['white', 'black']
pieces = ['pawn', 'rook', 'knight', 'bishop', 'queen', 'king']

for color in colors:
    for piece in pieces:
        # Create surface for piece
        surface = pygame.Surface(piece_size, pygame.SRCALPHA)
        
        # Fill with base color
        base_color = (230, 230, 230) if color == 'white' else (50, 50, 50)
        
        # Draw piece (simplified versions)
        if piece == 'pawn':
            pygame.draw.circle(surface, base_color, (40, 25), 15)
            pygame.draw.polygon(surface, base_color, [(25, 40), (55, 40), (50, 60), (30, 60)])
        elif piece == 'rook':
            pygame.draw.rect(surface, base_color, (25, 20, 30, 45))
            pygame.draw.rect(surface, base_color, (20, 60, 40, 10))
        elif piece == 'knight':
            pygame.draw.polygon(surface, base_color, [(30, 20), (55, 25), (40, 45), (30, 60), (50, 60)])
        elif piece == 'bishop':
            pygame.draw.circle(surface, base_color, (40, 25), 10)
            pygame.draw.polygon(surface, base_color, [(30, 30), (50, 30), (40, 60)])
        elif piece == 'queen':
            pygame.draw.circle(surface, base_color, (40, 20), 15)
            pygame.draw.polygon(surface, base_color, [(25, 30), (55, 30), (45, 60), (35, 60)])
        elif piece == 'king':
            pygame.draw.rect(surface, base_color, (35, 10, 10, 15))
            pygame.draw.circle(surface, base_color, (40, 30), 15)
            pygame.draw.polygon(surface, base_color, [(25, 35), (55, 35), (45, 60), (35, 60)])
        
        # Add outline
        outline_color = (0, 0, 0) if color == 'white' else (0, 0, 0)
        pygame.draw.rect(surface, outline_color, (0, 0, piece_size[0], piece_size[1]), 2)
        
        # Save the image
        filename = f"{color}_{piece}.png"
        pygame.image.save(surface, os.path.join('assets', filename))
        print(f"Created {filename}")

print("All chess piece images created successfully!")