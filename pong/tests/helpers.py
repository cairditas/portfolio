"""
Test helper functions and utilities

Provides utility functions for tests to reduce code duplication
and improve readability.
"""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from pong.game import (
    WINDOW_WIDTH, WINDOW_HEIGHT, GAME_AREA_WIDTH, GAME_AREA_HEIGHT,
    GAME_AREA_X, GAME_AREA_Y, PADDLE_WIDTH, PADDLE_HEIGHT, PADDLE_SPEED,
    BALL_SIZE, INITIAL_BALL_SPEED, SPEED_INCREMENT, MAX_LOSSES,
    COMPUTER_ERROR_CHANCE, Colors
)


def get_all_game_constants():
    """
    Get all game constants organized by category.
    
    Returns:
        Dictionary containing all game constants organized by category
    """
    return {
        'window': {
            'width': WINDOW_WIDTH,
            'height': WINDOW_HEIGHT
        },
        'game_area': {
            'x': GAME_AREA_X,
            'y': GAME_AREA_Y,
            'width': GAME_AREA_WIDTH,
            'height': GAME_AREA_HEIGHT
        },
        'paddle': {
            'width': PADDLE_WIDTH,
            'height': PADDLE_HEIGHT,
            'speed': PADDLE_SPEED
        },
        'ball': {
            'size': BALL_SIZE,
            'initial_speed': INITIAL_BALL_SPEED,
            'speed_increment': SPEED_INCREMENT
        },
        'rules': {
            'max_losses': MAX_LOSSES
        },
        'ai': {
            'error_chance': COMPUTER_ERROR_CHANCE
        },
        'colors': {
            'black': Colors.BLACK,
            'white': Colors.WHITE,
            'green': Colors.GREEN,
            'red': Colors.RED,
            'blue': Colors.BLUE,
            'gray': Colors.GRAY
        }
    }


def validate_constant_value(value, name, expected_type, min_value=None, max_value=None):
    """
    Validate a constant value against expected criteria.
    
    Args:
        value: The constant value to validate
        name: Name of the constant for error messages
        expected_type: Expected type of the constant
        min_value: Optional minimum value
        max_value: Optional maximum value
    
    Raises:
        AssertionError: If validation fails
    """
    assert isinstance(value, expected_type), f"{name} should be {expected_type.__name__}, got {type(value).__name__}"
    
    if min_value is not None:
        assert value >= min_value, f"{name} should be >= {min_value}, got {value}"
    
    if max_value is not None:
        assert value <= max_value, f"{name} should be <= {max_value}, got {value}"


def validate_rgb_color(color, name):
    """
    Validate that a color is a proper RGB tuple.
    
    Args:
        color: The color to validate
        name: Name of the color for error messages
    
    Raises:
        AssertionError: If validation fails
    """
    assert isinstance(color, tuple), f"{name} should be a tuple, got {type(color).__name__}"
    assert len(color) == 3, f"{name} should have 3 components, got {len(color)}"
    
    for i, component in enumerate(color):
        assert isinstance(component, int), f"{name}[{i}] should be int, got {type(component).__name__}"
        assert 0 <= component <= 255, f"{name}[{i}] should be 0-255, got {component}"


def validate_color_constants(constants):
    """
    Validate all color constants.
    
    Args:
        constants: Dictionary containing color constants
    """
    color_names = ['black', 'white', 'green', 'red', 'blue', 'gray']
    
    for color_name in color_names:
        assert color_name in constants['colors'], f"Missing color: {color_name}"
        validate_rgb_color(constants['colors'][color_name], color_name)


def validate_game_area_constants(constants):
    """
    Validate game area constants for logical consistency.
    
    Args:
        constants: Dictionary containing game area constants
    """
    game_area = constants['game_area']
    window = constants['window']
    
    # Game area should be within window bounds
    assert game_area['x'] >= 0, "Game area X should be non-negative"
    assert game_area['y'] >= 0, "Game area Y should be non-negative"
    assert game_area['x'] + game_area['width'] <= window['width'], "Game area should fit within window width"
    assert game_area['y'] + game_area['height'] <= window['height'], "Game area should fit within window height"
    
    # Game area should have reasonable dimensions
    assert game_area['width'] > 100, "Game area width should be reasonable"
    assert game_area['height'] > 100, "Game area height should be reasonable"


def validate_paddle_constants(constants):
    """
    Validate paddle constants for logical consistency.
    
    Args:
        constants: Dictionary containing paddle constants
    """
    paddle = constants['paddle']
    game_area = constants['game_area']
    
    # Paddle should be smaller than game area
    assert paddle['width'] < game_area['width'], "Paddle width should be less than game area width"
    assert paddle['height'] < game_area['height'], "Paddle height should be less than game area height"
    
    # Paddle speed should be reasonable
    assert paddle['speed'] > 0, "Paddle speed should be positive"
    assert paddle['speed'] <= 20, "Paddle speed should be reasonable (<= 20)"


def validate_ball_constants(constants):
    """
    Validate ball constants for logical consistency.
    
    Args:
        constants: Dictionary containing ball constants
    """
    ball = constants['ball']
    paddle = constants['paddle']
    game_area = constants['game_area']
    
    # Ball should be smaller than paddles
    assert ball['size'] <= paddle['width'], "Ball size should be <= paddle width"
    assert ball['size'] <= paddle['height'], "Ball size should be <= paddle height"
    
    # Ball speed should be reasonable
    assert ball['initial_speed'] > 0, "Ball initial speed should be positive"
    assert ball['speed_increment'] > 0, "Ball speed increment should be positive"
    
    # Ball should fit comfortably in game area
    assert ball['size'] * 10 < game_area['width'], "Ball should be reasonably sized for game area"


def validate_rule_constants(constants):
    """
    Validate game rule constants.
    
    Args:
        constants: Dictionary containing rule constants
    """
    rules = constants['rules']
    
    # Max losses should be reasonable
    assert rules['max_losses'] > 0, "Max losses should be positive"
    assert rules['max_losses'] <= 20, "Max losses should be reasonable (<= 20)"


def validate_ai_constants(constants):
    """
    Validate AI constants for logical consistency.
    
    Args:
        constants: Dictionary containing AI constants
    """
    ai = constants['ai']
    
    # Error chance should be between 0 and 1
    assert 0 <= ai['error_chance'] <= 1, "AI error chance should be between 0 and 1"
