#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Fonctions utilitaires pour le jeu Tetris
"""

import random
import time

def get_random_color():
    """Génère une couleur aléatoire au format hexadécimal
    
    Returns:
        str: Code couleur au format hexadécimal
    """
    r = random.randint(100, 255)
    g = random.randint(100, 255)
    b = random.randint(100, 255)
    return f"#{r:02x}{g:02x}{b:02x}"

def hsv_to_rgb(h, s, v):
    """Convertit une couleur HSV en RGB
    
    Args:
        h: Teinte (0-360)
        s: Saturation (0-1)
        v: Valeur (0-1)
    
    Returns:
        tuple: Triplet (r, g, b) avec des valeurs entre 0 et 255
    """
    h = h % 360
    c = v * s
    x = c * (1 - abs((h / 60) % 2 - 1))
    m = v - c
    
    if h < 60:
        r, g, b = c, x, 0
    elif h < 120:
        r, g, b = x, c, 0
    elif h < 180:
        r, g, b = 0, c, x
    elif h < 240:
        r, g, b = 0, x, c
    elif h < 300:
        r, g, b = x, 0, c
    else:
        r, g, b = c, 0, x
    
    r = int((r + m) * 255)
    g = int((g + m) * 255)
    b = int((b + m) * 255)
    
    return r, g, b

def get_rainbow_colors(time_offset=0):
    """Génère des couleurs arc-en-ciel en fonction du temps
    
    Args:
        time_offset: Décalage temporel en secondes
    
    Returns:
        list: Liste de codes couleur au format hexadécimal
    """
    colors = []
    t = time.time() + time_offset
    for i in range(7):
        hue = (t * 50 + i * 50) % 360
        r, g, b = hsv_to_rgb(hue, 0.8, 0.9)
        colors.append(f"#{r:02x}{g:02x}{b:02x}")
    
    return colors

def format_time(seconds):
    """Formate un temps en secondes en une chaîne lisible
    
    Args:
        seconds: Temps en secondes
    
    Returns:
        str: Temps formaté (mm:ss)
    """
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes:02d}:{seconds:02d}"

def create_heart_shape():
    """Crée une pièce en forme de cœur
    
    Returns:
        list: Forme de la pièce
    """
    return [
        [0, 1, 0, 1, 0],
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1],
        [0, 1, 1, 1, 0],
        [0, 0, 1, 0, 0]
    ]

def create_star_shape():
    """Crée une pièce en forme d'étoile
    
    Returns:
        list: Forme de la pièce
    """
    return [
        [0, 0, 1, 0, 0],
        [0, 1, 1, 1, 0],
        [1, 1, 1, 1, 1],
        [0, 1, 1, 1, 0],
        [0, 0, 1, 0, 0]
    ]
