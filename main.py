import requests
from bs4 import BeautifulSoup
import datetime
import sqlite3
import json

from MatchAnalyzer import MatchAnalyzer
from MatchDatabase import MatchDatabase

BASE_URL = "https://api.nhle.com"

def main():
    analyzer = MatchAnalyzer()
    players_goals_matches, all_players_goals = analyzer.analyze_last_three_matches()
    players_who_scored = analyzer.get_players_who_scored_in_all_matches(players_goals_matches)
    # Les joueurs qui ont marqué dans les 3 derniers matchs
    print("Joueurs qui ont marqué lors de chaque rencontre des 3 derniers matchs :")
    for player_id in players_who_scored:
        print(f"Joueur {player_id}")
        print(analyzer.get_player_info(player_id))
    # Le meilleur buteur des 3 derniers matchs
    best_scorer = analyzer.get_best_scorer(all_players_goals)
    print("Meilleur buteur des 3 derniers matchs :")
    print(f"Joueur {best_scorer}")
    print(analyzer.get_player_info(best_scorer))


# Exécuter la fonction principale
if __name__ == "__main__":
  main()
