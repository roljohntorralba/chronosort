#!/usr/bin/env python3
"""
ChronoSort GUI - File Date Organizer

A graphical user interface for organizing files by their creation/modification date.
Creates folders named with dates (YYYY-MM-DD format) and moves files into
the appropriate date folder.

Author: Rol John Torralba
"""

import os
import sys
import shutil
import threading
from datetime import datetime
from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext


class ChronoSortGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("ChronoSort - File Date Organizer")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        self.selected_directory = tk.StringVar()
        self.dry_run_mode = tk.BooleanVar(value=True)
        self.is_running = False
        
        self.setup_ui()
        
    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(4, weight=1)
        
        title_label = ttk.Label(main_frame, text="ChronoSort - File Date Organizer", 
                               font=('TkDefaultFont', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        ttk.Label(main_frame, text="Select Directory:").grid(row=1, column=0, sticky=tk.W, pady=5)
        
        dir_frame = ttk.Frame(main_frame)
        dir_frame.grid(row=1, column=1, columnspan=2, sticky=(tk.W, tk.E), padx=(10, 0), pady=5)
        dir_frame.columnconfigure(0, weight=1)
        
        self.dir_entry = ttk.Entry(dir_frame, textvariable=self.selected_directory, width=50)
        self.dir_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        
        browse_btn = ttk.Button(dir_frame, text="Browse", command=self.browse_directory)
        browse_btn.grid(row=0, column=1)
        
        options_frame = ttk.LabelFrame(main_frame, text="Options", padding="10")
        options_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        options_frame.columnconfigure(0, weight=1)
        
        dry_run_check = ttk.Checkbutton(options_frame, text="Dry Run (Preview mode - don't actually move files)", 
                                       variable=self.dry_run_mode)
        dry_run_check.grid(row=0, column=0, sticky=tk.W)
        
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=3, column=0, columnspan=3, pady=10)
        
        self.organize_btn = ttk.Button(buttons_frame, text="Organize Files", 
                                      command=self.start_organization)
        self.organize_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.cancel_btn = ttk.Button(buttons_frame, text="Cancel", 
                                    command=self.cancel_operation, state="disabled")
        self.cancel_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        clear_btn = ttk.Button(buttons_frame, text="Clear Log", command=self.clear_log)
        clear_btn.pack(side=tk.LEFT)
        
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(40, 0))
        
        log_frame = ttk.LabelFrame(main_frame, text="Output Log", padding="5")
        log_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, width=70, height=15, wrap=tk.WORD)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(5, 0))
        
    def browse_directory(self):
        """Open directory browser dialog."""
        directory = filedialog.askdirectory(title="Select directory to organize")
        if directory:
            self.selected_directory.set(directory)
            self.log(f"Selected directory: {directory}")
    
    def log(self, message):
        """Add message to log with timestamp."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_message = f"[{timestamp}] {message}\n"
        self.log_text.insert(tk.END, log_message)
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def clear_log(self):
        """Clear the log area."""
        self.log_text.delete(1.0, tk.END)
    
    def update_status(self, message):
        """Update status bar."""
        self.status_var.set(message)
    
    def start_organization(self):
        """Start the file organization process in a separate thread."""
        directory = self.selected_directory.get().strip()
        
        if not directory:
            messagebox.showerror("Error", "Please select a directory first.")
            return
        
        if not os.path.exists(directory):
            messagebox.showerror("Error", f"Directory '{directory}' does not exist.")
            return
        
        if not os.path.isdir(directory):
            messagebox.showerror("Error", f"'{directory}' is not a directory.")
            return
        
        if not self.dry_run_mode.get():
            result = messagebox.askyesno(
                "Confirm Organization", 
                f"This will organize files in:\n{directory}\n\nAre you sure you want to continue?"
            )
            if not result:
                return
        
        self.is_running = True
        self.organize_btn.config(state="disabled")
        self.cancel_btn.config(state="normal")
        self.progress.start()
        
        thread = threading.Thread(target=self.organize_files_thread, args=(directory,))
        thread.daemon = True
        thread.start()
    
    def cancel_operation(self):
        """Cancel the current operation."""
        self.is_running = False
        self.update_status("Cancelling operation...")
    
    def organize_files_thread(self, directory_path):
        """Thread function for organizing files."""
        try:
            self.update_status("Organizing files...")
            success = self.organize_files(directory_path, self.dry_run_mode.get())
            
            if success and not self.is_running:
                self.log("Organization cancelled by user.")
                self.update_status("Operation cancelled")
            elif success:
                self.log("Organization completed successfully!")
                self.update_status("Organization complete")
                if not self.dry_run_mode.get():
                    messagebox.showinfo("Success", "Files organized successfully!")
                else:
                    messagebox.showinfo("Preview Complete", "Dry run completed. Review the log to see what would be done.")
            else:
                self.log("Organization failed!")
                self.update_status("Organization failed")
                messagebox.showerror("Error", "Organization failed. Check the log for details.")
                
        except Exception as e:
            self.log(f"Unexpected error: {e}")
            self.update_status("Error occurred")
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")
        
        finally:
            self.root.after(0, self.reset_ui_state)
    
    def reset_ui_state(self):
        """Reset UI to initial state."""
        self.is_running = False
        self.organize_btn.config(state="normal")
        self.cancel_btn.config(state="disabled")
        self.progress.stop()
    
    def get_file_date(self, file_path):
        """Get the creation or modification date of a file."""
        try:
            stat = os.stat(file_path)
            creation_time = stat.st_birthtime if hasattr(stat, 'st_birthtime') else stat.st_ctime
            modification_time = stat.st_mtime
            
            file_timestamp = min(creation_time, modification_time)
            file_date = datetime.fromtimestamp(file_timestamp)
            return file_date.strftime('%Y-%m-%d')
        
        except Exception as e:
            self.log(f"Error getting date for {file_path}: {e}")
            return datetime.now().strftime('%Y-%m-%d')
    
    def create_date_folder(self, base_path, date_string):
        """Create a folder with the given date string if it doesn't exist."""
        folder_path = os.path.join(base_path, date_string)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            self.log(f"Created folder: {date_string}")
        return folder_path
    
    def is_date_folder(self, folder_name):
        """Check if a folder name matches the date pattern (YYYY-MM-DD)."""
        try:
            datetime.strptime(folder_name, '%Y-%m-%d')
            return True
        except ValueError:
            return False
    
    def organize_files(self, directory_path, dry_run=False):
        """Organize files in the given directory by their dates."""
        if not self.is_running:
            return False
        
        self.log(f"Organizing files in: {directory_path}")
        if dry_run:
            self.log("DRY RUN MODE - No files will be moved")
        self.log("-" * 50)
        
        files_moved = 0
        files_skipped = 0
        
        try:
            items = os.listdir(directory_path)
        except PermissionError:
            self.log(f"Error: Permission denied accessing '{directory_path}'")
            return False
        
        total_files = len([item for item in items if os.path.isfile(os.path.join(directory_path, item))])
        current_file = 0
        
        for item in items:
            if not self.is_running:
                return False
            
            item_path = os.path.join(directory_path, item)
            
            if os.path.isdir(item_path):
                if self.is_date_folder(item):
                    self.log(f"Skipping existing date folder: {item}")
                else:
                    self.log(f"Skipping directory: {item}")
                continue
            
            if item.startswith('.') or item.endswith('.DS_Store'):
                self.log(f"Skipping: {item}")
                files_skipped += 1
                continue
            
            current_file += 1
            self.update_status(f"Processing file {current_file}/{total_files}: {item}")
            
            file_date = self.get_file_date(item_path)
            
            if not dry_run:
                date_folder_path = self.create_date_folder(directory_path, file_date)
            else:
                date_folder_path = os.path.join(directory_path, file_date)
                self.log(f"Would create folder: {file_date}")
            
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
                    self.log(f"Moved: {item} -> {file_date}/{os.path.basename(destination_path)}")
                else:
                    self.log(f"Would move: {item} -> {file_date}/{item}")
                
                files_moved += 1
                
            except Exception as e:
                self.log(f"Error moving {item}: {e}")
                files_skipped += 1
        
        self.log("-" * 50)
        self.log(f"Summary:")
        self.log(f"Files processed: {files_moved}")
        self.log(f"Files skipped: {files_skipped}")
        
        if dry_run:
            self.log("\nTo actually move the files, uncheck 'Dry Run' and run again.")
        
        return True


def main():
    root = tk.Tk()
    app = ChronoSortGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
