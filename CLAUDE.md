# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Atlanta crime statistics dashboard built with Plotly Dash that visualizes crime data for specific addresses. Currently configured for 234 MEMORIAL DR SW but designed to be extended to multiple addresses.

## Commands

**IMPORTANT**: Never run the dashboard server directly. The user will run it in their terminal and refresh as needed.

```bash
# Install dependencies (only if needed)
pip install -r requirements.txt

# The user will run the dashboard with:
# python dashboard.py
# Dashboard will be available at http://127.0.0.1:8050/
```

## Architecture

### Data Pipeline
1. **data_loader.py**: CrimeDataLoader class handles CSV parsing and data transformations
   - Loads crime data from `raw-data/AxonCrimeData_Export_view_-3489168499745344284.csv` (2021-2025 data)
   - Filters crimes by address using case-insensitive substring matching
   - Provides quarterly and monthly aggregation methods
   - Handles malformed dates with `errors='coerce'`

2. **dashboard.py**: Plotly Dash application with interactive visualizations
   - Single-page app with date range filtering
   - Real-time updates via callbacks
   - Virtual scrolling for large datasets in crime details table

### Data Files
- **raw-data/** contains three CSV files spanning different time periods:
  - `Crime_Data_1997_2008_*.csv`: Historical data (1997-2008)
  - `2009_2020CrimeData_*.csv`: Mid-period data (2009-2020)  
  - `AxonCrimeData_Export_view_*.csv`: Current data (2021-2025) - actively used

### Key Features
- **Address Filtering**: Currently hardcoded to `PRIMARY_ADDRESS = "234 MEMORIAL DR SW"` in dashboard.py
- **Time Analysis**: Quarters formatted as "YYYY Q#", time of day split into Day (5am-5pm) vs Night (5pm-5am)
- **Crime Type Ranking**: Bar chart inverted to show highest crime counts at top
- **Date Format**: CSV dates are in format `%m/%d/%Y %I:%M:%S %p` (e.g., "1/5/2023 8:48:15 PM")

## Extension Points

To add multiple address support:
1. Modify dashboard.py to add address selector dropdown
2. Use `loader.get_multiple_addresses_data()` method already available in data_loader.py
3. Update charts to compare across addresses

To integrate historical data files:
1. Handle potential schema differences between the three CSV files
2. Add file selection or consolidation logic in CrimeDataLoader
3. Consider performance implications of loading 28 years of data