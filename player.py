class Joueur:
    """Classe représentant un joueur humain"""
    
    def __init__(self, nom):
        self.nom = nom
        self.score_total = 0
        
    def convertir_lettre_colonne(self, lettre):
        """Convertit une lettre (A-I) en indice de colonne (0-8)"""
        colonnes = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 
                   'F': 5, 'G': 6, 'H': 7, 'I': 8}
        return colonnes.get(lettre.upper(), -1)
    
    def jouer_tour(self, grille):
        """Permet au joueur de jouer un tour"""
        while True:
            print("\nQue voulez-vous faire?")
            print("  - Entrez 'ligne colonne valeur' (ex: '3 C 5') pour placer un nombre")
            print("  - Entrez 'C ligne colonne' pour supprimer (ex: 'C 3 C')")
            print("  - Entrez 'P' pour faire une pause")
            print("  - Entrez 'I' pour interrompre la partie")
            
            commande = input("\nVotre choix: ").strip().split()
            
            if not commande:
                print("Commande invalide!")
                continue
            
            if commande[0].upper() == 'P':
                return 'pause', None, None, None
            
            if commande[0].upper() == 'I':
                return 'interruption', None, None, None
            
            if commande[0].upper() == 'C':
                if len(commande) != 3:
                    print("Format: C ligne colonne")
                    continue
                try:
                    ligne = int(commande[1]) - 1
                    colonne = self.convertir_lettre_colonne(commande[2])
                    if 0 <= ligne < 9 and 0 <= colonne < 9:
                        return 'supprimer', ligne, colonne, None
                    else:
                        print("Coordonnées invalides!")
                except ValueError:
                    print("Ligne invalide!")
                continue
            
            if len(commande) == 3:
                try:
                    ligne = int(commande[0]) - 1
                    colonne = self.convertir_lettre_colonne(commande[1])
                    valeur = int(commande[2])
                    
                    if 0 <= ligne < 9 and 0 <= colonne < 9 and 1 <= valeur <= 9:
                        return 'placer', ligne, colonne, valeur
                    else:
                        print("Valeurs invalides! Ligne: 1-9, Colonne: A-I, Valeur: 1-9")
                except ValueError:
                    print("Format invalide!")
            else:
                print("Format invalide! Utilisez: ligne colonne valeur")
    
    def ajouter_score(self, points):
        """Ajoute des points au score total"""
        self.score_total += points