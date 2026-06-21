from game import Partie
from player import Joueur
from ia_player import IA_Joueur
import os

class Menu:
    """Classe gérant l'affichage des menus"""
    
    def __init__(self, score_manager):
        self.score_manager = score_manager
        self.joueur_actuel = None
    
    def afficher(self):
        """Affiche le menu principal"""
        while True:
            print("\n" + "="*50)
            print("              SUDOKU GAME")
            print("="*50)
            print("\n1. Nouvelle partie")
            print("2. Credits")
            print("3. Scores")
            print("4. Regles du jeu")
            print("5. Quitter")
            print("="*50)
            
            choix = input("\nVotre choix (1-5): ").strip()
            
            if choix == '1':
                self.nouvelle_partie()
            elif choix == '2':
                self.afficher_credits()
            elif choix == '3':
                self.score_manager.afficher_scores()
            elif choix == '4':
                self.afficher_regles()
            elif choix == '5':
                print("\nMerci d'avoir joue! A bientot!")
                break
            else:
                print("\nChoix invalide!")
  
    
    def nouvelle_partie(self):
        """Cree une nouvelle partie"""
        if not self.joueur_actuel:
            nom = input("\nEntrez votre nom: ").strip()
            if not nom:
                nom = "Joueur"
            self.joueur_actuel = Joueur(nom)
        
        print("\n--- Choisissez le niveau ---")
        print("1. Facile (+2 points)")
        print("2. Intermediaire (+4 points)")
        print("3. Difficile (+8 points)")
        
        choix_niveau = input("\nVotre choix (1-3): ").strip()
        
        niveaux = {'1': 'facile', '2': 'intermediaire', '3': 'difficile'}
        if choix_niveau not in niveaux:
            print("Niveau invalide!")
            return
        
        niveau = niveaux[choix_niveau]
        
        print("\n--- Choisissez le mode de jeu ---")
        print("1. Joueur humain")
        print("2. IA Joueur")
        
        choix_mode = input("\nVotre choix (1-2): ").strip()
        mode_ia = (choix_mode == '2')
        
        if mode_ia:
            ia_joueur = IA_Joueur(f"{self.joueur_actuel.nom}_IA")
            ia_joueur.score_total = self.joueur_actuel.score_total
            joueur = ia_joueur
        else:
            joueur = self.joueur_actuel
        
        partie = Partie(joueur, niveau, mode_ia)
        resultat = partie.demarrer()
        
        if mode_ia:
            self.joueur_actuel.score_total = joueur.score_total
        
        if resultat:
            self.score_manager.sauvegarder_score(self.joueur_actuel.nom, 
                                                 self.joueur_actuel.score_total)
        
        input("\nAppuyez sur Entree pour continuer...")
    
    def afficher_credits(self):
        """Affiche les credits"""
        print("\n" + "="*50)
        print("              CREDITS")
        print("="*50)
        print("\nDeveloppeur: Etudiant en Informatique")
        print("Projet: Semestre 2 - 2025/2026")
        print("Langage: Python 3")
        print("Bibliotheques: Matplotlib pour les graphiques")
        print("\nMerci d'avoir joue!")
        input("\nAppuyez sur Entree pour continuer...")
    
    def afficher_regles(self):
        """Affiche les regles du jeu"""
        print("\n" + "="*50)
        print("           REGLES DU SUDOKU")
        print("="*50)
        print("""
Le Sudoku se joue sur une grille de 9x9 cases.

Objectif: Remplir la grille avec les chiffres de 1 a 9.

Contraintes:
- Chaque ligne doit contenir les chiffres 1 a 9 sans repetition
- Chaque colonne doit contenir les chiffres 1 a 9 sans repetition
- Chaque carre 3x3 doit contenir les chiffres 1 a 9 sans repetition

Commandes:
- Pour placer un nombre: 'ligne colonne valeur' (ex: '3 C 5')
- Pour supprimer: 'C ligne colonne' (ex: 'C 3 C')
- Pause: 'P'
- Interruption: 'I'

Scores:
- Facile: Victoire +2 points / Interruption -1 point
- Intermediaire: Victoire +4 points / Interruption -2 points
- Difficile: Victoire +8 points / Interruption -3 points

Astuces:
- Les cases avec des chiffres au depart ne peuvent pas etre modifiees
- Vous pouvez supprimer uniquement les cases que vous avez placees
        """)
        input("\nAppuyez sur Entree pour continuer...")