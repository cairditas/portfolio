"""
Unit tests for Ball class

Tests individual ball functionality in isolation.
"""

import unittest
import math

from pong.game import Ball
from tests.helpers import get_all_game_constants
from tests.fixtures.test_config import TestDataRanges, TestTolerances
from tests.utils.test_assertions import GameAssertions
from tests.fixtures.test_builders import TestDataFactory, BallBuilder


class TestBall(unittest.TestCase):
    """Test ball functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.ball = TestDataFactory.create_ball()
        self.constants = get_all_game_constants()
    
    def test_ball_creation_and_properties(self):
        """Test ball creation and initial properties."""
        self.assertIsInstance(self.ball, Ball)
        self.assertEqual(self.ball.rect.width, self.constants['ball']['size'])
        self.assertEqual(self.ball.rect.height, self.constants['ball']['size'])
        self.assertEqual(self.ball.base_speed, self.constants['ball']['initial_speed'])
        self.assertIsInstance(self.ball.velocity_x, int)
        self.assertIsInstance(self.ball.velocity_y, int)
    
    def test_ball_reset_consistency(self):
        """Test ball reset produces consistent state."""
        reset_results = []
        initial_speed = self.constants['ball']['initial_speed']
        
        for _ in range(10):
            self.ball.reset()
            result = {
                'x': self.ball.rect.x,
                'y': self.ball.rect.y,
                'velocity_x': self.ball.velocity_x,
                'velocity_y': self.ball.velocity_y,
                'speed': math.sqrt(self.ball.velocity_x**2 + self.ball.velocity_y**2)
            }
            reset_results.append(result)
        
        # All resets should have same position
        x_positions = [r['x'] for r in reset_results]
        y_positions = [r['y'] for r in reset_results]
        
        self.assertTrue(all(x == x_positions[0] for x in x_positions))
        self.assertTrue(all(y == y_positions[0] for y in y_positions))
        
        # Speed should be consistent
        speeds = [r['speed'] for r in reset_results]
        self.assertTrue(all(abs(s - initial_speed) < 0.1 for s in speeds))
    
    def test_ball_speed_progression(self):
        """Test ball speed increases correctly."""
        initial_speed = self.ball.base_speed
        speed_increment = self.constants['ball']['speed_increment']
        
        self.ball.increase_speed()
        self.assertEqual(self.ball.base_speed, initial_speed + speed_increment)
        
        self.ball.increase_speed()
        self.assertEqual(self.ball.base_speed, initial_speed + 2 * speed_increment)
    
    def test_ball_angle_constraints(self):
        """Test ball always moves at valid angles."""
        angle_tests = []
        
        for _ in range(20):
            self.ball.reset()
            GameAssertions.assert_ball_angle_valid(self.ball)
            angle = math.degrees(math.atan2(abs(self.ball.velocity_y), abs(self.ball.velocity_x)))
            angle_tests.append(angle)
        
        # All angles should be within valid range
        for angle in angle_tests:
            self.assertGreaterEqual(angle, 30)
            self.assertLessEqual(angle, 60)
    
    def test_ball_wall_collisions(self):
        """Test ball collisions with top and bottom walls."""
        boundary_tests = [
            ('top', TestDataRanges.BOUNDARY_POSITIONS['top_near'], -5, 5),
            ('bottom', TestDataRanges.BOUNDARY_POSITIONS['bottom_near'], 5, -5),
        ]
        
        for boundary_type, position, initial_vy, expected_vy in boundary_tests:
            with self.subTest(boundary=boundary_type):
                ball = (BallBuilder()
                        .with_position(*position)
                        .with_velocity(5, initial_vy)
                        .build())
                
                ball.move()
                
                GameAssertions.assert_ball_at_boundary(ball, boundary_type)
                GameAssertions.assert_ball_velocity_direction(ball, 'down' if boundary_type == 'top' else 'up')
    
    def test_ball_horizontal_freedom(self):
        """Test ball can move horizontally without boundaries."""
        game_area = self.constants['game_area']
        
        horizontal_tests = [
            game_area['x'] - 100,  # Far left
            game_area['x'] + game_area['width'] + 100,  # Far right
        ]
        
        for test_x in horizontal_tests:
            with self.subTest(position=test_x):
                self.ball.rect.x = test_x
                self.ball.velocity_x = 0
                initial_x = self.ball.rect.x
                self.ball.move()
                self.assertEqual(self.ball.rect.x, initial_x)


if __name__ == '__main__':
    unittest.main()
