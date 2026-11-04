"""GPU tracker entry point. Live retailer collection is not implemented yet."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]


def validate_config(root: Path = ROOT) -> tuple[int, int]:
    """Validate starter references and public data files without network calls."""
    catalog = json.loads((root / "data/cards.json").read_text(encoding="utf-8"))
    watchlist = json.loads((root / "config/watchlist.json").read_text(encoding="utf-8"))
    cards = catalog["cards"]
    retailers = watchlist["retailers"]
    listings = watchlist["listings"]
    card_ids = {card["card_id"] for card in cards}
    retailer_ids = {retailer["retailer_id"] for retailer in retailers}
    if len(card_ids) != len(cards) or len(retailer_ids) != len(retailers):
        raise ValueError("Duplicate card or retailer identifiers")
    listing_ids = set()
    by_retailer = {retailer["retailer_id"]: retailer for retailer in retailers}
    for listing in listings:
        identifier = listing["listing_id"]
        if identifier in listing_ids:
            raise ValueError(f"Duplicate listing: {identifier}")
        listing_ids.add(identifier)
        if listing["card_id"] not in card_ids:
            raise ValueError(f"Unknown card: {identifier}")
        if listing["retailer_id"] not in retailer_ids:
            raise ValueError(f"Unknown retailer: {identifier}")
        url = urlparse(listing["product_url"])
        retailer = by_retailer[listing["retailer_id"]]
        if url.scheme != "https" or url.hostname != retailer["allowed_hostname"]:
            raise ValueError(f"Unexpected product URL: {identifier}")
        if listing["condition"] != "new":
            raise ValueError(f"Starter listing must be new: {identifier}")
        if not isinstance(listing["enabled"], bool):
            raise ValueError(f"enabled must be boolean: {identifier}")
    for name, key in (("latest.json", "listings"), ("summary.json", "comparisons")):
        data = json.loads((root / "data" / name).read_text(encoding="utf-8"))
        if data.get("schema_version") != "1.0" or not isinstance(data.get(key), list):
            raise ValueError(f"Invalid {name} envelope")
    if catalog.get("schema_version") != "1.0" or watchlist.get("schema_version") != "1.0":
        raise ValueError("Unsupported configuration schema")
    return len(cards), len(listings)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--validate-config", action="store_true",
                        help="Validate local configuration only; do not fetch or write prices")
    args = parser.parse_args()
    try:
        cards, listings = validate_config()
    except (ValueError, KeyError, TypeError, OSError) as exc:
        parser.exit(1, f"Configuration validation failed: {exc}\n")
    if args.validate_config:
        print(f"Configuration valid: {cards} cards, {listings} retailer listings.")
        return 0
    parser.exit(2, "Live collection is not implemented. Use --validate-config to check the scaffold.\n")


if __name__ == "__main__":
    raise SystemExit(main())
