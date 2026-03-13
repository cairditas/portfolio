"""
Integration tests for Pong game logic

Tests game components working together.
"""

import unittest

from pong.game import PongGame
from tests.helpers import get_all_game_constants
from tests.fixtures.test_config import ScoringScenarios
from tests.utils.test_assertions import GameAssertions
from tests.fixtures.test_builders import TestDataFactory


class TestPongGame(unittest.TestCase):
    """Test Pong game functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.game = TestDataFactory.create_game()
        self.constants = get_all_game_constants()
    
    def test_game_initialization_comprehensive(self):
        """Test comprehensive game initialization."""
        self.assertIsInstance(self.game, PongGame)
        self.assertEqual(self.game.game_state.player_score, 0)
        self.assertEqual(self.game.game_state.computer_score, 0)
        self.assertEqual(self.game.game_state.losses, 0)
        self.assertEqual(self.game.game_state.level, 1)
        self.assertEqual(self.game.game_state.high_score, 0)
        self.assertFalse(self.game.game_state.game_over)
        self.assertFalse(self.game.game_state.countdown_active)
        self.assertFalse(self.game.game_state.show_continue_prompt)
    
    def test_paddle_initial_positions(self):
        """Test paddles start at correct positions."""
        game_area = self.constants['game_area']
        colors = self.constants['colors']
        
        paddle_tests = [
            ('player_paddle', game_area['x'] + 20, colors['blue']),
            ('computer_paddle', game_area['x'] + game_area['width'] - 30, colors['red']),
        ]
        
        for paddle_name, expected_x, expected_color in paddle_tests:
            with self.subTest(paddle=paddle_name):
                paddle = self.game.game_objects[paddle_name]
                self.assertEqual(paddle.rect.x, expected_x)
                self.assertEqual(paddle.color, expected_color)
                # Should be vertically centered
                expected_y = game_area['y'] + game_area['height'] // 2 - paddle.rect.height // 2
                self.assertEqual(paddle.rect.y, expected_y)
    
    def test_scoring_scenarios(self):
        """Test different scoring scenarios."""
        # Test player scoring
        for ball_pos, expected_p_score, expected_c_score, expected_losses in ScoringScenarios.PLAYER_SCORES:
            with self.subTest(position=ball_pos):
                game = TestDataFactory.create_game()
                
                game.game_objects['ball'].rect.x, game.game_objects['ball'].rect.y = ball_pos
                result = game.handle_scoring()
                
                self.assertTrue(result)
                GameAssertions.assert_score_progression(game, expected_p_score, expected_c_score, expected_losses, expected_p_score + 1)
        
        # Test computer scoring
        for ball_pos, expected_p_score, expected_c_score, expected_losses in ScoringScenarios.COMPUTER_SCORES:
            with self.subTest(position=ball_pos):
                game = TestDataFactory.create_game()
                
                game.game_objects['ball'].rect.x, game.game_objects['ball'].rect.y = ball_pos
                result = game.handle_scoring()
                
                self.assertTrue(result)
                GameAssertions.assert_score_progression(game, expected_p_score, expected_c_score, expected_losses, 1)
    
    def test_game_over_conditions(self):
        """Test game over trigger conditions."""
        max_losses = self.constants['rules']['max_losses']
        game_area = self.constants['game_area']
        
        # Set up game over scenario
        self.game.game_state.losses = max_losses - 1
        self.game.game_objects['ball'].rect.right = game_area['x'] - 1
        
        # Trigger final loss
        self.game.handle_scoring()
        
        self.assertTrue(self.game.game_state.game_over)
        self.assertEqual(self.game.game_state.losses, max_losses)
    
    def test_high_score_tracking(self):
        """Test high score is tracked correctly."""
        # Player scores multiple times
        for i in range(3):
            game_area = self.constants['game_area']
            self.game.game_objects['ball'].rect.left = game_area['x'] + game_area['width'] + 1
            self.game.handle_scoring()
            
            expected_high_score = i + 1
            self.assertEqual(self.game.game_state.high_score, expected_high_score)
    
    def test_paddle_collision_detection(self):
        """Test paddle collision detection works."""
        # Test player paddle collision
        initial_velocity_x = self.game.game_objects['ball'].velocity_x
        
        # Position ball for collision with player paddle
        self.game.game_objects['ball'].rect.centerx = self.game.game_objects['player_paddle'].rect.centerx
        self.game.game_objects['ball'].rect.centery = self.game.game_objects['player_paddle'].rect.centery
        self.game.game_objects['ball'].velocity_x = -5  # Moving towards player paddle
        
        self.game.handle_paddle_collision()
        
        # Velocity should have reversed
        self.assertEqual(self.game.game_objects['ball'].velocity_x, 5)
        
        # Test computer paddle collision
        self.game.game_objects['ball'].rect.centerx = self.game.game_objects['computer_paddle'].rect.centerx
        self.game.game_objects['ball'].rect.centery = self.game.game_objects['computer_paddle'].rect.centery
        self.game.game_objects['ball'].velocity_x = 5  # Moving towards computer paddle
        
        self.game.handle_paddle_collision()
        
        # Velocity should have reversed again
        self.assertEqual(self.game.game_objects['ball'].velocity_x, -5)


if __name__ == '__main__':
    unittest.main()
