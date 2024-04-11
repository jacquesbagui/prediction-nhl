from flask import Flask, render_template
from MatchAnalyzer import MatchAnalyzer

app = Flask(__name__)

@app.route('/')
def index():
    analyzer = MatchAnalyzer()
    upcoming_matches = analyzer.get_confrontations_with_date()
    players_goals_matches, all_players_goals = analyzer.analyze_last_three_matches()
    players_who_scored = analyzer.get_players_who_scored_in_all_matches(players_goals_matches)
    players_infos_who_scored = []
    for player_id in players_who_scored:
        player_info = analyzer.get_player_info(player_id)
        players_infos_who_scored.append(player_info)
    best_scorers = analyzer.get_best_scorers(all_players_goals)
    players_best_scorers_info = []
    for best_scorer in best_scorers:
        player_best_scorer_info = analyzer.get_player_info(best_scorer)
        players_best_scorers_info.append(player_best_scorer_info)
    return render_template('index.html', players_infos_who_scored=players_infos_who_scored, players_best_scorers_info=players_best_scorers_info, upcoming_matches=upcoming_matches)

if __name__ == '__main__':
  app.run(debug=True)
