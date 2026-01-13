from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Tuple


MAGIC = b"NMR"
VERSION = 1


def load_codes_and_meta(path: Path) -> Tuple[Dict[str, str], dict]:
    data = json.loads(path.read_text(encoding="utf-8"))

    if "codes" in data and "meta" not in data:
        return data, {}

    if "codes" in data and "meta" in data:
        return data["codes"], data["meta"]

    raise ValueError("Nepoznat format huffman_codes.json")


def read_encoded_file(path: Path, meta: dict) -> Tuple[bytes, int]:
    raw = path.read_bytes()

    if raw.startswith(MAGIC):
        version = raw[3]
        if version != VERSION:
            raise ValueError("Nepodržana verzija binarne datoteke")

        pad_len = raw[4]
        payload = raw[5:]
        return payload, pad_len

    if "pad_len" not in meta:
        raise ValueError("Nedostaje pad_len (nema headera ni meta podataka)")

    return raw, meta["pad_len"]


def decode_bits(payload: bytes, pad_len: int, codes: Dict[str, str]) -> str:
    inv_codes = {v: k for k, v in codes.items()}

    bitstream = "".join(f"{b:08b}" for b in payload)
    if pad_len:
        bitstream = bitstream[:-pad_len]

    decoded = []
    buffer = ""

    for bit in bitstream:
        buffer += bit
        if buffer in inv_codes:
            decoded.append(inv_codes[buffer])
            buffer = ""

    if buffer:
        print("Upozorenje: preostali bitovi ignorirani")

    return "".join(decoded)

def verify_decoding(original_path: Path, decoded_path: Path) -> None:
    original = original_path.read_text(encoding="utf-8")
    decoded = decoded_path.read_text(encoding="utf-8")

    if original == decoded:
        print("VERIFIKACIJA USPJEŠNA")
        print("Dekodirani tekst identičan je originalu.")
        return

    print("VERIFIKACIJA NEUSPJEŠNA")
    print("Dekodirani tekst se razlikuje od originala.")

    min_len = min(len(original), len(decoded))
    for i in range(min_len):
        if original[i] != decoded[i]:
            print(f"Prva razlika na poziciji {i}:")
            print("Original:", repr(original[i:i+50]))
            print("Decoded :", repr(decoded[i:i+50]))
            return

    if len(original) != len(decoded):
        print("Različite duljine:")
        print("Original:", len(original))
        print("Decoded :", len(decoded))


def main() -> int:
    base = Path(".")

    codes_path = base / "huffman_codes.json"
    bin_path = base / "encoded_data.bin"
    out_path = base / "decoded_text.txt"
    original_path = base / "original.txt"

    if not codes_path.exists() or not bin_path.exists():
        print("Nedostaju ulazne datoteke.")
        return 1

    codes, meta = load_codes_and_meta(codes_path)
    payload, pad_len = read_encoded_file(bin_path, meta)

    text = decode_bits(payload, pad_len, codes)
    out_path.write_text(text, encoding="utf-8")

    print("=== DEKODIRANJE USPJEŠNO ===")
    print("Duljina dekodiranog teksta:", len(text))
    print("Spremljeno u:", out_path)

    if original_path.exists():
        verify_decoding(original_path, out_path)
    else:
        print("original.txt nije pronađen – preskačem verifikaciju.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
