# -*- coding: utf-8 -*- 

from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

# Connect to the database
conn = sqlite3.connect('game_sales.db',check_same_thread=False)
cursor = conn.cursor()

# Define a route to get all game alerts
@app.route('/salegames', methods=['GET'])
def get_game_sales():
    # Get all game alerts from the database
    cursor.execute("SELECT * FROM game_sales")
    game_sales = cursor.fetchall()

    # Convert the game alerts to a JSON object
    game_sales_json = []
    for game_alert in game_sales:
        game_sales_json.append({
            'title': game_alert[0],  # Use the correct index here
            'release_date': game_alert[1],  # Use the correct index here
            'discount_price': game_alert[2],  # Use the correct index here
            'discount_pct': game_alert[3],  # Use the correct index here
            'image_url': game_alert[4],  # Use the correct index here
            'game_url': game_alert[5]  # Use the correct index here

        })

    # Return the JSON object
    return jsonify(game_sales_json)


# Start the API server
if __name__ == '__main__':
    from waitress import serve
    serve(app, host="0.0.0.0", port=5000)