import json
import base64
from pathlib import Path
import requests

SERVER_URL = "http://172.16.1.1:8000/encode"  # IP poslužitelja

URL = "https://www.foi.unizg.hr/hr/novosti/besplatne-pripreme-za-drzavnu-maturu-iz-informatike-i-matematike"

client_dir = Path("./client1")
client_dir.mkdir(parents=True, exist_ok=True)

try:
    response = requests.post(SERVER_URL, json={"url": URL})
    response.raise_for_status()
    data = response.json()

    (client_dir / "original.txt").write_text(data["original_text"], encoding="utf-8")
    (client_dir / "huffman_codes.json").write_text(json.dumps(data["codes"], indent=2), encoding="utf-8")
    encoded_bytes = base64.b64decode(data["encoded_b64"])
    (client_dir / "encoded_data.bin").write_bytes(encoded_bytes)

    print(f"Datoteke za client1 spremljene u {client_dir}")

except Exception as e:
    print(f"Greška: {e}")
