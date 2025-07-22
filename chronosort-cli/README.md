# ChronoSort CLI

A command-line tool for organizing files by their creation/modification date.

## Features

- Organizes files into date-named folders (YYYY-MM-DD format)
- Dry-run mode for safe previewing
- Handles duplicate filenames automatically
- Cross-platform compatible (macOS, Windows, Linux)

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/chronosort.git
cd chronosort/chronosort-cli

# Create virtual environment (optional but recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# No additional dependencies required - uses Python standard library only
```

## Usage

```bash
# Organize files in current directory (dry run)
python chronosort.py --dry-run

# Organize files in current directory (actual move)
python chronosort.py

# Organize specific directory
python chronosort.py /path/to/photos

# Preview changes for specific directory
python chronosort.py /path/to/photos --dry-run
```

## Examples

Before:
```
photos/
├── IMG_001.jpg (created 2025-05-01)
├── IMG_002.jpg (created 2025-05-01)
├── vacation.mp4 (created 2025-05-03)
└── document.pdf (created 2025-05-02)
```

After:
```
photos/
├── 2025-05-01/
│   ├── IMG_001.jpg
│   └── IMG_002.jpg
├── 2025-05-02/
│   └── document.pdf
└── 2025-05-03/
    └── vacation.mp4
```

## Author

Roljohn Torralba

## License

MIT License
