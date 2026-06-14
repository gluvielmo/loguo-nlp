import csv
import re
import time
import requests
import sys

from datetime import datetime
from pathlib import Path

API_URL      = "http://localhost:3000/api/entry"
ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiIsImtpZCI6InJ0bWNpQWRaRzM1cm1GTEkiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2JzZ2J1ZmV6bXhnaWl1eGtzZ2dsLnN1cGFiYXNlLmNvL2F1dGgvdjEiLCJzdWIiOiI5NDE5ZGY5Ny01YzIwLTRlMjktYWNjOC05ODBlMjVlNmZmYzYiLCJhdWQiOiJhdXRoZW50aWNhdGVkIiwiZXhwIjoxNzc4MzgzNzM2LCJpYXQiOjE3NzgzODAxMzYsImVtYWlsIjoicGFuZGVtaWNAZXhhbXBsZS5jb20iLCJwaG9uZSI6IiIsImFwcF9tZXRhZGF0YSI6eyJwcm92aWRlciI6ImVtYWlsIiwicHJvdmlkZXJzIjpbImVtYWlsIl19LCJ1c2VyX21ldGFkYXRhIjp7ImVtYWlsIjoicGFuZGVtaWNAZXhhbXBsZS5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiZnVsbF9uYW1lIjoiUGFuZGVtaWMgSm91cm5hbCIsInBob25lX3ZlcmlmaWVkIjpmYWxzZSwic3ViIjoiOTQxOWRmOTctNWMyMC00ZTI5LWFjYzgtOTgwZTI1ZTZmZmM2In0sInJvbGUiOiJhdXRoZW50aWNhdGVkIiwiYWFsIjoiYWFsMSIsImFtciI6W3sibWV0aG9kIjoicGFzc3dvcmQiLCJ0aW1lc3RhbXAiOjE3NzgzODAxMzZ9XSwic2Vzc2lvbl9pZCI6IjY2YzBkNTUzLTlhNTktNDE4OS1hZmE0LTRkN2M1ZTg0M2Y3OCIsImlzX2Fub255bW91cyI6ZmFsc2V9.SpXYE7np1DC8SuPZbOOMdBlwtLkcN9K95l-UUqTBBHA"
EXPIRES_AT   = 1778383736
CSV_PATH     = Path(__file__).parent.parent / "data" / "pandemic_entries.csv"
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

    with open(csv_path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    rows = [
        r for r in rows
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