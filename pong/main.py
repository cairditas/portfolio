"""
Main entry point for Pong Game
"""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

from pong.game import PongGame

if __name__ == "__main__":
    game = PongGame()
    game.run()
