# Python Price Monitor

## Overview
The **Python Price Monitor** is a script that tracks product prices on [Books to Scrape](https://books.toscrape.com/) and notifies you of changes via **email** and **Telegram**.  
Key features include:  

- Scraping product prices across multiple pages.  
- Saving price history in CSV format.  
- Generating price trend charts for each product.  
- Sending notifications for price changes through **email** and **Telegram**.  
- Robust error handling using `try/except` to prevent crashes.  
- Secure handling of sensitive credentials via `.env` files.  

---

## Features

1. **Scraping & Monitoring**  
   - Fetches product titles and prices from the first 5 pages of the target website.  
   - Detects changes compared to previously stored prices.  

2. **Notifications**  
   - **Email:** Sends a detailed alert to your email when price changes occur.
   - **Telegram:** Sends the same alert via a Telegram bot.

     <img width="590" height="1280" alt="image" src="https://github.com/user-attachments/assets/3e1dab84-e9d0-4156-9838-25968ee3d1d0" />
     <img width="1433" height="866" alt="image" src="https://github.com/user-attachments/assets/7a2354d9-4ffa-4220-ad84-b743b4b839fc" />



3. **Reports & Charts**  
   - Saves product prices to `reports/price_report.xlsx`.  
   - Appends historical prices to `data/price_history.csv`.  
   - Generates charts in `reports/charts` folder showing price trends for each product.  

---

## Installation

### Prerequisites
- Python 3.11+  
- Recommended virtual environment (optional but advised)

### Clone the repository
```bash
git clone https://github.com/yourusername/price-monitor.git
cd price-monitor
