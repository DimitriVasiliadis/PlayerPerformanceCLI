# make this modular so that the database is built based on what the modules say data they need stored
# modules will add to current_stats and historcial_stats as needed. they will be flexable to be adjusted and added to on the fly without missing a beat or needing to be reset
# database completely dictated by the modules and this file will be for building the table based on what the modules say they need stored
# make the database updateable with one click (basically will just restart the program which will in term update the database). make the database resetable with one button and a confirmation

# only handles setup. data_handler and modules will handle specifics for each functionality
import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('player_stats.db')
cursor = conn.cursor()

# Create tables if they don't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS current_stats (
        id INTEGER PRIMARY KEY,
        player_id TEXT UNIQUE,
        player_name TEXT,
        current_rating INTEGER,
        peak_rating INTEGER,
        accuracy_head REAL,
        accuracy_body REAL,
        accuracy_legs REAL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS historical_stats (
        id INTEGER PRIMARY KEY,
        player_id TEXT,
        timestamp TEXT,
        rating INTEGER,
        accuracy_head REAL,
        accuracy_body REAL,
        accuracy_legs REAL,
        FOREIGN KEY (player_id) REFERENCES current_stats(player_id)
    )
''')

conn.commit()