
# -*- coding: utf-8 -*- 
import sqlite3

def create_database():
    # Create a database connection
    conn = sqlite3.connect('game_sales.db')

    # Create a cursor object
    cursor = conn.cursor()

    # Create a table
    cursor.execute('CREATE TABLE game_sales (title TEXT, release_date TEXT, discount_price TEXT, discount_pct TEXT, image_url TEXT, game_url TEXT)')

    # Commit the changes
    conn.commit()

    # Close the connection
    conn.close()

if __name__ == '__main__':
    create_database()
