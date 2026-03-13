#!/usr/bin/env python3
"""
Pong Game Launcher

Run the refactored Pong game with proper Python path setup.
"""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import and run the game
from pong.game import PongGame

if __name__ == "__main__":
    game = PongGame()
    game.run()
