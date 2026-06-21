from grid import GrilleSudoku
from player import Joueur
from ia_player import IA_Joueur
import os
import json

class Partie:
    """Classe gérant le déroulement d'une partie"""
    
    def __init__(self, joueur, niveau, mode_ia=False):
        self.joueur = joueur
        self.niveau = niveau
        self.mode_ia = mode_ia
        self.grille = GrilleSudoku()
        self.partie_active = True
        self.score_points = 0
        
        # Définir les points selon le niveau
        self.points_victoire = {'facile': 2, 'intermediaire': 4, 'difficile': 8}
        self.points_interruption = {'facile': -1, 'intermediaire': -2, 'difficile': -3}
    
    def demarrer(self):
        """Démarre la partie"""
        print(f"\n=== Nouvelle partie ===")
        print(f"Joueur: {self.joueur.nom}")
        print(f"Niveau: {self.niveau}")
        print(f"Mode: {'IA Joueur' if self.mode_ia else 'Joueur Humain'}")
        
        # Charger la grille
        if not self.grille.charger_depuis_fichier(self.niveau):
            print("Erreur lors du chargement de la grille!")
            return False
        
        # Vérifier s'il y a une partie sauvegardée
        if os.path.exists('sauvegarde/savegame.json'):
            reponse = input("Une partie sauvegardée existe. Voulez-vous la charger? (o/n): ")
            if reponse.lower() == 'o':
                self.charger_partie()
        
        return self.boucle_de_jeu()
    
    def boucle_de_jeu(self):
        """Boucle principale du jeu"""
        while self.partie_active:
            # Afficher l'état du jeu
            print(f"\n🎮 Joueur: {self.joueur.nom} | Score: {self.joueur.score_total}")
            self.grille.afficher()
            
            # Vérifier si la grille est complète
            if self.grille.est_complete():
                return self.fin_partie('victoire')
            
            # Jouer un tour
            if self.mode_ia and isinstance(self.joueur, IA_Joueur):
                action, ligne, col, valeur = self.joueur.jouer_tour(self.grille)
            else:
                action, ligne, col, valeur = self.joueur.jouer_tour(self.grille)
            
            # Traiter l'action
            if action == 'placer':
                success, message = self.grille.placer_valeur(ligne, col, valeur, self.mode_ia)
                print(f"\n{message}")
                
            elif action == 'supprimer':
                success, message = self.grille.supprimer_valeur(ligne, col)
                print(f"\n{message}")
                
            elif action == 'pause':
                return self.pause_partie()
                
            elif action == 'interruption':
                return self.fin_partie('interruption')
                
            elif action == 'bloque':
                print("\n❌ L'IA est bloquée! Impossible de continuer.")
                return self.fin_partie('interruption')
        
        return False
    
    def pause_partie(self):
        """Met la partie en pause et la sauvegarde"""
        print("\n Partie mise en pause et sauvegardée...")
        self.sauvegarder_partie()
        print("Vous pourrez reprendre cette partie plus tard.")
        return False
    
    def sauvegarder_partie(self):
        """Sauvegarde la partie en cours"""
        if not os.path.exists('sauvegarde'):
            os.makedirs('sauvegarde')
        
        sauvegarde = {
            'joueur_nom': self.joueur.nom,
            'joueur_score': self.joueur.score_total,
            'niveau': self.niveau,
            'mode_ia': self.mode_ia,
            'grille': self.grille.grille,
            'grille_originale': self.grille.grille_originale
        }
        
        with open('sauvegarde/savegame.json', 'w') as f:
            json.dump(sauvegarde, f)
    
    def charger_partie(self):
        """Charge une partie sauvegardée"""
        try:
            with open('sauvegarde/savegame.json', 'r') as f:
                sauvegarde = json.load(f)
                
            self.joueur.nom = sauvegarde['joueur_nom']
            self.joueur.score_total = sauvegarde['joueur_score']
            self.niveau = sauvegarde['niveau']
            self.mode_ia = sauvegarde['mode_ia']
            self.grille.grille = sauvegarde['grille']
            self.grille.grille_originale = sauvegarde['grille_originale']
            
            print("Partie chargée avec succès!")
            
        except Exception as e:
            print(f"Erreur lors du chargement: {e}")
    
    def fin_partie(self, type_fin):
        """Gère la fin de partie"""
        if type_fin == 'victoire':
            points = self.points_victoire[self.niveau]
            print(f"\n FÉLICITATIONS! Vous avez complété la grille!")
            print(f" Vous gagnez {points} points!")
            
        else:  # interruption
            points = self.points_interruption[self.niveau]
            print(f"\n Partie interrompue!")
            print(f" Vous perdez {abs(points)} points!")
        
        # Mettre à jour le score
        self.joueur.ajouter_score(points)
        print(f" Nouveau score total: {self.joueur.score_total}")
        
        # Supprimer la sauvegarde si elle existe
        if os.path.exists('sauvegarde/savegame.json'):
            os.remove('sauvegarde/savegame.json')
        
        return True