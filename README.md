# 🎮 Tetris à Deux Joueurs (Humain vs IA) 🤖

## 🌟 Présentation

Bienvenue dans le **Tetris à Deux Joueurs** ! Une version moderne et fun du célèbre jeu Tetris où vous affrontez une intelligence artificielle pour déterminer qui est le meilleur empileur de blocs !

Ce jeu combine le gameplay classique de Tetris avec des règles amusantes pour rendre l'expérience encore plus captivante !

## ✨ Fonctionnalités

- 🎲 **Deux joueurs simultanés** : Vous contre l'IA !
- 🎯 **Interface graphique** avec Tkinter
- 📊 **Système de score** détaillé et en temps réel
- 🧠 **IA** avec algorithme d'optimisation
- 🎁 **Règles spéciales** pour pimenter le jeu

## 🚀 Installation

### Prérequis

- Python 3.6 ou supérieur
- Tkinter (généralement inclus avec Python)

### Étapes d'installation

1. Clonez ce dépôt :

git clone https://github.com/mistwil777/tetris-vs-ia.git

cd tetris-vs-ia


2. Aucune dépendance supplémentaire n'est nécessaire !

3. Lancez le jeu :

python src/main.py


## 🎮 Comment jouer

### Contrôles

- ⬅️ **Flèche gauche** : Déplacer la pièce à gauche
- ➡️ **Flèche droite** : Déplacer la pièce à droite
- ⬇️ **Flèche bas** : Accélérer la chute
- ⬆️ **Flèche haut** : Faire pivoter la pièce
- **Espace** : Faire chuter la pièce instantanément
- **P** : Mettre le jeu en pause
- **R** : Recommencer une partie

### Objectif

Comme dans le Tetris classique, l'objectif est de compléter des lignes pour marquer des points. Mais attention, votre adversaire IA fait de même ! Le premier joueur dont la grille est remplie jusqu'en haut perd la partie.

## 🌈 Règles spéciales

Ce Tetris a 4 règles originales qui rendent le jeu encore plus fun :

### 🎁 Cadeau surprise

Quand un joueur complète 2 lignes d'un coup, l'adversaire reçoit une "pièce facile" (carrée ou en ligne) pour l'aider un peu. Un petit coup de pouce qui peut sauver la partie !

### ⏱️ Pause douceur

Tous les 1000 points, les pièces tombent 20% plus lentement pendant 10 secondes pour les deux joueurs. Un petit moment de répit pour souffler et réorganiser votre stratégie !

### 💖 Pièce rigolote

Tous les 3000 points, une pièce spéciale en forme de cœur ou d'étoile apparaît, valant 100 points bonus si elle est bien placée. Ces pièces apportent non seulement des points mais aussi un peu de fantaisie au jeu !

### 🌈 Arc-en-ciel

Toutes les 2 minutes, les pièces changent de couleur pendant 20 secondes. C'est purement esthétique, mais cela rend le jeu encore plus beau et dynamique !

## 🏆 Système de score

- **50 points** par ligne complétée
- **Bonus de 100 points** pour 2 lignes simultanées
- **Bonus de 200 points** pour 3 lignes simultanées
- **Bonus de 300 points** pour un Tetris (4 lignes)

## 🧠 L'IA

L'intelligence artificielle utilise un algorithme qui évalue plusieurs facteurs pour déterminer le meilleur placement pour chaque pièce :

- Hauteur cumulée du plateau
- Nombre de trous
- Régularité de la surface
- Lignes potentiellement complétées

## 👨‍💻 Structure du projet

tetris_vs_ia/
├── assets/ # Ressources graphiques
├── src/ # Code source
│ ├── init.py # Initialise le package
│ ├── main.py # Point d'entrée
│ ├── game.py # Logique principale du jeu
│ ├── board.py # Classe du plateau de jeu
│ ├── pieces.py # Classes des pièces
│ ├── ai.py # Intelligence artificielle
│ ├── ui.py # Interface utilisateur
│ └── utils.py # Fonctions utilitaires
├── README.md # Ce fichier
└── PROMPTS.md # Documentation des prompts utilisés


## 🌟 À propos

Ce projet a été réalisé dans le cadre d'un cours sur l'utilisation de l'IA générative. Tous les composants ont été créés avec l'aide d'outils d'IA.

## 🔄 Améliorations futures

- 🎵 Ajout d'effets sonores et de musique
- 🏆 Tableau des meilleurs scores
- 🌍 Mode multijoueur en réseau
- 📱 Version mobile tactile

## 📝 Licence

Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.

---

⭐ **Amusez-vous bien et que le meilleur empileur gagne !** ⭐
