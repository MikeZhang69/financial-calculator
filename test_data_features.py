#!/usr/bin/env python3
"""
Test script for data management features
"""

import json
import csv
from datetime import datetime
import os

def test_data_export():
    """Test CSV export functionality"""
    
    # Sample NPV calculation data
    npv_data = {
        'type': 'npv',
        'inputs': {
            'discount_rate': 10,
            'cash_flows': [-10000, 3000, 4000, 5000, 2000]
        },
        'results': {
            'npv': 1169.87,
            'irr': 0.1393,
            'payback': 3.2
        }
    }
    
    # Test CSV export
    filename = "test_npv_export.csv"
    
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['NPV Analysis Report'])
            writer.writerow(['Generated:', datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
            writer.writerow([])
            
            writer.writerow(['Inputs:'])
            writer.writerow(['Discount Rate (%)', npv_data['inputs']['discount_rate']])
            writer.writerow(['Cash Flows', ', '.join(map(str, npv_data['inputs']['cash_flows']))])
            writer.writerow([])
            
            writer.writerow(['Results:'])
            writer.writerow(['NPV ($)', f"{npv_data['results']['npv']:,.2f}"])
            writer.writerow(['IRR (%)', f"{npv_data['results']['irr']:.2%}"])
            writer.writerow(['Payback (years)', f"{npv_data['results']['payback']:.1f}"])
        
        print(f"✅ CSV export test successful: {filename}")
        
        # Clean up
        if os.path.exists(filename):
            os.remove(filename)
            
    except Exception as e:
        print(f"❌ CSV export test failed: {e}")

def test_json_storage():
    """Test JSON history storage"""
    
    # Sample history data
    history_data = [
        {
            'timestamp': datetime.now().isoformat(),
            'type': 'npv',
            'inputs': {'discount_rate': 10, 'cash_flows': [-1000, 300, 400, 500]},
            'results': {'npv': -21.04, 'irr': 0.0993, 'payback': 3.2}
        }
    ]
    
    filename = "test_history.json"
    
    try:
        # Test saving
        with open(filename, 'w') as f:
            json.dump(history_data, f, indent=2)
        
        # Test loading
        with open(filename, 'r') as f:
            loaded_data = json.load(f)
        
        if loaded_data == history_data:
            print("✅ JSON storage test successful")
        else:
            print("❌ JSON storage test failed: data mismatch")
        
        # Clean up
        if os.path.exists(filename):
            os.remove(filename)
            
    except Exception as e:
        print(f"❌ JSON storage test failed: {e}")

if __name__ == "__main__":
    print("Testing Data Management Features...")
    print("=" * 40)
    
    test_data_export()
    test_json_storage()
    
    print("\nData management tests completed!")