import random

class IA_Joueur:
    """Classe représentant l'IA qui joue au Sudoku"""
    
    def __init__(self, nom="IA_Joueur"):
        self.nom = nom
        self.score_total = 0
    
    def trouver_valeurs_possibles(self, grille, ligne, col):
        """Trouve toutes les valeurs possibles pour une case"""
        possibles = []
        for val in range(1, 10):
            if grille.est_valide(ligne, col, val):
                possibles.append(val)
        return possibles
    
    def choisir_meilleure_case(self, grille):
        """Choisit la case avec le moins de possibilités (stratégie MRV)"""
        cases_vides = grille.obtenir_cases_vides()
        if not cases_vides:
            return None
        
        meilleure_case = None
        min_possibilites = 10
        
        for ligne, col in cases_vides:
            possibles = self.trouver_valeurs_possibles(grille, ligne, col)
            if len(possibles) < min_possibilites:
                min_possibilites = len(possibles)
                meilleure_case = (ligne, col, possibles)
                if min_possibilites == 1:
                    break
        
        return meilleure_case
    
    def jouer_tour(self, grille):
        """L'IA joue un tour - place un nombre valide"""
        case_info = self.choisir_meilleure_case(grille)
        
        if not case_info:
            return 'complet', None, None, None
        
        ligne, col, possibles = case_info
        
        if possibles:
            valeur = possibles[0]  # Choisir la première valeur possible
            print(f"\n🤖 IA_Joueur place {valeur} à la position {ligne+1} {chr(65+col)}")
            return 'placer', ligne, col, valeur
        else:
            # Aucune valeur possible - situation bloquée
            return 'bloque', None, None, None
    
    def resoudre_completement(self, grille):
        """Résout complètement la grille (pour tester)"""
        # Implémentation d'un solveur de Sudoku complet
        def backtrack():
            cases_vides = grille.obtenir_cases_vides()
            if not cases_vides:
                return True
            
            ligne, col = cases_vides[0]
            for val in range(1, 10):
                if grille.est_valide(ligne, col, val):
                    grille.grille[ligne][col] = val
                    if backtrack():
                        return True
                    grille.grille[ligne][col] = 0
            return False
        
        # Créer une copie de la grille originale pour ne pas modifier les cases fixes
        grille_copie = grille.grille.copy()
        resultat = backtrack()
        return resultat
    
    def ajouter_score(self, points):
        """Ajoute des points au score total"""
        self.score_total += points