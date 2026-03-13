"""
Pong Game - A classic Pong implementation using Pygame

Refactored architecture with clean separation of concerns:
- core/: Centralized configuration management
- physics/: Physics calculations and movement logic  
- ai/: AI opponent logic and strategies
- game/: Game objects and main orchestration
- ui/: User interface rendering and input handling
"""

__version__ = "2.1.0"
__author__ = "Pong Game Developer"

# Main imports
from .game import PongGame, Paddle, Ball, GameState
from .core import config, Colors

__all__ = ['PongGame', 'Paddle', 'Ball', 'GameState', 'config', 'Colors']
