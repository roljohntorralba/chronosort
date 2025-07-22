# ChronoSort GUI

A graphical user interface for organizing files by their creation/modification date.

## Features

- Easy-to-use desktop application
- Directory browser with drag & drop support
- Real-time progress tracking
- Detailed operation logging
- Dry-run mode for safe previewing
- Cross-platform (macOS, Windows, Linux)

## Installation

### Option 1: Run from Source

```bash
# Clone the repository
git clone https://github.com/yourusername/chronosort.git
cd chronosort/chronosort-gui

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python chronosort_gui.py
```

### Option 2: Download Standalone Executable

Download the appropriate executable for your platform from the [Releases](https://github.com/yourusername/chronosort/releases) page:
- **macOS**: `ChronoSort-macOS`
- **Windows**: `ChronoSort-Windows.exe`
- **Linux**: `ChronoSort-Linux`

## Usage

1. Launch the application
2. Click "Browse" to select a directory
3. Enable "Dry Run" to preview changes
4. Click "Organize Files" to start
5. Review the log output
6. If satisfied with preview, disable "Dry Run" and run again

## Building Standalone Executable

```bash
# Install PyInstaller
pip install PyInstaller

# Build executable
pyinstaller --onefile --windowed --name "ChronoSort" chronosort_gui.py
```

## Troubleshooting

### macOS: tkinter not found
```bash
brew install python-tk
```

### Linux: tkinter not found
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# CentOS/RHEL
sudo yum install tkinter
```

## Author

Roljohn Torralba

## License

MIT License
