#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Interface utilisateur pour le jeu Tetris avec effets visuels améliorés
Utilise CustomTkinter pour un design moderne avec coins arrondis et effets 3D
"""

import tkinter as tk
from tkinter import font as tkfont
import time
import random
import customtkinter as ctk
from src.utils import get_rainbow_colors, format_time

class UI:
    """Interface utilisateur du jeu Tetris avec effets visuels améliorés"""
    
    def __init__(self, root, game):
        """Initialise l'interface utilisateur
        
        Args:
            root: Fenêtre principale CustomTkinter
            game: Instance du jeu
        """
        self.root = root
        self.game = game
        
        # Configuration du thème CustomTkinter
        ctk.set_appearance_mode("dark")  # Modes: "dark", "light"
        ctk.set_default_color_theme("blue")  # Thèmes: "blue", "green", "dark-blue"
        
        # Taille initiale des cellules (réduite pour assurer la visibilité complète)
        self.cell_size = 16
        
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
        self.root.minsize(900, 650)  # Taille minimale augmentée pour assurer la visibilité
        
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
            "shadow": "#191A21",            # Couleur des ombres
        }
        
        # Crée les éléments de l'interface
        self.create_ui_elements()
        
        # Lier l'événement de redimensionnement
        self.root.bind("<Configure>", self.on_resize)
    
    def create_ui_elements(self):
        """Crée les éléments de l'interface utilisateur avec coins arrondis et effet 3D"""
        # Structure principale
        self.main_frame = ctk.CTkFrame(self.root, corner_radius=0, fg_color=self.colors["bg_main"])
        self.main_frame.pack(fill="both", expand=True)
        
        # Configuration du système de grille
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.columnconfigure(2, weight=0)
        self.main_frame.rowconfigure(0, weight=0)  # Titre (fixe)
        self.main_frame.rowconfigure(1, weight=1)  # Plateaux de jeu (extensible)
        
        # Titre avec effet 3D
        self.title_frame = ctk.CTkFrame(
            self.main_frame, 
            corner_radius=15, 
            fg_color=self.colors["bg_main"],
            border_width=0
        )
        self.title_frame.grid(row=0, column=0, columnspan=3, sticky="ew", padx=20, pady=5)  # Padding réduit en haut
        
        self.title_label = ctk.CTkLabel(
            self.title_frame, 
            text="TETRIS DUEL", 
            font=ctk.CTkFont(family="Helvetica", size=24, weight="bold"),
            text_color=self.colors["accent"]
        )
        self.title_label.pack(pady=(5, 0))
        
        self.subtitle_label = ctk.CTkLabel(
            self.title_frame, 
            text="Humain vs Intelligence Artificielle", 
            font=ctk.CTkFont(family="Helvetica", size=16, weight="bold"),
            text_color=self.colors["text_title"]
        )
        self.subtitle_label.pack(pady=(0, 5))

        # Section du joueur humain avec coins arrondis
        self.human_section = self.create_3d_frame(
            self.main_frame, 
            row=1, 
            column=0, 
            title="JOUEUR", 
            corner_radius=20
        )
        
        # Section pour le score et la prochaine pièce du joueur humain
        self.human_info_container = ctk.CTkFrame(
            self.human_section, 
            corner_radius=15, 
            fg_color=self.colors["bg_panel"],
            border_width=1,
            border_color=self.colors["accent"]
        )
        self.human_info_container.pack(fill="x", padx=10, pady=(5, 5))  # Padding vertical réduit
        
        self.human_score_label = ctk.CTkLabel(
            self.human_info_container, 
            text="Score: 0", 
            font=ctk.CTkFont(family="Helvetica", size=14),
            text_color=self.colors["text_normal"]
        )
        self.human_score_label.pack(side="left", padx=10, pady=5)
        
        self.human_next_frame = ctk.CTkFrame(
            self.human_info_container,
            corner_radius=10,
            fg_color=self.colors["accent"],
            border_width=0
        )
        self.human_next_frame.pack(side="right", padx=10, pady=5)
        
        self.human_next_canvas = tk.Canvas(
            self.human_next_frame, 
            width=self.cell_size * 4,
            height=self.cell_size * 4,
            bg=self.colors["board_bg"],
            highlightthickness=0
        )
        self.human_next_canvas.pack(padx=2, pady=2)
        
        # Plateau du joueur humain (Canvas traditionnel pour le jeu)
        self.human_board_container = ctk.CTkFrame(
            self.human_section,
            corner_radius=0,
            fg_color=self.colors["bg_panel"],
            border_width=0
        )
        # Augmenter l'expansion pour maximiser l'espace disponible
        self.human_board_container.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Effet d'ombre pour le plateau (3D)
        self.human_shadow_frame = ctk.CTkFrame(
            self.human_board_container,
            corner_radius=15,
            fg_color=self.colors["shadow"],
            border_width=0
        )
        # Position ajustée pour garantir la visibilité complète
        self.human_shadow_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.95, relheight=0.95, x=5, y=5)
        
        # Cadre du plateau avec bordure réduite
        self.human_board_frame = ctk.CTkFrame(
            self.human_board_container,
            corner_radius=15,
            fg_color=self.colors["accent"],
            border_width=0
        )
        self.human_board_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.95, relheight=0.95)
        
        # Canvas standard pour le plateau de jeu avec padding réduit
        self.human_canvas = tk.Canvas(
            self.human_board_frame, 
            width=self.cell_size * self.game.human_board.width,
            height=self.cell_size * self.game.human_board.height,
            bg=self.colors["board_bg"],
            highlightthickness=0
        )
        self.human_canvas.pack(padx=3, pady=3)  # Padding réduit
        
        # Section de l'IA avec coins arrondis
        self.ai_section = self.create_3d_frame(
            self.main_frame, 
            row=1, 
            column=1, 
            title="INTELLIGENCE ARTIFICIELLE", 
            corner_radius=20
        )
        
        # Score et prochaine pièce de l'IA
        self.ai_info_container = ctk.CTkFrame(
            self.ai_section, 
            corner_radius=15, 
            fg_color=self.colors["bg_panel"],
            border_width=1,
            border_color=self.colors["accent"]
        )
        self.ai_info_container.pack(fill="x", padx=10, pady=(5, 5))  # Padding vertical réduit
        
        self.ai_score_label = ctk.CTkLabel(
            self.ai_info_container, 
            text="Score: 0", 
            font=ctk.CTkFont(family="Helvetica", size=14),
            text_color=self.colors["text_normal"]
        )
        self.ai_score_label.pack(side="left", padx=10, pady=5)
        
        self.ai_next_frame = ctk.CTkFrame(
            self.ai_info_container,
            corner_radius=10,
            fg_color=self.colors["accent"],
            border_width=0
        )
        self.ai_next_frame.pack(side="right", padx=10, pady=5)
        
        self.ai_next_canvas = tk.Canvas(
            self.ai_next_frame, 
            width=self.cell_size * 4,
            height=self.cell_size * 4,
            bg=self.colors["board_bg"],
            highlightthickness=0
        )
        self.ai_next_canvas.pack(padx=2, pady=2)
        
        # Plateau de l'IA
        self.ai_board_container = ctk.CTkFrame(
            self.ai_section,
            corner_radius=0,
            fg_color=self.colors["bg_panel"],
            border_width=0
        )
        # Augmenter l'expansion pour maximiser l'espace disponible
        self.ai_board_container.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Effet d'ombre pour le plateau de l'IA (3D)
        self.ai_shadow_frame = ctk.CTkFrame(
            self.ai_board_container,
            corner_radius=15,
            fg_color=self.colors["shadow"],
            border_width=0
        )
        # Position ajustée pour garantir la visibilité complète
        self.ai_shadow_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.95, relheight=0.95, x=5, y=5)
        
        # Cadre du plateau avec bordure réduite
        self.ai_board_frame = ctk.CTkFrame(
            self.ai_board_container,
            corner_radius=15,
            fg_color=self.colors["accent"],
            border_width=0
        )
        self.ai_board_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.95, relheight=0.95)
        
        # Canvas standard pour le plateau de jeu avec padding réduit
        self.ai_canvas = tk.Canvas(
            self.ai_board_frame, 
            width=self.cell_size * self.game.ai_board.width,
            height=self.cell_size * self.game.ai_board.height,
            bg=self.colors["board_bg"],
            highlightthickness=0
        )
        self.ai_canvas.pack(padx=3, pady=3)  # Padding réduit
        
        # Panneau d'information avec coins arrondis
        self.info_panel = ctk.CTkFrame(
            self.main_frame,
            corner_radius=20,
            fg_color=self.colors["bg_main"],
            border_width=0
        )
        self.info_panel.grid(row=1, column=2, padx=10, pady=10, sticky="ns")
        
        # Règles spéciales
        self.rules_frame = self.create_info_panel(
            self.info_panel, "RÈGLES SPÉCIALES", 15
        )
        self.rules_frame.pack(fill="x", padx=5, pady=5)
        
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
        self.controls_frame = self.create_info_panel(
            self.info_panel, "CONTRÔLES", 15
        )
        self.controls_frame.pack(fill="x", padx=5, pady=(15, 5))
        
        controls_text = """
        ⬅️ ➡️: Déplacer
        ⬆️: Rotation
        ⬇️: Accélérer
        Espace: Chute rapide
        P: Pause
        R: Recommencer
        """
        
        self.controls_text = ctk.CTkLabel(
            self.controls_frame, 
            text=controls_text.strip(), 
            font=ctk.CTkFont(family="Helvetica", size=12),
            text_color=self.colors["text_normal"],
            justify="left"
        )
        self.controls_text.pack(fill="both", expand=True, padx=10, pady=10)
        
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
    
    def create_3d_frame(self, parent, row, column, title, corner_radius=15):
        """Crée un cadre avec effet 3D en utilisant une ombre
        
        Args:
            parent: Widget parent
            row, column: Position dans la grille
            title: Titre du cadre
            corner_radius: Rayon des coins arrondis
            
        Returns:
            CTkFrame: Le cadre créé
        """
        # Cadre principal avec ombre
        frame = ctk.CTkFrame(
            parent,
            corner_radius=corner_radius,
            fg_color=self.colors["bg_panel"],
            border_width=2,
            border_color=self.colors["accent"]
        )
        frame.grid(row=row, column=column, padx=10, pady=5, sticky="nsew")  # Padding vertical réduit
        
        if title:
            title_label = ctk.CTkLabel(
                frame,
                text=title,
                font=ctk.CTkFont(family="Helvetica", size=16, weight="bold"),
                text_color=self.colors["accent"]
            )
            title_label.pack(pady=5)  # Padding vertical réduit
        
        return frame
    
    def create_info_panel(self, parent, title, corner_radius=10):
        """Crée un panneau d'information avec effet 3D
        
        Args:
            parent: Widget parent
            title: Titre du panneau
            corner_radius: Rayon des coins arrondis
            
        Returns:
            CTkFrame: Le cadre créé
        """
        # Cadre d'ombre
        shadow_frame = ctk.CTkFrame(
            parent,
            corner_radius=corner_radius,
            fg_color=self.colors["shadow"],
            border_width=0
        )
        shadow_frame.pack(fill="x", padx=5, pady=5)
        
        # Cadre extérieur
        outer_frame = ctk.CTkFrame(
            shadow_frame,
            corner_radius=corner_radius,
            fg_color=self.colors["accent"],
            border_width=0
        )
        outer_frame.pack(fill="x", padx=0, pady=0)
        
        # Cadre intérieur
        inner_frame = ctk.CTkFrame(
            outer_frame,
            corner_radius=corner_radius-2,
            fg_color=self.colors["bg_panel"],
            border_width=0
        )
        inner_frame.pack(fill="both", expand=True, padx=2, pady=2)
        
        # Titre
        if title:
            title_label = ctk.CTkLabel(
                inner_frame,
                text=title,
                font=ctk.CTkFont(family="Helvetica", size=16, weight="bold"),
                text_color=self.colors["accent"]
            )
            title_label.pack(pady=(5, 5))  # Padding vertical réduit
        
        return inner_frame
    
    def create_rule_indicator(self, parent, text, emoji, attr_name):
        """Crée un indicateur de règle
        
        Args:
            parent: Widget parent
            text: Texte de l'indicateur
            emoji: Emoji à afficher
            attr_name: Nom de l'attribut pour stocker le widget
        """
        frame = ctk.CTkFrame(parent, fg_color=self.colors["bg_panel"])
        frame.pack(fill="x", pady=(5, 5))
        
        emoji_label = ctk.CTkLabel(
            frame, 
            text=emoji + " ", 
            font=ctk.CTkFont(family="Helvetica", size=12),
            text_color=self.colors["text_normal"]
        )
        emoji_label.pack(side="left", padx=(10, 0))
        
        indicator = ctk.CTkLabel(
            frame, 
            text=f"{text}: Inactif", 
            font=ctk.CTkFont(family="Helvetica", size=12),
            text_color=self.colors["text_normal"]
        )
        indicator.pack(side="left", fill="x", expand=True)
        
        setattr(self, attr_name, indicator)
    
    def calculate_cell_size(self):
        """Calcule la taille optimale des cellules en fonction de l'espace disponible"""
        # Mettre à jour la fenêtre pour obtenir les dimensions actuelles
        self.root.update_idletasks()
        
        # Calculer l'espace disponible pour chaque plateau
        human_container_height = self.human_board_container.winfo_height()
        human_container_width = self.human_board_container.winfo_width()
        
        # Calculer la taille maximale possible des cellules (largeur et hauteur)
        # Réduire la largeur et la hauteur utilisables pour tenir compte des marges et bordures
        available_width = human_container_width * 0.9
        available_height = human_container_height * 0.9
        
        max_cell_width = available_width / self.game.human_board.width
        max_cell_height = available_height / self.game.human_board.height
        
        # Prendre la plus petite des deux valeurs pour que tout le plateau tienne
        # Réduire encore de 5% pour garantir la visibilité de la dernière ligne
        new_cell_size = min(max_cell_width, max_cell_height) * 0.95
        
        # Limiter la taille minimale et maximale (taille max réduite pour assurer la visibilité)
        self.cell_size = min(max(10, new_cell_size), 22)
        
        # Mettre à jour les dimensions des canvas
        self.update_canvas_sizes()
    
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
        self.human_score_label.configure(text=f"Score: {self.game.human_score}")
        self.ai_score_label.configure(text=f"Score: {self.game.ai_score}")
        
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
            
        # Dessine une bordure autour du plateau pour mieux le délimiter
        canvas.create_rectangle(
            0, 0, 
            board.width * self.cell_size, 
            board.height * self.cell_size,
            outline=self.colors["accent"], width=1
        )
    
    def draw_cell(self, canvas, x, y, color):
        """Dessine une cellule sur un canvas avec effet 3D
        
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
        border_width = max(1, int(self.cell_size * 0.08))  # Bordure plus fine
        
        # Bord clair (haut et gauche) - effet 3D
        canvas.create_line(
            x1, y1, x2, y1,
            fill=self.lighten_color(color), width=border_width
        )
        canvas.create_line(
            x1, y1, x1, y2,
            fill=self.lighten_color(color), width=border_width
        )
        
        # Bord sombre (bas et droite) - effet 3D
        canvas.create_line(
            x1, y2, x2, y2,
            fill=self.darken_color(color), width=border_width
        )
        canvas.create_line(
            x2, y1, x2, y2,
            fill=self.darken_color(color), width=border_width
        )
        
        # Effet de profondeur simplifié pour petites cellules
        if self.cell_size > 14:  # Seulement pour les cellules assez grandes
            padding = self.cell_size * 0.2
            canvas.create_rectangle(
                x1 + padding, y1 + padding,
                x2 - padding, y2 - padding,
                fill=self.lighten_color(color, amount=0.1),
                outline=""
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
            self.rainbow_indicator.configure(
                text=f"Arc-en-ciel: Actif ({remaining_time:.1f}s)",
                text_color=self.colors["highlight"]
            )
        else:
            next_rainbow = max(0, 120 - (time.time() - self.game.last_rainbow_time))
            self.rainbow_indicator.configure(
                text=f"Arc-en-ciel: {format_time(next_rainbow)}",
                text_color=self.colors["text_normal"]
            )
        
        # Pause douceur
        if self.game.pause_douceur_active["human"] or self.game.pause_douceur_active["ai"]:
            remaining_time = max(0, max(self.game.pause_douceur_end_time.values()) - time.time())
            self.pause_douceur_indicator.configure(
                text=f"Pause douceur: Actif ({remaining_time:.1f}s)",
                text_color=self.colors["highlight"]
            )
        else:
            next_pause = max(0, 1000 - (self.game.human_score % 1000), 1000 - (self.game.ai_score % 1000))
            self.pause_douceur_indicator.configure(
                text=f"Pause douceur: Dans {next_pause} points",
                text_color=self.colors["text_normal"]
            )
        
        # Pièce rigolote
        next_funny = max(0, 3000 - (self.game.human_score % 3000), 3000 - (self.game.ai_score % 3000))
        self.piece_rigolote_indicator.configure(
            text=f"Pièce rigolote: Dans {next_funny} points",
            text_color=self.colors["text_normal"]
        )
        
        # Cadeau surprise
        self.cadeau_indicator.configure(
            text=f"Cadeau surprise: 2 lignes = cadeau",
            text_color=self.colors["text_normal"]
        )
    
    def show_game_over(self, winner):
        """Affiche l'écran de fin de partie avec effet 3D
        
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
        
        # Effet de particules pour un rendu 3D
        for _ in range(100):
            x = random.randint(0, width)
            y = random.randint(0, height)
            size = random.randint(2, 10)
            color = random.choice(["#FFD700", "#FF6347", "#00BFFF", "#7FFF00", "#FFC0CB"])
            
            # Cercle avec dégradé pour effet 3D
            self.game_over_canvas.create_oval(
                x, y, x + size, y + size,
                fill=color, outline=self.lighten_color(color)
            )
            # Petit cercle blanc pour effet de reflet/brillance
            self.game_over_canvas.create_oval(
                x + size//4, y + size//4, x + size//2, y + size//2,
                fill="#FFFFFF", outline=""
            )
        
        # Centre de l'écran
        center_x = width // 2
        center_y = height // 2
        
        # Texte de game over avec effet d'ombre pour 3D
        shadow_offset = 4
        self.game_over_canvas.create_text(
            center_x + shadow_offset, center_y - 120 + shadow_offset, 
            text="GAME OVER", 
            font=("Helvetica", 36, "bold"), 
            fill="#000000"
        )
        self.game_over_canvas.create_text(
            center_x, center_y - 120, 
            text="GAME OVER", 
            font=("Helvetica", 36, "bold"), 
            fill="#FF5555"
        )
        
        # Texte du gagnant avec effet d'ombre pour 3D
        winner_text = "Le joueur gagne !" if winner == "human" else "L'IA gagne !"
        self.game_over_canvas.create_text(
            center_x + shadow_offset, center_y - 40 + shadow_offset, 
            text=winner_text, 
            font=("Helvetica", 18, "bold"), 
            fill="#000000"
        )
        self.game_over_canvas.create_text(
            center_x, center_y - 40, 
            text=winner_text, 
            font=("Helvetica", 18, "bold"), 
            fill="#F8F8F2"
        )
        
        # Scores
        self.game_over_canvas.create_text(
            center_x, center_y + 20, 
            text=f"Joueur: {self.game.human_score} - IA: {self.game.ai_score}", 
            font=("Helvetica", 14), 
            fill="#F8F8F2"
        )
        
        # Instructions pour recommencer
        self.game_over_canvas.create_text(
            center_x, center_y + 80, 
            text="Appuyez sur R pour recommencer", 
            font=("Helvetica", 12), 
            fill="#BD93F9"
        )
        
        # Création du bouton avec CustomTkinter
        restart_button = ctk.CTkButton(
            self.root,
            text="Recommencer",
            font=ctk.CTkFont(family="Helvetica", size=14),
            fg_color=self.colors["button_bg"],
            text_color=self.colors["button_fg"],
            hover_color=self.darken_color(self.colors["button_bg"], amount=0.1),
            corner_radius=10,
            border_width=2,
            border_color=self.colors["accent"],
            command=self.game.restart_game
        )
        # Placement du bouton sur le canvas
        button_window = self.game_over_canvas.create_window(
            center_x, center_y + 140, 
            window=restart_button
        )
    
    def hide_game_over(self):
        """Cache l'écran de fin de partie"""
        self.game_over_canvas.place_forget()
