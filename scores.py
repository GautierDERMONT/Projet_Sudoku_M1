import json
import os
import matplotlib.pyplot as plt

class ScoreManager:
    """Classe gerant les scores des joueurs"""
    
    def __init__(self, fichier_scores='scores.json'):
        self.fichier_scores = fichier_scores
        self.scores = self.charger_scores()
    
    def charger_scores(self):
        """Charge les scores depuis un fichier JSON"""
        if os.path.exists(self.fichier_scores):
            try:
                with open(self.fichier_scores, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def sauvegarder_scores(self):
        """Sauvegarde les scores dans un fichier JSON"""
        with open(self.fichier_scores, 'w') as f:
            json.dump(self.scores, f, indent=4)
    
    def sauvegarder_score(self, nom_joueur, score):
        """Sauvegarde le score d'un joueur"""
        if nom_joueur in self.scores:
            if score > self.scores[nom_joueur]:
                self.scores[nom_joueur] = score
        else:
            self.scores[nom_joueur] = score
        
        self.sauvegarder_scores()
    
    def afficher_scores(self):
        """Affiche les scores"""
        if not self.scores:
            print("\nAucun score enregistre pour le moment!")
            input("\nAppuyez sur Entree pour continuer...")
            return
        
        print("\n" + "="*50)
        print("          TABLEAU DES SCORES")
        print("="*50)
        
        scores_tries = sorted(self.scores.items(), key=lambda x: x[1], reverse=True)
        
        print("\nMeilleur score: {} avec {} points".format(
            scores_tries[0][0], scores_tries[0][1]))
        
        print("\nClassement complet:")
        print("-" * 30)
        for i, (nom, score) in enumerate(scores_tries, 1):
            print(f"{i:2}. {nom:15} : {score:5} points")
        
        self.afficher_graphique_scores(scores_tries)
        
        input("\nAppuyez sur Entree pour continuer...")
    
    def afficher_graphique_scores(self, scores_tries):
        """Affiche un graphique des scores avec matplotlib"""
        if not scores_tries:
            return
        
        noms = [nom for nom, _ in scores_tries[:10]]
        points = [score for _, score in scores_tries[:10]]
        
        plt.figure(figsize=(12, 6))
        bars = plt.barh(range(len(noms)), points, color='skyblue')
        
        for i, (bar, point) in enumerate(zip(bars, points)):
            plt.text(point + 1, bar.get_y() + bar.get_height()/2, 
                    str(point), va='center')
        
        plt.yticks(range(len(noms)), noms)
        plt.xlabel('Points')
        plt.title('Top 10 des meilleurs scores au Sudoku')
        plt.gca().invert_yaxis()
        plt.grid(True, axis='x', alpha=0.3)
        
        for i, (bar, point) in enumerate(zip(bars, points)):
            if i == 0:
                bar.set_color('gold')
            elif i == 1:
                bar.set_color('silver')
            elif i == 2:
                bar.set_color('#CD7F32')
            elif point < 0:
                bar.set_color('lightcoral')
        
        plt.tight_layout()
        plt.show()