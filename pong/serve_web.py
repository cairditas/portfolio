"""
Simple web server for testing the built Pong game
"""

import http.server
import socketserver
import os
import webbrowser
from pathlib import Path

PORT = 8000
BUILD_DIR = Path(__file__).parent / "build" / "web"

class GameHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=BUILD_DIR, **kwargs)

def serve_web():
    """Start a local web server for the game"""
    
    if not BUILD_DIR.exists():
        print("Web build not found! Please run: pygbag --build main.py")
        return
    
    os.chdir(BUILD_DIR)
    
    with socketserver.TCPServer(("", PORT), GameHTTPRequestHandler) as httpd:
        print(f"🎮 Pong Game Server")
        print(f"📍 Local URL: http://localhost:{PORT}")
        print(f"📁 Serving from: {BUILD_DIR}")
        print(f"🛑 Press Ctrl+C to stop")
        print()
        
        # Auto-open browser
        webbrowser.open(f"http://localhost:{PORT}")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n👋 Server stopped!")

if __name__ == "__main__":
    serve_web()
