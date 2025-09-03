# Archive Directory

This directory contains previous versions and implementations of the Atlanta Crime Map dashboard.

## Contents

### `dash_version/`
Contains the original Plotly Dash implementation of the crime dashboard. This version was replaced by the Streamlit implementation for easier deployment and maintenance.

- **dashboard.py**: Original Dash application with callback-based interactivity
- Features the same visualizations but uses Dash's callback architecture
- Preserved for reference and potential future use

## Why Archive?

The Dash version is preserved here because:
1. It represents significant development work
2. Some features may be unique to the Dash implementation
3. Could be useful for comparing frameworks
4. May be needed if switching back to Dash in the future

## To Run the Dash Version

If you want to run the archived Dash version:

1. Install Dash dependencies:
   ```bash
   pip install dash==2.14.2
   ```

2. Update imports in the file to use the current data structure

3. Run:
   ```bash
   python archive/dash_version/dashboard.py
   ```

Note: The Dash version may need updates to work with the current data structure.