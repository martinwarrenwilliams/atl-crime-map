# Raw Data Documentation

## Data Files

### Crime_Data_1997_2002.csv
- **Description**: Historical Atlanta crime data with UCR codes (Part 1)
- **Date Range**: 1997 to 2002
- **Format**: CSV
- **Size**: 57.9 MB
- **Records**: 327,061
- **Key Columns**: Address, Incident_#, UCR_#, Offense_Description, Report_date1, Date_From1, Day_From, Time_From, Weapon, Longitude, Latitude

### Crime_Data_2003_2008.csv
- **Description**: Historical Atlanta crime data with UCR codes (Part 2)
- **Date Range**: 2003 to 2008
- **Format**: CSV
- **Size**: 44.6 MB
- **Records**: 252,766
- **Key Columns**: Address, Incident_#, UCR_#, Offense_Description, Report_date1, Date_From1, Day_From, Time_From, Weapon, Longitude, Latitude
- **Note**: Includes 1 record from 2014 (data anomaly)

### 2009_2020CrimeData_3002993194443433393.csv
- **Description**: Atlanta crime data with NIBRS codes
- **Date Range**: 2009 to 2020
- **Format**: CSV
- **Size**: 56.5 MB
- **Records**: 366,824
- **Key Columns**: Report Number, Report Date, Day Occurred, Occur Date, Occur Time, Zone, Location, Crime Type, NIBRS Code, Longitude, Latitude

### AxonCrimeData_Export_view_6594257177302908045.csv
- **Description**: Current Atlanta crime data with NIBRS/UCR codes and offense classifications
- **Date Range**: 1/1/2021 to 12/14/2023
- **Format**: CSV
- **Size**: ~60 MB
- **Records**: 273,122
- **Key Columns**: IncidentNumber, FireArmInvolved, ReportDate, OccurredFromDate, OccurredToDate, NibrsUcrCode, NIBRS_Offense, StreetAddress, LocationType, Longitude, Latitude

## Data Notes

- **1997-2008**: Uses UCR (Uniform Crime Reporting) codes and detailed offense descriptions
  - Original file was split into two parts for git compatibility (was 102MB)
  - Part 1: 1997-2002 (327,061 records)
  - Part 2: 2003-2008 (252,766 records)
- **2009-2020**: Includes both crime type descriptions and NIBRS codes for standardization
- **2021-2023**: Uses NIBRS/UCR combined codes with full offense classifications and additional metadata
- All files include latitude/longitude coordinates for geographic analysis
- Total dataset covers ~950,000 crime records across 27 years

## File Processing Notes

- Original 1997-2008 file (`Crime_Data_1997_2008_-223750340949836035.csv`) was split using `split_crime_data.py` to keep files under 100MB for git
- Use `atl_ucr_nibrs_severity_crosswalk_full.csv` in data-processing folder to harmonize crime severity across all datasets