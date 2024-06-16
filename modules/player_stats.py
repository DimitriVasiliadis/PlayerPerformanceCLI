# in here will be the display function of the specific module. this allows for me to modularely customize each categorys display to correctly reflect the data
# we also handle the database updating in this file. We request from the Valorant API when the program is first executed. We have certain api requests for the data required to calculate and culminate
# all the data we want to reflect. we then store that given information in the hystorical database table based on how we recieve it from the Valorant API. We can then reflect that historical data to 
# our current table to display on the modules display function. the display function will pull the data from the current tables data to reflect in its display.
# we also need the description to be displayed in the modular main menu display for the base functionality of the program.

#functionality should be such that we can just remove a module file and it wont effect the program at all. it is all abstracted out such that it builds a custom application based on the modules present

import sqlite3
import requests


DESCRIPTION = "Player Statistics"


class PlayerStatsHandler:
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def fetch_current_stats(self, player_id):
        """Fetch current player statistics from the local database."""
        self.cursor.execute('''
            SELECT player_name, current_rating, peak_rating, accuracy_head, accuracy_body, accuracy_legs
            FROM current_stats
            WHERE player_id = ?
        ''', (player_id,))
        return self.cursor.fetchone()

    def display_player_stats(self, player_id):
        """Display player statistics."""
        player_stats = self.fetch_current_stats(player_id)
        if player_stats:
            print("Player Statistics:")
            print(f"Player Name: {player_stats[0]}")
            print(f"Current Rating: {player_stats[1]}")
            print(f"Peak Rating: {player_stats[2]}")
            print(f"Accuracy - Head: {player_stats[3]}%")
            print(f"Accuracy - Body: {player_stats[4]}%")
            print(f"Accuracy - Legs: {player_stats[5]}%")
        else:
            print("Player stats not found.")

    def update_player_stats(self, player_id):
        """Update player statistics by fetching data from the API."""
        # Perform API request to fetch player stats
        api_url = f"https://api.valorant.com/v1/players/{player_id}"
        headers = {'Authorization': 'Bearer YOUR_API_TOKEN'}
        response = requests.get(api_url, headers=headers)

        if response.status_code == 200:
            player_data = response.json()

            # Extract relevant stats from API response
            player_name = player_data.get('player_name')
            current_rating = player_data.get('current_rating')
            peak_rating = player_data.get('peak_rating')
            accuracy_head = player_data.get('accuracy', {}).get('head', 0.0)
            accuracy_body = player_data.get('accuracy', {}).get('body', 0.0)
            accuracy_legs = player_data.get('accuracy', {}).get('legs', 0.0)

            # Update or insert into current_stats table
            self.cursor.execute('''
                INSERT OR REPLACE INTO current_stats (player_id, player_name, current_rating, peak_rating,
                                                     accuracy_head, accuracy_body, accuracy_legs)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (player_id, player_name, current_rating, peak_rating, accuracy_head, accuracy_body, accuracy_legs))
            self.conn.commit()

            # Log historical stats
            self.cursor.execute('''
                INSERT INTO historical_stats (player_id, timestamp, rating, accuracy_head, accuracy_body, accuracy_legs)
                VALUES (?, CURRENT_TIMESTAMP, ?, ?, ?, ?)
            ''', (player_id, current_rating, accuracy_head, accuracy_body, accuracy_legs))
            self.conn.commit()

            print("Player stats updated successfully.")
        else:
            print(f"Failed to fetch player stats. Status code: {response.status_code}")

    def close_connection(self):
        """Close the database connection."""
        self.conn.close()

