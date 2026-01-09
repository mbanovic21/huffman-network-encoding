import base64, json, requests

API = "https://huffman-network-encoding.onrender.com"

r = requests.post(f"{API}/encode", json={"url": "https://en.wikipedia.org/wiki/Lionel_Messi"}, timeout=60)
r.raise_for_status()
data = r.json()

with open("huffman_codes.json", "w", encoding="utf-8") as f:
    json.dump(data["codes"], f, ensure_ascii=False, indent=2)

with open("received_data.bin", "wb") as f:
    f.write(base64.b64decode(data["encoded_b64"]))

print("OK:", data["title"])
print("Saved: huffman_codes.json, received_data.bin")