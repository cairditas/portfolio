"""
Main entry point for Pong Game
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def main():
    """Main entry point."""
    try:
        from pong.game import PongGame
        game = PongGame()
        game.run()
        return 0
    except ImportError as e:
        print(f"Import error: {e}")
        print("Run: pip install pygame")
        return 1
    except Exception as e:
        print(f"Game error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
