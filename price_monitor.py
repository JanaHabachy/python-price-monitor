import requests
import os
import pandas as pd
import re
import time
from datetime import datetime
from bs4 import BeautifulSoup
from send_email import send_email


def scrape_prices():

    data = []

    for page in range(1, 6):   # scrape first 5 pages

        url = f"https://books.toscrape.com/catalogue/page-{page}.html"

        response = requests.get(url)

        soup = BeautifulSoup(response.text, "html.parser")

        books = soup.find_all("article", class_="product_pod")

        time.sleep(1)

        for book in books:

            title = book.h3.a["title"]

            price_text = book.find("p", class_="price_color").text
            price = float(re.sub(r"[^\d.]", "", price_text))

            data.append({
                "title": title,
                "price": price
            })

        print(f"Page {page} scraped")

    print(f"\nTotal products scraped: {len(data)}")

    return data


def save_report(data):

    df = pd.DataFrame(data)

    report_path = "reports/price_report.xlsx"

    df.to_excel(report_path, index=False)

    print(f"Report saved to {report_path}")


def check_price_changes(data):

    file_path = "data/price_history.csv"

    if not os.path.exists(file_path):

        return pd.DataFrame()

    history = pd.read_csv(file_path)

    latest = history.sort_values("date").groupby("title").tail(1)

    current = pd.DataFrame(data)

    merged = current.merge(latest, on="title", suffixes=("_new", "_old"))

    changes = merged[merged["price_new"] != merged["price_old"]]

    return changes


def save_current_prices(data):

    df = pd.DataFrame(data)

    # add timestamp
    df["date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    file_path = "data/price_history.csv"

    # append instead of overwrite
    if os.path.exists(file_path):

        df.to_csv(file_path, mode="a", header=False, index=False)

    else:

        df.to_csv(file_path, index=False)

    print("Price history updated.")


def main():

    # Ensure folders exist
    os.makedirs("reports", exist_ok=True)
    os.makedirs("data", exist_ok=True)

    print("Starting price monitor...\n")

    data = scrape_prices()

    save_report(data)

    changes = check_price_changes(data)

    if not changes.empty:

        message = f"""
Price changes detected!

{changes.to_string(index=False)}
"""

        print("Price change detected! Sending email alert...")

        send_email(message)

    else:

        print("No price changes detected.")

    save_current_prices(data)

    print("\nPrice monitoring completed.")


if __name__ == "__main__":
    main()