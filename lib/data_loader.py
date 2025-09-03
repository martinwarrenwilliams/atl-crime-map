import pandas as pd
from datetime import datetime
import os
from pathlib import Path
from . import config

class CrimeDataLoader:
    def __init__(self, data_path=None):
        self.data_path = data_path if data_path else config.RAW_DATA_DIR
        self.latest_file = config.LATEST_DATA_FILE
        self.df = None
        
    def load_latest_data(self):
        file_path = os.path.join(self.data_path, self.latest_file)
        self.df = pd.read_csv(file_path, low_memory=False)
        
        date_format = config.DATE_FORMAT
        self.df['ReportDate'] = pd.to_datetime(self.df['ReportDate'], format=date_format, errors='coerce')
        self.df['OccurredFromDate'] = pd.to_datetime(self.df['OccurredFromDate'], format=date_format, errors='coerce')
        self.df['OccurredToDate'] = pd.to_datetime(self.df['OccurredToDate'], format=date_format, errors='coerce')
        
        self.df = self.df.dropna(subset=['OccurredFromDate'])
        
        return self.df
    
    def filter_by_address(self, address):
        if self.df is None:
            self.load_latest_data()
        
        filtered_df = self.df[self.df['StreetAddress'].str.upper().str.contains(address.upper(), na=False)]
        return filtered_df
    
    def get_crime_summary(self, address):
        filtered_df = self.filter_by_address(address)
        
        summary = {
            'total_crimes': len(filtered_df),
            'crime_types': filtered_df['NIBRS_Offense'].value_counts().to_dict(),
            'location_types': filtered_df['LocationType'].value_counts().to_dict(),
            'date_range': {
                'earliest': filtered_df['OccurredFromDate'].min() if len(filtered_df) > 0 else None,
                'latest': filtered_df['OccurredToDate'].max() if len(filtered_df) > 0 else None
            },
            'firearm_involved': filtered_df['FireArmInvolved'].value_counts().to_dict()
        }
        
        return summary
    
    def get_time_series_data(self, address, freq='M'):
        filtered_df = self.filter_by_address(address).copy()
        
        if len(filtered_df) == 0:
            return pd.DataFrame()
        
        filtered_df['month'] = filtered_df['OccurredFromDate'].dt.to_period(freq)
        time_series = filtered_df.groupby('month').size().reset_index(name='count')
        time_series['month'] = time_series['month'].dt.to_timestamp()
        
        return time_series
    
    def get_quarterly_time_series_data(self, address):
        filtered_df = self.filter_by_address(address).copy()
        
        if len(filtered_df) == 0:
            return pd.DataFrame()
        
        filtered_df['quarter'] = filtered_df['OccurredFromDate'].dt.to_period('Q')
        time_series = filtered_df.groupby('quarter').size().reset_index(name='count')
        
        time_series['quarter_label'] = time_series['quarter'].apply(lambda x: f"{x.year} Q{x.quarter}")
        time_series['quarter_date'] = time_series['quarter'].dt.to_timestamp()
        
        return time_series
    
    def get_multiple_addresses_data(self, addresses):
        results = {}
        for address in addresses:
            results[address] = {
                'data': self.filter_by_address(address),
                'summary': self.get_crime_summary(address)
            }
        return results