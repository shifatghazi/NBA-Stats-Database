COMP 3005 Final Project - Part 2
NBA Statistics and Game Tracking Database

DATABASE FILE NAME
nba_stats_project.db

DATABASE FILE LOCATION
./nba_stats_project.db

This is the actual SQLite database file for the project. It can be opened directly with the sqlite3 command line tool.

Example:
sqlite3 nba_stats_project.db

USER INTERFACE FILE
nba_cli.py

HOW TO RUN THE CUSTOM INTERFACE
1. Open a terminal in this folder.
2. Run:
   python3 nba_cli.py

ABOUT THE INTERFACE
The project includes a custom command-line interface written in Python using the built-in sqlite3 module.
The code uses raw SQL query strings, so the SQL is visible and is not hidden behind an ORM.

INCLUDED FILES
- nba_stats_project.db      -> actual SQLite database file
- nba_cli.py                -> custom command-line interface
- readme.txt                -> explains where the database is and how to run the project
- setup_database.sql        -> optional helper script used to create/populate the database

NOTES ABOUT THE IMPLEMENTATION
The implemented database follows the project schema and uses similar table/attribute names to the ER model.
For the actual runnable SQLite implementation, GAME includes season_id and INVOLVES includes team_score so that
season-based game queries and final-score style outputs can be demonstrated clearly in the video.

EXAMPLE QUERIES THAT CAN BE PERFORMED
1. Show all players on a selected team in a selected season.
2. Show all games for a selected team in a selected season.
3. Show player statistics across games.
4. Select a game and show the box score for that game.

Youtube Link:
https://youtu.be/wRwGQNm7pAQ
