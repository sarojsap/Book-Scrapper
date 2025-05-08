# Scraping data from the site and storing into database.
import requests     # Fetch data from the web (html, json, XML)
from bs4 import BeautifulSoup       
import sqlite3

URL = "https://books.toscrape.com/"

def create_table():
    con = sqlite3.connect("books.sqlite3")
    cursor = con.cursor()
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS books(
            id INTEGER primary key autoincrement,
            title TEXT,
            currency TEXT,
            price REAL
        );
        '''
    )
    con.close()
    print("Database and table created successfully.")

def insert_book(title, currency, price):
    con = sqlite3.connect("books.sqlite3")
    cursor = con.cursor()
    cursor.execute(
        "INSERT INTO books (title, currency, price) VALUES (?, ?, ?)", (title, currency, price)
    )
    con.commit()
    con.close()

def scrape_book(url):
    response = requests.get(url)
    if response.status_code != 200:
        return
    
    # Set encoding explicitly to handle special characters correctly
    response.encoding = response.apparent_encoding
    soup = BeautifulSoup(response.text, "html.parser")
    book_elements = soup.find_all("article", class_="product_pod")
    print(book_elements)
    for book in book_elements:
        title = book.h3.a['title']
        price_text = book.find('p', class_="price_color").text
        currency = price_text[0]
        price = float(price_text[1:])
        print(title, currency, price)
        insert_book(title, currency, price) # Function Call

    print("All data Scraped and Saved Successfully.")

create_table()      # Function calling

# Calling function: scrape_book()        
scrape_book(URL)
