import datetime
import requests
import sqlite3
import json

from MatchDatabase import MatchDatabase

BASE_URL = "https://api.nhle.com"

def main():
    db = MatchDatabase('nhl_db.db')
    db.create_table()
    today = datetime.date.today()
    nb_jours = 10
    for i in range(1, nb_jours):
            date = today - datetime.timedelta(days=i)
            date_str = date.strftime("%Y-%m-%d")
            matches = get_matches_with_date(date_str)
            for match in matches["games"]:
                match_object = {
                    "game_id": match["id"],
                    "homeTeam": {
                        "id" : match["homeTeam"]["id"],
                        "slug": match["homeTeam"]["abbrev"],
                        "team": match["homeTeam"]["placeName"]["default"],
                        "score": int(match["homeTeam"]["score"]) ,
                        "goals" : filterShotOnGoal(match["id"])
                    },
                    "awayTeam": {
                        "id" : match["awayTeam"]["id"],
                        "slug": match["awayTeam"]["abbrev"],
                        "team": match["awayTeam"]["placeName"]["default"],
                        "score": int(match["awayTeam"]["score"]),
                        "goals" : filterShotOnGoal(match["id"])
                    },
                    "date": date_str,
                }
                print("match_object :", match_object)
                match_existe = db.find_match_by_game_id(match_object["game_id"])
                if match_existe:
                    print(f"Le match {match_object['game_id']} existe déjà dans la base de données.")
                    return
                db.insert_match(match_object)
                
def filterShotOnGoal(game_id):
    url = f"https://api-web.nhle.com/v1/gamecenter/{game_id}/play-by-play"
    response = requests.get(url)
    plays = response.json()["plays"]
    filterShotOnGoal = json.dumps([play for play in plays if play["typeDescKey"] == "goal"])
    return filterShotOnGoal

# Fonction pour obtenir les matchs par date
def get_matches_with_date(date_str = None):
    default_date = datetime.date.today()
    if date_str is None:
        date_str = default_date.strftime("%Y-%m-%d")
    url = f"https://api-web.nhle.com/v1/schedule/{date_str}"
    response = requests.get(url)
    games = response.json()["gameWeek"][0]
    return games

# Exécuter la fonction principale
if __name__ == "__main__":
  main()