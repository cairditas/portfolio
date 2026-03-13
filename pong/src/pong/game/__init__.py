"""
Game module

Contains game objects and main game orchestration.
"""

from .objects import Paddle, Ball, GameState
from .pong_game import PongGame
from pong.core.config import config
from pong.core.config import Colors

# Export constants for backward compatibility
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

__all__ = [
    'Paddle', 'Ball', 'GameState', 'PongGame', 'Colors',
    'WINDOW_WIDTH', 'WINDOW_HEIGHT', 'GAME_AREA_WIDTH', 'GAME_AREA_HEIGHT',
    'GAME_AREA_X', 'GAME_AREA_Y', 'PADDLE_WIDTH', 'PADDLE_HEIGHT',
    'PADDLE_SPEED', 'BALL_SIZE', 'INITIAL_BALL_SPEED', 'SPEED_INCREMENT',
    'MAX_LOSSES', 'COMPUTER_ERROR_CHANCE'
]
