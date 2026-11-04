# Data model

## Identity

- `card_id`: stable exact-model identifier in data/cards.json.
- `listing_id`: configured retailer listing in config/watchlist.json.
- `offer_id`: identity of card + retailer + seller + condition + location. Changing sellers or conditions starts a different offer history.
- `run_id`: unique collection run.
- `observation_id`: stable per logical check, used for retry deduplication.

Use manufacturer part number or UPC for cross-retailer matching. Do not merge different cooling designs, memory capacities, or factory-OC variants merely because they share a GPU family.

## History observation fields

| Field | Meaning |
| --- | --- |
| observation_id, run_id | Observation identity and run provenance |
| listing_id, offer_id, card_id | Listing, comparable offer, and exact card |
| retailer_id, retailer_sku, product_url | Source identity |
| seller, condition, location | Offer identity; location may be null |
| attempted_at_utc | Check attempt timestamp |
| price_checked_at_utc | Successful price observation timestamp; null on failure |
| collection_status | success, timeout, blocked, http_error, parse_error, identity_mismatch |
| price_usd | Advertised item price; null on failure |
| currency | USD |
| shipping_usd | Known shipping cost; otherwise null |
| shipping_status | known, unknown, pickup_only |
| coupon, rebate | Separate objects or null; include terms |
| availability | in_stock, out_of_stock, preorder, unknown |
| stock_quantity_display | Retailer display such as 25+; null when absent |
| fulfillment | shipping, pickup, both, unknown |
| extraction_method | Parser or API provenance |
| error | Error details or null |

Store timestamps as ISO 8601 UTC strings with a Z suffix. Use null for unknown values. Out-of-stock price observations are valid history, but cannot win an in-stock offer comparison. Shipping and tax are not included in the advertised item price.

## Latest view

Each listing retains `last_attempt_at_utc`, `last_attempt_status`, and `last_successful_observation` separately. If a check fails, keep the prior successful observation with its original timestamp and mark it stale. Never move its price timestamp forward to the failed attempt.

## Summary view

Generate prior-check changes, 7/30-day comparisons, lowest observed price/date, and lowest current eligible price. Keep offer-level historical calculations separate from GPU-family minimum-price calculations. A missing comparison baseline yields null, not zero. Compare only the same offer identity. Document the lookback-selection rule before enabling summary generation.

## Schema evolution

Every JSON document carries `schema_version`. Extend fields compatibly where possible, and document breaking changes before migrating old snapshots. Generated latest/summary views must be rebuildable from catalog, watchlist, and history.
