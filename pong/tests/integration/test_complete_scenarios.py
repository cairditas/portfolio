"""
Integration tests for complete game scenarios

Tests end-to-end game functionality and complex scenarios.
"""

import unittest
import sys
import os
import warnings
import time
import gc
from unittest.mock import patch

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

# Suppress pygame warnings
warnings.filterwarnings("ignore", category=DeprecationWarning, module="pkg_resources")

from pong.game import PongGame
from tests.fixtures.test_config import IntegrationScenarios
from tests.utils.test_assertions import IntegrationAssertions, PerformanceAssertions, GameAssertions
from tests.fixtures.test_builders import TestDataFactory, GameScenarioBuilder


class TestCompleteGameScenarios(unittest.TestCase):
    """Test complete game scenarios."""
    
    def setUp(self):
        """Set up integration test fixtures."""
        self.factory = TestDataFactory()
        self.game = self.factory.create_game()
    
    def test_complete_game_scenario(self):
        """Test a complete game scenario from start to finish."""
        scenario = IntegrationScenarios.COMPLETE_GAME
        
        game = (GameScenarioBuilder()
                .create_game()
                .player_scores(scenario['player_scores'])
                .computer_scores(scenario['computer_scores'])
                .execute())
        
        IntegrationAssertions.assert_complete_game_scenario(
            game, scenario['player_scores'], scenario['computer_scores']
        )
    
    def test_boundary_collision_integration(self):
        """Test boundary collisions in realistic gameplay."""
        for scenario in IntegrationScenarios.BOUNDARY_COLLISIONS:
            with self.subTest(scenario=scenario):
                game = TestDataFactory.create_game()
                
                # Set up boundary scenario
                from tests.fixtures.test_config import TestDataRanges
                position = TestDataRanges.BOUNDARY_POSITIONS[scenario['position']]
                game.ball.rect.x, game.ball.rect.y = position
                game.ball.velocity_x, game.ball.velocity_y = scenario['velocity']
                
                # Move ball to trigger collision
                game.ball.move()
                
                IntegrationAssertions.assert_boundary_collision_scenario(
                    game.ball, scenario['expected_bounce'], scenario['velocity']
                )
    
    def test_game_loop_performance(self):
        """Test game loop performance meets requirements."""
        from tests.fixtures.test_config import PerformanceBenchmarks
        
        game = TestDataFactory.create_game()
        
        # Measure game loop performance
        start_time = time.time()
        
        for _ in range(10):
            # Simulate game loop operations
            game.player_paddle.move_up()
            game.player_paddle.move_down()
            game.computer_paddle.ai_move(200, 0, False)
            game.ball.move()
            game.handle_paddle_collision()
        
        end_time = time.time()
        loop_time = end_time - start_time
        
        PerformanceAssertions.assert_within_time_limit(
            loop_time, PerformanceBenchmarks.MAX_GAME_LOOP_TIME, "Game loop performance"
        )
    
    def test_memory_usage_stability(self):
        """Test memory usage remains stable during gameplay."""
        from tests.fixtures.test_config import PerformanceBenchmarks
        
        # Measure initial memory
        gc.collect()
        initial_objects = len(gc.get_objects())
        
        # Run multiple game operations
        for _ in range(50):
            game = TestDataFactory.create_game()
            game.ball.move()
            game.handle_paddle_collision()
            del game
        
        # Measure final memory
        gc.collect()
        final_objects = len(gc.get_objects())
        
        GameAssertions.assert_memory_stability(
            initial_objects, final_objects, PerformanceBenchmarks.MAX_MEMORY_GROWTH
        )


if __name__ == '__main__':
    unittest.main()
