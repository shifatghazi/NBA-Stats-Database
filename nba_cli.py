import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "nba_stats_project.db"

def connect_db():
    return sqlite3.connect(DB_PATH)

def print_header(title: str):
    print("\n" + "=" * 72)
    print(title)
    print("=" * 72)

def print_rows(headers, rows):
    if not rows:
        print("No results found.")
        return
    widths = [len(h) for h in headers]
    for row in rows:
        for i, value in enumerate(row):
            widths[i] = max(widths[i], len(str(value)))
    fmt = " | ".join("{:<" + str(w) + "}" for w in widths)
    print(fmt.format(*headers))
    print("-+-".join("-" * w for w in widths))
    for row in rows:
        print(fmt.format(*[str(v) for v in row]))

def list_teams(conn):
    cur = conn.cursor()
    cur.execute("SELECT team_id, city || ' ' || name FROM TEAM ORDER BY city, name;")
    return cur.fetchall()

def list_seasons(conn):
    cur = conn.cursor()
    cur.execute("SELECT season_id, year FROM SEASON ORDER BY season_id;")
    return cur.fetchall()

def list_players(conn):
    cur = conn.cursor()
    cur.execute("SELECT player_id, name FROM PLAYER ORDER BY name;")
    return cur.fetchall()

def list_games(conn):
    cur = conn.cursor()
    cur.execute("""
        SELECT g.game_id, g.game_date, g.location, s.year
        FROM GAME g
        JOIN SEASON s ON g.season_id = s.season_id
        ORDER BY g.game_date;
    """)
    return cur.fetchall()

def show_reference_data(conn):
    print_header("Available Teams")
    print_rows(["Team ID", "Team"], list_teams(conn))
    print_header("Available Seasons")
    print_rows(["Season ID", "Season"], list_seasons(conn))
    print_header("Available Players")
    print_rows(["Player ID", "Player"], list_players(conn))
    print_header("Available Games")
    print_rows(["Game ID", "Date", "Location", "Season"], list_games(conn))

def query_players_on_team_in_season(conn):
    print_header("Query 1: Players on a Team in a Season")
    print_rows(["Team ID", "Team"], list_teams(conn))
    print_rows(["Season ID", "Season"], list_seasons(conn))
    team_id = input("Enter a Team ID: ").strip()
    season_id = input("Enter a Season ID: ").strip()

    sql = """
        SELECT p.player_id, p.name, p.position, t.city || ' ' || t.name AS team_name, s.year AS season
        FROM PLAYS_FOR pf
        JOIN PLAYER p ON pf.player_id = p.player_id
        JOIN TEAM t ON pf.team_id = t.team_id
        JOIN SEASON s ON pf.season_id = s.season_id
        WHERE pf.team_id = ? AND pf.season_id = ?
        ORDER BY p.name;
    """
    cur = conn.cursor()
    cur.execute(sql, (team_id, season_id))
    rows = cur.fetchall()
    print_rows(["Player ID", "Player Name", "Position", "Team", "Season"], rows)

def query_games_for_team_in_season(conn):
    print_header("Query 2: Games for a Team in a Season")
    print_rows(["Team ID", "Team"], list_teams(conn))
    print_rows(["Season ID", "Season"], list_seasons(conn))
    team_id = input("Enter a Team ID: ").strip()
    season_id = input("Enter a Season ID: ").strip()

    sql = """
        SELECT 
            g.game_id,
            g.game_date,
            g.location,
            i.home_or_away,
            i.team_score
        FROM GAME g
        JOIN INVOLVES i ON g.game_id = i.game_id
        WHERE i.team_id = ? AND g.season_id = ?
        ORDER BY g.game_date;
    """
    cur = conn.cursor()
    cur.execute(sql, (team_id, season_id))
    rows = cur.fetchall()
    print_rows(["Game ID", "Date", "Location", "Home/Away", "Team Score"], rows)

def query_player_stats(conn):
    print_header("Query 3: Player Statistics Across Games")
    print_rows(["Player ID", "Player"], list_players(conn))
    player_id = input("Enter a Player ID: ").strip()

    sql = """
        SELECT 
            p.name,
            g.game_id,
            g.game_date,
            g.location,
            pi.points,
            pi.rebounds,
            pi.assists,
            pi.minutes_played
        FROM PLAYS_IN pi
        JOIN PLAYER p ON pi.player_id = p.player_id
        JOIN GAME g ON pi.game_id = g.game_id
        WHERE pi.player_id = ?
        ORDER BY g.game_date;
    """
    cur = conn.cursor()
    cur.execute(sql, (player_id,))
    rows = cur.fetchall()
    print_rows(
        ["Player", "Game ID", "Date", "Location", "Points", "Rebounds", "Assists", "Minutes"],
        rows
    )

def query_box_score_for_game(conn):
    print_header("Query 4: Player Box Score for a Selected Game")
    print_rows(["Game ID", "Date", "Location", "Season"], list_games(conn))
    game_id = input("Enter a Game ID: ").strip()

    sql = """
        SELECT
            p.name,
            p.position,
            pi.points,
            pi.rebounds,
            pi.assists,
            pi.minutes_played
        FROM PLAYS_IN pi
        JOIN PLAYER p ON pi.player_id = p.player_id
        WHERE pi.game_id = ?
        ORDER BY pi.points DESC, p.name;
    """
    cur = conn.cursor()
    cur.execute(sql, (game_id,))
    rows = cur.fetchall()
    print_rows(["Player", "Position", "Points", "Rebounds", "Assists", "Minutes"], rows)

def query_coach_for_team_in_season(conn):
    print_header("Query 5: Coach for a Team in a Season")
    print_rows(["Team ID", "Team"], list_teams(conn))
    print_rows(["Season ID", "Season"], list_seasons(conn))
    team_id = input("Enter a Team ID: ").strip()
    season_id = input("Enter a Season ID: ").strip()

    sql = """
        SELECT
            c.coach_id,
            c.name,
            t.city || ' ' || t.name AS team_name,
            s.year
        FROM COACHES ch
        JOIN COACH c ON ch.coach_id = c.coach_id
        JOIN TEAM t ON ch.team_id = t.team_id
        JOIN SEASON s ON ch.season_id = s.season_id
        WHERE ch.team_id = ? AND ch.season_id = ?;
    """
    cur = conn.cursor()
    cur.execute(sql, (team_id, season_id))
    rows = cur.fetchall()
    print_rows(["Coach ID", "Coach Name", "Team", "Season"], rows)

def main():
    if not DB_PATH.exists():
        print(f"Database file not found at: {DB_PATH}")
        return

    conn = connect_db()
    print_header("NBA Statistics and Game Tracking Database - Command Line Interface")
    print("This custom interface uses raw SQL queries executed through Python's sqlite3 module.")
    print(f"Active database: {DB_PATH}")

    while True:
        print("\nChoose an option:")
        print("1. Show players on a selected team in a selected season")
        print("2. Show all games for a selected team in a selected season")
        print("3. Show statistics for a selected player across games")
        print("4. Show player box score for a selected game")
        print("5. Show coach for a selected team in a selected season")
        print("6. Show reference data (teams, seasons, players, games)")
        print("0. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            query_players_on_team_in_season(conn)
        elif choice == "2":
            query_games_for_team_in_season(conn)
        elif choice == "3":
            query_player_stats(conn)
        elif choice == "4":
            query_box_score_for_game(conn)
        elif choice == "5":
            query_coach_for_team_in_season(conn)
        elif choice == "6":
            show_reference_data(conn)
        elif choice == "0":
            print("Exiting the interface.")
            conn.close()
            break
        else:
            print("Invalid choice. Please enter a number from the menu.")

if __name__ == "__main__":
    main()
