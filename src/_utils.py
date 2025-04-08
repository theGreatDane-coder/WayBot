from pathlib import Path
from datetime import datetime
import csv
from typing import Dict
import random

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

def init_csv_file() -> None:
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
            writer.writerow(CSV_HEADERS + ["lat", "lon"])
        print("CSV file initialized.")


def save_message_to_csv(message: Dict, lat: float, lon: float) -> None:
    """
    Appends the extracted message data to the CSV log.
    """
    row = extract_message_data(message)
    row = row + [lat, lon]
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
        datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S") if header == "timestamp" else deep_get(message, header)
        for header in CSV_HEADERS
    ]

def extract_coordinates(message: Dict) -> tuple[float, float]:
    """
    TODO: find way to extract coordinates
    """

    if message:

        athens_coords: list[tuple[float, float]] = [
            # 🏛️ Central Athens
            (37.9751, 23.7350),  # Panepistimiou St
            (37.9765, 23.7376),  # Mitropoleos St
            (37.9743, 23.7309),  # Stadiou St

            # 🌳 Kifisia (North)
            (38.0724, 23.8113),  # Kifisias Ave
            (38.0792, 23.8117),  # Charilaou Trikoupi St

            # 🛍️ Marousi
            (38.0503, 23.8044),  # Agiou Konstantinou St

            # 🧊 Chalandri
            (38.0166, 23.8006),  # Andrea Papandreou St
            (38.0193, 23.7917),  # Kifisias Ave

            # 🌲 Melissia
            (38.0571, 23.8336),  # Dimokratias Ave

            # 🛳️ Piraeus
            (37.9436, 23.6469),  # Akti Miaouli
            (37.9412, 23.6537),  # Grigoriou Labraki

            # 🚛 Keratsini
            (37.9611, 23.6197),  # Pavlou Mela St

            # 🏖️ Glyfada
            (37.8781, 23.7552),  # Grigoriou Lampraki St
            (37.8742, 23.7544),  # Lazaraki St

            # 🌊 Voula
            (37.8431, 23.7741),  # Vasileos Pavlou St

            # 🏄 Alimos
            (37.9102, 23.7153),  # Kalamakiou Ave

            # 🏠 Nea Smyrni
            (37.9458, 23.7126),  # Eleftheriou Venizelou Ave

            # 🧱 Nea Ionia
            (38.0353, 23.7601),  # Heraklion Ave

            # 🌇 Galatsi
            (38.0135, 23.7550),  # Veikou Ave

            # 🏭 Menidi (Acharnes)
            (38.0810, 23.7382),  # Karamanli Ave

            # 🧿 Agia Paraskevi
            (38.0165, 23.8277),  # Mesogeion Ave

            # 🏔️ Ilioupoli
            (37.9277, 23.7523),  # Eleftheriou Venizelou Ave

            # 🛣️ Argiroupoli
            (37.9052, 23.7286),  # Vouliagmenis Ave

            # 🌆 Nea Filadelfeia
            (38.0307, 23.7336),  # Dekeleias Ave

            # 🛒 Peristeri
            (38.0147, 23.6885),  # Thivon Ave

            # 🔧 Petroupoli
            (38.0372, 23.6845),  # 25 Martiou St

            # 🚦 Egaleo
            (37.9926, 23.6793),  # Iera Odos

            # 🎯 Zografou
            (37.9753, 23.7656),  # Olof Palme St
        ]

        # Pick one at random
        random_coord = random.choice(athens_coords)
        return random_coord