# Pocket Goblin prices

A daily price file for the Pocket Goblin app, built from
[Scryfall](https://scryfall.com)'s bulk data by a scheduled GitHub Actions job.

- **Download:** `https://github.com/robertlazau-design/pocket-goblin-prices/releases/download/latest/prices.deflate`
- **Format:** raw DEFLATE-compressed text. The first line is `#updated_at=<timestamp>`, then one
  line per printing: `scryfall_id,usd,usd_foil` (empty when there's no price).
- **Schedule:** daily at 22:30 UTC, after Scryfall's daily update. Run it by hand from the
  Actions tab ("Daily prices" → "Run workflow").

Card prices courtesy of Scryfall. Pocket Goblin is unofficial Fan Content permitted under
the Fan Content Policy. Not approved/endorsed by Wizards.

`build_price_file.py` is a copy of `tools/build_price_file.py` in the (private) app repo;
keep the two in sync.
