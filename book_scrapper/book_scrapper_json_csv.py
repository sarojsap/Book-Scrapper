# Scraping data from the site and storing into database.
import requests     # Fetch data from the web (html, json, XML)
from bs4 import BeautifulSoup       
import json
import csv

URL = "https://books.toscrape.com/"

def scrape_book(url):
    response = requests.get(url)
    if response.status_code != 200:
        return []
    
    # Set encoding explicitly to handle special characters correctly
    response.encoding = response.apparent_encoding

    soup = BeautifulSoup(response.text, "html.parser")
    book_elements = soup.find_all("article", class_="product_pod")

    books = []
    for book in book_elements:
        title = book.h3.a['title']
        price_text = book.find('p', class_="price_color").text
        currency = price_text[0]
        price = float(price_text[1:])
        # insert_book(title, currency, price)
        books.append({
            'title':title,
            'currency':currency,
            'price':price
        })

    print("All data Scrapped.")
    return books

def save_to_json(books):
    with open('books.json', 'w', encoding="utf-8") as f:
        json.dump(books, f, indent=4, ensure_ascii=False)

def save_to_csv(books):
    with open("books.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["title", "currency", "price"])
        writer.writeheader()
        writer.writerows(books)


books = scrape_book(URL)
save_to_json(books)
save_to_csv(books)