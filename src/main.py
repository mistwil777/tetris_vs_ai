#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import customtkinter as ctk

# Ajouter le répertoire parent au chemin de recherche des modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.game import Game

if __name__ == "__main__":
    """Point d'entrée principal du jeu"""
    # Initialiser CustomTkinter
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    
    game = Game(use_custom_tkinter=True)
    game.start()
