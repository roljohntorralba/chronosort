#!/bin/bash

echo "Building ChronoSort GUI executable..."

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Install PyInstaller if not already installed
pip install PyInstaller>=5.0

# Build the executable
pyinstaller --onefile \
           --windowed \
           --name "ChronoSort" \
           chronosort_gui.py

echo "Build complete!"
echo "Executable created in: dist/ChronoSort"
