#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Classes représentant les différentes pièces de Tetris
"""

import random
from enum import Enum, auto

class PieceType(Enum):
    """Types de pièces Tetris"""
    I = auto()  # Ligne
    J = auto()  # L gauche
    L = auto()  # L droite
    O = auto()  # Carré
    S = auto()  # S
    T = auto()  # T
    Z = auto()  # Z
    HEART = auto()  # Cœur (pièce spéciale)
    STAR = auto()  # Étoile (pièce spéciale)

class Piece:
    """Classe de base pour les pièces Tetris"""
    
    def __init__(self, piece_type):
        """Initialise une nouvelle pièce
        
        Args:
            piece_type: Type de la pièce (PieceType)
        """
        self.type = piece_type
        self.x = 3  # Position initiale en x
        self.y = 0  # Position initiale en y
        self.rotation = 0  # Rotation initiale
        self.color = self._get_color()
    
    def _get_color(self):
        """Retourne la couleur de la pièce en fonction de son type"""
        colors = {
            PieceType.I: "#00FFFF",  # Cyan
            PieceType.J: "#0000FF",  # Bleu
            PieceType.L: "#FF8000",  # Orange
            PieceType.O: "#FFFF00",  # Jaune
            PieceType.S: "#00FF00",  # Vert
            PieceType.T: "#8000FF",  # Violet
            PieceType.Z: "#FF0000",  # Rouge
            PieceType.HEART: "#FF00FF",  # Rose
            PieceType.STAR: "#FFFFFF",  # Blanc
        }
        return colors.get(self.type, "#888888")
    
    def get_shape(self):
        """Retourne la forme de la pièce en fonction de sa rotation"""
        shapes = self._get_shapes()
        return shapes[self.rotation % len(shapes)]
    
    def _get_shapes(self):
        """Retourne toutes les formes possibles de la pièce"""
        # À implémenter dans les classes dérivées
        return []
    
    def rotate(self):
        """Fait pivoter la pièce"""
        shapes = self._get_shapes()
        self.rotation = (self.rotation + 1) % len(shapes)

class IPiece(Piece):
    """Pièce en forme de I (ligne)"""
    
    def __init__(self):
        super().__init__(PieceType.I)
    
    def _get_shapes(self):
        return [
            [
                [0, 0, 0, 0],
                [1, 1, 1, 1],
                [0, 0, 0, 0],
                [0, 0, 0, 0]
            ],
            [
                [0, 0, 1, 0],
                [0, 0, 1, 0],
                [0, 0, 1, 0],
                [0, 0, 1, 0]
            ]
        ]

class JPiece(Piece):
    """Pièce en forme de J (L gauche)"""
    
    def __init__(self):
        super().__init__(PieceType.J)
    
    def _get_shapes(self):
        return [
            [
                [1, 0, 0],
                [1, 1, 1],
                [0, 0, 0]
            ],
            [
                [0, 1, 1],
                [0, 1, 0],
                [0, 1, 0]
            ],
            [
                [0, 0, 0],
                [1, 1, 1],
                [0, 0, 1]
            ],
            [
                [0, 1, 0],
                [0, 1, 0],
                [1, 1, 0]
            ]
        ]

class LPiece(Piece):
    """Pièce en forme de L (L droite)"""
    
    def __init__(self):
        super().__init__(PieceType.L)
    
    def _get_shapes(self):
        return [
            [
                [0, 0, 1],
                [1, 1, 1],
                [0, 0, 0]
            ],
            [
                [0, 1, 0],
                [0, 1, 0],
                [0, 1, 1]
            ],
            [
                [0, 0, 0],
                [1, 1, 1],
                [1, 0, 0]
            ],
            [
                [1, 1, 0],
                [0, 1, 0],
                [0, 1, 0]
            ]
        ]

class OPiece(Piece):
    """Pièce en forme de O (carré)"""
    
    def __init__(self):
        super().__init__(PieceType.O)
    
    def _get_shapes(self):
        return [
            [
                [1, 1],
                [1, 1]
            ]
        ]

class SPiece(Piece):
    """Pièce en forme de S"""
    
    def __init__(self):
        super().__init__(PieceType.S)
    
    def _get_shapes(self):
        return [
            [
                [0, 1, 1],
                [1, 1, 0],
                [0, 0, 0]
            ],
            [
                [0, 1, 0],
                [0, 1, 1],
                [0, 0, 1]
            ]
        ]

class TPiece(Piece):
    """Pièce en forme de T"""
    
    def __init__(self):
        super().__init__(PieceType.T)
    
    def _get_shapes(self):
        return [
            [
                [0, 1, 0],
                [1, 1, 1],
                [0, 0, 0]
            ],
            [
                [0, 1, 0],
                [0, 1, 1],
                [0, 1, 0]
            ],
            [
                [0, 0, 0],
                [1, 1, 1],
                [0, 1, 0]
            ],
            [
                [0, 1, 0],
                [1, 1, 0],
                [0, 1, 0]
            ]
        ]

class ZPiece(Piece):
    """Pièce en forme de Z"""
    
    def __init__(self):
        super().__init__(PieceType.Z)
