import sqlite3

class MatchDatabase:
    def __init__(self, db_file):
        self.db_file = db_file

    def connect(self):
        self.conn = sqlite3.connect(self.db_file)
        self.cur = self.conn.cursor()

    def disconnect(self):
        self.conn.close()

    def create_table(self):
        self.connect()
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS match_table (
                id INTEGER PRIMARY KEY,
                game_id TEXT,
                home_team_id INTEGER,
                home_team_slug TEXT,
                home_team_name TEXT,
                home_team_score INTEGER,
                home_team_goals TEXT,
                away_team_id INTEGER,
                away_team_slug TEXT,
                away_team_name TEXT,
                away_team_score INTEGER,
                away_team_goals TEXT,
                match_date TEXT
            )
        ''')
        self.disconnect()
        
    def find_match_by_game_id(self, game_id):
        self.connect()
        self.cur.execute('''
            SELECT * FROM match_table
            WHERE game_id = ?
        ''', (game_id,))
        match = self.cur.fetchone()
        self.disconnect()
        return match
    
    def insert_match(self, match):
        self.connect()
        sql = '''
            INSERT INTO match_table (game_id, home_team_id, home_team_slug, home_team_name, home_team_score, home_team_goals,
                                    away_team_id, away_team_slug, away_team_name, away_team_score, away_team_goals, match_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        values = (
            match["game_id"],
            match["homeTeam"]["id"],
            match["homeTeam"]["slug"],
            match["homeTeam"]["team"],
            match["homeTeam"]["score"],
            match["homeTeam"]["goals"],
            match["awayTeam"]["id"],
            match["awayTeam"]["slug"],
            match["awayTeam"]["team"],
            match["awayTeam"]["score"],
            match["awayTeam"]["goals"],
            match["date"]
        )
        self.cur.execute(sql, values)
        self.conn.commit()
        self.disconnect()

    def find_matches_by_teams(self, home_team_slug, away_team_slug):
        self.connect()
        self.cur.execute('''
            SELECT * FROM match_table
            WHERE (home_team_slug = ? AND away_team_slug = ?)
            OR (home_team_slug = ? AND away_team_slug = ?)
        ''', (home_team_slug, away_team_slug, away_team_slug, home_team_slug))
        matches_data = self.cur.fetchall()
        # Récupérer les noms de colonnes
        column_names = [description[0] for description in self.cur.description]
        matches = [dict(zip(column_names, match)) for match in matches_data]
        self.disconnect()
        return matches

def main():
    # Exemple d'utilisation de la classe MatchDatabase
    db = MatchDatabase('nhl_db.db')
    db.create_table()

    # Exemple d'insertion d'un match
    match = {
        "game_id": "game123",
        "homeTeam": {"id": 1, "slug": "home_team_slug", "team": "Home Team", "score": 3, "goals": "[]"},
        "awayTeam": {"id": 2, "slug": "away_team_slug", "team": "Away Team", "score": 2, "goals": "[]"},
        "date": "2024-04-05"
    }
    db.insert_match(match)

    # Exemple de recherche de matchs par équipes
    home_team_slug = "home_team_slug"
    away_team_slug = "away_team_slug"
    matches = db.find_matches_by_teams(home_team_slug, away_team_slug)
    print("Matches pour les équipes en confrontation :")
    for match in matches:
        print(match)

if __name__ == "__main__":
    main()
