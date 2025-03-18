#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Interface utilisateur pour le jeu Tetris
Utilise Tkinter pour afficher le jeu et gérer les interactions
"""

import tkinter as tk
from tkinter import font as tkfont
import time
import random
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
        
        # La taille des cellules sera calculée dynamiquement
        self.cell_size = 18  # Taille de départ plus petite
        
        # Configure la fenêtre principale
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Dimensions initiales de la fenêtre (75% de l'écran)
        window_width = int(screen_width * 0.75)
        window_height = int(screen_height * 0.75)
        
        # Position pour centrer la fenêtre
        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2
        
        self.root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
        self.root.minsize(800, 600)
        
        # Couleurs de l'interface
        self.colors = {
            "bg_main": "#1E1E2E",           # Fond principal sombre
            "bg_panel": "#2D2D42",          # Fond des panneaux
            "text_title": "#F8F8F2",        # Texte des titres
            "text_normal": "#F8F8F2",       # Texte normal
            "accent": "#BD93F9",            # Couleur d'accentuation
            "grid_line": "#44475A",         # Lignes de la grille
            "highlight": "#FF79C6",         # Surbrillance
            "button_bg": "#6272A4",         # Fond des boutons
            "button_fg": "#F8F8F2",         # Texte des boutons
            "board_bg": "#282A36",          # Fond du plateau de jeu
        }
        
        # Crée un style de police personnalisé
        self.title_font = tkfont.Font(family="Helvetica", size=24, weight="bold")
        self.section_font = tkfont.Font(family="Helvetica", size=16, weight="bold")
        self.score_font = tkfont.Font(family="Helvetica", size=14)
        self.info_font = tkfont.Font(family="Helvetica", size=12)
        self.game_over_font = tkfont.Font(family="Helvetica", size=36, weight="bold")
        
        # Crée les éléments de l'interface
        self.create_ui_elements()
        
        # Lier l'événement de redimensionnement
        self.root.bind("<Configure>", self.on_resize)
    
    def create_ui_elements(self):
        """Crée les éléments de l'interface utilisateur"""
        # Utilisation d'un gestionnaire de mise en page grid pour un meilleur redimensionnement
        self.main_frame = tk.Frame(self.root, bg=self.colors["bg_main"])
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Configuration des poids pour permettre un redimensionnement correct
        self.main_frame.columnconfigure(0, weight=1)  # Colonne joueur
        self.main_frame.columnconfigure(1, weight=1)  # Colonne IA
        self.main_frame.columnconfigure(2, weight=0)  # Colonne informations (taille fixe)
        
        self.main_frame.rowconfigure(0, weight=0)  # Ligne titre (fixe)
        self.main_frame.rowconfigure(1, weight=1)  # Ligne plateaux de jeu (redimensionnable)
        
        # Titre
        self.title_frame = tk.Frame(self.main_frame, bg=self.colors["bg_main"], padx=10, pady=5)
        self.title_frame.grid(row=0, column=0, columnspan=3, sticky="ew")
        
        self.title_label = tk.Label(
            self.title_frame, 
            text="TETRIS DUEL", 
            font=self.title_font, 
            bg=self.colors["bg_main"],
            fg=self.colors["accent"]
        )
        self.title_label.pack(pady=(5, 0))
        
        self.subtitle_label = tk.Label(
            self.title_frame, 
            text="Humain vs Intelligence Artificielle", 
            font=self.section_font, 
            bg=self.colors["bg_main"],
            fg=self.colors["text_title"]
        )
        self.subtitle_label.pack(pady=(0, 5))
        
        # Section du joueur humain
        self.human_section = tk.Frame(self.main_frame, bg=self.colors["bg_main"])
        self.human_section.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        
        # Pour que le contenu s'adapte à la taille disponible
        self.human_section.rowconfigure(0, weight=0)  # Score et prochaine pièce (fixe)
        self.human_section.rowconfigure(1, weight=1)  # Plateau (redimensionnable)
        self.human_section.columnconfigure(0, weight=1)
        
        # Section de l'IA
        self.ai_section = tk.Frame(self.main_frame, bg=self.colors["bg_main"])
        self.ai_section.grid(row=1, column=1, sticky="nsew", padx=10, pady=5)
        
        # Pour que le contenu s'adapte à la taille disponible
        self.ai_section.rowconfigure(0, weight=0)  # Score et prochaine pièce (fixe)
        self.ai_section.rowconfigure(1, weight=1)  # Plateau (redimensionnable)
        self.ai_section.columnconfigure(0, weight=1)
        
        # Panneau d'information
        self.info_panel = tk.Frame(self.main_frame, bg=self.colors["bg_main"])
        self.info_panel.grid(row=1, column=2, sticky="ns", padx=10, pady=5)
        
        # Informations du joueur humain
        self.human_info = tk.Frame(self.human_section, bg=self.colors["bg_panel"], padx=10, pady=5)
        self.human_info.grid(row=0, column=0, sticky="ew")
        
        self.human_label = tk.Label(
            self.human_info, 
            text="JOUEUR", 
            font=self.section_font, 
            bg=self.colors["bg_panel"],
            fg=self.colors["accent"]
        )
        self.human_label.pack(side=tk.LEFT, padx=(0, 10))
        
        self.human_score_label = tk.Label(
            self.human_info, 
            text="Score: 0", 
            font=self.score_font, 
            bg=self.colors["bg_panel"],
            fg=self.colors["text_normal"]
        )
        self.human_score_label.pack(side=tk.LEFT, padx=10)
        
        self.human_next_frame = tk.Frame(
            self.human_info,
            bg=self.colors["accent"],
            padx=2,
            pady=2
        )
        self.human_next_frame.pack(side=tk.RIGHT, padx=(10, 0))
        
        self.human_next_canvas = tk.Canvas(
            self.human_next_frame, 
            width=self.cell_size * 4,
            height=self.cell_size * 4,
            bg=self.colors["board_bg"]
        )
        self.human_next_canvas.pack()
        
        # Plateau du joueur humain
        self.human_board_container = tk.Frame(
            self.human_section,
            bg=self.colors["bg_main"],
            padx=5,
            pady=5
        )
        self.human_board_container.grid(row=1, column=0, sticky="nsew")
        
        self.human_board_container.rowconfigure(0, weight=1)
        self.human_board_container.columnconfigure(0, weight=1)
        
        self.human_board_frame = tk.Frame(
            self.human_board_container,
            bg=self.colors["accent"],
            padx=2,
            pady=2
        )
        self.human_board_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        self.human_canvas = tk.Canvas(
            self.human_board_frame, 
            width=self.cell_size * self.game.human_board.width,
            height=self.cell_size * self.game.human_board.height,
            bg=self.colors["board_bg"]
        )
        self.human_canvas.pack()
        
        # Informations de l'IA
        self.ai_info = tk.Frame(self.ai_section, bg=self.colors["bg_panel"], padx=10, pady=5)
        self.ai_info.grid(row=0, column=0, sticky="ew")
        
        self.ai_label = tk.Label(
            self.ai_info, 
            text="IA", 
            font=self.section_font, 
            bg=self.colors["bg_panel"],
            fg=self.colors["accent"]
        )
        self.ai_label.pack(side=tk.LEFT, padx=(0, 10))
        
        self.ai_score_label = tk.Label(
            self.ai_info, 
            text="Score: 0", 
            font=self.score_font, 
            bg=self.colors["bg_panel"],
            fg=self.colors["text_normal"]
        )
        self.ai_score_label.pack(side=tk.LEFT, padx=10)
        
        self.ai_next_frame = tk.Frame(
            self.ai_info,
            bg=self.colors["accent"],
            padx=2,
            pady=2
        )
        self.ai_next_frame.pack(side=tk.RIGHT, padx=(10, 0))
        
        self.ai_next_canvas = tk.Canvas(
            self.ai_next_frame, 
            width=self.cell_size * 4,
            height=self.cell_size * 4,
            bg=self.colors["board_bg"]
        )
        self.ai_next_canvas.pack()
        
        # Plateau de l'IA
        self.ai_board_container = tk.Frame(
            self.ai_section,
            bg=self.colors["bg_main"],
            padx=5,
            pady=5
        )
        self.ai_board_container.grid(row=1, column=0, sticky="nsew")
        
        self.ai_board_container.rowconfigure(0, weight=1)
        self.ai_board_container.columnconfigure(0, weight=1)
        
        self.ai_board_frame = tk.Frame(
            self.ai_board_container,
            bg=self.colors["accent"],
            padx=2,
            pady=2
        )
        self.ai_board_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        self.ai_canvas = tk.Canvas(
            self.ai_board_frame, 
            width=self.cell_size * self.game.ai_board.width,
            height=self.cell_size * self.game.ai_board.height,
            bg=self.colors["board_bg"]
        )
        self.ai_canvas.pack()
        
        # Règles spéciales
        self.rules_frame = self.create_panel(
            self.info_panel, "RÈGLES SPÉCIALES", 0, 0, pady=(0, 15)
        )
        
        # Indicateurs des règles
        self.create_rule_indicator(
            self.rules_frame, "Arc-en-ciel", "🌈", "rainbow_indicator"
        )
        self.create_rule_indicator(
            self.rules_frame, "Pause douceur", "⏱️", "pause_douceur_indicator"
        )
        self.create_rule_indicator(
            self.rules_frame, "Pièce rigolote", "💖", "piece_rigolote_indicator"
        )
        self.create_rule_indicator(
            self.rules_frame, "Cadeau surprise", "🎁", "cadeau_indicator"
        )
        
        # Contrôles
        self.controls_frame = self.create_panel(
            self.info_panel, "CONTRÔLES", 1, 0, pady=(15, 0)
        )
        
        controls_text = """
        ⬅️ ➡️: Déplacer
        ⬆️: Rotation
        ⬇️: Accélérer
        Espace: Chute rapide
        P: Pause
        R: Recommencer
        """
        
        self.controls_text = tk.Label(
            self.controls_frame, 
            text=controls_text.strip(), 
            font=self.info_font, 
            bg=self.colors["bg_panel"],
            fg=self.colors["text_normal"],
            justify=tk.LEFT,
            padx=10,
            pady=5
        )
        self.controls_text.pack(fill=tk.BOTH, expand=True)
        
        # Canvas de game over (initialement caché)
        self.game_over_canvas = tk.Canvas(
            self.root, 
            width=1280, 
            height=720, 
            bg="#000000",
            highlightthickness=0
        )
        
        # Calculer la taille initiale des cellules
        self.root.update_idletasks()
        self.calculate_cell_size()
    
    def create_panel(self, parent, title, row, column, padx=(0, 0), pady=(0, 0)):
        """Crée un panneau avec un titre
        
        Args:
            parent: Widget parent
            title: Titre du panneau
            row, column: Position dans la grille
            padx, pady: Padding
        
        Returns:
            tk.Frame: Le cadre créé
        """
        # Cadre externe avec bordure colorée
        outer_frame = tk.Frame(
            parent, 
            bg=self.colors["accent"],
            padx=2,
            pady=2,
            bd=0
        )
        outer_frame.grid(row=row, column=column, padx=padx, pady=pady, sticky="ew")
        
        # Cadre interne
        frame = tk.Frame(
            outer_frame, 
            bg=self.colors["bg_panel"],
            padx=10,
            pady=10
        )
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Titre
        title_label = tk.Label(
            frame, 
            text=title, 
            font=self.section_font, 
            bg=self.colors["bg_panel"],
            fg=self.colors["accent"]
        )
        title_label.pack(pady=(0, 10))
        
        return frame
    
    def create_rule_indicator(self, parent, text, emoji, attr_name):
        """Crée un indicateur de règle
        
        Args:
            parent: Widget parent
            text: Texte de l'indicateur
            emoji: Emoji à afficher
            attr_name: Nom de l'attribut pour stocker le widget
        """
        frame = tk.Frame(parent, bg=self.colors["bg_panel"])
        frame.pack(fill=tk.X, pady=(5, 5))
        
        emoji_label = tk.Label(
            frame, 
            text=emoji + " ", 
            font=self.info_font, 
            bg=self.colors["bg_panel"],
            fg=self.colors["text_normal"]
        )
        emoji_label.pack(side=tk.LEFT)
        
        indicator = tk.Label(
            frame, 
            text=f"{text}: Inactif", 
            font=self.info_font, 
            bg=self.colors["bg_panel"],
            fg=self.colors["text_normal"]
        )
        indicator.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        setattr(self, attr_name, indicator)
    
    def calculate_cell_size(self):
        """Calcule la taille optimale des cellules en fonction de l'espace disponible"""
        # Mettre à jour la fenêtre pour obtenir les dimensions actuelles
        self.root.update_idletasks()
        
        # Calculer l'espace disponible pour chaque plateau
        human_container_height = self.human_board_container.winfo_height()
        human_container_width = self.human_board_container.winfo_width()
        
        # Calculer la taille maximale possible des cellules (largeur et hauteur)
        max_cell_width = human_container_width / self.game.human_board.width
        max_cell_height = human_container_height / self.game.human_board.height
        
        # Prendre la plus petite des deux valeurs pour que tout le plateau tienne
        new_cell_size = min(max_cell_width, max_cell_height) * 0.9  # 90% pour laisser une marge
        
        # Limiter la taille minimale et maximale
        self.cell_size = min(max(12, new_cell_size), 25)
        
        # Mettre à jour les dimensions des canvas
        self.update_canvas_sizes()
        
        # Repositionner les plateaux au centre de leurs conteneurs
        self.update_board_positions()
    
    def update_canvas_sizes(self):
        """Met à jour les dimensions des canvas en fonction de la taille des cellules"""
        # Plateaux de jeu
        board_width = self.cell_size * self.game.human_board.width
        board_height = self.cell_size * self.game.human_board.height
        
        self.human_canvas.config(width=board_width, height=board_height)
        self.ai_canvas.config(width=board_width, height=board_height)
        
        # Pièces suivantes
        next_piece_size = self.cell_size * 4
        self.human_next_canvas.config(width=next_piece_size, height=next_piece_size)
        self.ai_next_canvas.config(width=next_piece_size, height=next_piece_size)
    
    def update_board_positions(self):
        """Repositionne les plateaux de jeu au centre de leurs conteneurs"""
        # Mettre à jour les cadres des plateaux
        self.human_board_frame.update_idletasks()
        self.ai_board_frame.update_idletasks()
        
        # Mise à jour des positions avec place pour centrer
        self.human_board_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.ai_board_frame.place(relx=0.5, rely=0.5, anchor="center")
    
    def on_resize(self, event):
        """Gère le redimensionnement de la fenêtre"""
        # Ne réagir qu'aux événements de redimensionnement de la fenêtre principale
        if event.widget == self.root:
            # Recalculer la taille des cellules
            self.calculate_cell_size()
            
            # Redessiner les éléments
            self.update_display()
    
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
        
        # Dessine les lignes de la grille
        for x in range(board.width + 1):
            canvas.create_line(
                x * self.cell_size, 0, 
                x * self.cell_size, board.height * self.cell_size, 
                fill=self.colors["grid_line"], width=1
            )
        
        for y in range(board.height + 1):
            canvas.create_line(
                0, y * self.cell_size, 
                board.width * self.cell_size, y * self.cell_size, 
                fill=self.colors["grid_line"], width=1
            )
    
    def draw_cell(self, canvas, x, y, color):
        """Dessine une cellule sur un canvas
        
        Args:
            canvas: Canvas sur lequel dessiner
            x: Position x de la cellule
            y: Position y de la cellule
            color: Couleur de la cellule
        """
        # Calcule les coordonnées
        x1 = x * self.cell_size + 1
        y1 = y * self.cell_size + 1
        x2 = (x + 1) * self.cell_size - 1
        y2 = (y + 1) * self.cell_size - 1
        
        # Dessine le rectangle principal
        canvas.create_rectangle(
            x1, y1, x2, y2,
            fill=color, outline=""
        )
        
        # Effet 3D simplifié adapté à des cellules plus petites
        border_width = max(1, int(self.cell_size * 0.1))
        
        # Bord clair (haut et gauche)
        canvas.create_line(
            x1, y1, x2, y1,
            fill=self.lighten_color(color), width=border_width
        )
        canvas.create_line(
            x1, y1, x1, y2,
            fill=self.lighten_color(color), width=border_width
        )
        
        # Bord sombre (bas et droite)
        canvas.create_line(
            x1, y2, x2, y2,
            fill=self.darken_color(color), width=border_width
        )
        canvas.create_line(
            x2, y1, x2, y2,
            fill=self.darken_color(color), width=border_width
        )
    
    def lighten_color(self, hex_color, amount=0.3):
        """Éclaircit une couleur hexadécimale
        
        Args:
            hex_color: Couleur au format hexadécimal (#RRGGBB)
            amount: Quantité d'éclaircissement (0-1)
        
        Returns:
            str: Couleur éclaircie au format hexadécimal
        """
        # Convertit la couleur hexadécimale en RGB
        hex_color = hex_color.lstrip('#')
        r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
        
        # Éclaircit la couleur
        r = min(255, int(r + (255 - r) * amount))
        g = min(255, int(g + (255 - g) * amount))
        b = min(255, int(b + (255 - b) * amount))
        
        # Convertit en hexadécimal
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def darken_color(self, hex_color, amount=0.3):
        """Assombrit une couleur hexadécimale
        
        Args:
            hex_color: Couleur au format hexadécimal (#RRGGBB)
            amount: Quantité d'assombrissement (0-1)
        
        Returns:
            str: Couleur assombrie au format hexadécimal
        """
        # Convertit la couleur hexadécimale en RGB
        hex_color = hex_color.lstrip('#')
        r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
        
        # Assombrit la couleur
        r = max(0, int(r * (1 - amount)))
        g = max(0, int(g * (1 - amount)))
        b = max(0, int(b * (1 - amount)))
        
        # Convertit en hexadécimal
        return f"#{r:02x}{g:02x}{b:02x}"
    
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
            center_x = (4 - shape_width) // 2
            center_y = (4 - shape_height) // 2
            
            # Dessine la pièce
            for y, row in enumerate(shape):
                for x, cell in enumerate(row):
                    if cell:
                        # Dessine la cellule centrée
                        self.draw_cell(canvas, center_x + x, center_y + y, color)
            
            # Dessine une fine bordure autour du canvas
            canvas.create_rectangle(
                0, 0, canvas.winfo_reqwidth(), canvas.winfo_reqheight(),
                outline=self.colors["grid_line"], width=1
            )
    
    def update_special_rules_indicators(self):
        """Met à jour les indicateurs des règles spéciales"""
        # Arc-en-ciel
        if self.game.rainbow_mode:
            remaining_time = max(0, self.game.rainbow_end_time - time.time())
            self.rainbow_indicator.config(
                text=f"Arc-en-ciel: Actif ({remaining_time:.1f}s)",
                fg=self.colors["highlight"]
            )
        else:
            next_rainbow = max(0, 120 - (time.time() - self.game.last_rainbow_time))
            self.rainbow_indicator.config(
                text=f"Arc-en-ciel: {format_time(next_rainbow)}",
                fg=self.colors["text_normal"]
            )
        
        # Pause douceur
        if self.game.pause_douceur_active["human"] or self.game.pause_douceur_active["ai"]:
            remaining_time = max(0, max(self.game.pause_douceur_end_time.values()) - time.time())
            self.pause_douceur_indicator.config(
                text=f"Pause douceur: Actif ({remaining_time:.1f}s)",
                fg=self.colors["highlight"]
            )
        else:
            next_pause = max(0, 1000 - (self.game.human_score % 1000), 1000 - (self.game.ai_score % 1000))
            self.pause_douceur_indicator.config(
                text=f"Pause douceur: Dans {next_pause} points",
                fg=self.colors["text_normal"]
            )
        
        # Pièce rigolote
        next_funny = max(0, 3000 - (self.game.human_score % 3000), 3000 - (self.game.ai_score % 3000))
        self.piece_rigolote_indicator.config(
            text=f"Pièce rigolote: Dans {next_funny} points",
            fg=self.colors["text_normal"]
        )
        
        # Cadeau surprise
        self.cadeau_indicator.config(
            text=f"Cadeau surprise: 2 lignes = cadeau",
            fg=self.colors["text_normal"]
        )
    
    def show_game_over(self, winner):
        """Affiche l'écran de fin de partie
        
        Args:
            winner: Le gagnant ("human" ou "ai")
        """
        # Adapter le canvas à la taille actuelle de la fenêtre
        self.game_over_canvas.config(
            width=self.root.winfo_width(),
            height=self.root.winfo_height()
        )
        
        # Affiche le canvas de game over
        self.game_over_canvas.place(x=0, y=0)
        
        # Crée un dégradé de fond
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        
        for i in range(20):
            y = i * (height / 20)
            color = f"#{20 + i*5:02x}{10 + i*3:02x}{30 + i*5:02x}"
            self.game_over_canvas.create_rectangle(
                0, y, width, y + (height / 20),
                fill=color, outline=""
            )
        
        # Effet de particules
        for _ in range(50):
            x = random.randint(0, width)
            y = random.randint(0, height)
            size = random.randint(3, 8)
            color = random.choice(["#FFD700", "#FF6347", "#00BFFF", "#7FFF00"])
            self.game_over_canvas.create_oval(
                x, y, x + size, y + size,
                fill=color, outline=""
            )
        
        # Centre de l'écran
        center_x = width // 2
        center_y = height // 2
        
        # Texte de game over
        self.game_over_canvas.create_text(
            center_x, center_y - 120, 
            text="GAME OVER", 
            font=self.game_over_font, 
            fill="#FF5555"
        )
        
        # Texte du gagnant
        winner_text = "Le joueur gagne !" if winner == "human" else "L'IA gagne !"
        self.game_over_canvas.create_text(
            center_x, center_y - 40, 
            text=winner_text, 
            font=self.section_font, 
            fill="#F8F8F2"
        )
        
        # Scores
        self.game_over_canvas.create_text(
            center_x, center_y + 20, 
            text=f"Joueur: {self.game.human_score} - IA: {self.game.ai_score}", 
            font=self.score_font, 
            fill="#F8F8F2"
        )
        
        # Instructions pour recommencer
        self.game_over_canvas.create_text(
            center_x, center_y + 80, 
            text="Appuyez sur R pour recommencer", 
            font=self.info_font, 
            fill="#BD93F9"
        )
        
        # Cadre du bouton
        button_frame = tk.Frame(
            self.game_over_canvas,
            bg="#BD93F9",
            padx=2,
            pady=2
        )
        button_window = self.game_over_canvas.create_window(center_x, center_y + 140, window=button_frame)
        
        # Bouton pour recommencer
        restart_button = tk.Button(
            button_frame, 
            text="Recommencer", 
            font=self.score_font,
            bg="#6272A4",
            fg="#F8F8F2",
            padx=20,
            pady=10,
            relief=tk.FLAT,
            activebackground="#7286B4",
            activeforeground="#FFFFFF",
            command=self.game.restart_game
        )
        restart_button.pack()
    
    def hide_game_over(self):
        """Cache l'écran de fin de partie"""
        self.game_over_canvas.place_forget()
