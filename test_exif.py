#!/usr/bin/env python3
"""
Test script to verify EXIF functionality
"""

import os
import sys
import tempfile
from datetime import datetime

# Add the chronosort-cli directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'chronosort-cli'))

from chronosort import get_file_date, get_exif_date

def test_exif_functionality():
    """Test EXIF date extraction functionality."""
    print("Testing EXIF functionality...")
    print(f"Pillow available: {os.path.exists('/Users/roljohntorralba/Projects/file-date-organizer/chronosort_env/lib/python3.13/site-packages/PIL')}")
    
    # Create a temporary directory for testing
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"\nTesting directory: {temp_dir}")
        
        # Create a simple text file to test non-image files
        text_file = os.path.join(temp_dir, "test.txt")
        with open(text_file, 'w') as f:
            f.write("This is a test file")
        
        print(f"\nTesting text file: {os.path.basename(text_file)}")
        file_date = get_file_date(text_file)
        print(f"File date: {file_date}")
        
        # Test EXIF function directly on text file (should return None)
        exif_date = get_exif_date(text_file)
        print(f"EXIF date: {exif_date}")
        
        print("\nFor testing with actual photos, please place some JPEG files in the test directory and run the organizer.")

if __name__ == "__main__":
    test_exif_functionality()
