import random
import copy

class GrilleSudoku:
    """Classe représentant la grille de Sudoku"""
    
    def __init__(self):
        self.grille = [[0 for _ in range(9)] for _ in range(9)]
        self.grille_originale = [[0 for _ in range(9)] for _ in range(9)]
        
    def charger_depuis_fichier(self, niveau):
        """Charge une grille depuis un fichier texte selon le niveau"""
        fichiers = {
            'facile': 'grilles/facile.txt',
            'intermediaire': 'grilles/intermediaire.txt',
            'difficile': 'grilles/difficile.txt'
        }
        
        try:
            with open(fichiers[niveau], 'r') as f:
                for i in range(9):
                    ligne = f.readline().strip()
                    for j, char in enumerate(ligne.split()):
                        val = int(char)
                        self.grille[i][j] = val
                        self.grille_originale[i][j] = val
            return True
        except FileNotFoundError:
            
            self.generer_grille_test(niveau)
            return True
        except Exception as e:
            print(f"Erreur lors du chargement: {e}")
            return False
    
    def generer_grille_test(self, niveau):
        if niveau == 'facile':
            # Grille facile de test
            grille_test = [
                [5, 3, 0, 0, 7, 0, 0, 0, 0],
                [6, 0, 0, 1, 9, 5, 0, 0, 0],
                [0, 9, 8, 0, 0, 0, 0, 6, 0],
                [8, 0, 0, 0, 6, 0, 0, 0, 3],
                [4, 0, 0, 8, 0, 3, 0, 0, 1],
                [7, 0, 0, 0, 2, 0, 0, 0, 6],
                [0, 6, 0, 0, 0, 0, 2, 8, 0],
                [0, 0, 0, 4, 1, 9, 0, 0, 5],
                [0, 0, 0, 0, 8, 0, 0, 7, 9]
            ]
        elif niveau == 'intermediaire':
            grille_test = [
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 3, 0, 8, 5],
                [0, 0, 1, 0, 2, 0, 0, 0, 0],
                [0, 0, 0, 5, 0, 7, 0, 0, 0],
                [0, 0, 4, 0, 0, 0, 1, 0, 0],
                [0, 9, 0, 0, 0, 0, 0, 0, 0],
                [5, 0, 0, 0, 0, 0, 0, 7, 3],
                [0, 0, 2, 0, 1, 0, 0, 0, 0],
                [0, 0, 0, 0, 4, 0, 0, 0, 9]
            ]
        else:  # difficile
            grille_test = [
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 5, 0, 7, 0, 0, 0],
                [0, 0, 4, 0, 0, 0, 1, 0, 0],
                [0, 9, 0, 0, 0, 0, 0, 0, 0],
                [5, 0, 0, 0, 0, 0, 0, 7, 3],
                [0, 0, 2, 0, 1, 0, 0, 0, 0],
                [0, 0, 0, 0, 4, 0, 0, 0, 9]
            ]
        
        for i in range(9):
            for j in range(9):
                self.grille[i][j] = grille_test[i][j]
                self.grille_originale[i][j] = grille_test[i][j]
    
    def est_valide(self, ligne, col, valeur):
        if valeur == 0:
            return True
        
        # Vérifier la ligne
        for j in range(9):
            if self.grille[ligne][j] == valeur and j != col:
                return False
        
        # Vérifier colonne
        for i in range(9):
            if self.grille[i][col] == valeur and i != ligne:
                return False
        
        # Vérifier le carré 3x3
        debut_ligne = (ligne // 3) * 3
        debut_col = (col // 3) * 3
        for i in range(debut_ligne, debut_ligne + 3):
            for j in range(debut_col, debut_col + 3):
                if self.grille[i][j] == valeur and (i != ligne or j != col):
                    return False
        
        return True
    
    def est_complete(self):
        """Vérifie si la grille est complète"""
        for i in range(9):
            for j in range(9):
                if self.grille[i][j] == 0:
                    return False
        return True
    
    def placer_valeur(self, ligne, col, valeur, est_ia=False):
        if not est_ia and self.grille_originale[ligne][col] != 0:
            return False, "Cette case est déjà remplie initialement!"
        
        if valeur < 1 or valeur > 9:
            return False, "La valeur doit être entre 1 et 9"
        
        if self.est_valide(ligne, col, valeur):
            self.grille[ligne][col] = valeur
            return True, "Placement réussi!"
        else:
            return False, "Placement invalide!"
    
    def supprimer_valeur(self, ligne, col):
        if self.grille_originale[ligne][col] != 0:
            return False, "Impossible de supprimer une case initiale!"
        
        if self.grille[ligne][col] == 0:
            return False, "Cette case est déjà vide!"
        
        self.grille[ligne][col] = 0
        return True, "Valeur supprimée!"
    
    def afficher(self):
        print("\n     A  B  C   D  E  F   G  H  I")
        print("   -------------------------------")
        
        for i in range(9):
            print(f"{i+1:2} |", end=" ")
            for j in range(9):
                if self.grille[i][j] == 0:
                    print(".", end=" ")
                else:
                    print(self.grille[i][j], end=" ")
                if (j + 1) % 3 == 0 and j < 8:
                    print("|", end=" ")
                elif j < 8:
                    print("", end=" ")
            print("|")
            if (i + 1) % 3 == 0 and i < 8:
                print("   -------------------------------")
        
        print("   -------------------------------")
    
    def sauvegarder(self, nom_fichier):
        import json
        data = {
            'grille': self.grille,
            'grille_originale': self.grille_originale
        }
        with open(nom_fichier, 'w') as f:
            json.dump(data, f)
    
    def charger_sauvegarde(self, nom_fichier):
        import json
        try:
            with open(nom_fichier, 'r') as f:
                data = json.load(f)
                self.grille = data['grille']
                self.grille_originale = data['grille_originale']
            return True
        except:
            return False
    
    def obtenir_cases_vides(self):
        vides = []
        for i in range(9):
            for j in range(9):
                if self.grille[i][j] == 0:
                    vides.append((i, j))
        return vides