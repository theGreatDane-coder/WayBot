from pathlib import Path
from datetime import datetime
import csv
from typing import Dict

BASE_DIR = Path(__file__).resolve().parent.parent
CSV_FILE = BASE_DIR / "db" / "messages.csv"
CSV_HEADERS = [
    "message_id",
    "timestamp",
    "from.first_name",
    "from.last_name",
    "from.id",
    "text"
]

def init_csv_file():
    """
    Ensures the 'db/messages.csv' file is ready to use.
    - Creates the parent folder if it doesn't exist
    - Creates the file if missing
    - Adds header row on first creation
    """
    CSV_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not CSV_FILE.exists():
        with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(CSV_HEADERS)
        print("CSV file initialized.")


def save_message_to_csv(message: Dict):
    """
    Appends the extracted message data to the CSV log.
    """
    row = extract_message_data(message)

    with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(row)
    print(f"📩 Logged message from {row[2]}: {row[3]}")


def extract_message_data(message: Dict) -> list[str]:
    """
    Extracts values from the Telegram message based on CSV_HEADERS.
    Supports dot notation for nested fields (e.g. 'from.first_name').
    Returns a list of values in header order.
    """
    def deep_get(data: dict, header: str) -> str:
        """
        Safely get a nested value from a dictionary using dot notation.
        Example: deep_get(message, "from.first_name") → "Kostas"
        """
        keys = header.split(".")  # Split 'from.first_name' into ['from', 'first_name']

        for key in keys:
            # If the current level is a dictionary, get the next level
            if isinstance(data, dict):
                data = data.get(key, "")  # Use .get to avoid crashes
            else:
                return ""  # If it's not a dict, stop and return empty string

        return str(data)  # Always return a string (safe for CSV)

    return [
        datetime.utcnow().isoformat() if header == "timestamp" else deep_get(message, header)
        for header in CSV_HEADERS
    ]