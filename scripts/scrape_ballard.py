"""
Scraper for Martha Ballard's Diary on dohistory.org

How it works:
  1. Start at the first _txt.html page and follow "next page" links to
     discover every page chunk (pages cover irregular date ranges, ~20 entries each)
  2. For each chunk, fetch the corresponding _print.html (same filename, no nav noise)
  3. Parse entries using bare day numbers as delimiters (e.g. "23" alone on a line)
  4. Save results to data/ballard_diary.csv

Run:
  pip install requests beautifulsoup4
  python scripts/scrape_ballard.py
"""

import csv
import re
import time
from datetime import date
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

# --- Config ------------------------------------------------------------------

FIRST_PAGE = "https://dohistory.org/diary/1785/01/17850101_txt.html"
OUTPUT = Path(__file__).parent.parent / "data" / "ballard_diary.csv"
DELAY_SECONDS = 1.0  # be polite — one request per second

# --- Helpers -----------------------------------------------------------------


def next_txt_url(html: str, current_url: str) -> str | None:
    """
    Find the 'next page' link in a _txt.html page and return its absolute URL.
    Returns None when we've reached the last page.
    """
    soup = BeautifulSoup(html, "html.parser")
    # The next page link has the text "next page" (case-insensitive)
    link = soup.find("a", string=re.compile(r"next\s+page", re.IGNORECASE))
    if link and link.get("href"):
        return urljoin(current_url, link["href"])
    return None


def print_url_from_txt(txt_url: str) -> str:
    """Convert a _txt.html URL to its _print.html equivalent."""
    return txt_url.replace("_txt.html", "_print.html")


def parse_date_range(html: str) -> tuple[int, int, int] | None:
    """
    Extract the start year and month from the page title, e.g.
    'Martha Ballard's Diary, January 1 - 22, 1785 (P)' → (1785, 1)
    Returns (year, month, start_day) or None if not found.
    """
    soup = BeautifulSoup(html, "html.parser")
    title = soup.find("title")
    if not title:
        return None
    text = title.get_text()
    # Match patterns like "January 1 - 22, 1785" or "January 23 - February 15, 1785"
    months = {
        "jan": 1, "feb": 2, "mar": 3, "apr": 4,
        "may": 5, "jun": 6, "jul": 7, "aug": 8,
        "sep": 9, "oct": 10, "nov": 11, "dec": 12,
    }
    m = re.search(
        r"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z.]*"
        r"\s+(\d{1,2})",
        text, re.IGNORECASE
    )
    year_m = re.search(r"\b(1[78]\d{2})\b", text)
    if m and year_m:
        month = months[m.group(1).lower()[:3]]
        day = int(m.group(2))
        year = int(year_m.group(1))
        return year, month, day
    return None


def parse_entries(html: str, year: int, start_month: int, start_day: int) -> list[dict]:
    """
    Extract diary entries from a _print.html page.

    Entry structure on the print page:
        DAY_NUMBER          ← bare integer on its own line (e.g. "23")
        [REF]               ← bracketed page/column reference (e.g. "[1]")
        entry text...

    The day number resets to 1 when crossing a month boundary within the chunk.
    We track month rollovers using the start_month and start_day.
    """
    soup = BeautifulSoup(html, "html.parser")
    full_text = soup.get_text(separator="\n")

    # Match a bare day number (1-31) on its own line
    day_marker = re.compile(r"^(\d{1,2})\s*$", re.MULTILINE)
    markers = list(day_marker.finditer(full_text))

    entries = []
    current_month = start_month
    current_year = year
    prev_day = start_day - 1  # will be updated on first marker

    # Attribution footer that appears after the last entry on every print page
    footer_pattern = re.compile(
        r"\s*Source:\s*www\.doHistory\.org.*$", re.IGNORECASE | re.DOTALL
    )

    for i, match in enumerate(markers):
        day = int(match.group(1))

        # Detect month rollover: day dropped back (e.g. 31 → 1)
        if day < prev_day:
            if current_month == 12:
                current_month = 1
                current_year += 1
            else:
                current_month += 1
        prev_day = day

        # Grab text until the next day marker (or end of page)
        start = match.end()
        end = markers[i + 1].start() if i + 1 < len(markers) else len(full_text)
        text = full_text[start:end]

        # Remove the [REF] bracket at the start (page/column reference)
        text = re.sub(r"^\s*\[\s*\d*\s*\]\s*", "", text)

        # Strip attribution footer (only present on the last entry of each page)
        text = footer_pattern.sub("", text)

        # Clean up whitespace
        text = re.sub(r"\s+", " ", text).strip()

        if not text:
            continue

        try:
            entry_date = date(current_year, current_month, day)
        except ValueError:
            continue

        entries.append({
            "date": entry_date.isoformat(),
            "text": text,
        })

    return entries


def _sort_csv(path: Path):
    """Re-write the CSV sorted by date ascending."""
    import csv as _csv
    with open(path, newline="", encoding="utf-8") as f:
        rows = list(_csv.DictReader(f))
    rows.sort(key=lambda r: r["date"])
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = _csv.DictWriter(f, fieldnames=["date", "text"])
        writer.writeheader()
        writer.writerows(rows)


# --- Main --------------------------------------------------------------------


def scrape():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (research/educational scraper; Martha Ballard diary)"
    })

    total_entries = 0
    page_count = 0
    txt_url = FIRST_PAGE

    with open(OUTPUT, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["date", "text"])
        writer.writeheader()

        while txt_url:
            page_count += 1
            print(f"[{page_count}] {txt_url} ... ", end="", flush=True)

            # Fetch the _txt.html page (for navigation only)
            try:
                txt_resp = session.get(txt_url, timeout=15)
                txt_resp.raise_for_status()
            except requests.RequestException as e:
                print(f"ERROR fetching txt: {e}")
                break

            # Find next page before moving on
            next_url = next_txt_url(txt_resp.text, txt_url)

            # Fetch the cleaner _print.html version for parsing
            print_url = print_url_from_txt(txt_url)
            try:
                print_resp = session.get(print_url, timeout=15)
                print_resp.raise_for_status()
            except requests.RequestException as e:
                print(f"ERROR fetching print: {e}")
                txt_url = next_url
                time.sleep(DELAY_SECONDS)
                continue

            # Parse the date range from the print page title
            date_info = parse_date_range(print_resp.text)
            if date_info:
                year, month, start_day = date_info
                entries = parse_entries(print_resp.text, year, month, start_day)
            else:
                print("WARN: could not parse date range")
                entries = []

            writer.writerows(entries)
            total_entries += len(entries)
            print(f"{len(entries)} entries")

            txt_url = next_url
            time.sleep(DELAY_SECONDS)

    print(f"\nDone. {page_count} pages, {total_entries} total entries → {OUTPUT}")
    print("Sorting by date...", end=" ", flush=True)
    _sort_csv(OUTPUT)
    print("done.")


if __name__ == "__main__":
    scrape()
