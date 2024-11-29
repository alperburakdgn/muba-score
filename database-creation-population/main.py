from database import initialize_db, add_league, update_missing_statistics, update_all_coaches, update_transfers, add_venues

def main():
    # MySQL bağlantısını başlat
    conn = initialize_db()

    if conn is None:
        print("Veritabanı bağlantısı kurulamadı.")
        return

    print("Veritabanı bağlantısı başarıyla kuruldu.")

    # Ligler ve ülkeler
    leagues = [
        {"id": 39, "name": "Premier League", "country": "England"},
        {"id": 61, "name": "Ligue 1", "country": "France"},
        {"id": 78, "name": "Bundesliga", "country": "Germany"},
        {"id": 135, "name": "Serie A", "country": "Italy"},
        {"id": 140, "name": "La Liga", "country": "Spain"}
    ]
    season = 2023  # 2022/2023 sezonu
    '''players = get_players(611, 2020)
    save_players_to_db(conn, players, 2020)'''

    '''update_missing_statistics(conn, season)'''
    '''update_all_coaches(conn)'''
    '''update_transfers(conn, 140, season)'''
    add_venues(conn)

    '''for league in leagues:
        # Lig ekleme
        add_league(conn, league["id"], league["name"], league["country"], season)'''


if __name__ == "__main__":
    main()


''',
        {"id": 61, "name": "Ligue 1", "country": "France"},
        {"id": 39, "name": "Premier League", "country": "England"},
        {"id": 78, "name": "Bundesliga", "country": "Germany"},
        {"id": 135, "name": "Serie A", "country": "Italy"},
        {"id": 140, "name": "La Liga", "country": "Spain"}
'''
