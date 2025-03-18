#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Intelligence artificielle pour le jeu Tetris
Implémente un algorithme simple pour déterminer le meilleur placement d'une pièce
"""

import copy
import random

class AI:
    """Intelligence artificielle simple pour le jeu Tetris"""
    
    def __init__(self, board):
        """Initialise l'IA avec un plateau de jeu
        
        Args:
            board: Plateau de jeu de l'IA
        """
        self.board = board
        
        # Paramètres d'évaluation des positions
        self.weights = {
            'height': -0.510066,  # Hauteur cumulée 
            'lines': 0.760666,    # Lignes complètes
            'holes': -0.35663,    # Nombre de trous
            'bumpiness': -0.184483 # Irrégularité du terrain
        }
    
    def get_best_move(self, piece):
        """Détermine le meilleur placement pour une pièce
        
        Args:
            piece: Pièce à placer
            
        Returns:
            dict: Dictionnaire contenant la position x et la rotation optimales
                  ou None si aucun placement valide n'est trouvé
        """
        if not piece:
            return None
        
        best_score = float('-inf')
        best_move = None
        
        # Essaie toutes les rotations possibles
        for rotation in range(4):  # Maximum 4 rotations
            test_piece = copy.deepcopy(piece)
            test_piece.rotation = rotation
            
            # Pour chaque rotation, essaie toutes les positions x possibles
            for x in range(-2, self.board.width + 2):
                test_piece = copy.deepcopy(piece)
                test_piece.rotation = rotation
                test_piece.x = x
                
                # Fait tomber la pièce jusqu'à ce qu'elle ne puisse plus descendre
                test_piece.y = 0
                while self.board.is_valid_position(test_piece):
                    test_piece.y += 1
                
                # Remonte d'une case pour obtenir la dernière position valide
                test_piece.y -= 1
                
                # Vérifie si le placement est valide
                if test_piece.y >= 0 and self.board.is_valid_position(test_piece):
                    # Simule l'ajout de la pièce au plateau et évalue la position
                    test_board = copy.deepcopy(self.board)
                    test_board.add_piece(test_piece)
                    
                    # Évalue la position
                    score = self.evaluate_position(test_board)
                    
                    # Met à jour le meilleur mouvement si nécessaire
                    if score > best_score:
                        best_score = score
                        best_move = {"x": x, "rotation": rotation}
                        
                        # Ajoute un peu d'aléatoire pour éviter les mouvements trop prévisibles
                        if random.random() < 0.1:  # 10% de chance de choisir une position différente
                            best_score = score + random.uniform(-0.1, 0.1)
        
        return best_move
    
    def evaluate_position(self, board):
        """Évalue une position de jeu
        
        Args:
            board: Plateau de jeu à évaluer
            
        Returns:
            float: Score d'évaluation
        """
        # Récupère les informations sur le plateau
        heights = board.get_height_profile()
        holes = board.get_holes_count()
        
        # Calcule les métriques d'évaluation
        aggregate_height = sum(heights)
        complete_lines = sum(1 for y in range(board.height) if all(board.grid[y]))
        bumpiness = sum(abs(heights[i] - heights[i+1]) for i in range(len(heights)-1))
        
        # Calcule le score d'évaluation
        score = (
            self.weights['height'] * aggregate_height +
            self.weights['lines'] * complete_lines +
            self.weights['holes'] * holes +
            self.weights['bumpiness'] * bumpiness
        )
        
        return score
