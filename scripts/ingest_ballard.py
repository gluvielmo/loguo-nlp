import csv
import re
import time
import requests
import sys

from datetime import datetime
from pathlib import Path

API_URL      = "http://localhost:3000/api/entry"
ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiIsImtpZCI6InJ0bWNpQWRaRzM1cm1GTEkiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2JzZ2J1ZmV6bXhnaWl1eGtzZ2dsLnN1cGFiYXNlLmNvL2F1dGgvdjEiLCJzdWIiOiI3NzdiMDg1Yy04YjI3LTRiOTUtOTNlOC1lODY4MDJkZGU3NTMiLCJhdWQiOiJhdXRoZW50aWNhdGVkIiwiZXhwIjoxNzc4MzAwODc2LCJpYXQiOjE3NzgyOTcyNzYsImVtYWlsIjoibWFydGhhQGV4YW1wbGUuY29tIiwicGhvbmUiOiIiLCJhcHBfbWV0YWRhdGEiOnsicHJvdmlkZXIiOiJlbWFpbCIsInByb3ZpZGVycyI6WyJlbWFpbCJdfSwidXNlcl9tZXRhZGF0YSI6eyJlbWFpbCI6Im1hcnRoYUBleGFtcGxlLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJmdWxsX25hbWUiOiJNYXJ0aGEgQmFsbGFyZCIsInBob25lX3ZlcmlmaWVkIjpmYWxzZSwic3ViIjoiNzc3YjA4NWMtOGIyNy00Yjk1LTkzZTgtZTg2ODAyZGRlNzUzIn0sInJvbGUiOiJhdXRoZW50aWNhdGVkIiwiYWFsIjoiYWFsMSIsImFtciI6W3sibWV0aG9kIjoicGFzc3dvcmQiLCJ0aW1lc3RhbXAiOjE3NzgyOTcyNzZ9XSwic2Vzc2lvbl9pZCI6Ijk3ZmNiNzE3LWVkMGMtNDMyZC1iZmM1LWQzZjE2MjkwMTc0MSIsImlzX2Fub255bW91cyI6ZmFsc2V9.Sp1taAVKpEp4mDiwMGjWpVvOcOU5WQ177C-AQnUk8Ew"
EXPIRES_AT   = 1778300876
CSV_PATH     = Path(__file__).parent.parent / "data" / "ballard_diary.csv"
DELAY_SEC    = 0.3

HEADERS = {
    "Content-Type":  "application/json",
    "Authorization": f"Bearer {ACCESS_TOKEN}",
}

def check_token():
    now = int(datetime.now().timestamp())

    remaining = EXPIRES_AT - now

    if remaining < 300:
        print(f"Token expires in {remaining}s — re-authenticate first")
        sys.exit(1)
    print(f"Token valid for {remaining // 60}m {remaining % 60}s")

def clean_entry(text: str) -> str:
    text = re.sub(r'\[.*?\]', '', text)
    text = re.sub(r'  +', ' ', text)

    return text.strip()

def ingest(csv_path: str):
    check_token()

    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    rows = [
        r for r in rows
        if r.get("date", "").startswith(("1793", "1794", "1795", "1796"))
    ]
    rows = rows[:500]

    total = len(rows)
    success = 0
    failed = []

    print(f"Ingesting {total} entries...\n")

    for i, row in enumerate(rows):
        content = clean_entry(row.get("text", ""))

        if not content:
            print(f"[{i+1}/{total}] Skipping empty entry")
            continue

        try:
            res = requests.post(
                API_URL,
                json={"content": content, "tags": []},
                headers=HEADERS,
            )

            if res.status_code == 200:
                success += 1
                print(f"[{i+1}/{total}] ✓  {row.get('date', 'unknown date')}")
            elif res.status_code == 401:
                print("401 Unauthorized — token likely expired, stopping")
                sys.exit(1)
            else:
                print(f"[{i+1}/{total}] ✗  {res.status_code} — {res.text[:80]}")
                failed.append({"index": i, "date": row.get("date"), "reason": res.text})

        except requests.exceptions.Timeout:
            print(f"[{i+1}/{total}] ✗  Timeout — skipping")
            failed.append({"index": i, "date": row.get("date"), "reason": "timeout"})

        except requests.exceptions.RequestException as e:
            print(f"[{i+1}/{total}] ✗  Request error: {e}")
            failed.append({"index": i, "date": row.get("date"), "reason": str(e)})

        time.sleep(DELAY_SEC)

# summary

    print(f"\n{'─'*40}")
    print(f"Done: {success}/{total} succeeded")

    if failed:
        print(f"Failed: {len(failed)} entries")
        for entry in failed[:10]:
            print(f"  [{entry['index']}] {entry['date']} — {entry['reason'][:60]}")
        if len(failed) > 10:
            print(f"  ... and {len(failed) - 10} more")

        with open("failed_entries.csv", "w", newline="") as out:
            writer = csv.DictWriter(out, fieldnames=["index", "date", "reason"])
            writer.writeheader()
            writer.writerows(failed)
        print("Failed entries saved to failed_entries.csv")


if __name__ == "__main__":
    ingest(CSV_PATH)