#!/bin/bash

# Pong Game Startup Script

echo "=== Pong Game Launcher ==="
echo "1. Run locally (requires pygame)"
echo "2. Build for web (requires pygbag)"
echo "3. Run tests"
echo "4. Exit"
echo ""

read -p "Choose an option (1-4): " choice

case $choice in
    1)
        echo "Starting Pong game locally..."
        source venv/bin/activate
        python main.py
        ;;
    2)
        echo "Building Pong game for web..."
        source venv/bin/activate
        pygbag --build main.py
        echo "Build complete! Files are in build/web/"
        echo "To test locally, run: python -m http.server 8000 --directory build/web"
        ;;
    3)
        echo "Running tests..."
        source venv/bin/activate
        python -m pytest tests/ -v
        ;;
    4)
        echo "Goodbye!"
        exit 0
        ;;
    *)
        echo "Invalid option!"
        exit 1
        ;;
esac
