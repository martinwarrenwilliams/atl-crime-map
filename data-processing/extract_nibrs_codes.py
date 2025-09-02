import pandas as pd
from pathlib import Path
import re

def extract_nibrs_codes():
    # File paths
    file_2009_2020 = Path(r"D:\local-repo\atl-crime-map\raw-data\2009_2020CrimeData_3002993194443433393.csv")
    file_2020_plus = Path(r"D:\local-repo\atl-crime-map\raw-data\AxonCrimeData_Export_view_6594257177302908045.csv")
    
    # Read 2009-2020 data
    print("Reading 2009-2020 data...")
    df1 = pd.read_csv(file_2009_2020, encoding='utf-8-sig')
    nibrs_2009_2020 = df1[['NIBRS Code', 'Crime Type']].copy()
    nibrs_2009_2020.columns = ['Code', 'Description']
    nibrs_2009_2020['Source'] = '2009-2020'
    
    # Read 2020+ data
    print("Reading 2020+ data...")
    df2 = pd.read_csv(file_2020_plus, encoding='utf-8-sig')
    nibrs_2020_plus = df2[['NibrsUcrCode', 'NIBRS_Offense']].copy()
    nibrs_2020_plus.columns = ['Code', 'Description']
    nibrs_2020_plus['Source'] = '2020+'
    
    # Remove nulls and get unique combinations
    nibrs_2009_2020 = nibrs_2009_2020.dropna()
    nibrs_2020_plus = nibrs_2020_plus.dropna()
    
    # Get unique combinations
    unique_2009_2020 = nibrs_2009_2020.drop_duplicates()
    unique_2020_plus = nibrs_2020_plus.drop_duplicates()
    
    # Combine all data
    all_codes = pd.concat([unique_2009_2020, unique_2020_plus])
    
    # Group by code to see all descriptions
    code_groups = all_codes.groupby('Code').agg({
        'Description': lambda x: list(set(x)),
        'Source': lambda x: list(set(x))
    }).reset_index()
    
    # Sort alphanumerically
    code_groups = code_groups.sort_values('Code')
    
    # Format output
    output_lines = []
    output_lines.append("NIBRS CODES AND OFFENSE DESCRIPTIONS - ATLANTA CRIME DATA")
    output_lines.append("=" * 70)
    output_lines.append(f"Total unique NIBRS codes found: {len(code_groups)}")
    output_lines.append(f"Codes in 2009-2020 data: {len(unique_2009_2020['Code'].unique())}")
    output_lines.append(f"Codes in 2020+ data: {len(unique_2020_plus['Code'].unique())}")
    output_lines.append("=" * 70)
    output_lines.append("")
    
    for _, row in code_groups.iterrows():
        code = row['Code']
        descriptions = row['Description']
        sources = row['Source']
        
        output_lines.append(f"Code: {code}")
        output_lines.append(f"  Sources: {', '.join(sorted(sources))}")
        
        if len(descriptions) == 1:
            output_lines.append(f"  Description: {descriptions[0]}")
        else:
            output_lines.append(f"  Descriptions ({len(descriptions)} variations):")
            for desc in sorted(descriptions):
                output_lines.append(f"    - {desc}")
        output_lines.append("")
    
    return "\n".join(output_lines)

if __name__ == "__main__":
    result = extract_nibrs_codes()
    
    # Save to file
    output_path = Path(r"D:\local-repo\atl-crime-map\data-processing\nibrs_codes_reference.txt")
    with open(output_path, 'w') as f:
        f.write(result)
    
    print(result)
    print(f"\nReference file saved to: {output_path}")