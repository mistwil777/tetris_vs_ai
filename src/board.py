#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Classe représentant le plateau de jeu de Tetris
"""

class Board:
    """Représentation du plateau de jeu (grille)"""
    
    def __init__(self, width=10, height=20):
        """Initialise un nouveau plateau de jeu
        
        Args:
            width: Largeur du plateau en nombre de cellules
            height: Hauteur du plateau en nombre de cellules
        """
        self.width = width
        self.height = height
        self.grid = [[0 for _ in range(width)] for _ in range(height)]
    
    def is_valid_position(self, piece):
        """Vérifie si une pièce peut être placée à sa position actuelle
        
        Args:
            piece: Pièce à vérifier
            
        Returns:
            bool: True si la position est valide, False sinon
        """
        if not piece:
            return False
        
        for y_offset, row in enumerate(piece.get_shape()):
            for x_offset, cell in enumerate(row):
                if cell:
                    # Position de la cellule dans la grille
                    x = piece.x + x_offset
                    y = piece.y + y_offset
                    
                    # Vérifie si la cellule est dans les limites de la grille
                    if (x < 0 or x >= self.width or 
                        y < 0 or y >= self.height or 
                        # Vérifie si la cellule est déjà occupée
                        (y >= 0 and self.grid[y][x])):
                        return False
        
        return True
    
    def add_piece(self, piece):
        """Ajoute une pièce au plateau et retourne le nombre de lignes effacées
        
        Args:
            piece: Pièce à ajouter
            
        Returns:
            int: Nombre de lignes effacées
        """
        if not piece:
            return 0
        
        # Ajoute la pièce à la grille
        for y_offset, row in enumerate(piece.get_shape()):
            for x_offset, cell in enumerate(row):
                if cell:
                    x = piece.x + x_offset
                    y = piece.y + y_offset
                    
                    # Vérifie si la position est valide
                    if 0 <= x < self.width and 0 <= y < self.height:
                        self.grid[y][x] = piece.color
        
        # Efface les lignes complètes
        return self.clear_lines()
    
    def clear_lines(self):
        """Efface les lignes complètes et retourne le nombre de lignes effacées
        
        Returns:
            int: Nombre de lignes effacées
        """
        lines_cleared = 0
        y = self.height - 1
        
        while y >= 0:
            # Vérifie si la ligne est complète
            if all(self.grid[y]):
                lines_cleared += 1
                
                # Déplace toutes les lignes au-dessus vers le bas
                for y2 in range(y, 0, -1):
                    self.grid[y2] = self.grid[y2 - 1].copy()
                
                # Crée une nouvelle ligne vide en haut
                self.grid[0] = [0 for _ in range(self.width)]
            else:
                y -= 1
        
        return lines_cleared
    
    def get_grid(self):
        """Retourne la grille actuelle"""
        return self.grid
    
    def get_height_profile(self):
        """Retourne le profil de hauteur de la grille (pour l'IA)
        
        Returns:
            list: Liste des hauteurs de chaque colonne
        """
        heights = []
        
        for x in range(self.width):
            # Trouve la hauteur de chaque colonne
            for y in range(self.height):
                if self.grid[y][x]:
                    heights.append(self.height - y)
                    break
            else:
                heights.append(0)
        
        return heights
    
    def get_holes_count(self):
        """Retourne le nombre de trous dans la grille (pour l'IA)
        
        Un trou est une cellule vide avec au moins une cellule pleine au-dessus
        
        Returns:
            int: Nombre de trous
        """
        holes = 0
        
        for x in range(self.width):
            # Trouve le premier bloc de chaque colonne
            found_block = False
            for y in range(self.height):
                if self.grid[y][x]:
                    found_block = True
                elif found_block:
                    # Un trou est une cellule vide sous un bloc
                    holes += 1
        
        return holes
    
    def reset(self):
        """Réinitialise le plateau"""
        self.grid = [[0 for _ in range(self.width)] for _ in range(self.height)]
