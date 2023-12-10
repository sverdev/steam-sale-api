# -*- coding: utf-8 -*- 
import sqlite3
import requests
from bs4 import BeautifulSoup
import unicodedata, re


def delete_previous_data():
    conn = sqlite3.connect('game_sales.db',check_same_thread=False)
    cursor = conn.cursor()

    # Delete all previous game alerts
    cursor.execute("DELETE FROM game_sales")

    # Commit and close the connection
    conn.commit()
    conn.close()

# Function to crawl and save discount information
def crawl_and_save_discounts():
    # Delete previous data before crawling
    delete_previous_data()

    start_page = 0
    end_page = 3
    whole_source = ""

    for page_number in range(start_page, end_page + 1):
        url = 'https://store.steampowered.com/search/?specials=1&filter=topsellers&page=' + str(page_number)
        response = requests.get(url)
        whole_source += response.text

    soup = BeautifulSoup(whole_source, 'html.parser')
    games = soup.select('div#search_resultsRows > a')

    conn = sqlite3.connect('game_sales.db')
    cursor = conn.cursor()

    for game in games:
        title = game.find('span', class_='title').text.strip()
        release_date = game.find('div', class_='search_released').text.strip()
        discount_price = game.find('div', class_='discount_final_price').text.strip().replace("₩ ", "")
        discount_original_price = game.find('div', class_='discount_original_price').text.strip()
        image_url = game.find('div', class_='search_capsule').find('img')['src']
        game_url = game['href']
        
            # Use regular expression to extract the unique ID from the URL
        match = re.search(r"/apps/(\d+)/", image_url)
        if match:
            unique_id = match.group(1)
            image_url = f'https://cdn.cloudflare.steamstatic.com/steam/apps/{unique_id}/header.jpg'
        else:
            unique_id = None  # You can set it to a default value or handle it as needed


        
        # Insert the data into the database
        cursor.execute("INSERT INTO game_sales (title, release_date, discount_price, discount_original_price, image_url, game_url) VALUES (?, ?, ?, ?, ?, ?)",
                   (title, release_date, discount_price, discount_original_price, image_url, game_url))

    # Commit and close the connection
    conn.commit()
    conn.close()

crawl_and_save_discounts()
