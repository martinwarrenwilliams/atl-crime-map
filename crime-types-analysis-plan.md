# Crime Types Analysis Plan

## Overview
Comprehensive analysis of crime types across three Atlanta crime data files spanning 1997-2025, identifying formatting differences and preparing for dashboard integration.

## Key Findings from Initial Analysis

### Crime Type Classifications by Period

#### 1997-2008 File (`Crime_Data_1997_2008_3118992194175389166.csv`)
- **Total Records**: 579,827
- **Unique Crime Types**: 94
- **Classification System**: Detailed descriptions with subcategories
- **Top Crime Types**:
  - LAR-ARTICLES FROM VEHICLE: 107,626
  - BURGLARY-FORCED ENTRY-RESIDENC: 58,768
  - LARCENY-FROM BUILDING: 51,323
  - AUTOTHEFT: 50,008
  - LAR-PARTS FROM VEHICLE: 44,482

#### 2009-2020 File (`2009_2020CrimeData_3434152755446864633.csv`)
- **Total Records**: 366,824
- **Unique Crime Types**: 7 (highly aggregated)
- **Classification System**: Broad categories only
- **Crime Types**:
  - LARCENY-FROM VEHICLE: 114,560
  - LARCENY-NON VEHICLE: 88,356
  - BURGLARY: 62,641
  - AUTO THEFT: 50,349
  - AGG ASSAULT: 27,212
  - ROBBERY: 22,582
  - HOMICIDE: 1,124
- **Note**: User will provide updated file with NIBRS classifications

#### 2021-2025 File (`AxonCrimeData_Export_view_-3489168499745344284.csv`)
- **Total Records**: 273,122
- **Unique Crime Types**: 57
- **Classification System**: NIBRS (National Incident-Based Reporting System)
- **Top Crime Types**:
  - All Other Offenses: 56,386
  - Theft From Motor Vehicle: 36,796
  - Destruction/Damage/Vandalism of Property: 21,680
  - Drug/Narcotic Violations: 19,187
  - Motor Vehicle Theft: 18,514

## Formatting Differences

### Column Structure Changes

| Aspect | 1997-2008 | 2009-2020 | 2021-2025 |
|--------|-----------|-----------|-----------|
| **Crime Type Field** | Offense_Description | Crime Type | NIBRS_Offense |
| **Address Field** | Address | Location | StreetAddress |
| **Date Column(s)** | Report_date1 | Report Date | ReportDate, OccurredFromDate, OccurredToDate |
| **Date Format** | MM/DD/YYYY H:MM:SS AM/PM | MM/DD/YYYY H:MM:SS AM/PM | MM/DD/YYYY H:MM:SS AM/PM |
| **Additional Fields** | Incident_#, x, y | Day Occurred, Occur Time, Zone | FireArmInvolved, LocationType, Beat, NhoodName, DISTRICT, NPU |

## Next Steps

### 1. Create Data Processing Infrastructure
- Create `data-processing/` folder for analysis outputs
- Set up Python scripts for data transformation

### 2. Generate Crime Types Analysis CSV
Create `crime_types_analysis.csv` with following columns:
- `source_file`: Which raw data file the crime type comes from
- `year_range`: Time period covered (e.g., "1997-2008")
- `crime_type_original`: Original crime type text from source
- `count`: Number of occurrences
- `classification_system`: Type of classification (Detailed/Broad/NIBRS)
- `nibrs_mapping`: Suggested NIBRS category for standardization
- `category_group`: High-level category for dashboard visualization

### 3. Create Crime Type Mapping Dictionary
Develop mappings between different classification systems:
- Map detailed 1997-2008 descriptions to NIBRS categories
- Map broad 2009-2020 categories to NIBRS subcategories
- Ensure consistent categorization across all time periods

### 4. Data Integration Considerations
- **Performance**: Consider data volume when loading all three files (1.2M+ records total)
- **Schema Normalization**: Create unified schema for dashboard consumption
- **Date Handling**: Standardize date formats and handle malformed dates
- **Address Standardization**: Normalize address formats for consistent filtering

## Technical Implementation Notes

### Python Processing Script Structure
```python
# Key components needed:
1. Data loader class extension to handle multiple file formats
2. Crime type normalizer/mapper
3. Statistical analysis functions
4. CSV export with proper encoding for special characters
```

### Dashboard Integration Points
- Extend `CrimeDataLoader` class to handle multiple source files
- Add file selection dropdown or date-based automatic source selection
- Implement crime type mapping layer for consistent visualization
- Consider caching strategy for performance with large datasets

## Data Quality Considerations
- Handle inconsistent capitalization in crime types
- Address potential duplicates across file boundaries
- Validate date ranges don't overlap between files
- Document any data gaps or anomalies found

## Deliverables
1. `data-processing/crime_types_analysis.csv` - Complete crime type inventory
2. Python script for generating the analysis
3. Documentation of mapping decisions
4. Recommendations for dashboard updates to support historical data

---
*Note: This plan will be updated once the new 2009-2020 file with NIBRS classifications is available.*