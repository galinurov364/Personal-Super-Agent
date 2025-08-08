#!/usr/bin/env python3
"""
Range Checker Script
Checks if numbers fall within specified ranges.

Usage:
  python3 check_range.py 75 70 80 120 110 130 85 80 90

Format: value min max value min max ...
(triplets of numbers: value, range minimum, range maximum)
"""

import sys

def check_ranges():
    """Checks triplets of numbers for range compliance"""
    
    # Check command line arguments
    args = sys.argv[1:]  # remove script name
    
    if len(args) == 0:
        print("❌ Error: need to specify numbers for checking")
        print("📖 Usage: python3 check_range.py 75 70 80 120 110 130")
        print("📖 Format: value min max value min max ...")
        return
    
    if len(args) % 3 != 0:
        print("❌ Error: number count must be divisible by 3")
        print("📖 Each triplet: value minimum maximum")
        return
    
    # Process number triplets
    print("🔍 Range Check:")
    print("=" * 50)
    
    try:
        for i in range(0, len(args), 3):
            value = float(args[i])
            min_val = float(args[i + 1])
            max_val = float(args[i + 2])
            
            # Check range
            is_in_range = min_val <= value <= max_val
            status = "✅ In range" if is_in_range else "❌ Out of range"
            
            print(f"{value:8.1f} | [{min_val:6.1f} - {max_val:6.1f}] | {status}")
            
    except ValueError:
        print("❌ Error: all arguments must be numbers")
        return
    
    print("=" * 50)

if __name__ == "__main__":
    check_ranges() 