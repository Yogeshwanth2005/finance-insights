#!/usr/bin/env python3
"""
Finance Insights - Sample Data Generator
Generates test Excel files for development and testing
"""

import pandas as pd
from datetime import datetime, timedelta
import random
import sys

def create_sample_excel(filename='sample_payments.xlsx', num_records=50):
    """Generate sample payment data for testing"""
    
    companies = [
        'ABC Corporation',
        'XYZ Limited',
        'Tech Solutions Inc',
        'Global Services Ltd',
        'Digital Innovations',
        'Enterprise Systems',
        'Cloud Computing Co',
        'Data Analytics Plus',
        'Business Consulting Group',
        'Financial Services Ltd',
        'Innovation Labs',
        'Growth Partners Inc'
    ]
    
    today = datetime.now()
    data = []
    
    print(f"📊 Generating {num_records} sample payment records...")
    
    for i in range(num_records):
        company = random.choice(companies)
        amount = round(random.uniform(1000, 50000), 2)
        due_date = today - timedelta(days=random.randint(0, 90))
        
        # 70% paid, 30% unpaid (creates realistic late payment scenarios)
        if random.random() < 0.7:
            payment_days = random.randint(-10, 45)
            payment_date = due_date + timedelta(days=payment_days)
        else:
            payment_date = None
        
        data.append({
            'Customer': company,
            'Amount': amount,
            'Due Date': due_date.strftime('%Y-%m-%d'),
            'Payment Date': payment_date.strftime('%Y-%m-%d') if payment_date else '',
            'Email': f'contact@{company.lower().replace(" ", "")}.com',
            'Phone': f'+1-{random.randint(200, 999)}-{random.randint(200, 999)}-{random.randint(1000, 9999)}'
        })
    
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)
    
    print(f"✅ Sample file created: {filename}")
    print(f"📊 Generated {len(data)} records")
    print(f"\n📝 File contains:")
    print(f"   - {len(df)} invoices")
    print(f"   - {len(df['Customer'].unique())} unique customers")
    print(f"   - Total amount: ${df['Amount'].sum():,.2f}")
    
    return filename

if __name__ == '__main__':
    try:
        create_sample_excel()
        print("\n✅ Ready to upload to Finance Insights!")
    except ImportError:
        print("❌ Please install: pip install pandas openpyxl")
    except Exception as e:
        print(f"❌ Error: {e}")
