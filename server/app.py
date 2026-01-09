from __future__ import annotations

import base64
import json
from pathlib import Path

from flask import Flask, request, jsonify

from scraper import scrape_url
from huffman_encoder import compress_text_to_files

app = Flask(__name__)

SERVER_DIR = Path(__file__).resolve().parent

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/encode")
def encode():
    data = request.get_json(force=True, silent=True) or {}
    url = (data.get("url") or "").strip()
    if not url:
        return jsonify({"error": "Missing 'url'"}), 400

    try:
        res = scrape_url(url)
        if not res.text:
            return jsonify({"error": "No text extracted"}), 422

        meta = compress_text_to_files(res.text, out_dir=SERVER_DIR)

        codes = json.loads((SERVER_DIR / "huffman_codes.json").read_text(encoding="utf-8"))
        bin_bytes = (SERVER_DIR / "encoded_data.bin").read_bytes()

        return jsonify({
            "title": res.title,
            "meta": meta,
            "codes": codes,
            "encoded_b64": base64.b64encode(bin_bytes).decode("ascii"),
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
