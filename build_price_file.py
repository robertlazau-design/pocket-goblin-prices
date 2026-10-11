#!/usr/bin/env python3
"""Build the daily price file the app downloads.

Reads Scryfall's Default Cards bulk file and writes one line per printing that has
a price: "scryfall_id,usd,usd_foil". The first line is "#updated_at=<Scryfall's
timestamp>". The file is raw DEFLATE-compressed, which iOS can decompress without
extra libraries.

Runs daily in the pocket-goblin-prices GitHub repo (see prices-repo/), and can be
run locally:

    python3 tools/build_price_file.py [output path]

Card prices courtesy of Scryfall (https://scryfall.com).
"""

import gzip
import json
import os
import sys
import urllib.request
import zlib

BULK_INFO_URL = "https://api.scryfall.com/bulk-data/default-cards"
HEADERS = {"User-Agent": "PocketGoblin/0.1 (price file builder)", "Accept": "application/json;q=0.9,*/*;q=0.8"}


def fetch(url, accept_json=True):
    request = urllib.request.Request(url, headers=HEADERS)
    response = urllib.request.urlopen(request, timeout=300)
    return json.load(response) if accept_json else response


def price_lines(lines):
    for line in lines:
        line = line.strip().rstrip(",")
        if not line.startswith("{"):
            continue
        card = json.loads(line)
        if card.get("digital"):
            continue
        prices = card.get("prices") or {}
        usd, foil = prices.get("usd"), prices.get("usd_foil")
        if usd or foil:
            yield f'{card["id"]},{usd or ""},{foil or ""}'


def main():
    output = sys.argv[1] if len(sys.argv) > 1 else "prices.deflate"
    info = fetch(BULK_INFO_URL)
    print(f"Reading {info['jsonl_download_uri']}")
    with fetch(info["jsonl_download_uri"], accept_json=False) as response, \
            gzip.open(response, "rt", encoding="utf-8") as lines:
        body = "\n".join(price_lines(lines))

    text = f"#updated_at={info['updated_at']}\n{body}\n"
    # wbits=-15: raw DEFLATE with no header, what iOS's NSData decompression expects.
    compressor = zlib.compressobj(level=9, wbits=-15)
    data = compressor.compress(text.encode()) + compressor.flush()
    with open(output, "wb") as f:
        f.write(data)
    count = body.count("\n") + 1
    print(f"Wrote {count:,} prices to {output} ({len(data) / 1e6:.1f} MB)")


if __name__ == "__main__":
    main()
