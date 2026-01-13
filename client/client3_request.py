import json
import base64
from pathlib import Path
import requests

SERVER_URL = "http://172.16.1.10:8000/encode"

URL = "https://www.techradar.com/phones/android/google-messages-is-getting-a-big-update-in-2026-here-are-the-3-new-whatsapp-style-features-to-look-out-for"

client_dir = Path("./client3")
client_dir.mkdir(parents=True, exist_ok=True)

try:
    response = requests.post(SERVER_URL, json={"url": URL})
    response.raise_for_status()
    data = response.json()

    (client_dir / "original.txt").write_text(data["original_text"], encoding="utf-8")
    (client_dir / "huffman_codes.json").write_text(json.dumps(data["codes"], indent=2), encoding="utf-8")
    encoded_bytes = base64.b64decode(data["encoded_b64"])
    (client_dir / "encoded_data.bin").write_bytes(encoded_bytes)

    print(f"Datoteke za client3 spremljene u {client_dir}")

except Exception as e:
    print(f"Greška: {e}")
