#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Interface utilisateur pour le jeu Tetris
Utilise Tkinter pour afficher le jeu et gérer les interactions
"""

import tkinter as tk
from tkinter import font as tkfont
import time
from src.utils import get_rainbow_colors, format_time

class UI:
    """Interface utilisateur du jeu Tetris"""
    
    def __init__(self, root, game):
        """Initialise l'interface utilisateur
        
        Args:
            root: Fenêtre principale Tkinter
            game: Instance du jeu
        """
        self.root = root
        self.game = game
        self.cell_size = 30  # Taille des cellules en pixels
        
        # Configure la fenêtre principale
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        
        # Crée un style de police personnalisé
        self.title_font = tkfont.Font(family="Helvetica", size=24, weight="bold")
        self.score_font = tkfont.Font(family="Helvetica", size=14)
        self.info_font = tkfont.Font(family="Helvetica", size=12)
        self.game_over_font = tkfont.Font(family="Helvetica", size=36, weight="bold")
        
        # Crée les éléments de l'interface
        self.create_ui_elements()
    
    def create_ui_elements(self):
        """Crée les éléments de l'interface utilisateur"""
        # Cadre principal
        self.main_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Titre
        self.title_label = tk.Label(
            self.main_frame, 
            text="Tetris à deux joueurs", 
            font=self.title_font, 
            bg="#f0f0f0"
        )
        self.title_label.grid(row=0, column=0, columnspan=4, pady=(0, 20))
        
        # Cadre du joueur humain
        self.human_frame = tk.Frame(self.main_frame, bg="#e0e0e0", padx=10, pady=10)
        self.human_frame.grid(row=1, column=0, padx=(0, 10))
        
        # Titre du joueur humain
        self.human_title = tk.Label(
            self.human_frame, 
            text="Joueur", 
            font=self.score_font, 
            bg="#e0e0e0"
        )
        self.human_title.pack(pady=(0, 10))
        
        # Score du joueur humain
        self.human_score_label = tk.Label(
            self.human_frame, 
            text="Score: 0", 
            font=self.score_font, 
            bg="#e0e0e0"
        )
        self.human_score_label.pack(pady=(0, 10))
        
        # Canvas du plateau du joueur humain
        self.human_canvas = tk.Canvas(
            self.human_frame, 
            width=self.cell_size * self.game.human_board.width,
            height=self.cell_size * self.game.human_board.height,
            bg="black"
        )
        self.human_canvas.pack()
        
        # Cadre de l'IA
        self.ai_frame = tk.Frame(self.main_frame, bg="#e0e0e0", padx=10, pady=10)
        self.ai_frame.grid(row=1, column=1, padx=(10, 0))
        
        # Titre de l'IA
        self.ai_title = tk.Label(
            self.ai_frame, 
            text="IA", 
            font=self.score_font, 
            bg="#e0e0e0"
        )
        self.ai_title.pack(pady=(0, 10))
        
        # Score de l'IA
        self.ai_score_label = tk.Label(
            self.ai_frame, 
            text="Score: 0", 
            font=self.score_font, 
            bg="#e0e0e0"
        )
        self.ai_score_label.pack(pady=(0, 10))
        
        # Canvas du plateau de l'IA
        self.ai_canvas = tk.Canvas(
            self.ai_frame, 
            width=self.cell_size * self.game.ai_board.width,
            height=self.cell_size * self.game.ai_board.height,
            bg="black"
        )
        self.ai_canvas.pack()
        
        # Informations sur les pièces suivantes
        self.next_pieces_frame = tk.Frame(self.main_frame, bg="#e0e0e0", padx=10, pady=10)
        self.next_pieces_frame.grid(row=1, column=2, padx=(20, 0), sticky="n")
        
        # Titre pour les pièces suivantes
        self.next_pieces_label = tk.Label(
            self.next_pieces_frame, 
            text="Pièces suivantes", 
            font=self.score_font, 
            bg="#e0e0e0"
        )
        self.next_pieces_label.pack(pady=(0, 10))
        
        # Canvas pour la pièce suivante du joueur humain
        self.human_next_label = tk.Label(
            self.next_pieces_frame, 
            text="Joueur", 
            font=self.info_font, 
            bg="#e0e0e0"
        )
        self.human_next_label.pack(pady=(10, 5))
        
        self.human_next_canvas = tk.Canvas(
            self.next_pieces_frame, 
            width=self.cell_size * 5,
            height=self.cell_size * 5,
            bg="black"
        )
        self.human_next_canvas.pack(pady=(0, 10))
        
        # Canvas pour la pièce suivante de l'IA
        self.ai_next_label = tk.Label(
            self.next_pieces_frame, 
            text="IA", 
            font=self.info_font, 
            bg="#e0e0e0"
        )
        self.ai_next_label.pack(pady=(10, 5))
        
        self.ai_next_canvas = tk.Canvas(
            self.next_pieces_frame, 
            width=self.cell_size * 5,
            height=self.cell_size * 5,
            bg="black"
        )
        self.ai_next_canvas.pack(pady=(0, 10))
        
        # Informations sur les règles spéciales
        self.info_frame = tk.Frame(self.main_frame, bg="#e0e0e0", padx=10, pady=10)
        self.info_frame.grid(row=1, column=3, padx=(20, 0), sticky="n")
        
        # Titre pour les règles spéciales
        self.info_title = tk.Label(
            self.info_frame, 
            text="Règles spéciales", 
            font=self.score_font, 
            bg="#e0e0e0"
        )
        self.info_title.pack(pady=(0, 10))
        
        # Indicateurs pour les règles spéciales
        self.rainbow_indicator = tk.Label(
            self.info_frame, 
            text="Arc-en-ciel: Inactif", 
            font=self.info_font, 
            bg="#e0e0e0"
        )
        self.rainbow_indicator.pack(pady=(0, 5))
        
        self.pause_douceur_indicator = tk.Label(
            self.info_frame, 
            text="Pause douceur: Inactif", 
            font=self.info_font, 
            bg="#e0e0e0"
        )
        self.pause_douceur_indicator.pack(pady=(0, 5))
        
        self.piece_rigolote_indicator = tk.Label(
            self.info_frame, 
            text="Pièce rigolote: Inactif", 
            font=self.info_font, 
            bg="#e0e0e0"
        )
        self.piece_rigolote_indicator.pack(pady=(0, 5))
        
        self.cadeau_indicator = tk.Label(
            self.info_frame, 
            text="Cadeau surprise: Inactif", 
            font=self.info_font, 
            bg="#e0e0e0"
        )
        self.cadeau_indicator.pack(pady=(0, 5))
        
        # Contrôles et aide
        self.controls_frame = tk.Frame(self.info_frame, bg="#e0e0e0")
        self.controls_frame.pack(pady=(20, 0))
        
        self.controls_title = tk.Label(
            self.controls_frame, 
            text="Contrôles", 
            font=self.info_font, 
            bg="#e0e0e0"
        )
        self.controls_title.pack(pady=(0, 5))
        
        self.controls_text = tk.Label(
            self.controls_frame, 
            text="Flèches: Déplacer\nHaut: Rotation\nEspace: Chute rapide\nP: Pause\nR: Recommencer", 
            font=self.info_font, 
            bg="#e0e0e0",
            justify=tk.LEFT
        )
        self.controls_text.pack()
        
        # Canvas de game over (initialement caché)
        self.game_over_canvas = tk.Canvas(
            self.root, 
            width=800, 
            height=600, 
            bg="black",
            highlightthickness=0
        )
        
    def update_display(self):
        """Met à jour l'affichage du jeu"""
        # Met à jour les scores
        self.human_score_label.config(text=f"Score: {self.game.human_score}")
        self.ai_score_label.config(text=f"Score: {self.game.ai_score}")
        
        # Met à jour les plateaux
        self.update_board(self.human_canvas, self.game.human_board, self.game.human_current_piece)
        self.update_board(self.ai_canvas, self.game.ai_board, self.game.ai_current_piece)
        
        # Met à jour les pièces suivantes
        self.update_next_piece(self.human_next_canvas, self.game.human_next_piece)
        self.update_next_piece(self.ai_next_canvas, self.game.ai_next_piece)
        
        # Met à jour les indicateurs des règles spéciales
        self.update_special_rules_indicators()
        
        # Met à jour la fenêtre
        self.root.update()
    
    def update_board(self, canvas, board, current_piece):
        """Met à jour l'affichage d'un plateau de jeu
        
        Args:
            canvas: Canvas à mettre à jour
            board: Plateau de jeu à afficher
            current_piece: Pièce en cours de chute
        """
        # Efface le canvas
        canvas.delete("all")
        
        # Dessine la grille du plateau
        for y in range(board.height):
            for x in range(board.width):
                # Récupère la couleur de la cellule
                cell_value = board.grid[y][x]
                
                if cell_value:
                    # Cellule occupée par une pièce
                    color = cell_value
                    
                    # Applique l'effet arc-en-ciel si actif
                    if self.game.rainbow_mode:
                        rainbow_colors = get_rainbow_colors()
                        color = rainbow_colors[(x + y) % len(rainbow_colors)]
                    
                    # Dessine la cellule
                    self.draw_cell(canvas, x, y, color)
        
        # Dessine la pièce en cours de chute
        if current_piece:
            shape = current_piece.get_shape()
            color = current_piece.color
            
            # Applique l'effet arc-en-ciel si actif
            if self.game.rainbow_mode:
                rainbow_colors = get_rainbow_colors()
                color = rainbow_colors[int(time.time() * 5) % len(rainbow_colors)]
            
            for y_offset, row in enumerate(shape):
                for x_offset, cell in enumerate(row):
                    if cell:
                        x = current_piece.x + x_offset
                        y = current_piece.y + y_offset
                        
                        # Vérifie si la cellule est dans les limites du plateau
                        if 0 <= x < board.width and 0 <= y < board.height:
                            self.draw_cell(canvas, x, y, color)
        
        # Dessine les bordures de la grille
        for x in range(board.width + 1):
            canvas.create_line(
                x * self.cell_size, 0, 
                x * self.cell_size, board.height * self.cell_size, 
                fill="#333333"
            )
        
        for y in range(board.height + 1):
            canvas.create_line(
                0, y * self.cell_size, 
                board.width * self.cell_size, y * self.cell_size, 
                fill="#333333"
            )
    
    def draw_cell(self, canvas, x, y, color):
        """Dessine une cellule sur un canvas
        
        Args:
            canvas: Canvas sur lequel dessiner
            x: Position x de la cellule
            y: Position y de la cellule
            color: Couleur de la cellule
        """
        # Dessine un rectangle représentant la cellule
        canvas.create_rectangle(
            x * self.cell_size, y * self.cell_size,
            (x + 1) * self.cell_size, (y + 1) * self.cell_size,
            fill=color, outline="#333333"
        )
        
        # Ajoute un effet 3D avec des lignes claires et sombres
        # Bordure supérieure et gauche (claire)
        canvas.create_line(
            x * self.cell_size, y * self.cell_size,
            (x + 1) * self.cell_size - 1, y * self.cell_size,
            fill="#ffffff", width=2
        )
        canvas.create_line(
            x * self.cell_size, y * self.cell_size,
            x * self.cell_size, (y + 1) * self.cell_size - 1,
            fill="#ffffff", width=2
        )
        
        # Bordure inférieure et droite (sombre)
        canvas.create_line(
            x * self.cell_size, (y + 1) * self.cell_size - 1,
            (x + 1) * self.cell_size, (y + 1) * self.cell_size - 1,
            fill="#555555", width=2
        )
        canvas.create_line(
            (x + 1) * self.cell_size - 1, y * self.cell_size,
            (x + 1) * self.cell_size - 1, (y + 1) * self.cell_size,
            fill="#555555", width=2
        )
    
    def update_next_piece(self, canvas, next_piece):
        """Met à jour l'affichage de la pièce suivante
        
        Args:
            canvas: Canvas à mettre à jour
            next_piece: Pièce suivante à afficher
        """
        # Efface le canvas
        canvas.delete("all")
        
        if next_piece:
            shape = next_piece.get_shape()
            color = next_piece.color
            
            # Applique l'effet arc-en-ciel si actif
            if self.game.rainbow_mode:
                rainbow_colors = get_rainbow_colors()
                color = rainbow_colors[int(time.time() * 5) % len(rainbow_colors)]
            
            # Détermine les dimensions de la forme
            shape_width = len(shape[0])
            shape_height = len(shape)
            
            # Détermine la position pour centrer la forme
            center_x = (5 - shape_width) // 2
            center_y = (5 - shape_height) // 2
            
            # Dessine la pièce
            for y, row in enumerate(shape):
                for x, cell in enumerate(row):
                    if cell:
                        # Dessine la cellule centrée
                        self.draw_cell(canvas, center_x + x, center_y + y, color)
    
    def update_special_rules_indicators(self):
        """Met à jour les indicateurs des règles spéciales"""
        # Arc-en-ciel
        if self.game.rainbow_mode:
            remaining_time = max(0, self.game.rainbow_end_time - time.time())
            self.rainbow_indicator.config(
                text=f"Arc-en-ciel: Actif ({remaining_time:.1f}s)",
                fg="#ff0000"
            )
        else:
            next_rainbow = max(0, 120 - (time.time() - self.game.last_rainbow_time))
            self.rainbow_indicator.config(
                text=f"Arc-en-ciel: {format_time(next_rainbow)}",
                fg="black"
            )
        
        # Pause douceur
        if self.game.pause_douceur_active["human"] or self.game.pause_douceur_active["ai"]:
            remaining_time = max(0, max(self.game.pause_douceur_end_time.values()) - time.time())
            self.pause_douceur_indicator.config(
                text=f"Pause douceur: Actif ({remaining_time:.1f}s)",
                fg="#00aa00"
            )
        else:
            next_pause = max(0, 1000 - (self.game.human_score % 1000), 1000 - (self.game.ai_score % 1000))
            self.pause_douceur_indicator.config(
                text=f"Pause douceur: Dans {next_pause} points",
                fg="black"
            )
        
        # Pièce rigolote
        next_funny = max(0, 3000 - (self.game.human_score % 3000), 3000 - (self.game.ai_score % 3000))
        self.piece_rigolote_indicator.config(
            text=f"Pièce rigolote: Dans {next_funny} points",
            fg="black"
        )
        
        # Cadeau surprise
        self.cadeau_indicator.config(
            text=f"Cadeau surprise: 2 lignes = cadeau",
            fg="black"
        )
    
    def show_game_over(self, winner):
        """Affiche l'écran de fin de partie
        
        Args:
            winner: Le gagnant ("human" ou "ai")
        """
        # Affiche le canvas de game over
        self.game_over_canvas.place(x=0, y=0)
        
        # Texte de game over
        self.game_over_canvas.create_text(
            400, 200, 
            text="GAME OVER", 
            font=self.game_over_font, 
            fill="#ff0000"
        )
        
        # Texte du gagnant
        winner_text = "Le joueur gagne !" if winner == "human" else "L'IA gagne !"
        self.game_over_canvas.create_text(
            400, 250, 
            text=winner_text, 
            font=self.title_font, 
            fill="#ffffff"
        )
        
        # Scores
        self.game_over_canvas.create_text(
            400, 300, 
            text=f"Joueur: {self.game.human_score} - IA: {self.game.ai_score}", 
            font=self.score_font, 
            fill="#ffffff"
        )
        
        # Instructions pour recommencer
        self.game_over_canvas.create_text(
            400, 350, 
            text="Appuyez sur R pour recommencer", 
            font=self.info_font, 
            fill="#ffffff"
        )
        
        # Bouton pour recommencer
        restart_button = tk.Button(
            self.game_over_canvas, 
            text="Recommencer", 
            font=self.score_font,
            command=self.game.restart_game
        )
        restart_button_window = self.game_over_canvas.create_window(400, 400, window=restart_button)
    
    def hide_game_over(self):
        """Cache l'écran de fin de partie"""
        self.game_over_canvas.place_forget()
