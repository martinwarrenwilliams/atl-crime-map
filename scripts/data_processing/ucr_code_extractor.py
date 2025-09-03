#!/usr/bin/env python3
"""
UCR Code and Offense Description Extractor

This script reads the Atlanta crime data CSV file (1997-2008) and extracts
all unique UCR codes with their corresponding offense descriptions.
"""

import pandas as pd
import re
from collections import defaultdict


def extract_ucr_codes_and_descriptions(csv_file_path):
    """
    Extract unique UCR codes and their descriptions from the crime data CSV.
    
    Args:
        csv_file_path (str): Path to the crime data CSV file
        
    Returns:
        dict: Dictionary mapping UCR codes to lists of unique descriptions
    """
    print(f"Reading CSV file: {csv_file_path}")
    
    try:
        # Read the CSV file using pandas for robust parsing
        df = pd.read_csv(csv_file_path, low_memory=False)
        print(f"Successfully loaded {len(df)} records")
        
        # Display column names to verify structure
        print(f"Columns: {list(df.columns)}")
        
        # Extract UCR codes and offense descriptions (columns 3 and 4, 0-indexed as 2 and 3)
        ucr_col = df.columns[2]  # UCR_#
        offense_col = df.columns[3]  # Offense_Description
        
        print(f"Using columns: '{ucr_col}' and '{offense_col}'")
        
        # Create a clean dataset with valid UCR codes and descriptions
        clean_data = df[[ucr_col, offense_col]].copy()
        
        # Convert UCR codes to string and clean up
        clean_data[ucr_col] = clean_data[ucr_col].astype(str)
        
        # Filter for valid UCR codes (1-3 digits only)
        ucr_pattern = r'^[0-9]{1,3}$'
        valid_ucr_mask = clean_data[ucr_col].str.match(ucr_pattern, na=False)
        
        print(f"Records before filtering: {len(clean_data)}")
        clean_data = clean_data[valid_ucr_mask]
        print(f"Records after filtering for valid UCR codes: {len(clean_data)}")
        
        # Remove records with missing offense descriptions
        clean_data = clean_data.dropna(subset=[offense_col])
        print(f"Records after removing missing descriptions: {len(clean_data)}")
        
        # Get unique UCR code and description pairs
        unique_pairs = clean_data.drop_duplicates()
        print(f"Unique UCR code + description pairs: {len(unique_pairs)}")
        
        # Group descriptions by UCR code
        ucr_descriptions = defaultdict(set)
        
        for _, row in unique_pairs.iterrows():
            ucr_code = int(row[ucr_col])
            description = row[offense_col].strip()
            ucr_descriptions[ucr_code].add(description)
        
        # Convert sets to sorted lists for consistent output
        for ucr_code in ucr_descriptions:
            ucr_descriptions[ucr_code] = sorted(list(ucr_descriptions[ucr_code]))
        
        print(f"Total unique UCR codes found: {len(ucr_descriptions)}")
        
        return dict(ucr_descriptions)
        
    except Exception as e:
        print(f"Error processing file: {e}")
        return {}


def display_ucr_codes(ucr_data):
    """
    Display the UCR codes and their descriptions in a formatted way.
    
    Args:
        ucr_data (dict): Dictionary mapping UCR codes to descriptions
    """
    if not ucr_data:
        print("No UCR data to display")
        return
    
    print("\n" + "="*80)
    print("ATLANTA CRIME DATA (1997-2008) - UCR CODES AND DESCRIPTIONS")
    print("="*80)
    
    # Sort by UCR code numerically
    sorted_codes = sorted(ucr_data.keys())
    
    for ucr_code in sorted_codes:
        descriptions = ucr_data[ucr_code]
        print(f"\nUCR Code: {ucr_code}")
        print("-" * 40)
        
        if len(descriptions) == 1:
            print(f"  Description: {descriptions[0]}")
        else:
            print(f"  Descriptions ({len(descriptions)} variations):")
            for i, desc in enumerate(descriptions, 1):
                print(f"    {i:2d}. {desc}")


def generate_summary_statistics(ucr_data):
    """
    Generate and display summary statistics about the UCR codes.
    
    Args:
        ucr_data (dict): Dictionary mapping UCR codes to descriptions
    """
    if not ucr_data:
        return
    
    print("\n" + "="*80)
    print("SUMMARY STATISTICS")
    print("="*80)
    
    total_codes = len(ucr_data)
    total_descriptions = sum(len(descriptions) for descriptions in ucr_data.values())
    codes_with_multiple_desc = sum(1 for descriptions in ucr_data.values() if len(descriptions) > 1)
    
    print(f"Total unique UCR codes: {total_codes}")
    print(f"Total unique descriptions: {total_descriptions}")
    print(f"Average descriptions per code: {total_descriptions/total_codes:.2f}")
    print(f"Codes with multiple descriptions: {codes_with_multiple_desc}")
    
    # Find codes with most variations
    max_variations = max(len(descriptions) for descriptions in ucr_data.values())
    codes_with_max_variations = [code for code, descriptions in ucr_data.items() 
                                if len(descriptions) == max_variations]
    
    print(f"Maximum variations for a single code: {max_variations}")
    print(f"Code(s) with most variations: {codes_with_max_variations}")
    
    # UCR code ranges
    min_code = min(ucr_data.keys())
    max_code = max(ucr_data.keys())
    print(f"UCR code range: {min_code} - {max_code}")


def main():
    """Main function to run the UCR code extraction."""
    
    # Path to the crime data CSV file
    csv_file_path = r"D:\local-repo\atl-crime-map\raw-data\Crime_Data_1997_2008_-223750340949836035.csv"
    
    # Extract UCR codes and descriptions
    ucr_data = extract_ucr_codes_and_descriptions(csv_file_path)
    
    if ucr_data:
        # Display the results
        display_ucr_codes(ucr_data)
        
        # Generate summary statistics
        generate_summary_statistics(ucr_data)
        
        # Automatically save results to a file
        output_file = "ucr_codes_and_descriptions.txt"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("ATLANTA CRIME DATA (1997-2008) - UCR CODES AND DESCRIPTIONS\n")
            f.write("="*80 + "\n\n")
            
            sorted_codes = sorted(ucr_data.keys())
            for ucr_code in sorted_codes:
                descriptions = ucr_data[ucr_code]
                f.write(f"UCR Code: {ucr_code}\n")
                f.write("-" * 40 + "\n")
                
                if len(descriptions) == 1:
                    f.write(f"  Description: {descriptions[0]}\n")
                else:
                    f.write(f"  Descriptions ({len(descriptions)} variations):\n")
                    for i, desc in enumerate(descriptions, 1):
                        f.write(f"    {i:2d}. {desc}\n")
                f.write("\n")
                
        print(f"\nResults saved to: {output_file}")
    
    else:
        print("Failed to extract UCR codes and descriptions.")


if __name__ == "__main__":
    main()