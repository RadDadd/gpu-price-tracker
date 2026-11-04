# Price history

No production observations have been collected yet.

Use paths such as `2026/11/2026-11-04.json`, partitioned by UTC observation date. Each file contains `schema_version`, `date_utc`, and an `observations` array.

When multiple runs occur on a date, append new observations; do not replace that day's previous observations. Use a unique `run_id` and a stable `observation_id` to make retries idempotent. A retry of the same logical observation must not duplicate it.

Preserve successful unchanged prices and failed checks. See [the field contract](../../docs/data-model.md). Example records must remain clearly marked examples and must never be published as actual history.
