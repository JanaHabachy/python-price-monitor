# price_monitor.py
import os
import pandas as pd
import re
import matplotlib.pyplot as plt
from datetime import datetime
from send_email import send_email
from send_telegram import send_telegram
from scraper import scrape_prices  # Import from scraper.py

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
    df["date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file_path = "data/price_history.csv"
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
        safe_title = re.sub(r'[\\/*?:"<>|]', "_", product[:50])
        file_name = f"reports/charts/{safe_title}.png"
        plt.savefig(file_name)
        plt.close()

    print(f"Generated charts for {len(products)} products")

def main():
    # Ensure folders exist
    os.makedirs("reports", exist_ok=True)
    os.makedirs("data", exist_ok=True)

    print("Starting price monitor...\n")

    send_telegram("Test message: Telegram notifications are working.")

    data = scrape_prices()  # now uses scraper.py

    save_report(data)

    changes = check_price_changes(data)

    if not changes.empty:
        message = f"""Price changes detected! {changes.to_string(index=False)}"""
        print("Price change detected! Sending notifications...")
        send_email(message)
        send_telegram(message)
        print("Email and Telegram alerts sent.")
    else:
        print("No price changes detected.")

    save_current_prices(data)

    print("\nPrice monitoring completed.")

    generate_price_charts()

if __name__ == "__main__":
    main()