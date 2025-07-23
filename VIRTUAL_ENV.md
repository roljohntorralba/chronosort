# Virtual Environment Setup

This project uses a virtual environment to manage dependencies, particularly for EXIF metadata support.

## Setup Instructions

1. **Create the virtual environment:**
   ```bash
   python3 -m venv chronosort_env
   ```

2. **Activate the virtual environment:**
   ```bash
   # macOS/Linux
   source chronosort_env/bin/activate
   
   # Windows
   chronosort_env\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Dependencies

- **Pillow (>=9.0.0)**: For reading EXIF metadata from photo files
- **tkinter**: For GUI support (usually included with Python)

## Usage with Virtual Environment

Always activate the virtual environment before running the applications:

```bash
# Activate virtual environment
source chronosort_env/bin/activate

# Run CLI version
python chronosort-cli/chronosort.py

# Run GUI version
python chronosort-gui/chronosort_gui.py
```

## Deactivating

When you're done working with the project:
```bash
deactivate
```
