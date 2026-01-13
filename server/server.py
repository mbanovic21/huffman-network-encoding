from __future__ import annotations

import sys
from pathlib import Path

from scraper import scrape_url
from huffman_encoder import compress_text_to_files


def main() -> int:
    if len(sys.argv) >= 2:
        url = sys.argv[1].strip()
    else:
        url = input("Unesi URL: ").strip()

    try:
        result = scrape_url(url)
    except Exception as e:
        print(f"[ERROR] Scraping nije uspio: {e}", file=sys.stderr)
        return 1

    if not result.text:
        print("[ERROR] Nema teksta za kompresiju.", file=sys.stderr)
        return 2

    out_dir = Path(__file__).resolve().parent
    meta = compress_text_to_files(result.text, out_dir=out_dir)

    print("=== SERVER OK ===")
    print("Title:", result.title)
    print("Original chars:", meta["original_chars"])
    print("Encoded bytes:", meta["encoded_bytes"])
    print("Tokens:", meta["total_tokens"], "| Unique:", meta["unique_tokens"])
    print("Files written:")
    print(" - huffman_codes.json")
    print(" - encoded_data.bin")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())