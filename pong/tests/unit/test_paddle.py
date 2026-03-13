"""
Unit tests for Paddle class

Tests individual paddle functionality in isolation.
"""

import unittest

from pong.game import Paddle
from tests.helpers import get_all_game_constants
from tests.fixtures.test_config import TestDataRanges, TestTolerances
from tests.utils.test_assertions import GameAssertions
from tests.fixtures.test_builders import TestDataFactory, PaddleBuilder


class TestPaddle(unittest.TestCase):
    """Test paddle functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.paddle = TestDataFactory.create_paddle()
        self.constants = get_all_game_constants()
    
    def test_paddle_creation(self):
        """Test paddle creation with default parameters."""
        self.assertIsInstance(self.paddle, Paddle)
        self.assertEqual(self.paddle.rect.x, 100)
        self.assertEqual(self.paddle.rect.y, 200)
        self.assertEqual(self.paddle.color, self.constants['colors']['blue'])
        self.assertEqual(self.paddle.y_amount, self.constants['paddle']['speed'])
    
    def test_paddle_movement(self):
        """Test paddle movement methods."""
        initial_y = self.paddle.rect.y
        paddle_speed = self.constants['paddle']['speed']
        
        # Test movement up
        self.paddle.move_up()
        self.assertEqual(self.paddle.rect.y, initial_y - paddle_speed)
        
        # Test movement down
        self.paddle.move_down()
        self.assertEqual(self.paddle.rect.y, initial_y)
    
    def test_paddle_movement_by_amount(self):
        """Test paddle movement by specific amount."""
        initial_y = self.paddle.rect.y
        
        # Move up by amount
        self.paddle.move_up_by_amount(15)
        self.assertEqual(self.paddle.rect.y, initial_y - 15)
        
        # Move down by amount
        self.paddle.move_down_by_amount(25)
        self.assertEqual(self.paddle.rect.y, initial_y + 10)
    
    def test_paddle_boundary_conditions(self):
        """Test paddle respects boundaries."""
        game_area = self.constants['game_area']
        paddle_height = self.constants['paddle']['height']
        
        boundary_tests = [
            ('at_top_boundary', game_area['y']),
            ('at_bottom_boundary', game_area['y'] + game_area['height'] - paddle_height),
        ]
        
        for builder_method, expected_y in boundary_tests:
            with self.subTest(method=builder_method):
                paddle = getattr(PaddleBuilder(), builder_method)().build()
                self.assertEqual(paddle.rect.y, expected_y)
                
                # Test movement doesn't go past boundary
                initial_y = paddle.rect.y
                if 'top' in builder_method:
                    paddle.move_up()
                    GameAssertions.assert_paddle_in_bounds(paddle)
                else:
                    paddle.move_down()
                    GameAssertions.assert_paddle_in_bounds(paddle)
    
    def test_paddle_movement_by_amount_edge_cases(self):
        """Test paddle movement by amount with edge cases."""
        game_area = self.constants['game_area']
        paddle_height = self.constants['paddle']['height']
        
        edge_cases = [
            (50, game_area['y'] + 5, 'clamp_to_boundary'),
            (50, game_area['y'] + game_area['height'] - paddle_height - 5, 'clamp_to_boundary'),
            (10, game_area['y'] + 50, 'normal_movement'),
        ]
        
        for amount, initial_pos, behavior in edge_cases:
            with self.subTest(amount=amount, behavior=behavior):
                self.paddle.rect.y = initial_pos
                initial_y = self.paddle.rect.y
                
                if amount > 0:
                    self.paddle.move_down_by_amount(amount)
                else:
                    self.paddle.move_up_by_amount(abs(amount))
                
                if behavior == 'clamp_to_boundary':
                    GameAssertions.assert_paddle_in_bounds(self.paddle)
                else:
                    self.assertNotEqual(self.paddle.rect.y, initial_y)
    
    def test_paddle_ai_movement(self):
        """Test AI paddle movement with different scenarios."""
        ai_tests = TestDataRanges.AI_TEST_SCENARIUM
        
        for scenario in ai_tests:
            with self.subTest(scenario=scenario):
                initial_y = self.paddle.rect.centery
                self.paddle.ai_move(scenario['ball_y'], scenario['ball_velocity_y'], scenario['make_mistake'])
                
                # Check that paddle moved
                final_y = self.paddle.rect.centery
                self.assertNotEqual(final_y, initial_y, "Paddle should have moved")
                
                # For mistake scenarios, check it moved away from ball
                if scenario['make_mistake']:
                    if scenario['ball_y'] > initial_y:
                        self.assertLess(final_y, initial_y, "Mistake should move away from ball")
                    else:
                        self.assertGreater(final_y, initial_y, "Mistake should move away from ball")


if __name__ == '__main__':
    unittest.main()
