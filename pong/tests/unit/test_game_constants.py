"""
Unit tests for game constants

Tests that all game constants are properly defined and have valid values.
"""

import unittest

from tests.helpers import get_all_game_constants, validate_constant_value, validate_rgb_color


class TestGameConstants(unittest.TestCase):
    """Test game constants are properly defined."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.constants = get_all_game_constants()
    
    def test_window_constants(self):
        """Test window dimension constants."""
        window = self.constants['window']
        
        validate_constant_value(window['width'], 'WINDOW_WIDTH', int, min_value=1)
        validate_constant_value(window['height'], 'WINDOW_HEIGHT', int, min_value=1)
        
        # Window should be larger than game area
        game_area = self.constants['game_area']
        self.assertGreater(window['width'], game_area['x'] + game_area['width'])
        self.assertGreater(window['height'], game_area['y'] + game_area['height'])
    
    def test_game_area_constants(self):
        """Test game area dimension constants."""
        game_area = self.constants['game_area']
        
        validate_constant_value(game_area['width'], 'GAME_AREA_WIDTH', int, min_value=1)
        validate_constant_value(game_area['height'], 'GAME_AREA_HEIGHT', int, min_value=1)
        validate_constant_value(game_area['x'], 'GAME_AREA_X', int, min_value=0)
        validate_constant_value(game_area['y'], 'GAME_AREA_Y', int, min_value=0)
    
    def test_object_constants(self):
        """Test paddle and ball dimension constants."""
        paddle = self.constants['paddle']
        ball = self.constants['ball']
        
        # Paddle constants
        validate_constant_value(paddle['width'], 'PADDLE_WIDTH', int, min_value=1)
        validate_constant_value(paddle['height'], 'PADDLE_HEIGHT', int, min_value=1)
        validate_constant_value(paddle['speed'], 'PADDLE_SPEED', int, min_value=1)
        
        # Ball constants
        validate_constant_value(ball['size'], 'BALL_SIZE', int, min_value=1)
        validate_constant_value(ball['initial_speed'], 'INITIAL_BALL_SPEED', (int, float), min_value=1)
        validate_constant_value(ball['speed_increment'], 'SPEED_INCREMENT', (int, float), min_value=0)
    
    def test_game_rule_constants(self):
        """Test game rule constants."""
        rules = self.constants['rules']
        ai = self.constants['ai']
        
        validate_constant_value(rules['max_losses'], 'MAX_LOSSES', int, min_value=1)
        validate_constant_value(ai['error_chance'], 'COMPUTER_ERROR_CHANCE', (int, float), min_value=0, max_value=1)
    
    def test_color_constants(self):
        """Test color constants are valid RGB tuples."""
        colors = self.constants['colors']
        
        for color_name, color_value in colors.items():
            validate_rgb_color(color_value, f"Colors.{color_name.upper()}")


if __name__ == '__main__':
    unittest.main()
