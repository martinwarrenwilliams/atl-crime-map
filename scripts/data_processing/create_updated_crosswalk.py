import pandas as pd
from pathlib import Path

def create_comprehensive_crosswalk():
    """Create a comprehensive UCR/NIBRS to severity crosswalk for Atlanta crime data."""
    
    # Read existing crosswalk
    existing_path = Path(r"D:\local-repo\atl-crime-map\data-processing\atl_ucr_nibrs_severity_crosswalk_full.csv")
    df_existing = pd.read_csv(existing_path)
    
    # Create new rows list starting with corrected existing data
    rows = []
    
    # First, correct existing NIBRS codes with updated severity levels
    severity_corrections = {
        '23A': 'Low',  # Pocket-picking
        '23B': 'Low',  # Purse-snatching
        '23C': 'Low',  # Shoplifting
        '23E': 'Low',  # Theft from coin machine
        '290': 'Low',  # Vandalism
        '35B': 'Low',  # Drug Equipment
        '720': 'Low',  # Animal Cruelty
    }
    
    # Process existing NIBRS codes
    for _, row in df_existing.iterrows():
        code = str(row['nibrs_code'])
        new_severity = severity_corrections.get(code, row['severity'])
        
        rows.append({
            'code': code,
            'code_type': 'NIBRS',
            'offense_description': row['nibrs_offense'],
            'severity': new_severity,
            'crime_against': row['crime_against'],
            'ucr_index_category': row['ucr_index_category'] if pd.notna(row['ucr_index_category']) else '',
            'ucr_part': row['ucr_part'] if pd.notna(row['ucr_part']) else '',
            'data_years': '2009-2024',
            'notes': row['notes'] if pd.notna(row['notes']) else ''
        })
    
    # Add UCR codes from 1997-2008
    ucr_codes = [
        # HIGH SEVERITY - Homicides
        ('110', 'UCR', 'Homicide/Willful Killing', 'High', 'Person', 'Murder', 'I', '1997-2008', 'Multiple variations'),
        ('120', 'UCR', 'Negligent Manslaughter', 'High', 'Person', 'Manslaughter', 'I', '1997-2008', ''),
        
        # HIGH SEVERITY - Sex crimes
        ('210', 'UCR', 'Rape', 'High', 'Person', 'Rape', 'I', '1997-2008', 'Gun/weapon/strongarm'),
        ('220', 'UCR', 'Attempted Rape', 'High', 'Person', 'Rape', 'I', '1997-2008', 'All variations'),
        
        # HIGH SEVERITY - Armed Robbery (3xx series)
        ('311', 'UCR', 'Robbery-Street-Gun', 'High', 'Property', 'Robbery', 'I', '1997-2008', ''),
        ('312', 'UCR', 'Robbery-Business-Gun', 'High', 'Property', 'Robbery', 'I', '1997-2008', ''),
        ('313', 'UCR', 'Robbery-Gas Station-Gun', 'High', 'Property', 'Robbery', 'I', '1997-2008', ''),
        ('314', 'UCR', 'Robbery-Convenience Store-Gun', 'High', 'Property', 'Robbery', 'I', '1997-2008', ''),
        ('315', 'UCR', 'Robbery-Residence-Gun', 'High', 'Property', 'Robbery', 'I', '1997-2008', ''),
        ('316', 'UCR', 'Robbery-Bank-Gun', 'High', 'Property', 'Robbery', 'I', '1997-2008', ''),
        ('317', 'UCR', 'Robbery-Misc-Gun', 'High', 'Property', 'Robbery', 'I', '1997-2008', ''),
        ('321', 'UCR', 'Robbery-Street-Knife', 'High', 'Property', 'Robbery', 'I', '1997-2008', ''),
        ('322', 'UCR', 'Robbery-Business-Knife', 'High', 'Property', 'Robbery', 'I', '1997-2008', ''),
        ('323', 'UCR', 'Robbery-Gas Station-Knife', 'High', 'Property', 'Robbery', 'I', '1997-2008', ''),
        ('324', 'UCR', 'Robbery-Convenience Store-Knife', 'High', 'Property', 'Robbery', 'I', '1997-2008', ''),
        ('325', 'UCR', 'Robbery-Residence-Knife', 'High', 'Property', 'Robbery', 'I', '1997-2008', ''),
        ('326', 'UCR', 'Robbery-Bank-Knife', 'High', 'Property', 'Robbery', 'I', '1997-2008', ''),
        ('327', 'UCR', 'Robbery-Misc-Knife', 'High', 'Property', 'Robbery', 'I', '1997-2008', ''),
        ('331', 'UCR', 'Robbery-Street-Other Weapon', 'High', 'Property', 'Robbery', 'I', '1997-2008', ''),
        ('332', 'UCR', 'Robbery-Business-Other Weapon', 'High', 'Property', 'Robbery', 'I', '1997-2008', ''),
        ('333', 'UCR', 'Robbery-Gas Station-Other', 'High', 'Property', 'Robbery', 'I', '1997-2008', ''),
        ('334', 'UCR', 'Robbery-Convenience Store-Other', 'High', 'Property', 'Robbery', 'I', '1997-2008', ''),
        ('335', 'UCR', 'Robbery-Residence-Other Weapon', 'High', 'Property', 'Robbery', 'I', '1997-2008', ''),
        ('336', 'UCR', 'Robbery-Bank-Other', 'High', 'Property', 'Robbery', 'I', '1997-2008', ''),
        ('337', 'UCR', 'Robbery-Misc-Other Weapon', 'High', 'Property', 'Robbery', 'I', '1997-2008', ''),
        ('341', 'UCR', 'Robbery-Street-Strongarm', 'High', 'Property', 'Robbery', 'I', '1997-2008', ''),
        ('342', 'UCR', 'Robbery-Business-Strongarm', 'High', 'Property', 'Robbery', 'I', '1997-2008', ''),
        ('343', 'UCR', 'Robbery-Gas Station-Strongarm', 'High', 'Property', 'Robbery', 'I', '1997-2008', ''),
        ('344', 'UCR', 'Robbery-Convenience Store-Strongarm', 'High', 'Property', 'Robbery', 'I', '1997-2008', ''),
        ('345', 'UCR', 'Robbery-Residence-Strongarm', 'High', 'Property', 'Robbery', 'I', '1997-2008', ''),
        ('346', 'UCR', 'Robbery-Bank-Strongarm', 'High', 'Property', 'Robbery', 'I', '1997-2008', ''),
        ('347', 'UCR', 'Robbery-Misc-Strongarm', 'High', 'Property', 'Robbery', 'I', '1997-2008', ''),
        
        # MIXED - Assault codes (check description for severity)
        ('410', 'UCR', 'Assault-Mixed', 'High', 'Person', 'Aggravated Assault', 'I', '1997-2008', 'Check description for AGGR vs SIMPLE'),
        ('420', 'UCR', 'Assault-Mixed', 'High', 'Person', 'Aggravated Assault', 'I', '1997-2008', 'Check description for AGGR vs SIMPLE'),
        ('430', 'UCR', 'Assault-Mixed', 'High', 'Person', 'Aggravated Assault', 'I', '1997-2008', 'Check description for AGGR vs SIMPLE'),
        ('440', 'UCR', 'Assault-Mixed', 'High', 'Person', 'Aggravated Assault', 'I', '1997-2008', 'Check description for AGGR vs SIMPLE'),
        
        # MEDIUM SEVERITY - Burglary
        ('511', 'UCR', 'Burglary-Forced Entry-Residence', 'Medium', 'Property', 'Burglary', 'I', '1997-2008', ''),
        ('512', 'UCR', 'Burglary-Forced Entry-NonResidence', 'Medium', 'Property', 'Burglary', 'I', '1997-2008', ''),
        ('521', 'UCR', 'Burglary-No Forced Entry-Residence', 'Medium', 'Property', 'Burglary', 'I', '1997-2008', ''),
        ('522', 'UCR', 'Burglary-No Forced Entry-NonResidence', 'Medium', 'Property', 'Burglary', 'I', '1997-2008', ''),
        ('531', 'UCR', 'Attempted Burglary-Residence', 'Medium', 'Property', 'Burglary', 'I', '1997-2008', ''),
        ('532', 'UCR', 'Attempted Burglary-NonResidence', 'Medium', 'Property', 'Burglary', 'I', '1997-2008', ''),
        
        # MEDIUM SEVERITY - Larceny/Theft
        ('610', 'UCR', 'Larceny-Pocket Picking', 'Low', 'Property', 'Larceny', 'I', '1997-2008', ''),
        ('620', 'UCR', 'Larceny-Purse Snatching', 'Low', 'Property', 'Larceny', 'I', '1997-2008', ''),
        ('630', 'UCR', 'Shoplifting', 'Low', 'Property', 'Larceny', 'I', '1997-2008', ''),
        ('640', 'UCR', 'Larceny-Articles from Vehicle', 'Medium', 'Property', 'Larceny', 'I', '1997-2008', ''),
        ('650', 'UCR', 'Larceny-Parts from Vehicle', 'Medium', 'Property', 'Larceny', 'I', '1997-2008', ''),
        ('660', 'UCR', 'Larceny-Bicycle', 'Low', 'Property', 'Larceny', 'I', '1997-2008', ''),
        ('670', 'UCR', 'Larceny-From Building', 'Medium', 'Property', 'Larceny', 'I', '1997-2008', ''),
        ('680', 'UCR', 'Larceny-From Coin Machine', 'Low', 'Property', 'Larceny', 'I', '1997-2008', ''),
        ('690', 'UCR', 'Larceny-Other', 'Medium', 'Property', 'Larceny', 'I', '1997-2008', ''),
        
        # MEDIUM SEVERITY - Auto Theft
        ('710', 'UCR', 'Auto Theft', 'Medium', 'Property', 'Motor Vehicle Theft', 'I', '1997-2008', ''),
        ('720', 'UCR', 'Theft of Truck/Van/Bus', 'Medium', 'Property', 'Motor Vehicle Theft', 'I', '1997-2008', ''),
        ('730', 'UCR', 'Theft of Other Vehicle', 'Medium', 'Property', 'Motor Vehicle Theft', 'I', '1997-2008', ''),
    ]
    
    # Add UCR codes to rows
    for ucr_data in ucr_codes:
        rows.append({
            'code': ucr_data[0],
            'code_type': ucr_data[1],
            'offense_description': ucr_data[2],
            'severity': ucr_data[3],
            'crime_against': ucr_data[4],
            'ucr_index_category': ucr_data[5],
            'ucr_part': ucr_data[6],
            'data_years': ucr_data[7],
            'notes': ucr_data[8]
        })
    
    # Add additional NIBRS codes from 2009-2020 data that aren't in existing crosswalk
    additional_nibrs = [
        # Robbery variations from 2009-2020
        ('1201', 'NIBRS', 'Robbery', 'High', 'Property', 'Robbery', 'I', '2009-2020', ''),
        ('1201C', 'NIBRS', 'Robbery', 'High', 'Property', 'Robbery', 'I', '2009-2020', ''),
        ('1201D', 'NIBRS', 'Robbery', 'High', 'Property', 'Robbery', 'I', '2009-2020', ''),
        ('1202', 'NIBRS', 'Robbery', 'High', 'Property', 'Robbery', 'I', '2009-2020', ''),
        ('1202J', 'NIBRS', 'Robbery', 'High', 'Property', 'Robbery', 'I', '2009-2020', ''),
        ('1202K', 'NIBRS', 'Robbery', 'High', 'Property', 'Robbery', 'I', '2009-2020', ''),
        ('1202L', 'NIBRS', 'Robbery', 'High', 'Property', 'Robbery', 'I', '2009-2020', ''),
        ('1202Q', 'NIBRS', 'Robbery', 'High', 'Property', 'Robbery', 'I', '2009-2020', ''),
        ('1202R', 'NIBRS', 'Robbery', 'High', 'Property', 'Robbery', 'I', '2009-2020', ''),
        ('1203', 'NIBRS', 'Robbery', 'High', 'Property', 'Robbery', 'I', '2009-2020', ''),
        ('1203X', 'NIBRS', 'Robbery', 'High', 'Property', 'Robbery', 'I', '2009-2020', 'Sometimes coded as Larceny'),
        ('1203Y', 'NIBRS', 'Robbery', 'High', 'Property', 'Robbery', 'I', '2009-2020', ''),
        ('1204', 'NIBRS', 'Robbery', 'High', 'Property', 'Robbery', 'I', '2009-2020', ''),
        ('1205', 'NIBRS', 'Robbery', 'High', 'Property', 'Robbery', 'I', '2009-2020', ''),
        ('1205K', 'NIBRS', 'Robbery', 'High', 'Property', 'Robbery', 'I', '2009-2020', ''),
        ('1206', 'NIBRS', 'Robbery', 'High', 'Property', 'Robbery', 'I', '2009-2020', ''),
        ('1207', 'NIBRS', 'Robbery', 'High', 'Property', 'Robbery', 'I', '2009-2020', ''),
        ('1208', 'NIBRS', 'Robbery', 'High', 'Property', 'Robbery', 'I', '2009-2020', ''),
        ('1208K', 'NIBRS', 'Robbery', 'High', 'Property', 'Robbery', 'I', '2009-2020', ''),
        ('1209', 'NIBRS', 'Robbery', 'High', 'Property', 'Robbery', 'I', '2009-2020', ''),
        ('1211G', 'NIBRS', 'Robbery', 'High', 'Property', 'Robbery', 'I', '2009-2020', ''),
        ('1211K', 'NIBRS', 'Robbery', 'High', 'Property', 'Robbery', 'I', '2009-2020', ''),
        ('1211O', 'NIBRS', 'Robbery', 'High', 'Property', 'Robbery', 'I', '2009-2020', ''),
        ('1211S', 'NIBRS', 'Robbery', 'High', 'Property', 'Robbery', 'I', '2009-2020', ''),
        ('1212', 'NIBRS', 'Robbery', 'High', 'Property', 'Robbery', 'I', '2009-2020', ''),
        ('1299G', 'NIBRS', 'Robbery', 'High', 'Property', 'Robbery', 'I', '2009-2020', ''),
        ('1299K', 'NIBRS', 'Robbery', 'High', 'Property', 'Robbery', 'I', '2009-2020', ''),
        ('1299O', 'NIBRS', 'Robbery', 'High', 'Property', 'Robbery', 'I', '2009-2020', ''),
        ('1299S', 'NIBRS', 'Robbery', 'High', 'Property', 'Robbery', 'I', '2009-2020', 'Sometimes coded as Larceny'),
        
        # Aggravated Assault variations
        ('1006', 'NIBRS', 'Aggravated Assault', 'High', 'Person', 'Aggravated Assault', 'I', '2009-2020', ''),
        ('1313', 'NIBRS', 'Aggravated Assault', 'High', 'Person', 'Aggravated Assault', 'I', '2009-2020', ''),
        ('1314', 'NIBRS', 'Aggravated Assault', 'High', 'Person', 'Aggravated Assault', 'I', '2009-2020', ''),
        ('1315', 'NIBRS', 'Aggravated Assault', 'High', 'Person', 'Aggravated Assault', 'I', '2009-2020', ''),
        ('1315K', 'NIBRS', 'Aggravated Assault', 'High', 'Person', 'Aggravated Assault', 'I', '2009-2020', ''),
        ('1316', 'NIBRS', 'Aggravated Assault', 'High', 'Person', 'Aggravated Assault', 'I', '2009-2020', 'Sometimes coded as Larceny'),
        ('1318', 'NIBRS', 'Aggravated Assault', 'High', 'Person', 'Aggravated Assault', 'I', '2009-2020', ''),
        ('1376', 'NIBRS', 'Aggravated Assault', 'High', 'Person', 'Aggravated Assault', 'I', '2009-2020', ''),
        ('1377', 'NIBRS', 'Aggravated Assault', 'High', 'Person', 'Aggravated Assault', 'I', '2009-2020', ''),
        ('1399', 'NIBRS', 'Aggravated Assault', 'High', 'Person', 'Aggravated Assault', 'I', '2009-2020', ''),
        ('3562', 'NIBRS', 'Aggravated Assault', 'High', 'Person', 'Aggravated Assault', 'I', '2009-2020', ''),
        ('5299', 'NIBRS', 'Aggravated Assault', 'High', 'Person', 'Aggravated Assault', 'I', '2009-2020', ''),
        ('5311', 'NIBRS', 'Aggravated Assault', 'High', 'Person', 'Aggravated Assault', 'I', '2009-2020', ''),
        
        # Burglary variations
        ('2006', 'NIBRS', 'Burglary', 'Medium', 'Property', 'Burglary', 'I', '2009-2020', ''),
        ('2202', 'NIBRS', 'Burglary', 'Medium', 'Property', 'Burglary', 'I', '2009-2020', ''),
        ('2202A', 'NIBRS', 'Burglary', 'Medium', 'Property', 'Burglary', 'I', '2009-2020', ''),
        ('2203', 'NIBRS', 'Burglary', 'Medium', 'Property', 'Burglary', 'I', '2009-2020', ''),
        ('2203A', 'NIBRS', 'Burglary', 'Medium', 'Property', 'Burglary', 'I', '2009-2020', ''),
        ('2204', 'NIBRS', 'Burglary', 'Medium', 'Property', 'Burglary', 'I', '2009-2020', ''),
        ('2205', 'NIBRS', 'Burglary', 'Medium', 'Property', 'Burglary', 'I', '2009-2020', 'Sometimes coded as Larceny'),
        ('2206', 'NIBRS', 'Burglary/Auto Theft/Larceny', 'Medium', 'Property', 'Burglary', 'I', '2009-2020', 'Multiple crime types'),
        ('5707', 'NIBRS', 'Burglary/Auto Theft', 'Medium', 'Property', 'Burglary', 'I', '2009-2020', ''),
        
        # Larceny variations
        ('105', 'NIBRS', 'Larceny-Non Vehicle', 'Medium', 'Property', 'Larceny', 'I', '2009-2020', ''),
        ('2099', 'NIBRS', 'Larceny-Non Vehicle/Auto Theft', 'Medium', 'Property', 'Larceny', 'I', '2009-2020', ''),
        ('2301', 'NIBRS', 'Larceny-Non Vehicle', 'Medium', 'Property', 'Larceny', 'I', '2009-2020', ''),
        ('2302', 'NIBRS', 'Larceny-Non Vehicle', 'Medium', 'Property', 'Larceny', 'I', '2009-2020', 'Sometimes Robbery'),
        ('2303', 'NIBRS', 'Larceny-Non Vehicle', 'Medium', 'Property', 'Larceny', 'I', '2009-2020', 'Sometimes Robbery'),
        ('2304', 'NIBRS', 'Larceny-From Vehicle', 'Medium', 'Property', 'Larceny', 'I', '2009-2020', ''),
        ('2305', 'NIBRS', 'Larceny-From Vehicle/Auto Theft', 'Medium', 'Property', 'Larceny', 'I', '2009-2020', ''),
        ('2307', 'NIBRS', 'Larceny-Non Vehicle', 'Medium', 'Property', 'Larceny', 'I', '2009-2020', ''),
        ('2308', 'NIBRS', 'Larceny-Non Vehicle', 'Medium', 'Property', 'Larceny', 'I', '2009-2020', ''),
        ('2310', 'NIBRS', 'Larceny-Non Vehicle', 'Medium', 'Property', 'Larceny', 'I', '2009-2020', ''),
        ('2314', 'NIBRS', 'Larceny-Non Vehicle', 'Medium', 'Property', 'Larceny', 'I', '2009-2020', ''),
        ('2316', 'NIBRS', 'Larceny-Non Vehicle', 'Medium', 'Property', 'Larceny', 'I', '2009-2020', ''),
        ('2317', 'NIBRS', 'Larceny-Non Vehicle', 'Medium', 'Property', 'Larceny', 'I', '2009-2020', ''),
        ('2318', 'NIBRS', 'Larceny-Non Vehicle', 'Medium', 'Property', 'Larceny', 'I', '2009-2020', ''),
        ('2361', 'NIBRS', 'Larceny-Non Vehicle', 'Medium', 'Property', 'Larceny', 'I', '2009-2020', ''),
        ('2373', 'NIBRS', 'Larceny-Non Vehicle', 'Medium', 'Property', 'Larceny', 'I', '2009-2020', ''),
        ('2374', 'NIBRS', 'Larceny-Non Vehicle', 'Medium', 'Property', 'Larceny', 'I', '2009-2020', ''),
        ('2382', 'NIBRS', 'Larceny-Non Vehicle/Auto Theft', 'Medium', 'Property', 'Larceny', 'I', '2009-2020', ''),
        ('2399', 'NIBRS', 'Larceny/Auto Theft', 'Medium', 'Property', 'Larceny', 'I', '2009-2020', 'Multiple types'),
        ('2803', 'NIBRS', 'Larceny-From Vehicle', 'Medium', 'Property', 'Larceny', 'I', '2009-2020', ''),
        ('2804', 'NIBRS', 'Larceny-From Vehicle', 'Medium', 'Property', 'Larceny', 'I', '2009-2020', ''),
        ('2899', 'NIBRS', 'Larceny/Auto Theft', 'Medium', 'Property', 'Larceny', 'I', '2009-2020', 'Multiple types'),
        ('9920', 'NIBRS', 'Larceny-From Vehicle', 'Medium', 'Property', 'Larceny', 'I', '2009-2020', ''),
        
        # Auto Theft variations
        ('2404', 'NIBRS', 'Auto Theft', 'Medium', 'Property', 'Motor Vehicle Theft', 'I', '2009-2020', 'Sometimes Robbery'),
        ('2404A', 'NIBRS', 'Auto Theft', 'Medium', 'Property', 'Motor Vehicle Theft', 'I', '2009-2020', ''),
        ('2424', 'NIBRS', 'Auto Theft', 'Medium', 'Property', 'Motor Vehicle Theft', 'I', '2009-2020', ''),
        ('2424A', 'NIBRS', 'Auto Theft', 'Medium', 'Property', 'Motor Vehicle Theft', 'I', '2009-2020', ''),
        ('2434', 'NIBRS', 'Auto Theft', 'Medium', 'Property', 'Motor Vehicle Theft', 'I', '2009-2020', 'Sometimes Larceny'),
        ('2434A', 'NIBRS', 'Auto Theft', 'Medium', 'Property', 'Motor Vehicle Theft', 'I', '2009-2020', 'Sometimes Agg Assault'),
        ('2599', 'NIBRS', 'Auto Theft/Robbery', 'High', 'Property', 'Robbery', 'I', '2009-2020', 'Coded as Robbery'),
        ('7399', 'NIBRS', 'Auto Theft/Robbery', 'High', 'Property', 'Robbery', 'I', '2009-2020', ''),
        
        # Homicide variations
        ('8', 'NIBRS', 'Homicide', 'High', 'Person', 'Murder', 'I', '2009-2020', ''),
        ('901', 'NIBRS', 'Homicide', 'High', 'Person', 'Murder', 'I', '2009-2020', ''),
        ('902', 'NIBRS', 'Homicide', 'High', 'Person', 'Murder', 'I', '2009-2020', ''),
        ('903', 'NIBRS', 'Homicide', 'High', 'Person', 'Murder', 'I', '2009-2020', ''),
        ('904', 'NIBRS', 'Homicide', 'High', 'Person', 'Murder', 'I', '2009-2020', ''),
        ('911', 'NIBRS', 'Homicide', 'High', 'Person', 'Murder', 'I', '2009-2020', ''),
        ('912', 'NIBRS', 'Homicide', 'High', 'Person', 'Murder', 'I', '2009-2020', ''),
        ('999', 'NIBRS', 'Homicide', 'High', 'Person', 'Murder', 'I', '2009-2020', ''),
        
        # Mixed/Multiple crime type codes
        ('2902', 'NIBRS', 'Multiple Crime Types', 'High', 'Varies', '', 'I', '2009-2020', 'Can be Homicide/Assault/Burglary/Theft'),
        ('9999', 'NIBRS', 'Multiple Crime Types', 'Medium', 'Varies', '', 'I', '2009-2020', 'Various crime types'),
    ]
    
    # Add additional NIBRS codes
    for nibrs_data in additional_nibrs:
        rows.append({
            'code': nibrs_data[0],
            'code_type': nibrs_data[1],
            'offense_description': nibrs_data[2],
            'severity': nibrs_data[3],
            'crime_against': nibrs_data[4],
            'ucr_index_category': nibrs_data[5],
            'ucr_part': nibrs_data[6],
            'data_years': nibrs_data[7],
            'notes': nibrs_data[8]
        })
    
    # Create DataFrame
    df_final = pd.DataFrame(rows)
    
    # Sort by code type, then code
    df_final['code_numeric'] = pd.to_numeric(df_final['code'], errors='coerce')
    df_final = df_final.sort_values(['code_type', 'code_numeric', 'code'])
    df_final = df_final.drop('code_numeric', axis=1)
    
    # Reorder columns
    column_order = [
        'code', 'code_type', 'offense_description', 'severity',
        'crime_against', 'ucr_index_category', 'ucr_part', 
        'data_years', 'notes'
    ]
    df_final = df_final[column_order]
    
    # Save to CSV
    output_path = Path(r"D:\local-repo\atl-crime-map\data-processing\atl_ucr_nibrs_severity_crosswalk_updated.csv")
    df_final.to_csv(output_path, index=False)
    
    # Print summary
    print(f"Total codes in crosswalk: {len(df_final)}")
    print(f"UCR codes: {len(df_final[df_final['code_type'] == 'UCR'])}")
    print(f"NIBRS codes: {len(df_final[df_final['code_type'] == 'NIBRS'])}")
    print(f"\nSeverity distribution:")
    print(df_final['severity'].value_counts())
    print(f"\nFile saved to: {output_path}")
    
    return df_final

if __name__ == "__main__":
    df = create_comprehensive_crosswalk()