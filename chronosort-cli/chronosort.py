#!/usr/bin/env python3
"""
ChronoSort CLI - File Date Organizer

Organizes files in a directory by their creation/modification date.
Creates folders named with dates (YYYY-MM-DD format) and moves files into
the appropriate date folder based on when they were created or last modified.

Author: Roljohn Torralba
Usage: python chronosort.py [directory_path] [--dry-run]
"""

import os
import sys
import shutil
from datetime import datetime
from pathlib import Path
import argparse


def get_file_date(file_path):
    """Get the creation or modification date of a file."""
    try:
        stat = os.stat(file_path)
        creation_time = stat.st_birthtime if hasattr(stat, 'st_birthtime') else stat.st_ctime
        modification_time = stat.st_mtime
        
        file_timestamp = min(creation_time, modification_time)
        file_date = datetime.fromtimestamp(file_timestamp)
        return file_date.strftime('%Y-%m-%d')
    
    except Exception as e:
        print(f"Error getting date for {file_path}: {e}")
        return datetime.now().strftime('%Y-%m-%d')


def create_date_folder(base_path, date_string):
    """Create a folder with the given date string if it doesn't exist."""
    folder_path = os.path.join(base_path, date_string)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Created folder: {date_string}")
    return folder_path


def is_date_folder(folder_name):
    """Check if a folder name matches the date pattern (YYYY-MM-DD)."""
    try:
        datetime.strptime(folder_name, '%Y-%m-%d')
        return True
    except ValueError:
        return False


def organize_files(directory_path, dry_run=False):
    """Organize files in the given directory by their dates."""
    if not os.path.exists(directory_path):
        print(f"Error: Directory '{directory_path}' does not exist.")
        return False
    
    if not os.path.isdir(directory_path):
        print(f"Error: '{directory_path}' is not a directory.")
        return False
    
    print(f"Organizing files in: {directory_path}")
    if dry_run:
        print("DRY RUN MODE - No files will be moved")
    print("-" * 50)
    
    files_moved = 0
    files_skipped = 0
    
    try:
        items = os.listdir(directory_path)
    except PermissionError:
        print(f"Error: Permission denied accessing '{directory_path}'")
        return False
    
    for item in items:
        item_path = os.path.join(directory_path, item)
        
        if os.path.isdir(item_path):
            if is_date_folder(item):
                print(f"Skipping existing date folder: {item}")
            else:
                print(f"Skipping directory: {item}")
            continue
        
        if item.startswith('.') or item == os.path.basename(__file__):
            print(f"Skipping: {item}")
            files_skipped += 1
            continue
        
        file_date = get_file_date(item_path)
        
        if not dry_run:
            date_folder_path = create_date_folder(directory_path, file_date)
        else:
            date_folder_path = os.path.join(directory_path, file_date)
            print(f"Would create folder: {file_date}")
        
        destination_path = os.path.join(date_folder_path, item)
        
        try:
            if not dry_run:
                if os.path.exists(destination_path):
                    base, ext = os.path.splitext(item)
                    counter = 1
                    while os.path.exists(destination_path):
                        new_name = f"{base}_{counter}{ext}"
                        destination_path = os.path.join(date_folder_path, new_name)
                        counter += 1
                
                shutil.move(item_path, destination_path)
                print(f"Moved: {item} -> {file_date}/{os.path.basename(destination_path)}")
            else:
                print(f"Would move: {item} -> {file_date}/{item}")
            
            files_moved += 1
            
        except Exception as e:
            print(f"Error moving {item}: {e}")
            files_skipped += 1
    
    print("-" * 50)
    print(f"Summary:")
    print(f"Files processed: {files_moved}")
    print(f"Files skipped: {files_skipped}")
    
    if dry_run:
        print("\nTo actually move the files, run the script without the --dry-run flag.")
    
    return True


def main():
    parser = argparse.ArgumentParser(
        description="ChronoSort - Organize files by their creation/modification date",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python chronosort.py                    # Organize current directory
  python chronosort.py /path/to/photos   # Organize specific directory
  python chronosort.py --dry-run         # Preview what would be done
        """
    )
    
    parser.add_argument(
        'directory',
        nargs='?',
        default='.',
        help='Directory to organize (default: current directory)'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be done without actually moving files'
    )
    
    args = parser.parse_args()
    directory_path = os.path.abspath(args.directory)
    
    print("ChronoSort - File Date Organizer")
    print("=" * 50)
    
    if not args.dry_run:
        print(f"This will organize files in: {directory_path}")
        response = input("Do you want to continue? (y/N): ").strip().lower()
        if response not in ['y', 'yes']:
            print("Operation cancelled.")
            return
    
    success = organize_files(directory_path, args.dry_run)
    
    if success:
        print("\nOrganization complete!")
    else:
        print("\nOrganization failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
