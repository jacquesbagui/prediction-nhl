from MatchDatabase import MatchDatabase
import requests
import datetime
import json

class MatchAnalyzer:
    def __init__(self):
        self.db = MatchDatabase('nhl_db.db')
    
    def filter_shot_on_goal(self, game_id):
        url = f"https://api-web.nhle.com/v1/gamecenter/{game_id}/play-by-play"
        response = requests.get(url)
        plays = response.json()["plays"]
        filter_shot_on_goal = json.dumps([play for play in plays if play["typeDescKey"] == "shot-on-goal"])
        return filter_shot_on_goal
    
    def get_matches_with_date(self, date_str=None):
        default_date = datetime.date.today()
        if date_str is None:
            date_str = default_date.strftime("%Y-%m-%d")
        url = f"https://api-web.nhle.com/v1/schedule/{date_str}"
        response = requests.get(url)
        games = response.json()["gameWeek"][0]
        return games
    
    def get_confrontations_with_date(self, date_str=None):
        games = self.get_matches_with_date(date_str)
        confrontations = []
        for game in games["games"]:
            confrontations.append({
                "homeTeam": game["homeTeam"]["placeName"]["default"],
                "awayTeam": game["awayTeam"]["placeName"]["default"],
            })
        return confrontations
      
    def get_player_info(self, player_id):
        url = f"https://api-web.nhle.com/v1/player/{player_id}/landing"
        response = requests.get(url)
        player = response.json()
        return {
            'Team': player['fullTeamName']['default'], 
            'FirstName': player['firstName']['default'], 
            'LastName': player['lastName']['default'], 
            'sweaterNumber': player['sweaterNumber'],
            'featuredStats': player['featuredStats'],
        }
        
    def analyze_last_three_matches(self):
        matches_with_date = self.get_matches_with_date()
        matches = matches_with_date["games"]
        players_goals_matches = [{}, {}, {}]  # Un dictionnaire par match pour stocker les joueurs qui ont marqué
        all_players_goals = {}
        
        for match in matches:
            home_team = match["homeTeam"]["abbrev"]
            away_team = match["awayTeam"]["abbrev"]
            teams_games = self.db.find_matches_by_teams(home_team, away_team)
            
            for i, game in enumerate(teams_games[:3], start=0):  # Parcourir les 3 derniers matchs
                home_goals_details = json.loads(game["home_team_goals"])
                away_goals_details = json.loads(game["away_team_goals"])
                
                for goal in home_goals_details:
                    scoring_player_id = goal['details']['scoringPlayerId']
                    if scoring_player_id:
                        players_goals_matches[i][scoring_player_id] = True
                        all_players_goals[scoring_player_id] = all_players_goals.get(scoring_player_id, 0) + 1
                
                for goal in away_goals_details:
                    scoring_player_id = goal['details'].get('scoringPlayerId')
                    if scoring_player_id:
                        players_goals_matches[i][scoring_player_id] = True
                        all_players_goals[scoring_player_id] = all_players_goals.get(scoring_player_id, 0) + 1
        
        return players_goals_matches, all_players_goals
    
    def get_players_who_scored_in_all_matches(self, players_goals_matches):
        players_who_scored_in_all_matches = set.intersection(*[set(players.keys()) for players in players_goals_matches])
        return players_who_scored_in_all_matches

    def get_best_scorer(self, all_players_goals):
        best_scorer = max(all_players_goals, key=all_players_goals.get)
        return best_scorer
    
    def get_best_scorers(self, all_players_goals, n=3):
        sorted_players = sorted(all_players_goals.items(), key=lambda x: x[1], reverse=True)
        best_scorers = [player_id for player_id, _ in sorted_players[:n]]
        return best_scorers