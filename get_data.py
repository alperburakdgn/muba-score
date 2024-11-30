import mysql.connector
import sys
sys.stdout.reconfigure(encoding='utf-8')


# Veritabanı bağlantı bilgileri
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "9168",
    "database": "project",
    "auth_plugin": "mysql_native_password"
}

def get_players_by_team(team_id):
    """Belirli bir takıma ait oyuncuları veritabanından çeker."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        query = """
            SELECT player_id, first_name, last_name, position, age, nationality
            FROM Players
            WHERE team_id = %s;
        """
        cursor.execute(query, (team_id,))
        players = cursor.fetchall()  # [(player_id, first_name, last_name, position, age, nationality), ...]
        return players
    except mysql.connector.Error as err:
        print(f"Veritabanı Hatası: {err}")
        return []
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

            

def get_player_statistics(player_id):
    """Belirli bir oyuncunun istatistiklerini veritabanından çeker."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        query = """
            SELECT goals, assists, yellow_card, red_cards, minutes_played, season
            FROM Statistics
            WHERE player_id = %s;
        """
        cursor.execute(query, (player_id,))
        statistics = cursor.fetchall()  # [(goals, assists, yellow_card, red_cards, minutes_play, season), ...]
        return statistics
    except mysql.connector.Error as err:
        print(f"Veritabanı Hatası: {err}")
        return []
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


def get_leagues():
    """Veritabanından ligleri çeker."""

    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        query = "SELECT league_id, league_name FROM Leagues;"
        cursor.execute(query)
        leagues = cursor.fetchall()  # [(39, 'Premier League'), (40, 'La Liga'), ...]
        print(leagues)
        return leagues
    except mysql.connector.Error as err:
        print(f"Veritabanı Hatası: {err}")
        return []
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def get_teams_by_league(league_id):
    """Belirli bir ligdeki takımları veritabanından çeker."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        query = "SELECT team_id, team_name FROM Teams WHERE league_id = %s;"
        cursor.execute(query, (league_id,))
        teams = cursor.fetchall()  # [(1, 'Manchester United'), (2, 'Liverpool'), ...]
        return teams
    except mysql.connector.Error as err:
        print(f"Veritabanı Hatası: {err}")
        return []
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
            
def search_players_by_name(first_name, last_name):
    """Ad ve soyada göre oyuncu araması yapar, takım bilgisiyle birlikte döner."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        query = """
            SELECT 
                Players.player_id,
                Players.first_name, 
                Players.last_name, 
                Players.position, 
                Players.age, 
                Players.nationality, 
                Teams.team_name
            FROM Players
            LEFT JOIN Teams ON Players.team_id = Teams.team_id
            WHERE Players.first_name LIKE %s AND Players.last_name LIKE %s;
        """
        cursor.execute(query, (f"%{first_name}%", f"%{last_name}%"))
        players = cursor.fetchall()  # [(player_id, first_name, last_name, position, age, nationality, team_name), ...]
        return players
    except mysql.connector.Error as err:
        print(f"Veritabanı Hatası: {err}")
        return []
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()



def search_team_by_name(team_name):
    """Veritabanında takım adıyla arama yapar."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        query = """
            SELECT team_id, team_name, league_id
            FROM Teams
            WHERE team_name LIKE %s;
        """
        cursor.execute(query, (f"%{team_name}%",))
        results = cursor.fetchall()  # [(team_id, team_name, league_id), ...]
        return results
    except mysql.connector.Error as err:
        print(f"Veritabanı Hatası: {err}")
        return []
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()



def get_stadium_details(team_id):
    """Belirli bir takımın stadyum kapasitesi ve konum bilgilerini veritabanından çeker."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        query = """
            SELECT stadium, capacity, location
            FROM Teams
            WHERE team_id = %s;
        """
        cursor.execute(query, (team_id,))
        stadium_details = cursor.fetchone()  # Tek bir satır dönecek (stadium_name, capacity, location)
        return stadium_details if stadium_details else ("Bilinmiyor", "Bilinmiyor", "Bilinmiyor")
    except mysql.connector.Error as err:
        print(f"Veritabanı Hatası: {err}")
        return ("Bilinmiyor", "Bilinmiyor", "Bilinmiyor")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
            
            
def get_team_details(team_id):
    """Belirli bir takımın stadyum ve antrenör bilgilerini veritabanından çeker."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        query = """
            SELECT stadium, coach_name
            FROM Teams
            WHERE team_id = %s;
        """
        cursor.execute(query, (team_id,))
        details = cursor.fetchone()  # Tek bir satır dönecek (stadium_name, coach_name)
        return details if details else ("Bilinmiyor", "Bilinmiyor")
    except mysql.connector.Error as err:
        print(f"Veritabanı Hatası: {err}")
        return ("Bilinmiyor", "Bilinmiyor")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def get_gelen_transfers_by_team(team_id):
    """Belirli bir takıma ait transferleri veritabanından çeker."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        query = """
            SELECT transfer_id, player_id, transfer_date, transfer_fee, from_team_id, to_team_id
            FROM Transfers
            WHERE to_team_id = %s;
        """
        cursor.execute(query, (team_id,))
        transfers = cursor.fetchall()  # [(transfer_id, player_id, transfer_date, transfer_type, fee, from_team_id, to_team_id), ...]
        return transfers
    except mysql.connector.Error as err:
        print(f"Veritabanı Hatası: {err}")
        return []
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
def get_team_name(team_id):
    """Takım ID'sine göre takım adını veritabanından çeker."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        query = "SELECT team_name FROM Teams WHERE team_id = %s;"
        cursor.execute(query, (team_id,))
        result = cursor.fetchone()
        return result[0] if result else "Bilinmiyor"
    except mysql.connector.Error as err:
        print(f"Veritabanı Hatası: {err}")
        return "Bilinmiyor"
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

            
def get_giden_transfers_by_team(team_id):
    """Belirli bir takıma ait transferleri veritabanından çeker."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        query = """
            SELECT transfer_id, player_id, transfer_date, transfer_fee, from_team_id, to_team_id
            FROM Transfers
            WHERE from_team_id = %s;
        """
        cursor.execute(query, (team_id,))
        transfers = cursor.fetchall()  # [(transfer_id, player_id, transfer_date, transfer_type, fee, from_team_id, to_team_id), ...]
        return transfers
    except mysql.connector.Error as err:
        print(f"Veritabanı Hatası: {err}")
        return []
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
            
def get_player_information_by_player_id(player_id):
    """Belirli bir oyuncu ait oyuncuları veritabanından çeker."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        query = """
            SELECT player_id, first_name, last_name, position, age, nationality
            FROM Players
            WHERE player_id = %s;
        """
        cursor.execute(query, (player_id,))
        players = cursor.fetchall()  # [(player_id, first_name, last_name, position, age, nationality), ...]
        return players
    except mysql.connector.Error as err:
        print(f"Veritabanı Hatası: {err}")
        return []
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


def get_fixtures_by_team(team_id):
    """Bir takıma ait tüm maçların fikstür bilgilerini çeker."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        query = """
            SELECT 
                match_id, league_id, season, round, date, referee,
                home_team_id, home_team_name, away_team_id, away_team_name,
                home_goals, away_goals, winner_team_id
            FROM Matches
            WHERE home_team_id = %s OR away_team_id = %s
            ORDER BY date;
        """
        cursor.execute(query, (team_id, team_id))
        fixtures = cursor.fetchall()
        return fixtures  # [(match_id, league_id, season, round, ...), ...]
    except mysql.connector.Error as err:
        print(f"Veritabanı Hatası: {err}")
        return []
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
            
def get_match_events(match_id):
    """Bir maça ait olayları veritabanından çeker."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        query = """
            SELECT 
                event_id, team_name, player_name, assist_name, 
                event_type, event_detail, elapsed_time
            FROM MatchEvents
            WHERE match_id = %s
            ORDER BY elapsed_time;
        """
        cursor.execute(query, (match_id,))
        events = cursor.fetchall()
        return events  # [(event_id, team_name, player_name, assist_name, ...), ...]
    except mysql.connector.Error as err:
        print(f"Veritabanı Hatası: {err}")
        return []
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
