import pandas as pd
import re
from pathlib import Path

def extract_ucr_codes():
    csv_path = Path(r"D:\local-repo\atl-crime-map\raw-data\Crime_Data_1997_2008_-223750340949836035.csv")
    
    df = pd.read_csv(csv_path, encoding='utf-8-sig')
    
    ucr_column = df.columns[2]
    offense_column = df.columns[3]
    
    df_clean = df[[ucr_column, offense_column]].copy()
    df_clean.columns = ['UCR_Code', 'Offense_Description']
    
    df_clean['UCR_Code'] = df_clean['UCR_Code'].astype(str)
    df_clean = df_clean[df_clean['UCR_Code'].str.match(r'^[0-9]{1,3}$', na=False)]
    
    df_clean['UCR_Code'] = df_clean['UCR_Code'].astype(int)
    
    unique_pairs = df_clean.drop_duplicates()
    
    ucr_groups = unique_pairs.groupby('UCR_Code')['Offense_Description'].apply(list).reset_index()
    ucr_groups = ucr_groups.sort_values('UCR_Code')
    
    output_lines = []
    output_lines.append("UCR CODES AND OFFENSE DESCRIPTIONS - 1997-2008 DATA")
    output_lines.append("=" * 60)
    output_lines.append(f"Total unique UCR codes: {len(ucr_groups)}")
    output_lines.append(f"Total unique code-description pairs: {len(unique_pairs)}")
    output_lines.append("=" * 60)
    output_lines.append("")
    
    for _, row in ucr_groups.iterrows():
        ucr_code = row['UCR_Code']
        descriptions = row['Offense_Description']
        
        output_lines.append(f"UCR Code: {ucr_code:03d}")
        if len(descriptions) == 1:
            output_lines.append(f"  Description: {descriptions[0]}")
        else:
            output_lines.append(f"  Descriptions ({len(descriptions)} variations):")
            for desc in sorted(set(descriptions)):
                output_lines.append(f"    - {desc}")
        output_lines.append("")
    
    return "\n".join(output_lines)

if __name__ == "__main__":
    result = extract_ucr_codes()
    
    output_path = Path(r"D:\local-repo\atl-crime-map\data-processing\ucr_codes_reference_1997_2008.txt")
    with open(output_path, 'w') as f:
        f.write(result)
    
    print(result)
    print(f"\nReference file saved to: {output_path}")