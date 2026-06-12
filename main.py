from menu import Menu
from scores import ScoreManager
import sys

def main():
    score_manager = ScoreManager()
    menu = Menu(score_manager)
    menu.afficher()

if __name__ == "__main__":
    main()