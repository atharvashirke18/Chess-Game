import pygame
import os

def load_image(filename, size=(80, 80)):
    """Load an image and scale it to the desired size"""
    try:
        image = pygame.image.load(os.path.join('assets', filename))
        return pygame.transform.scale(image, size)
    except pygame.error:
        # Create a placeholder if image not found
        surface = pygame.Surface(size, pygame.SRCALPHA)
        pygame.draw.rect(surface, (200, 0, 0), (0, 0, size[0], size[1]), 2)
        return surface