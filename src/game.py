#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Classe principale du jeu Tetris à deux joueurs
Gère la logique du jeu et coordonne les interactions entre les composants
"""

import time
import random
import tkinter as tk
from src.board import Board
from src.pieces import get_random_piece, PieceType
from src.ai import AI
from src.ui import UI

class Game:
    """Classe principale qui gère le déroulement du jeu"""
    
    def __init__(self):
        """Initialise une nouvelle partie de Tetris"""
        self.root = tk.Tk()
        self.root.title("Tetris à deux joueurs (Humain vs IA)")
        self.root.configure(bg="#f0f0f0")
        
        # Initialisation des plateaux de jeu
        self.human_board = Board(width=10, height=20)
        self.ai_board = Board(width=10, height=20)
        
        # Initialisation de l'IA
        self.ai = AI(self.ai_board)
        
        # Initialisation de l'interface utilisateur
        self.ui = UI(self.root, self)
        
        # Variables de jeu
        self.human_score = 0
        self.ai_score = 0
        self.human_current_piece = None
        self.human_next_piece = None
        self.ai_current_piece = None
        self.ai_next_piece = None
        self.game_speed = 500  # Vitesse de chute des pièces en ms
        self.game_running = False
        self.rainbow_mode = False
        self.pause_douceur_active = {"human": False, "ai": False}
        self.pause_douceur_end_time = {"human": 0, "ai": 0}
        
        # Timers pour les règles spéciales
        self.last_rainbow_time = time.time()
        self.rainbow_end_time = 0
        
        # Configuration des événements clavier
        self.setup_keyboard_events()
    
    def setup_keyboard_events(self):
        """Configure les événements clavier pour le joueur humain"""
        self.root.bind("<Left>", lambda event: self.move_human_piece(-1, 0))
        self.root.bind("<Right>", lambda event: self.move_human_piece(1, 0))
        self.root.bind("<Down>", lambda event: self.move_human_piece(0, 1))
        self.root.bind("<Up>", lambda event: self.rotate_human_piece())
        self.root.bind("<space>", lambda event: self.hard_drop_human_piece())
        self.root.bind("p", lambda event: self.toggle_pause())
        self.root.bind("r", lambda event: self.restart_game())
    
    def start(self):
        """Démarre le jeu"""
        self.game_running = True
        self.human_current_piece = get_random_piece()
        self.human_next_piece = get_random_piece()
        self.ai_current_piece = get_random_piece()
        self.ai_next_piece = get_random_piece()
        
        # Démarrage des boucles de jeu
        self.update_game()
        self.run_ai_turn()
        
        # Démarrage de la boucle principale Tkinter
        self.root.mainloop()
    
    def update_game(self):
        """Met à jour l'état du jeu à chaque tick"""
        if not self.game_running:
            return
        
        # Vérifie les règles spéciales
        self.check_special_rules()
        
        # Fait tomber la pièce du joueur humain
        if not self.move_human_piece(0, 1):
            self.lock_human_piece()
        
        # Met à jour l'affichage
        self.ui.update_display()
        
        # Programme le prochain tick
        speed = self.get_current_speed("human")
        self.root.after(speed, self.update_game)
    
    def run_ai_turn(self):
        """Exécute le tour de l'IA"""
        if not self.game_running:
            return
        
        # L'IA prend sa décision
        move = self.ai.get_best_move(self.ai_current_piece)
        
        # Applique le mouvement
        if move:
            self.ai_current_piece.x = move["x"]
            self.ai_current_piece.rotation = move["rotation"]
            
            # Fait tomber la pièce de l'IA
            if not self.move_ai_piece(0, 1):
                self.lock_ai_piece()
        else:
            # Si aucun mouvement valide n'est trouvé, on fait tomber la pièce
            if not self.move_ai_piece(0, 1):
                self.lock_ai_piece()
        
        # Met à jour l'affichage
        self.ui.update_display()
        
        # Programme le prochain tour de l'IA
        speed = self.get_current_speed("ai")
        self.root.after(speed, self.run_ai_turn)
    
    def get_current_speed(self, player):
        """Retourne la vitesse actuelle du jeu pour un joueur donné"""
        speed = self.game_speed
        
        # Ralentissement si "Pause douceur" est active
        if self.pause_douceur_active[player]:
            speed = int(speed * 1.2)  # 20% plus lent
            
            # Vérifie si la pause douceur est terminée
            if time.time() > self.pause_douceur_end_time[player]:
                self.pause_douceur_active[player] = False
        
        return speed
    
    def move_human_piece(self, dx, dy):
        """Déplace la pièce du joueur humain"""
        if not self.game_running or not self.human_current_piece:
            return False
        
        # Sauvegarde la position actuelle
        old_x, old_y = self.human_current_piece.x, self.human_current_piece.y
        
        # Essaye de déplacer la pièce
        self.human_current_piece.x += dx
        self.human_current_piece.y += dy
        
        # Vérifie si le mouvement est valide
        if not self.human_board.is_valid_position(self.human_current_piece):
            # Restaure la position si le mouvement est invalide
            self.human_current_piece.x, self.human_current_piece.y = old_x, old_y
            return False
        
        return True
    
    def move_ai_piece(self, dx, dy):
        """Déplace la pièce de l'IA"""
        if not self.game_running or not self.ai_current_piece:
            return False
        
        # Sauvegarde la position actuelle
        old_x, old_y = self.ai_current_piece.x, self.ai_current_piece.y
        
        # Essaye de déplacer la pièce
        self.ai_current_piece.x += dx
        self.ai_current_piece.y += dy
        
        # Vérifie si le mouvement est valide
        if not self.ai_board.is_valid_position(self.ai_current_piece):
            # Restaure la position si le mouvement est invalide
            self.ai_current_piece.x, self.ai_current_piece.y = old_x, old_y
            return False
        
        return True
    
    def rotate_human_piece(self):
        """Fait pivoter la pièce du joueur humain"""
        if not self.game_running or not self.human_current_piece:
            return False
        
        # Sauvegarde la rotation actuelle
        old_rotation = self.human_current_piece.rotation
        
        # Essaye de faire pivoter la pièce
        self.human_current_piece.rotate()
        
        # Vérifie si la rotation est valide
        if not self.human_board.is_valid_position(self.human_current_piece):
            # Restaure la rotation si elle est invalide
            self.human_current_piece.rotation = old_rotation
            return False
        
        return True
    
    def hard_drop_human_piece(self):
        """Fait tomber instantanément la pièce du joueur humain"""
        if not self.game_running or not self.human_current_piece:
            return
        
        # Fait tomber la pièce jusqu'à ce qu'elle ne puisse plus descendre
        while self.move_human_piece(0, 1):
            pass
        
        # Verrouille la pièce
        self.lock_human_piece()
    
    def lock_human_piece(self):
        """Verrouille la pièce du joueur humain sur le plateau"""
        if not self.human_current_piece:
            return
        
        # Ajoute la pièce au plateau
        cleared_lines = self.human_board.add_piece(self.human_current_piece)
        
        # Met à jour le score
        self.update_score("human", cleared_lines)
        
        # Vérifie les règles spéciales
        self.check_gift_rule("human", cleared_lines)
        
        # Passe à la pièce suivante
        self.human_current_piece = self.human_next_piece
        self.human_next_piece = get_random_piece()
        
        # Vérifie si la partie est terminée
        if not self.human_board.is_valid_position(self.human_current_piece):
            self.game_over("ai")
    
    def lock_ai_piece(self):
        """Verrouille la pièce de l'IA sur le plateau"""
        if not self.ai_current_piece:
            return
        
        # Ajoute la pièce au plateau
        cleared_lines = self.ai_board.add_piece(self.ai_current_piece)
        
        # Met à jour le score
        self.update_score("ai", cleared_lines)
        
        # Vérifie les règles spéciales
        self.check_gift_rule("ai", cleared_lines)
        
        # Passe à la pièce suivante
        self.ai_current_piece = self.ai_next_piece
        self.ai_next_piece = get_random_piece()
        
        # Vérifie si la partie est terminée
        if not self.ai_board.is_valid_position(self.ai_current_piece):
            self.game_over("human")
    
    def update_score(self, player, cleared_lines):
        """Met à jour le score d'un joueur en fonction des lignes effacées"""
        if player == "human":
            # Score de base
            if cleared_lines == 1:
                self.human_score += 50
            elif cleared_lines == 2:
                self.human_score += 150  # 50*2 + 50 (bonus)
            elif cleared_lines == 3:
                self.human_score += 350  # 50*3 + 200 (bonus)
            elif cleared_lines == 4:
                self.human_score += 500  # 50*4 + 300 (bonus)
            
            # Vérifie si on active la "Pause douceur"
            if self.human_score // 1000 > (self.human_score - self.calculate_score(cleared_lines)) // 1000:
                self.activate_pause_douceur("human")
                self.activate_pause_douceur("ai")
            
            # Vérifie si on active la "Pièce rigolote"
            if self.human_score // 3000 > (self.human_score - self.calculate_score(cleared_lines)) // 3000:
                self.activate_funny_piece("human")
        else:
            # Score de base
            if cleared_lines == 1:
                self.ai_score += 50
            elif cleared_lines == 2:
                self.ai_score += 150  # 50*2 + 50 (bonus)
            elif cleared_lines == 3:
                self.ai_score += 350  # 50*3 + 200 (bonus)
            elif cleared_lines == 4:
                self.ai_score += 500  # 50*4 + 300 (bonus)
            
            # Vérifie si on active la "Pause douceur"
            if self.ai_score // 1000 > (self.ai_score - self.calculate_score(cleared_lines)) // 1000:
                self.activate_pause_douceur("ai")
                self.activate_pause_douceur("human")
            
            # Vérifie si on active la "Pièce rigolote"
            if self.ai_score // 3000 > (self.ai_score - self.calculate_score(cleared_lines)) // 3000:
                self.activate_funny_piece("ai")
    
    def calculate_score(self, cleared_lines):
        """Calcule le score en fonction du nombre de lignes effacées"""
        if cleared_lines == 1:
            return 50
        elif cleared_lines == 2:
            return 150
        elif cleared_lines == 3:
            return 350
        elif cleared_lines == 4:
            return 500
        return 0
    
    def check_gift_rule(self, player, cleared_lines):
        """Vérifie et applique la règle "Cadeau surprise" si nécessaire"""
        if cleared_lines == 2:
            # Détermine quel joueur reçoit le cadeau
            recipient = "ai" if player == "human" else "human"
            
            # Crée une pièce facile (carré ou ligne)
            easy_piece = get_random_piece(only_easy=True)
            
            # Remplace la prochaine pièce du joueur qui reçoit le cadeau
            if recipient == "human":
                self.human_next_piece = easy_piece
            else:
                self.ai_next_piece = easy_piece
    
    def activate_pause_douceur(self, player):
        """Active la règle "Pause douceur" pour un joueur"""
        self.pause_douceur_active[player] = True
        self.pause_douceur_end_time[player] = time.time() + 10  # Dure 10 secondes
    
    def activate_funny_piece(self, player):
        """Active la règle "Pièce rigolote" pour un joueur"""
        # Crée une pièce spéciale (cœur ou étoile)
        special_piece = get_random_piece(special=True)
        
        # Remplace la prochaine pièce du joueur
        if player == "human":
            self.human_next_piece = special_piece
        else:
            self.ai_next_piece = special_piece
    
    def check_special_rules(self):
        """Vérifie et applique les règles spéciales basées sur le temps"""
        current_time = time.time()
        
        # Vérifie la règle "Arc-en-ciel"
        if current_time - self.last_rainbow_time >= 120:  # 2 minutes
            self.activate_rainbow_mode()
            self.last_rainbow_time = current_time
        
        # Désactive le mode arc-en-ciel si nécessaire
        if self.rainbow_mode and current_time > self.rainbow_end_time:
            self.rainbow_mode = False
    
    def activate_rainbow_mode(self):
        """Active la règle "Arc-en-ciel" pour les deux joueurs"""
        self.rainbow_mode = True
        self.rainbow_end_time = time.time() + 20  # Dure 20 secondes
    
    def toggle_pause(self):
        """Met le jeu en pause ou le reprend"""
        self.game_running = not self.game_running
        
        if self.game_running:
            # Reprendre le jeu
            self.update_game()
            self.run_ai_turn()
    
    def restart_game(self):
        """Redémarre le jeu"""
        # Réinitialise les plateaux
        self.human_board = Board(width=10, height=20)
        self.ai_board = Board(width=10, height=20)
        
        # Réinitialise les scores
        self.human_score = 0
        self.ai_score = 0
        
        # Réinitialise les pièces
        self.human_current_piece = get_random_piece()
        self.human_next_piece = get_random_piece()
        self.ai_current_piece = get_random_piece()
        self.ai_next_piece = get_random_piece()
        
        # Réinitialise les règles spéciales
        self.rainbow_mode = False
        self.pause_douceur_active = {"human": False, "ai": False}
        self.last_rainbow_time = time.time()
        
        # Reprend le jeu
        self.game_running = True
        self.update_game()
        self.run_ai_turn()
    
    def game_over(self, winner):
        """Termine la partie et affiche le gagnant"""
        self.game_running = False
        self.ui.show_game_over(winner)
