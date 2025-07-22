# ChronoSort

A powerful file organization tool that automatically sorts files into date-based folders. Available as both a command-line tool and desktop application.

## Overview

ChronoSort analyzes file creation and modification dates, then organizes them into folders named with the date (YYYY-MM-DD format). Perfect for organizing photos, documents, downloads, or any collection of files that need chronological organization.

## Projects

### 📱 [ChronoSort CLI](./chronosort-cli/)
Command-line interface for batch file organization. Perfect for automation and server environments.

**Features:**
- Lightning-fast batch processing
- Dry-run mode for safe previewing
- Cross-platform compatibility
- No external dependencies

### 🖥️ [ChronoSort GUI](./chronosort-gui/)
Desktop application with intuitive graphical interface. Ideal for everyday users who prefer visual tools.

**Features:**
- User-friendly interface
- Real-time progress tracking
- Detailed operation logging
- Available as standalone executable

## Quick Start

### CLI Version
```bash
cd chronosort-cli
python chronosort.py /path/to/files --dry-run
```

### GUI Version
```bash
cd chronosort-gui
python chronosort_gui.py
```

## Example Organization

**Before:**
```
photos/
├── IMG_001.jpg (created 2025-05-01)
├── IMG_002.jpg (created 2025-05-01)
├── vacation.mp4 (created 2025-05-03)
└── document.pdf (created 2025-05-02)
```

**After:**
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

## Installation

Choose your preferred method:

1. **Download executables** from [Releases](https://github.com/roljohntorralba/chronosort/releases)
2. **Clone and run from source** (requires Python 3.7+)

```bash
git clone https://github.com/roljohntorralba/chronosort.git
cd chronosort
```

## Use Cases

- 📸 **Photo Organization**: Sort photos by capture date
- 📄 **Document Management**: Organize files by creation date
- 💾 **Download Cleanup**: Sort downloads chronologically
- 🗂️ **Archive Management**: Organize any file collection by date
- 🏢 **Backup Organization**: Sort backup files by date

## Safety Features

- **Dry-run mode**: Preview changes before execution
- **Duplicate handling**: Automatically renames conflicting files
- **Error recovery**: Continues processing if individual files fail
- **Detailed logging**: Complete record of all operations

## Requirements

- **Python 3.7+** (for running from source)
- **macOS 10.14+, Windows 10+, or Linux** (for executables)

## Contributing

Contributions welcome! Please read our contributing guidelines and submit pull requests.

## Author

**Rol John Torralba**

## License

MIT License - see LICENSE file for details.

## Support

- 🐛 [Report Issues](https://github.com/roljohntorralba/chronosort/issues)
- 💡 [Feature Requests](https://github.com/roljohntorralba/chronosort/discussions)
- 📖 [Documentation](https://github.com/roljohntorralba/chronosort/wiki)
