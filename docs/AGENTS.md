# AGENTS.md

Guidance for AI coding assistants working in this repository.

## Project Overview
- Purpose: Plotly Dash app visualizing Atlanta crime data for a specific address (currently `234 MEMORIAL DR SW`).
- Entry points:
  - `dashboard.py`: Dash UI, callbacks, visualizations.
  - `data_loader.py`: CSV loading, date parsing, filtering, aggregations.
  - `data-processing/`: scripts and reference files for NIBRS/UCR mapping and severity crosswalks.
- Active dataset: `raw-data/AxonCrimeData_Export_view_6594257177302908045.csv` (2021–2025 data).

## Do/Don’t
- Do: keep changes minimal and focused; match existing style; explain reasoning in PR descriptions or commit messages if requested.
- Do: reference concrete files and lines when proposing edits.
- Do: validate that changes won’t break running the app with `python dashboard.py` (user will run this).
- Don’t: start the server yourself; the user runs `python dashboard.py`.
- Don’t: introduce new dependencies unless necessary; prefer using what’s in `requirements.txt`.
- Don’t: refactor broadly or reformat files unrelated to a task.

## How to Run (for the user)
```bash
pip install -r requirements.txt
python dashboard.py
# App at http://127.0.0.1:8050/
```

## Architecture Notes
- Address filtering: substring, case-insensitive match on `StreetAddress` in `CrimeDataLoader.filter_by_address()`.
- Date parsing: `ReportDate`, `OccurredFromDate`, `OccurredToDate` parsed via `pd.to_datetime(..., errors='coerce')`; rows with null `OccurredFromDate` dropped.
- Time series: Quarterly aggregation available via `get_quarterly_time_series_data()` with labels like `YYYY Q#`.
- Severity crosswalk: optional CSV at `data-processing/atl_ucr_nibrs_severity_crosswalk_full.csv` mapped by `offense_description → severity`.
- Dashboard: single-page layout with date range filter, multiple charts, and a virtualized details table.

## Repo Map
- `dashboard.py`: Dash app, charts, severity/time stats, table.
- `data_loader.py`: `CrimeDataLoader` with loading, filtering, summaries, time series helpers.
- `data-processing/`:
  - `crime_severity_mapping.md`: background on severity mapping.
  - `atl_ucr_nibrs_severity_crosswalk_full.csv`: offense → severity crosswalk used by the dashboard.
  - Scripts for creating crosswalks and handling historical codes.
- `raw-data/`: CSVs spanning 1997–2025 (only the 2021–2025 file is active in the app now).

## Common Tasks (Playbooks)
- Add multiple-address support:
  1) Add a dropdown for addresses in `dashboard.py` (e.g., distinct values from `StreetAddress` or a curated list).
  2) Replace `PRIMARY_ADDRESS` usage with the dropdown value in callbacks.
  3) Optionally use `CrimeDataLoader.get_multiple_addresses_data()` for combined/comparative views.

- Integrate historical files (1997–2020):
  1) Extend `CrimeDataLoader` to load multiple files and normalize schemas (different column names per period).
  2) Add mapping layer to align crime type fields to NIBRS or a common taxonomy.
  3) Consider caching (in-memory) after first load to avoid repeated parsing costs.

- Severity chart ordering (requested next step):
  - Ensure severity order is High → Medium → Low via a categorical type and `category_orders` in Plotly.
  - Current implementation in `dashboard.py` already enforces order (`severity_order = ['High', 'Medium', 'Low']`). Keep any new visuals consistent.

## Coding Guidelines
- Style: keep imports, layout dicts, and Plotly config consistent with current patterns in `dashboard.py`.
- Data safety: always `copy()` DataFrames before assigning new columns to avoid chained assignment warnings.
- Performance: avoid full scans when possible; reuse loaded DataFrame from `CrimeDataLoader`.
- UX: for empty states, return a figure with a centered annotation as done in `update_dashboard()`.

## Known Gotchas
- Date parsing relies on `%m/%d/%Y %I:%M:%S %p`; malformed rows are coerced to NaT.
- The crosswalk may be missing for some offenses; code defaults missing severities to `Low` and excludes `Exclude`.
- Address filtering is substring-based; similar addresses may collide (e.g., suite numbers). Consider exact match or normalization if needed.

## Good First Improvements
- Add an address selector and thread it through callbacks.
- Add an option to toggle Monthly vs Quarterly trends.
- Add caching to `CrimeDataLoader` for multi-file loads.
- Flesh out `README.md` with setup, data notes, and screenshots.

## Assistant Etiquette
- Describe intended changes before large edits; group related edits together.
- Prefer small, surgical patches; avoid broad rewrites.
- If adding files or scripts, place them logically (e.g., `data-processing/` for ETL/mapping utilities).

