import requests
import os
import pandas as pd
import re
import time
import matplotlib.pyplot as plt
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


def generate_price_charts():

    history_file = "data/price_history.csv"

    if not os.path.exists(history_file):
        print("No price history found. Skipping charts.")
        return

    df = pd.read_csv(history_file)

    df['date'] = pd.to_datetime(df['date'])

    os.makedirs("reports/charts", exist_ok=True)

    products = df['title'].unique()

    for product in products:

        product_df = df[df['title'] == product].sort_values('date')

        plt.figure(figsize=(8,4))
        plt.plot(product_df['date'], product_df['price'], marker='o')
        plt.title(f'Price Trend: {product}')
        plt.xlabel('Date')
        plt.ylabel('Price (£)')
        plt.xticks(rotation=45)
        plt.tight_layout()

        # sanitize filename for Windows
        safe_title = re.sub(r'[\\/*?:"<>|]', "_", product[:50])
        file_name = f"reports/charts/{safe_title}.png"

        plt.savefig(file_name)
        plt.close()

    print(f"Generated charts for {len(products)} products")

    history_file = "data/price_history.csv"

    if not os.path.exists(history_file):
        print("No price history found. Skipping charts.")
        return

    df = pd.read_csv(history_file)

    # Convert date to datetime
    df['date'] = pd.to_datetime(df['date'])

    # Ensure reports folder exists
    os.makedirs("reports/charts", exist_ok=True)

    products = df['title'].unique()

    for product in products:

        product_df = df[df['title'] == product].sort_values('date')

        plt.figure(figsize=(8,4))
        plt.plot(product_df['date'], product_df['price'], marker='o')
        plt.title(f'Price Trend: {product}')
        plt.xlabel('Date')
        plt.ylabel('Price (£)')
        plt.xticks(rotation=45)
        plt.tight_layout()

        file_name = f"reports/charts/{product[:50].replace('/', '_')}.png"
        plt.savefig(file_name)
        plt.close()

    print(f"Generated charts for {len(products)} products")



def main():

    # Ensure folders exist
    os.makedirs("reports", exist_ok=True)
    os.makedirs("data", exist_ok=True)

    print("Starting price monitor...\n")

    data = scrape_prices()

    save_report(data)

    changes = check_price_changes(data)

    if not changes.empty:

        message = f"""Price changes detected!{changes.to_string(index=False)}"""

        print("Price change detected! Sending email alert...")

        send_email(message)

    else:

        print("No price changes detected.")

    save_current_prices(data)

    print("\nPrice monitoring completed.")

    generate_price_charts()


if __name__ == "__main__":
    main()