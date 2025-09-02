import pandas as pd
from pathlib import Path

def split_crime_data_file():
    """Split the large 1997-2008 crime data file into two parts by year."""
    
    # File paths
    input_file = Path(r"D:\local-repo\atl-crime-map\raw-data\Crime_Data_1997_2008_-223750340949836035.csv")
    output_file_1 = Path(r"D:\local-repo\atl-crime-map\raw-data\Crime_Data_1997_2002.csv")
    output_file_2 = Path(r"D:\local-repo\atl-crime-map\raw-data\Crime_Data_2003_2008.csv")
    
    print(f"Reading large file: {input_file}")
    print("This may take a moment...")
    
    # Read the CSV file
    df = pd.read_csv(input_file, encoding='utf-8-sig')
    
    print(f"Total rows: {len(df)}")
    print(f"Columns: {list(df.columns)}")
    
    # Parse the date column - it's in 'Report_date1' column
    # Format is like "10/4/1997 4:00:00 AM"
    df['Year'] = pd.to_datetime(df['Report_date1'], format='%m/%d/%Y %I:%M:%S %p', errors='coerce').dt.year
    
    # Check year distribution
    year_counts = df['Year'].value_counts().sort_index()
    print("\nRows per year:")
    print(year_counts)
    
    # Split into two parts: 1997-2002 and 2003-2008
    df_part1 = df[df['Year'] <= 2002].copy()
    df_part2 = df[df['Year'] >= 2003].copy()
    
    # Drop the temporary Year column before saving
    df_part1 = df_part1.drop('Year', axis=1)
    df_part2 = df_part2.drop('Year', axis=1)
    
    print(f"\nPart 1 (1997-2002): {len(df_part1)} rows")
    print(f"Part 2 (2003-2008): {len(df_part2)} rows")
    
    # Save the split files
    print(f"\nSaving Part 1 to: {output_file_1}")
    df_part1.to_csv(output_file_1, index=False, encoding='utf-8-sig')
    
    print(f"Saving Part 2 to: {output_file_2}")
    df_part2.to_csv(output_file_2, index=False, encoding='utf-8-sig')
    
    print("\nSplit complete!")
    
    # Check file sizes
    import os
    size1 = os.path.getsize(output_file_1) / (1024 * 1024)  # Convert to MB
    size2 = os.path.getsize(output_file_2) / (1024 * 1024)  # Convert to MB
    
    print(f"\nFile sizes:")
    print(f"Part 1: {size1:.1f} MB")
    print(f"Part 2: {size2:.1f} MB")
    
    return df_part1, df_part2

if __name__ == "__main__":
    split_crime_data_file()