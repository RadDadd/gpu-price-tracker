# GPU Price Tracker

Tracks GPU prices and availability across major retailers, preserves daily price history, and powers an interactive comparison dashboard on raddata.dev.

## Current status

Manual retailer checks populate the live dashboard at https://raddata.dev/gpu-tracker.html. The latest data and dated observations are stored in this repository; failed seller checks are recorded without treating marketplace prices as retailer offers. Automatic collection is not implemented or scheduled; `collection_enabled` remains false.

The watchlist contains seven exact Gigabyte models across Micro Center (Overland Park), Newegg, Best Buy, and B&H Photo: RTX 5060 WINDFORCE OC 8G, RTX 5060 Ti WINDFORCE OC 16G, RTX 5070 WINDFORCE OC SFF 12G, RTX 5070 Ti WINDFORCE OC SFF 16G, RTX 5080 WINDFORCE OC SFF 16G, RX 9060 XT GAMING OC 16G, and RX 9070 XT GAMING OC 16G. Amazon is excluded. VRAM, memory type, bus width, and GPU core counts are verified against Gigabyte specifications. New cards start history at their first actual check; no earlier prices are backfilled.

## Layout

```text
config/watchlist.json                   Retailers and product listings
data/cards.json                         Stable card identifiers and specs
data/latest.json                        Latest check and last successful price
data/summary.json                       Generated comparison metrics
data/history/                           Permanent dated observations
scripts/collect_prices.py               Collector entry point; validation only
scripts/build_summary.py                Reserved summary entry point
docs/data-model.md                      Observation fields and history rules
.github/workflows/collect-prices.yml     Manual configuration validation only
requirements.txt                        Runtime dependency policy
```

## Validate locally

Use Python 3.11 or newer. The scaffold uses the Python standard library, with no packages to install.

```bash
python scripts/collect_prices.py --validate-config
```

You can also run **Validate tracker scaffold** from the GitHub Actions tab. The workflow has read-only permissions, makes no retailer requests, and does not modify data.

## Planned collection flow

1. Load the catalog and watchlist.
2. Fetch configured product listings with bounded timeouts, request spacing, and retries.
3. Match the exact card, retailer seller, condition, and store before accepting an offer.
4. Record a UTC timestamp and a success/error result per listing.
5. Append observations to dated history, then rebuild latest and summary views.
6. Commit validated data for the raddata.dev frontend to consume.

Target cadence: daily, around 7:17 a.m. America/Chicago. Set up timezone handling and scheduling after the live collector is tested. Manual runs must preserve prior observations and use unique run IDs.

## Data rules

- History is stored as observations, not reconstructed from Git commits.
- Retain successful observations even when prices do not change.
- A failed check is not a zero price or an out-of-stock observation.
- The visible **Price checked** timestamp is the last successful price observation.
- Keep last-attempt and last-success timestamps separate; flag stale retained prices.
- Unknown shipping is null, not free shipping.
- Separate rebates, coupons, membership prices, and open-box/marketplace offers.
- Exclude unavailable and stale offers from lowest-current-price comparisons.
- Store UTC; display dates and times in America/Chicago.

See [the data model](docs/data-model.md) for the field contract.

## Next steps

- Implement and verify the four retailer adapters.
- Automate the existing observation contract with append-safe history writing and error handling.
- Implement latest/summary generation and enable daily collection.
- Continue building price history from fresh checks; the first snapshot has no prior-price baseline.

## Credentials and licensing

Never commit credentials. If integrations require keys, use GitHub Actions secrets.
No license has been selected.
