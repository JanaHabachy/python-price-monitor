# scraper.py
import requests
from bs4 import BeautifulSoup
import re
import time
import pandas as pd

def scrape_prices(pages=5):

    data = []

    for page in range(1, pages + 1):
        url = f"https://books.toscrape.com/catalogue/page-{page}.html"

        try:
            response = requests.get(url)
            response.raise_for_status()  # raise error if request fails
        except Exception as e:
            print(f"Failed to fetch page {page}: {e}")
            continue

        soup = BeautifulSoup(response.text, "html.parser")
        books = soup.find_all("article", class_="product_pod")
        time.sleep(1)  # polite scraping

        for book in books:
            title = book.h3.a["title"]
            price_text = book.find("p", class_="price_color").text
            price = float(re.sub(r"[^\d.]", "", price_text))
            data.append({"title": title, "price": price})

        print(f"Page {page} scraped")

    print(f"\nTotal products scraped: {len(data)}")
    return data