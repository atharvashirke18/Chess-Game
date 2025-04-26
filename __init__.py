# pieces/__init__.py

# Import all piece classes so they can be accessed directly from pieces package
# from .piece import Piece
# from .pawn import Pawn
# from .knight import Knight
from .bishop import Bishop
from .rook import Rook
from .queen import Queen
from .king import King

# Without the imports in __init__.py:
# These imports are redundant and should be removed
# from pieces.pawn import Pawn
# from pieces.knight import Knight
# etc.

# Importing directly from the current package
from .pawn import Pawn
from .knight import Knight  # Much cleaner
from pieces import Pawn, Knight  # Much cleaner