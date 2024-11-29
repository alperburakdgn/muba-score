import mysql.connector
import requests
API_URL = "https://v3.football.api-sports.io"
API_KEY = "d502f3949161ad154d69db8690562dc3"

HEADERS = {
    "x-rapidapi-key": API_KEY,
    "x-rapidapi-host": "v3.football.api-sports.io"
}

def get_teams(league_id, season):
    """Belirli bir lig ve sezona ait takımları çeker."""
    url = f"{API_URL}/teams?league={league_id}&season={season}"
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code == 200:
        data = response.json()
        return data["response"]
    else:
        print(f"API Hatası: {response.status_code} - {response.text}")
        return None

def get_players(team_id, season):
    """Belirli bir takım ve sezona ait oyuncuları çeker."""
    url = f"{API_URL}/players?team={team_id}&season={season}"
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code == 200:
        data = response.json()
        return data["response"]
    else:
        print(f"API Hatası: {response.status_code} - {response.text}")
        return None

def get_matches(league_id, season):
    """Belirli bir lig ve sezona ait fikstürleri çeker."""
    url = f"{API_URL}/fixtures?league={league_id}&season={season}"

    response = requests.get(url, headers=HEADERS)

    if response.status_code == 200:
        fixtures = response.json()
        return fixtures["response"]
    else:
        print(f"API Hatası: {response.status_code} - {response.text}")
        return []
    

def get_match_events(match_id):
    """Belirli bir maç için etkinlik verilerini API'den çeker."""
    url = f"{API_URL}/fixtures/events?fixture={match_id}"
    

    response = requests.get(url, headers=HEADERS)

    if response.status_code == 200:
        events = response.json()
        return events["response"]
    else:
        print(f"API Hatası: {response.status_code} - {response.text}")
        return []



DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "maho",
    "database": "project"
    #"auth_plugin": "mysql_native_password"
}

def initialize_db():
    """MySQL bağlantısını kurar."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # Ligler tablosunu oluştur
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Leagues (
            league_id INT AUTO_INCREMENT PRIMARY KEY,
            league_name VARCHAR(255) NOT NULL,
            country VARCHAR(100) NOT NULL,
            season VARCHAR(50) NOT NULL
        )
        """)

        # Takımlar tablosunu oluştur
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Teams (
            team_id INT AUTO_INCREMENT PRIMARY KEY,
            team_name VARCHAR(255) NOT NULL UNIQUE,
            league_id INT NOT NULL,
            stadium VARCHAR(255) NOT NULL,
            coach_name VARCHAR(255) NOT NULL,
            capacity INT NOT NULL,
            location VARCHAR(255) NOT NULL,
            FOREIGN KEY (league_id) REFERENCES Leagues(league_id)
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Players (
            player_id INT PRIMARY KEY,
            first_name VARCHAR(255) NOT NULL,
            last_name VARCHAR(255) NOT NULL,
            team_id INT NOT NULL,
            position VARCHAR(50),
            age INT,
            nationality VARCHAR(100),
            FOREIGN KEY (team_id) REFERENCES Teams(team_id)
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Statistics (
            stat_id INT AUTO_INCREMENT PRIMARY KEY,
            player_id INT NOT NULL,
            goals INT DEFAULT 0,
            assists INT DEFAULT 0,
            yellow_card INT DEFAULT 0,
            red_cards INT DEFAULT 0,
            minutes_played INT DEFAULT 0,
            season YEAR NOT NULL,
            FOREIGN KEY (player_id) REFERENCES Players(player_id),
            UNIQUE (player_id, season)
        )        
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Matches (
            match_id INT PRIMARY KEY,
            league_id INT NOT NULL,
            season YEAR NOT NULL,
            round VARCHAR(50),
            date DATETIME NOT NULL,
            referee VARCHAR(100),
            home_team_id INT NOT NULL,
            home_team_name VARCHAR(100),
            away_team_id INT NOT NULL,
            away_team_name VARCHAR(100),
            home_goals INT DEFAULT 0,
            away_goals INT DEFAULT 0,
            winner_team_id INT DEFAULT NULL,
            FOREIGN KEY (league_id) REFERENCES Leagues(league_id) ON DELETE CASCADE,
            FOREIGN KEY (home_team_id) REFERENCES Teams(team_id) ON DELETE CASCADE,
            FOREIGN KEY (away_team_id) REFERENCES Teams(team_id) ON DELETE CASCADE
        );
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS MatchEvents (
            event_id INT AUTO_INCREMENT PRIMARY KEY,
            match_id INT NOT NULL,
            team_id INT NOT NULL,
            team_name VARCHAR(255),
            player_id INT,
            player_name VARCHAR(255),
            assist_id INT,
            assist_name VARCHAR(255),
            event_type VARCHAR(50),
            event_detail VARCHAR(255),
            elapsed_time INT,
            FOREIGN KEY (match_id) REFERENCES Matches(match_id),
            FOREIGN KEY (player_id) REFERENCES Players(player_id),
            FOREIGN KEY (assist_id) REFERENCES Players(player_id),
            FOREIGN KEY (team_id) REFERENCES Teams(team_id)
        );
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Transfers (
                transfer_id INT AUTO_INCREMENT PRIMARY KEY,
                player_id INT NOT NULL,
                from_team_id INT NOT NULL,
                to_team_id INT NOT NULL,
                transfer_fee VARCHAR(255),
                transfer_date DATE NOT NULL,
                FOREIGN KEY (player_id) REFERENCES Players(player_id),
                FOREIGN KEY (from_team_id) REFERENCES Teams(team_id),
                FOREIGN KEY (to_team_id) REFERENCES Teams(team_id)
            );
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Venues (
                venue_id INT PRIMARY KEY,
                venue_name VARCHAR(255),
                location VARCHAR(255),
                capacity INT NOT NULL
            );
        """)

        conn.commit()
        print("MySQL veritabanı ve tablolar başarıyla oluşturuldu!")
        return conn

    except mysql.connector.Error as err:
        print(f"MySQL Hatası: {err}")
        return None


def save_teams_to_db(conn, league_id, season):
    """Takımları ve mekanları veritabanına kaydeder."""
    teams = get_teams(league_id, season)
    cursor = conn.cursor()
    for team in teams:
        team_id = team["team"]["id"]
        team_name = team["team"]["name"]
        venue_name = team["venue"]["name"]
        coach_name = team["team"].get("coach_name", "Unknown")
        capacity = team["venue"]["capacity"]
        city = team["venue"]["city"]
        try:
            # Takım kontrolü
            cursor.execute("SELECT * FROM Teams WHERE team_id = %s", (team["team"]["id"],))
            if not cursor.fetchone():
                # Takımı ekle
                cursor.execute("""
                    INSERT INTO Teams (team_id, team_name, league_id, stadium, coach_name, capacity, location)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (
                    team_id,
                    team_name,
                    league_id,
                    venue_name,
                    coach_name,
                    capacity,
                    city
                ))
                conn.commit()
            save_players_to_db(conn, team_id, season)
        except Exception as e:
            print(f"Takım eklenirken hata oluştu: {e}")
    
    save_matches_to_db(conn, league_id, season)



def add_league(conn, league_id, league_name, country, season):
    """Lig bilgilerini veritabanına ekler."""
    cursor = conn.cursor()
    try:
        # Lig var mı kontrol et
        cursor.execute("SELECT * FROM Leagues WHERE league_id = %s", (league_id,))
        if cursor.fetchone():
            print(f"Lig zaten mevcut: {league_name} ({season})")
        else:
            # Lig yoksa ekle
            cursor.execute("""
                INSERT INTO Leagues (league_id, league_name, country, season)
                VALUES (%s, %s, %s, %s)
            """, (league_id, league_name, country, season))
            conn.commit()
            print(f"Lig eklendi: {league_name} ({season})")

        save_teams_to_db(conn, league_id, season)

    except Exception as e:
        print(f"Lig eklenirken hata oluştu: {e}")

def save_players_to_db(conn, team_id, season):
    """Oyuncuları veritabanına kaydeder."""
    cursor = conn.cursor()
    players = get_players(team_id, season)

    for player in players:
        # Oyuncu verileri
        player_id = player["player"]["id"]
        first_name = player["player"]["firstname"]
        last_name = player["player"]["lastname"]
        age = player["player"].get("age", None)
        nationality = player["player"].get("nationality", "Unknown")
        statistics = player["statistics"][0]
        team_id = statistics["team"]["id"]
        team_name = statistics["team"]["name"]
        position = statistics["games"]["position"]
        goals = statistics["goals"]["total"]
        assists = statistics["goals"]["assists"]
        yellow_card = statistics["cards"]["yellow"]
        red_cards = statistics["cards"]["red"]
        minutes_played = statistics["games"]["minutes"]
        try:

            cursor.execute("SELECT * FROM Players WHERE player_id = %s", (player_id,))
            if not cursor.fetchone():

                # Takımın mevcut olup olmadığını kontrol et
                cursor.execute("SELECT * FROM Teams WHERE team_id = %s", (team_id,))
                if not cursor.fetchone():
                    print(f"Takım {team_name} veritabanında bulunamadı, oyuncu eklenemedi.")
                    continue

                # Oyuncu ekle
                cursor.execute("""
                    INSERT INTO Players (player_id, first_name, last_name, team_id, position, age, nationality)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (
                    player_id,
                    first_name,
                    last_name,
                    team_id,
                    position,
                    age,
                    nationality
                ))
                conn.commit()

                print(f"Oyuncu eklendi: {last_name}")

                try:
                    cursor.execute("SELECT * FROM Statistics WHERE player_id = %s and season = %s", (player_id,season))
                    if not cursor.fetchone():
                        cursor.execute("""
                        INSERT INTO Statistics (player_id, goals, assists, yellow_card, red_cards, minutes_played, season)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                        """, (player_id, goals, assists, yellow_card, red_cards, minutes_played, season))
                        conn.commit()

                except Exception as e:
                    print(f"Stat eklenirken hata oluştu: {e}")


        except Exception as e:
            print(f"Oyuncu eklenirken hata oluştu: {e}")

        

            
def save_matches_to_db(conn, league_id, season):
    """Liglerin fikstürlerini veritabanına kaydeder."""
    cursor = conn.cursor()
    matches = get_matches(league_id, season)

    for match in matches:
        # Fixture bilgileri
        match_id = match["fixture"]["id"]
        referee = match["fixture"].get("referee", None)
        date = match["fixture"]["date"]
        home_team_id = match["teams"]["home"]["id"]
        home_team_name = match["teams"]["home"]["name"]
        away_team_id = match["teams"]["away"]["id"]
        away_team_name = match["teams"]["away"]["name"]
        home_goals = match["goals"]["home"]
        away_goals = match["goals"]["away"]
        round_info = match["league"]["round"]
        cursor.execute("SELECT * FROM Matches WHERE match_id = %s", (match_id,))
        try:
            if not cursor.fetchone():
                # Kazanan takım bilgisi
                winner_team_id = None
                if match["teams"]["home"]["winner"]:
                    winner_team_id = home_team_id
                elif match["teams"]["away"]["winner"]:
                    winner_team_id = away_team_id

                # Takımların mevcut olup olmadığını kontrol et
                cursor.execute("SELECT * FROM Teams WHERE team_id = %s", (home_team_id,))
                if not cursor.fetchone():
                    print(f"Ev sahibi takım bulunamadı: {home_team_name}")
                    continue

                cursor.execute("SELECT * FROM Teams WHERE team_id = %s", (away_team_id,))
                if not cursor.fetchone():
                    print(f"Deplasman takımı bulunamadı: {away_team_name}")
                    continue

                # Veritabanına ekle
                cursor.execute("""
                    INSERT INTO Matches (match_id, league_id, season, round, date, referee, home_team_id, home_team_name,
                                         away_team_id, away_team_name, home_goals, away_goals, winner_team_id)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    match_id, league_id, season, round_info, date, referee, home_team_id, home_team_name,
                    away_team_id, away_team_name, home_goals, away_goals, winner_team_id
                ))
                conn.commit()
            save_match_events_to_db(conn, match_id)
        except Exception as e:
            print(f"Maç eklenirken hata oluştu: {e}")


def save_match_events_to_db(conn, match_id):
    """Maç etkinliklerini veritabanına kaydeder."""
    cursor = conn.cursor()
    events = get_match_events(match_id)
    for event in events:
        try:
            # Etkinlik bilgileri
            event_type = event["type"]
            event_detail = event.get("detail", None)
            player_id = event["player"]["id"] if event["player"] else None
            player_name = event["player"]["name"] if event["player"] else None
            assist_id = event["assist"]["id"] if event.get("assist") and event["assist"] else None
            assist_name = event["assist"]["name"] if event.get("assist") and event["assist"] else None
            team_id = event["team"]["id"]
            team_name = event["team"]["name"]
            elapsed_time = event["time"]["elapsed"]

            # Oyuncu varsa ekle
            cursor.execute("SELECT * FROM Players WHERE player_id = %s", (player_id,))
            if not cursor.fetchone():
                save_player_if_not_exists(conn, player_id, team_id)
            
            # Oyuncu varsa ekle
            cursor.execute("SELECT * FROM Players WHERE player_id = %s", (assist_id,))
            if not cursor.fetchone():
                save_player_if_not_exists(conn, assist_id, team_id)

            # Veritabanına ekle
            cursor.execute("""
                INSERT INTO MatchEvents (match_id, team_id, team_name, player_id, player_name, assist_id, assist_name, event_type, event_detail, elapsed_time)
                VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (match_id, team_id, team_name, player_id, player_name,
                  assist_id, assist_name, event_type, event_detail, elapsed_time))
            conn.commit()
            print(f"Etkinlik kaydedildi: {event_type} - {player_name} - {elapsed_time} dk")
        except Exception as e:
            print(f"Etkinlik eklenirken hata oluştu: {e}")


def save_player_if_not_exists(conn, player_id, team_id):
    """Oyuncu veritabanında yoksa ekler."""
    cursor = conn.cursor()
    # Oyuncu ekle
    print("oyuncu yok")
    url = f"{API_URL}/players/profiles"
    params = {"player": player_id}
    response = requests.get(url, headers=HEADERS, params=params)
    response.raise_for_status()
    
    if response.status_code == 200:
        data = response.json()
    player = data["response"][0]["player"]

    player_id = player["id"]
    first_name = player["firstname"]
    last_name = player["lastname"]
    age = player.get("age", None)
    nationality = player.get("nationality", "Unknown")
    position = player["position"]

    try:
        cursor.execute("SELECT * FROM Players WHERE player_id = %s", (player_id,))
        if not cursor.fetchone():
            cursor.execute("""
                INSERT INTO Players (player_id, first_name, last_name, team_id, position, age, nationality)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                player_id,
                first_name,
                last_name,
                team_id,
                position,
                age,
                nationality
            ))
            conn.commit()

    except Exception as e:
        print(f"Hata: {e}")


def update_missing_statistics(conn, season):
    cursor = conn.cursor()

    # Tüm oyuncuları Player tablosundan al
    cursor.execute("SELECT player_id, team_id FROM Players")
    players = cursor.fetchall()

    for player in players:
        player_id = player[0]
        team_id = player[1]

        # Teams tablosundan league_id'yi al
        cursor.execute("SELECT league_id FROM Teams WHERE team_id = %s", (team_id,))
        league_info = cursor.fetchone()

        if not league_info:
            print(f"No league found for team_id: {team_id}. Skipping player_id: {player_id}")
            continue

        league_id = league_info[0]

        # Statistics tablosunda bu oyuncu var mı kontrol et
        cursor.execute("SELECT * FROM Statistics WHERE player_id = %s AND season = %s", (player_id, season))
        stat_exists = cursor.fetchone()

        if not stat_exists:
            print(f"Missing statistics for player_id: {player_id}, fetching from API...")
            try:
                url = f"{API_URL}/players?id={player_id}&league={league_id}&season={season}"
                params = {"id": player_id, "league": league_id, "season": season}
                response = requests.get(url, headers=HEADERS)

                if response.status_code != 200:
                    print(f"API Error: {response.status_code} - {response.text}")
                    continue

                data = response.json()
                if "response" not in data or not data["response"]:
                    print(f"No data found for player_id: {player_id}")
                    continue

                player_data = data["response"][0]  # İlk öğeyi al
                statistics = player_data["statistics"]

                if not statistics:
                    print(f"No statistics available for player_id: {player_id}")
                    continue

                # İlk istatistik kaydını alın
                stat = statistics[0]
                goals = stat["goals"].get("total", 0)
                assists = stat["goals"].get("assists", 0)
                yellow_card = stat["cards"].get("yellow", 0)
                red_cards = stat["cards"].get("red", 0)
                minutes_played = stat["games"].get("minutes", 0)

                cursor.execute("""
                    INSERT INTO Statistics (player_id, goals, assists, yellow_card, red_cards, minutes_played, season)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (player_id, goals, assists, yellow_card, red_cards, minutes_played, season))
                conn.commit()
                print(f"Statistics added for player_id: {player_id}")

            except Exception as e:
                print(f"Error adding statistics for player_id {player_id}: {e}")



def update_all_coaches(conn):
    cursor = conn.cursor()

    try:
        # Teams tablosundaki tüm takımları çek
        cursor.execute("SELECT team_id FROM Teams")
        teams = cursor.fetchall()

        for team in teams:
            team_id = team[0]

            # API'den koç bilgisi al
            url = f"{API_URL}/coachs?team={team_id}"
            response = requests.get(url, headers=HEADERS)

            if response.status_code == 200:
                coaches = response.json().get("response", [])
                if coaches:
                    active_coaches = []
                    for coach in coaches:
                        for career in coach.get("career", []):
                            if career["team"]["id"] == team_id and career["end"] is None:
                                active_coaches.append(coach)

                    # Eğer birden fazla aktif koç varsa ilkini seç
                    if active_coaches:
                        latest_coach = active_coaches[0]
                        coach_name = latest_coach["name"]
                    else:
                        coach_name = "Unknown"
                else:
                    coach_name = "Unknown"
            else:
                print(f"API Error for team_id {team_id}: {response.status_code} - {response.text}")
                coach_name = "Unknown"

            # Veritabanını güncelle
            cursor.execute("UPDATE Teams SET coach_name = %s WHERE team_id = %s", (coach_name, team_id))

        # Tüm değişiklikleri bir kerede commit et
        conn.commit()
        print("All coaches updated successfully.")

    except mysql.connector.Error as e:
        print(f"Database error: {e}")




def update_transfers(conn, league_id, season):
    """Belirtilen sezona ve lig id'sine göre transfer bilgilerini günceller."""
    cursor = conn.cursor()

    # Lig içindeki takımları al
    cursor.execute("SELECT team_id FROM Teams WHERE league_id = %s", (league_id,))
    teams = cursor.fetchall()

    if not teams:
        print(f"Ligde (ID: {league_id}) takım bulunamadı!")
        return

    for team in teams:
        team_id = team[0]
        print(f"Transfer bilgileri alınıyor: Team ID {team_id}")

        # API'den transfer bilgilerini çek
        url = f"{API_URL}/transfers?team={team_id}"
        response = requests.get(url, headers=HEADERS)

        if response.status_code != 200:
            print(f"API Error: {response.status_code} - {response.text}")
            continue

        data = response.json()
        players_transfers = data.get("response", [])

        for player_data in players_transfers:
            player = player_data.get("player", {})
            player_id = player.get("id")
            transfers = player_data.get("transfers", [])

            for transfer in transfers:
                transfer_date = transfer.get("date")

                # Tarih kontrolü yap (string'e dönüştürerek)
                if not transfer_date or not str(transfer_date).startswith(str(season)):
                    continue

                teams = transfer.get("teams", {})
                from_team = teams.get("out")
                to_team = teams.get("in")
                from_team_id = from_team["id"] if from_team else None
                to_team_id = to_team["id"] if to_team else None
                transfer_fee = transfer.get("type", "N/A")  # Ücret yerine tür ekleniyor

                # from_team_id ve to_team_id'nin Teams tablosunda olup olmadığını kontrol et
                if from_team_id:
                    cursor.execute("SELECT team_id FROM Teams WHERE team_id = %s", (from_team_id,))
                    if not cursor.fetchone():
                        print(f"From team {from_team_id} veritabanında bulunamadı, transfer atlandı.")
                        continue

                if to_team_id:
                    cursor.execute("SELECT team_id FROM Teams WHERE team_id = %s", (to_team_id,))
                    if not cursor.fetchone():
                        print(f"To team {to_team_id} veritabanında bulunamadı, transfer atlandı.")
                        continue

                try:
                    # Transferi ekle
                    cursor.execute("""
                        INSERT INTO Transfers (player_id, from_team_id, to_team_id, transfer_fee, transfer_date)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (player_id, from_team_id, to_team_id, transfer_fee, transfer_date))
                    print(f"Transfer eklendi: Player ID {player_id} -> {transfer_date}")
                    # Değişiklikleri kaydet
                    conn.commit()
                except mysql.connector.Error as e:
                    print(f"Transfer eklenirken hata: {e}")

    cursor.close()
    print("Transfer bilgileri başarıyla güncellendi!")


def add_venues(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT stadium FROM Teams")
    venues = cursor.fetchall()

    if venues:
        for tmp in venues:
            venue_name = tmp[0]
            url = f"{API_URL}/venues?name={venue_name}"
            response = requests.get(url, headers=HEADERS)
            if response.status_code != 200:
                print(f"API Error: {response.status_code} - {response.text}")
                continue

            data = response.json()
            venue = data.get("response", [])[0]
            venue_id = venue["id"]
            location = venue["city"]
            name = venue["name"]
            capacity = venue["capacity"]

            try:
                # Transferi ekle
                cursor.execute("""
                    INSERT INTO Venues (venue_id, venue_name, location, capacity)
                    VALUES (%s, %s, %s, %s)
                """, (venue_id, name, location, capacity))
                print(f"{name} stadı eklendi")
                conn.commit()

            except Exception as e:
                print(f"Stat yüklenirken hata: {e}")

