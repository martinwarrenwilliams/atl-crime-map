#!/usr/bin/env python3
"""
NIBRS Code Extraction Script

This script reads two CSV files containing Atlanta crime data and extracts
all unique NIBRS codes with their descriptions, combining data from both sources
and identifying any variations in descriptions for the same code.

Files processed:
1. 2009_2020CrimeData_3002993194443433393.csv (columns: NIBRS Code, Crime Type)
2. AxonCrimeData_Export_view_6594257177302908045.csv (columns: NibrsUcrCode, NIBRS_Offense)
"""

import pandas as pd
import os
from collections import defaultdict

def load_nibrs_codes_from_file1(filepath):
    """Load NIBRS codes from the 2009-2020 crime data file."""
    print(f"Loading NIBRS codes from: {filepath}")
    
    # Read only the columns we need
    df = pd.read_csv(filepath, usecols=['NIBRS Code', 'Crime Type'])
    
    # Remove rows where NIBRS Code is null/empty
    df = df.dropna(subset=['NIBRS Code'])
    df = df[df['NIBRS Code'].astype(str).str.strip() != '']
    
    # Create mapping of NIBRS Code -> Crime Type
    nibrs_map = {}
    for _, row in df.iterrows():
        code = str(row['NIBRS Code']).strip()
        crime_type = str(row['Crime Type']).strip() if pd.notna(row['Crime Type']) else ''
        
        if code and code != 'nan':
            nibrs_map[code] = crime_type
    
    print(f"  Found {len(nibrs_map)} unique NIBRS codes")
    return nibrs_map

def load_nibrs_codes_from_file2(filepath):
    """Load NIBRS codes from the Axon crime data export file."""
    print(f"Loading NIBRS codes from: {filepath}")
    
    # Read only the columns we need
    df = pd.read_csv(filepath, usecols=['NibrsUcrCode', 'NIBRS_Offense'])
    
    # Remove rows where NibrsUcrCode is null/empty
    df = df.dropna(subset=['NibrsUcrCode'])
    df = df[df['NibrsUcrCode'].astype(str).str.strip() != '']
    
    # Create mapping of NibrsUcrCode -> NIBRS_Offense
    nibrs_map = {}
    for _, row in df.iterrows():
        code = str(row['NibrsUcrCode']).strip()
        offense = str(row['NIBRS_Offense']).strip() if pd.notna(row['NIBRS_Offense']) else ''
        
        if code and code != 'nan':
            nibrs_map[code] = offense
    
    print(f"  Found {len(nibrs_map)} unique NIBRS codes")
    return nibrs_map

def combine_and_analyze_codes(codes1, codes2):
    """Combine codes from both files and analyze for variations."""
    print("\nCombining and analyzing NIBRS codes...")
    
    # Get all unique codes
    all_codes = set(codes1.keys()) | set(codes2.keys())
    
    # Build combined data structure
    combined_data = []
    variations_found = []
    
    for code in sorted(all_codes):
        desc1 = codes1.get(code, '')
        desc2 = codes2.get(code, '')
        
        # Determine primary description and sources
        sources = []
        descriptions = []
        
        if desc1:
            sources.append('2009-2020')
            descriptions.append(desc1)
        if desc2:
            sources.append('Axon')
            descriptions.append(desc2)
        
        # Check for description variations
        unique_descriptions = list(set(descriptions))
        has_variation = len(unique_descriptions) > 1
        
        if has_variation:
            variations_found.append({
                'code': code,
                'desc1': desc1,
                'desc2': desc2
            })
        
        # Use the longest/most descriptive description as primary
        primary_desc = max(descriptions, key=len) if descriptions else ''
        
        combined_data.append({
            'nibrs_code': code,
            'description': primary_desc,
            'sources': ', '.join(sources),
            'has_variation': has_variation,
            'desc_2009_2020': desc1,
            'desc_axon': desc2
        })
    
    return combined_data, variations_found

def print_results(combined_data, variations_found):
    """Print the comprehensive results."""
    print(f"\n{'='*80}")
    print("COMPREHENSIVE NIBRS CODES ANALYSIS")
    print(f"{'='*80}")
    
    print(f"\nTotal unique NIBRS codes found: {len(combined_data)}")
    print(f"Codes with description variations: {len(variations_found)}")
    
    if variations_found:
        print(f"\n{'='*60}")
        print("CODES WITH DESCRIPTION VARIATIONS:")
        print(f"{'='*60}")
        
        for var in variations_found:
            print(f"\nCode: {var['code']}")
            print(f"  2009-2020 file: {var['desc1']}")
            print(f"  Axon file:      {var['desc2']}")
    
    print(f"\n{'='*60}")
    print("ALL NIBRS CODES (sorted alphanumerically):")
    print(f"{'='*60}")
    
    print(f"{'Code':<8} {'Description':<50} {'Sources':<20}")
    print(f"{'-'*8} {'-'*50} {'-'*20}")
    
    for item in combined_data:
        code = item['nibrs_code']
        desc = item['description'][:47] + '...' if len(item['description']) > 50 else item['description']
        sources = item['sources']
        variation_marker = ' *' if item['has_variation'] else ''
        
        print(f"{code:<8} {desc:<50} {sources:<20}{variation_marker}")
    
    if variations_found:
        print(f"\n* Indicates codes with description variations between sources")

def save_to_csv(combined_data, output_file):
    """Save results to CSV file."""
    df = pd.DataFrame(combined_data)
    df.to_csv(output_file, index=False)
    print(f"\nResults saved to: {output_file}")

def main():
    # Define file paths
    base_dir = r"D:\local-repo\atl-crime-map\raw-data"
    file1 = os.path.join(base_dir, "2009_2020CrimeData_3002993194443433393.csv")
    file2 = os.path.join(base_dir, "AxonCrimeData_Export_view_6594257177302908045.csv")
    
    # Verify files exist
    if not os.path.exists(file1):
        print(f"Error: File not found: {file1}")
        return
    if not os.path.exists(file2):
        print(f"Error: File not found: {file2}")
        return
    
    print("Starting NIBRS Code extraction and analysis...")
    print(f"File 1: {file1}")
    print(f"File 2: {file2}")
    
    try:
        # Load NIBRS codes from both files
        codes1 = load_nibrs_codes_from_file1(file1)
        codes2 = load_nibrs_codes_from_file2(file2)
        
        # Combine and analyze
        combined_data, variations_found = combine_and_analyze_codes(codes1, codes2)
        
        # Print results
        print_results(combined_data, variations_found)
        
        # Save to CSV
        output_file = os.path.join(os.path.dirname(__file__), "nibrs_codes_analysis.csv")
        save_to_csv(combined_data, output_file)
        
        print(f"\n{'='*80}")
        print("Analysis complete!")
        
    except Exception as e:
        print(f"Error processing files: {str(e)}")
        raise

if __name__ == "__main__":
    main()