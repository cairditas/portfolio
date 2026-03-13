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
    
    def test_ai_miss_rate(self):
        """Test AI miss rate is approximately 2%."""
        from pong.ai import BasicAIStrategy
        from pong.core.config import config
        
        ai_strategy = BasicAIStrategy()
        
        # Test many iterations to get accurate miss rate
        total_tests = 1000
        mistakes = 0
        
        for i in range(total_tests):
            movement_amount, made_mistake = ai_strategy.calculate_move(200, 0, 250)
            if made_mistake:
                mistakes += 1
        
        miss_rate = (mistakes / total_tests) * 100
        
        # Check if miss rate is close to 2% (allowing some variance)
        self.assertAlmostEqual(miss_rate, config.ai.error_chance * 100, delta=2.0,
                              msg=f"AI miss rate ({miss_rate:.1f}%) should be close to {config.ai.error_chance * 100}%")
        
        # Also check that AI doesn't miss too much (should be less than 5%)
        self.assertLess(miss_rate, 5.0, "AI miss rate should be less than 5%")
        
        # And doesn't miss too little (should be more than 0.5%)
        self.assertGreater(miss_rate, 0.5, "AI miss rate should be more than 0.5%")

    def test_paddle_ai_movement(self):
        """Test AI paddle movement with different scenarios."""
        from pong.ai import BasicAIStrategy
        ai_strategy = BasicAIStrategy()
        
        # Test only non-mistake scenarios since mistakes are random
        normal_scenarios = [s for s in TestDataRanges.AI_TEST_SCENARIUM if not s['make_mistake']]
        
        for scenario in normal_scenarios:
            with self.subTest(scenario=scenario):
                initial_y = self.paddle.rect.centery
                
                # Use the new AI system
                movement_amount, made_mistake = ai_strategy.calculate_move(
                    scenario['ball_y'], 
                    scenario['ball_velocity_y'], 
                    self.paddle.rect.centery
                )
                
                # Apply movement
                if movement_amount > 0:
                    self.paddle.move_down_by_amount(movement_amount)
                elif movement_amount < 0:
                    self.paddle.move_up_by_amount(abs(movement_amount))
                
                # Check that paddle moved
                final_y = self.paddle.rect.centery
                self.assertNotEqual(final_y, initial_y, "Paddle should have moved")
                
                # Check movement direction (only for non-mistake scenarios)
                if scenario['expected_direction'] == 'up':
                    self.assertLess(final_y, initial_y, "Should move up")
                elif scenario['expected_direction'] == 'down':
                    self.assertGreater(final_y, initial_y, "Should move down")


if __name__ == '__main__':
    unittest.main()
