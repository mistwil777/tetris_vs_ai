#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Tetris à deux joueurs (Humain vs IA)
Point d'entrée principal du jeu
"""

import sys
import os

# Ajouter le répertoire parent au chemin de recherche des modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.game import Game

if __name__ == "__main__":
    """Point d'entrée principal du jeu"""
    game = Game()
    game.start()
