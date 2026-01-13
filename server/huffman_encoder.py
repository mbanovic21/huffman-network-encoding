from __future__ import annotations

import heapq
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple


MAGIC = b"NMR"
VERSION = 1
TOKEN_REGEX = r"\w+|[^\w]"


@dataclass(frozen=True)
class Node:
    freq: int
    token: Optional[str] = None
    left: Optional["Node"] = None
    right: Optional["Node"] = None


def tokenize(text: str, pattern: str = TOKEN_REGEX) -> List[str]:
    return re.findall(pattern, text, flags=re.UNICODE)


def frequencies(tokens: List[str]) -> Dict[str, int]:
    freq: Dict[str, int] = {}
    for t in tokens:
        freq[t] = freq.get(t, 0) + 1
    return freq


def build_huffman_tree(freq: Dict[str, int]) -> Node:
    heap: List[Tuple[int, int, Node]] = []
    tie = 0
    for tok, fr in freq.items():
        heapq.heappush(heap, (fr, tie, Node(freq=fr, token=tok)))
        tie += 1

    if not heap:
        raise ValueError("Nema tokena za kodiranje (prazan tekst).")

    if len(heap) == 1:
        fr, _, only = heap[0]
        return Node(freq=fr, left=only, right=None, token=None)

    while len(heap) > 1:
        f1, _, n1 = heapq.heappop(heap)
        f2, _, n2 = heapq.heappop(heap)
        parent = Node(freq=f1 + f2, left=n1, right=n2, token=None)
        heapq.heappush(heap, (parent.freq, tie, parent))
        tie += 1

    return heap[0][2]


def build_codes(root: Node) -> Dict[str, str]:
    codes: Dict[str, str] = {}

    def dfs(node: Node, path: str) -> None:
        if node.token is not None:
            codes[node.token] = path or "0"
            return
        if node.left is not None:
            dfs(node.left, path + "0")
        if node.right is not None:
            dfs(node.right, path + "1")

    dfs(root, "")
    return codes


def encode_tokens(tokens: List[str], codes: Dict[str, str]) -> Tuple[bytes, int]:
    bitstr = "".join(codes[t] for t in tokens)

    pad_len = (8 - (len(bitstr) % 8)) % 8
    if pad_len:
        bitstr += "0" * pad_len

    data = bytearray()
    for i in range(0, len(bitstr), 8):
        byte = int(bitstr[i:i+8], 2)
        data.append(byte)

    return bytes(data), pad_len


def write_bin(path: Path, payload: bytes, pad_len: int) -> None:
    if not (0 <= pad_len <= 7):
        raise ValueError("pad_len mora biti 0..7")

    with path.open("wb") as f:
        f.write(MAGIC)
        f.write(bytes([VERSION]))
        f.write(bytes([pad_len]))
        f.write(payload)


def write_codes_json(path: Path, codes: Dict[str, str], meta: Dict) -> None:
    out = {
        "meta": meta,
        "codes": codes,
    }
    path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")


def compress_text_to_files(
    text: str,
    out_dir: str | Path,
    codes_filename: str = "huffman_codes.json",
    bin_filename: str = "encoded_data.bin",
    tokenizer_regex: str = TOKEN_REGEX,
) -> Dict:
    out_path = Path(out_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    tokens = tokenize(text, pattern=tokenizer_regex)
    freq = frequencies(tokens)
    tree = build_huffman_tree(freq)
    codes = build_codes(tree)
    payload, pad_len = encode_tokens(tokens, codes)

    meta = {
        "version": VERSION,
        "tokenizer_regex": tokenizer_regex,
        "total_tokens": len(tokens),
        "unique_tokens": len(freq),
        "pad_len": pad_len,
        "original_chars": len(text),
        "encoded_bytes": len(payload),
    }

    write_codes_json(out_path / codes_filename, codes, meta)
    write_bin(out_path / bin_filename, payload, pad_len)

    return meta
