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

# Main game class for easy import
from .game import PongGame
from .core import config, Colors

# Legacy compatibility - expose key classes from original game.py
from .game import Paddle, Ball, GameState

# Export configuration constants for backward compatibility
WINDOW_WIDTH = config.window.width
WINDOW_HEIGHT = config.window.height
GAME_AREA_WIDTH = config.game_area.width
GAME_AREA_HEIGHT = config.game_area.height
GAME_AREA_X = config.game_area.x
GAME_AREA_Y = config.game_area.y
PADDLE_WIDTH = config.paddle.width
PADDLE_HEIGHT = config.paddle.height
PADDLE_SPEED = config.paddle.speed
BALL_SIZE = config.ball.size
INITIAL_BALL_SPEED = config.ball.initial_speed
SPEED_INCREMENT = config.ball.speed_increment
MAX_LOSSES = config.rules.max_losses
COMPUTER_ERROR_CHANCE = config.ai.error_chance
