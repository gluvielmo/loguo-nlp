import csv
import re
import time
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://pjp-featuredentries.core.uconn.edu/"
TOTAL_PAGES = 86
OUTPUT_FILE = "data/pandemic_entries.csv"


def scrape_page(session, page):
    resp = session.get(BASE_URL, params={"page": page, "type": "text_only"}, timeout=15)
    resp.raise_for_status()
    resp.encoding = "utf-8"
    soup = BeautifulSoup(resp.text, "html.parser")

    entries = []
    cards = soup.find_all(class_="card")
    for card in cards:
        date_el = card.find(class_="text-muted")
        text_el = card.find(class_="card-text")
        if not date_el or not text_el:
            continue
        date = date_el.get_text(strip=True)
        raw = text_el.get_text(separator=" ", strip=True)
        text = re.sub(r"<[^>]+>", "", raw).strip()
        entries.append((date, text))
    return entries


def main():
    session = requests.Session()
    session.headers["User-Agent"] = "Mozilla/5.0 (research scraper)"

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["date", "text"])

        for page in range(1, TOTAL_PAGES + 1):
            print(f"Scraping page {page}/{TOTAL_PAGES}...", end=" ")
            try:
                entries = scrape_page(session, page)
                writer.writerows(entries)
                print(f"{len(entries)} entries")
            except Exception as e:
                print(f"ERROR: {e}")
            time.sleep(0.5)

    print(f"Done. Output saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
