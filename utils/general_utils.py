from datetime import datetime

import os
import pandas as pd
import logging
import re

logging.basicConfig(
    filename='log_output.log',
    filemode='a',
    level=logging.INFO,
    format='{"time":  %(asctime)s, "class": "%(name)s", "level": "%(levelname)s", "msg": %(message)s}'
)

class LogUtils:
    @staticmethod
    def get_logger(uid):
        return logging.getLogger(uid)

class GeneralUtils:
    def is_primitive_type(self, obj):
        primitive_types = (int, float, str, bool, type(None))
        return isinstance(obj, primitive_types)
        
    def filter_primitive_attributes(self, row: dict):
        return dict(filter(lambda item: self.is_primitive_type(item[1]), row.items()))
    
    @staticmethod
    def get_script_directory():
        """Get the directory path where the script is located."""
        return os.path.dirname(os.path.abspath(__file__))
    
    def find_files_by_extension(self, extension: str):
        script_directory = self.get_script_directory()

        # List all files in the script directory
        all_files = os.listdir(script_directory)

        # Filter files with the specified extension and get their full paths
        matching_files = [os.path.join(script_directory, file) for file in all_files if file.lower().endswith(f'.{extension.lower()}')]

        return matching_files
    
    def find_row_with_label(self, df: pd.DataFrame, label):
        # Check if the DataFrame contains the specified value in any column
        if any(df.isin([label]).any().values):
            # Find the index where the value is present
            label_index = df[df.eq(label).any(axis=1)].index[0]

            # Retrieve the DataFrame with the specified row
            label_df = df.loc[[label_index]]

            # Filter out rows with NaN values in all columns
            label_df = label_df.dropna(axis=1, how='all')

            return label_df
        else:
            return None
        
    def get_value_from_label_df(self, label_df: pd.DataFrame):
        # Check if the DataFrame has any rows
        if not label_df.empty:
            # Assume the value is in the second column (change index if needed)
            value_column_index = 1

            # Get the value from the DataFrame
            value = label_df.iloc[0, value_column_index]

            return value
        else:
            return None
        
    def transform_to_snake_case(self, column_name: str):
        # Replace spaces and special characters with underscores
        column_name = column_name.replace(' ', '_')

        # Remove special characters and convert to lowercase
        column_name = re.sub(r'[^a-zA-Z0-9_]', '', column_name.lower())
        return column_name

    def read_csv_and_transform(self, csv_path):
        # Read CSV file
        df = pd.read_csv(csv_path)

        # Transform column names to snake case
        df.columns = [self.transform_to_snake_case(col) for col in df.columns]

        return df
    
    def convert_string_dates_to_datetime(self, df: pd.DataFrame):
        for column in df.columns:
            # Check if the column contains "date" in its name
            if 'date' in column.lower():
                # Convert "date" columns to string
                df[column] = df[column].fillna(datetime.now().strftime('%Y%m%d')).astype(int).astype(str)

        for column in df.columns:
            # Check if the column values are datetime strings
            if pd.api.types.is_string_dtype(df[column]) and df[column].str.match(r'\d{8}').all():
                df[column] = pd.to_datetime(df[column], errors='coerce', format='%Y%m%d')
        
        return df
    
    def convert_to_boolean(self, df: pd.DataFrame):
        """
        Convert columns in a DataFrame to boolean if they contain only 'Y' and 'N'.

        Parameters:
        - df: DataFrame
        """
        for column_name in df.columns:
            # Check if the column contains only 'Y' and 'N'
            unique_values = df[column_name].dropna().unique()
            if column_name in ["stop_advance_flag", "modification_flag"]:
                # Replace 'N' with False
                df[column_name] = df[column_name].replace({'N': False, 'Y': True})

                # Convert to boolean
                df[column_name] = df[column_name].astype(bool)
                print(f"replaceing {column_name} with boolean.")
        
        return df