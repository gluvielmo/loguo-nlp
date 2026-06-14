"""
Scrape dooce.com archive entries into a CSV.

How it works:
  1. Fetch each yearly archive page for 2009 through 2023.
  2. Collect every linked post URL and its archive date from the year page.
  3. Fetch each post page and extract the title plus cleaned body text.
  4. Save results to data/dooce_2009_2023.csv

Cleaning rules:
  - Remove images and image wrappers
  - Remove entry footer/navigation noise
  - Preserve visible anchor text but drop URLs
  - Collapse whitespace while keeping paragraph breaks

Run:
  python scripts/scrape_dooce.py
"""

from __future__ import annotations

import csv
import re
import time
from collections import OrderedDict
from datetime import datetime
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from bs4.element import NavigableString, Tag

BASE_URL = "https://dooce.com"
START_YEAR = 2009
END_YEAR = 2023
OUTPUT = Path(__file__).parent.parent / "data" / "dooce_2009_2023.csv"
DELAY_SECONDS = 0.75
TIMEOUT_SECONDS = 20


def archive_url(year: int) -> str:
    return f"{BASE_URL}/archives-{year}/"


def clean_text(value: str) -> str:
    value = value.replace("\xa0", " ")
    value = re.sub(r"[ \t\r\f\v]+", " ", value)
    value = re.sub(r"\n{3,}", "\n\n", value)
    return value.strip()


def parse_archive_entries(html: str, current_year: int) -> list[dict[str, str]]:
    soup = BeautifulSoup(html, "html.parser")
    content = soup.find("main", id="content") or soup
    results: list[dict[str, str]] = []

    date_pattern = re.compile(r"^\d{2}-[A-Za-z]{3}-\d{4}$")

    for anchor in content.find_all("a", href=True):
        href = urljoin(BASE_URL, anchor["href"])
        title = clean_text(anchor.get_text(" ", strip=True))
        sibling = anchor.next_sibling

        if not title or f"/{current_year}/" not in href:
            continue
        if not sibling or not isinstance(sibling, NavigableString):
            continue

        sibling_text = re.sub(r"^[^0-9]+|[^0-9A-Za-z-]+$", "", str(sibling).strip())
        if not date_pattern.match(sibling_text):
            continue

        parsed_date = datetime.strptime(sibling_text, "%d-%b-%Y").date().isoformat()
        results.append(
            {
                "archive_date": parsed_date,
                "title": title,
                "url": href,
            }
        )

    # Preserve original order while deduplicating URLs.
    deduped = OrderedDict()
    for result in results:
        deduped.setdefault(result["url"], result)
    return list(deduped.values())


def remove_unwanted_nodes(entry_content: Tag) -> None:
    selectors = [
        "img",
        "script",
        "style",
        "div.drupal_image_wrapper",
        "div.entry-links",
        "figure",
        "figcaption",
        ".sharedaddy",
        ".jp-relatedposts",
    ]
    for selector in selectors:
        for node in entry_content.select(selector):
            node.decompose()

    for anchor in entry_content.find_all("a"):
        if anchor.find("img"):
            anchor.decompose()
            continue

        text = anchor.get_text(" ", strip=True)
        if text:
            anchor.replace_with(NavigableString(text))
        else:
            anchor.decompose()


def extract_blocks(entry_content: Tag) -> list[str]:
    block_tags = {
        "p",
        "blockquote",
        "li",
        "h2",
        "h3",
        "h4",
        "pre",
    }
    blocks: list[str] = []

    for child in entry_content.children:
        if isinstance(child, NavigableString):
            text = clean_text(str(child))
            if text:
                blocks.append(text)
            continue

        if not isinstance(child, Tag):
            continue

        if child.name in {"ul", "ol"}:
            for item in child.find_all("li", recursive=False):
                text = clean_text(item.get_text(" ", strip=True))
                if text:
                    blocks.append(text)
            continue

        if child.name in block_tags:
            text = clean_text(child.get_text(" ", strip=True))
            if text:
                blocks.append(text)
            continue

        text = clean_text(child.get_text(" ", strip=True))
        if text:
            blocks.append(text)

    deduped_blocks: list[str] = []
    for block in blocks:
        if not deduped_blocks or deduped_blocks[-1] != block:
            deduped_blocks.append(block)
    return deduped_blocks


def parse_post(html: str, url: str) -> dict[str, str]:
    soup = BeautifulSoup(html, "html.parser")
    article = soup.find("article", class_=re.compile(r"\bpost\b"))
    if not article:
        raise ValueError(f"Could not find article on {url}")

    title_el = article.find("h1", class_="entry-title")
    date_el = article.find(class_="entry-date")
    content_el = article.find("div", class_="entry-content")

    if not title_el or not date_el or not content_el:
        raise ValueError(f"Missing title/date/content on {url}")

    remove_unwanted_nodes(content_el)
    text = "\n\n".join(extract_blocks(content_el))

    date_text = clean_text(date_el.get_text(" ", strip=True))
    parsed_date = datetime.strptime(date_text, "%B %d, %Y").date().isoformat()

    return {
        "date": parsed_date,
        "title": clean_text(title_el.get_text(" ", strip=True)),
        "text": clean_text(text),
        "url": url,
    }


def fetch(session: requests.Session, url: str) -> str:
    response = session.get(url, timeout=TIMEOUT_SECONDS)
    response.raise_for_status()
    response.encoding = "utf-8"
    return response.text


def scrape() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": (
                "Mozilla/5.0 (compatible; dooce archive scraper for research/export)"
            )
        }
    )

    archive_entries: list[dict[str, str]] = []
    for year in range(START_YEAR, END_YEAR + 1):
        url = archive_url(year)
        print(f"Loading archive {year}...", end=" ", flush=True)
        html = fetch(session, url)
        year_entries = parse_archive_entries(html, year)
        archive_entries.extend(year_entries)
        print(f"{len(year_entries)} entries")
        time.sleep(DELAY_SECONDS)

    print(f"Collected {len(archive_entries)} archive links")

    rows: list[dict[str, str]] = []
    failures: list[tuple[str, str]] = []

    for index, entry in enumerate(archive_entries, start=1):
        print(f"[{index}/{len(archive_entries)}] {entry['url']}...", end=" ", flush=True)
        try:
            html = fetch(session, entry["url"])
            row = parse_post(html, entry["url"])
            if row["date"] != entry["archive_date"]:
                print(
                    f"WARN date mismatch archive={entry['archive_date']} post={row['date']}"
                )
            else:
                print("ok")
            rows.append(row)
        except Exception as exc:  # noqa: BLE001
            print(f"ERROR {exc}")
            failures.append((entry["url"], str(exc)))
        time.sleep(DELAY_SECONDS)

    rows.sort(key=lambda row: (row["date"], row["url"]))

    with open(OUTPUT, "w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=["date", "title", "text", "url"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nWrote {len(rows)} rows to {OUTPUT}")
    if failures:
        print(f"{len(failures)} pages failed:")
        for url, error in failures:
            print(f"  - {url}: {error}")


if __name__ == "__main__":
    scrape()
