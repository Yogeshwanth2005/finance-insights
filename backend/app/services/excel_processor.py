import pandas as pd
import numpy as np
from datetime import datetime
from dateutil import parser as dateutil_parser
import os

class ExcelProcessor:
    """Process Excel files and detect column mappings"""
    
    COMMON_COLUMN_NAMES = {
        'customer': ['customer', 'customer_name', 'name', 'company', 'client'],
        'amount': ['amount', 'invoice_amount', 'total', 'value', 'payment_amount'],
        'due_date': ['due_date', 'due', 'payment_due', 'deadline'],
        'payment_date': ['payment_date', 'paid_date', 'paid_on', 'payment_date', 'date_paid'],
        'email': ['email', 'email_address', 'contact_email'],
        'phone': ['phone', 'phone_number', 'contact']
    }
    
    @staticmethod
    def detect_columns(df):
        """Auto-detect column mappings in DataFrame"""
        detected = {}
        df_columns_lower = {col.lower(): col for col in df.columns}
        
        for field, aliases in ExcelProcessor.COMMON_COLUMN_NAMES.items():
            for alias in aliases:
                if alias in df_columns_lower:
                    detected[field] = df_columns_lower[alias]
                    break
        
        return detected
    
    @staticmethod
    def read_excel(file_path, sheet_name=0):
        """Read Excel file and return DataFrame"""
        try:
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            return df
        except Exception as e:
            raise Exception(f"Failed to read Excel file: {str(e)}")
    
    @staticmethod
    def parse_date(date_value):
        """Parse various date formats"""
        if pd.isna(date_value) or date_value == '':
            return None
        
        if isinstance(date_value, datetime):
            return date_value
        
        if isinstance(date_value, (int, float)):
            # Excel date serial number
            try:
                return pd.Timestamp(date_value, unit='D', origin=pd.Timestamp('1899-12-30')).to_pydatetime()
            except:
                return None
        
        try:
            return dateutil_parser.parse(str(date_value))
        except:
            return None
    
    @staticmethod
    def validate_and_process(df, column_mapping):
        """Validate and process the data"""
        required_fields = ['customer', 'amount', 'due_date']
        
        # Check required columns
        missing = [f for f in required_fields if column_mapping.get(f) not in df.columns]
        if missing:
            raise Exception(f"Missing required columns: {missing}")
        
        processed_data = []
        
        for idx, row in df.iterrows():
            try:
                customer_name = str(row[column_mapping['customer']]).strip()
                amount = float(row[column_mapping['amount']])
                due_date = ExcelProcessor.parse_date(row[column_mapping['due_date']])
                payment_date = None
                
                if 'payment_date' in column_mapping and column_mapping['payment_date'] in df.columns:
                    payment_date = ExcelProcessor.parse_date(row[column_mapping['payment_date']])
                
                if not customer_name or amount <= 0 or not due_date:
                    continue
                
                processed_data.append({
                    'customer_name': customer_name,
                    'amount': amount,
                    'due_date': due_date,
                    'payment_date': payment_date,
                    'email': row.get(column_mapping.get('email'), '') if 'email' in column_mapping else '',
                    'phone': row.get(column_mapping.get('phone'), '') if 'phone' in column_mapping else '',
                })
            except Exception as e:
                # Skip rows with errors
                continue
        
        if not processed_data:
            raise Exception("No valid records found in Excel file")
        
        return processed_data
