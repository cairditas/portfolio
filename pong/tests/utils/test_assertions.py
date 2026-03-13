"""
Custom Test Assertions

Domain-specific assertion methods for clearer test intent and better error messages.
These assertions provide semantic meaning to test validations and make debugging easier.
"""

import math
import sys
import os
from typing import Tuple, Optional

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from pong.core.config import config
from tests.fixtures.test_config import TestTolerances

# Get constants for test convenience
GAME_AREA_X = config.game_area.x
GAME_AREA_Y = config.game_area.y
GAME_AREA_WIDTH = config.game_area.width
GAME_AREA_HEIGHT = config.game_area.height
BALL_SIZE = config.ball.size


class GameAssertions:
    """Custom assertions for game-specific test validations."""
    
    @staticmethod
    def assert_ball_at_boundary(ball, boundary_type: str, tolerance: int = TestTolerances.BOUNDARY_MARGIN):
        """
        Assert ball is at specified boundary within tolerance.
        
        Args:
            ball: Ball object to check
            boundary_type: Type of boundary ('top', 'bottom', 'left', 'right')
            tolerance: Allowed deviation from exact boundary
        """
        if boundary_type == 'top':
            actual_position = ball.rect.top
            expected_position = GAME_AREA_Y
            message = f"Expected ball top to be at {expected_position} ± {tolerance}, got {actual_position}"
            assert abs(actual_position - expected_position) <= tolerance, message
            
        elif boundary_type == 'bottom':
            actual_position = ball.rect.bottom
            expected_position = GAME_AREA_Y + GAME_AREA_HEIGHT
            message = f"Expected ball bottom to be at {expected_position} ± {tolerance}, got {actual_position}"
            assert abs(actual_position - expected_position) <= tolerance, message
            
        elif boundary_type == 'left':
            actual_position = ball.rect.left
            expected_position = GAME_AREA_X
            message = f"Expected ball left to be at {expected_position} ± {tolerance}, got {actual_position}"
            assert abs(actual_position - expected_position) <= tolerance, message
            
        elif boundary_type == 'right':
            actual_position = ball.rect.right
            expected_position = GAME_AREA_X + GAME_AREA_WIDTH
            message = f"Expected ball right to be at {expected_position} ± {tolerance}, got {actual_position}"
            assert abs(actual_position - expected_position) <= tolerance, message
            
        else:
            raise ValueError(f"Unknown boundary type: {boundary_type}")
    
    @staticmethod
    def assert_ball_velocity_direction(ball, expected_direction: str, tolerance: float = TestTolerances.VELOCITY_TOLERANCE):
        """
        Assert ball velocity is in expected direction.
        
        Args:
            ball: Ball object to check
            expected_direction: Expected direction ('up', 'down', 'left', 'right')
            tolerance: Allowed deviation from exact direction
        """
        vx, vy = ball.velocity_x, ball.velocity_y
        
        if expected_direction == 'up':
            message = f"Expected ball velocity to be upward (vy < 0), got vy={vy}"
            assert vy < 0, message
            
        elif expected_direction == 'down':
            message = f"Expected ball velocity to be downward (vy > 0), got vy={vy}"
            assert vy > 0, message
            
        elif expected_direction == 'left':
            message = f"Expected ball velocity to be leftward (vx < 0), got vx={vx}"
            assert vx < 0, message
            
        elif expected_direction == 'right':
            message = f"Expected ball velocity to be rightward (vx > 0), got vx={vx}"
            assert vx > 0, message
            
        else:
            raise ValueError(f"Unknown direction: {expected_direction}")
    
    @staticmethod
    def assert_paddle_in_bounds(paddle, margin: int = 0):
        """
        Assert paddle is within game area boundaries.
        
        Args:
            paddle: Paddle object to check
            margin: Allowed margin outside boundaries
        """
        top_boundary = GAME_AREA_Y - margin
        bottom_boundary = GAME_AREA_Y + GAME_AREA_HEIGHT + margin
        
        message_top = f"Paddle top {paddle.rect.top} should be >= {top_boundary}"
        assert paddle.rect.top >= top_boundary, message_top
        
        message_bottom = f"Paddle bottom {paddle.rect.bottom} should be <= {bottom_boundary}"
        assert paddle.rect.bottom <= bottom_boundary, message_bottom
    
    @staticmethod
    def assert_paddle_movement_direction(paddle, expected_direction: str, initial_y: Optional[int] = None):
        """
        Assert paddle moved in expected direction.
        
        Args:
            paddle: Paddle object to check
            expected_direction: Expected movement direction ('up', 'down')
            initial_y: Initial Y position for comparison (optional)
        """
        if initial_y is None:
            raise ValueError("initial_y must be provided for movement comparison")
        
        current_y = paddle.rect.y
        movement = current_y - initial_y
        
        if expected_direction == 'up':
            message = f"Expected paddle to move up (negative movement), got movement={movement}"
            assert movement < 0, message
            
        elif expected_direction == 'down':
            message = f"Expected paddle to move down (positive movement), got movement={movement}"
            assert movement > 0, message
            
        else:
            raise ValueError(f"Unknown direction: {expected_direction}")
    
    @staticmethod
    def assert_ball_angle_valid(ball, min_angle: float = 30, max_angle: float = 60):
        """
        Assert ball angle is within valid range (not purely vertical).
        
        Args:
            ball: Ball object to check
            min_angle: Minimum allowed angle in degrees
            max_angle: Maximum allowed angle in degrees
        """
        # Calculate angle from velocity components
        speed = math.sqrt(ball.velocity_x**2 + ball.velocity_y**2)
        if speed == 0:
            raise ValueError("Ball has zero velocity")
        
        # Calculate angle (0 = right, 90 = up)
        angle = math.degrees(math.atan2(abs(ball.velocity_y), abs(ball.velocity_x)))
        
        message = f"Ball angle {angle}° should be between {min_angle}° and {max_angle}°"
        assert min_angle <= angle <= max_angle, message
    
    @staticmethod
    def assert_game_state(game, expected_state: dict):
        """
        Assert game matches expected state.
        
        Args:
            game: Game object to check
            expected_state: Dictionary of expected values
        """
        for attribute, expected_value in expected_state.items():
            actual_value = getattr(game, attribute)
            message = f"Game.{attribute} should be {expected_value}, got {actual_value}"
            assert actual_value == expected_value, message
    
    @staticmethod
    def assert_score_progression(game, expected_player_score: int, expected_computer_score: int, 
                             expected_losses: int, expected_level: int):
        """
        Assert game scores match expected values.
        
        Args:
            game: Game object to check
            expected_player_score: Expected player score
            expected_computer_score: Expected computer score
            expected_losses: Expected losses
            expected_level: Expected level
        """
        errors = []
        
        if game.game_state.player_score != expected_player_score:
            errors.append(f"Player score: expected {expected_player_score}, got {game.game_state.player_score}")
        
        if game.game_state.computer_score != expected_computer_score:
            errors.append(f"Computer score: expected {expected_computer_score}, got {game.game_state.computer_score}")
        
        if game.game_state.losses != expected_losses:
            errors.append(f"Losses: expected {expected_losses}, got {game.game_state.losses}")
        
        if game.game_state.level != expected_level:
            errors.append(f"Level: expected {expected_level}, got {game.game_state.level}")
        
        if errors:
            raise AssertionError("Score assertion failed: " + "; ".join(errors))
    
    @staticmethod
    def assert_performance_benchmark(actual_time: float, benchmark_time: float, 
                                  threshold: float = TestTolerances.PERFORMANCE_DEGRADATION_THRESHOLD):
        """
        Assert performance meets benchmark requirements.
        
        Args:
            actual_time: Measured execution time
            benchmark_time: Expected benchmark time
            threshold: Maximum allowed degradation factor
        """
        max_allowed_time = benchmark_time * threshold
        message = f"Performance {actual_time:.3f}s exceeds benchmark {benchmark_time:.3f}s (max allowed: {max_allowed_time:.3f}s)"
        assert actual_time <= max_allowed_time, message
    
    @staticmethod
    def assert_memory_stability(initial_objects: int, final_objects: int, 
                             max_growth: int = TestTolerances.MAX_MEMORY_GROWTH):
        """
        Assert memory usage remained stable.
        
        Args:
            initial_objects: Initial object count
            final_objects: Final object count
            max_growth: Maximum allowed object growth
        """
        growth = final_objects - initial_objects
        message = f"Memory grew by {growth} objects, max allowed: {max_growth}"
        assert growth <= max_growth, message
    
    @staticmethod
    def assert_collision_occurred(obj1_rect, obj2_rect, should_collide: bool):
        """
        Assert collision state between two objects.
        
        Args:
            obj1_rect: First object's rectangle
            obj2_rect: Second object's rectangle
            should_collide: Whether collision should occur
        """
        collision = obj1_rect.colliderect(obj2_rect)
        
        if should_collide:
            message = f"Expected collision between {obj1_rect} and {obj2_rect}"
            assert collision, message
        else:
            message = f"Expected no collision between {obj1_rect} and {obj2_rect}"
            assert not collision, message
    
    @staticmethod
    def assert_color_valid(color: Tuple[int, int, int], color_name: str = "Color"):
        """
        Assert color is a valid RGB tuple.
        
        Args:
            color: Color tuple to validate
            color_name: Name of color for error message
        """
        assert isinstance(color, tuple), f"{color_name} should be a tuple"
        assert len(color) == 3, f"{color_name} should have 3 components (RGB)"
        
        for i, component in enumerate(color):
            assert isinstance(component, int), f"{color_name}[{i}] should be an integer"
            assert 0 <= component <= 255, f"{color_name}[{i}] should be between 0 and 255, got {component}"


class PerformanceAssertions:
    """Assertions specifically for performance testing."""
    
    @staticmethod
    def assert_within_time_limit(actual_time: float, time_limit: float, operation_name: str):
        """
        Assert operation completed within time limit.
        
        Args:
            actual_time: Measured execution time
            time_limit: Maximum allowed time
            operation_name: Description of operation for error message
        """
        message = f"{operation_name} took {actual_time:.3f}s, limit is {time_limit:.3f}s"
        assert actual_time <= time_limit, message
    
    @staticmethod
    def assert_fps_achieved(frame_time: float, target_fps: int, operation_name: str):
        """
        Assert target FPS was achieved.
        
        Args:
            frame_time: Time per frame in seconds
            target_fps: Target frames per second
            operation_name: Description of operation
        """
        actual_fps = 1.0 / frame_time if frame_time > 0 else float('inf')
        message = f"{operation_name}: {actual_fps:.1f} FPS, target {target_fps} FPS"
        assert actual_fps >= target_fps * 0.9, message  # Allow 10% tolerance


class IntegrationAssertions:
    """Assertions for integration testing scenarios."""
    
    @staticmethod
    def assert_complete_game_scenario(game, player_scores: int, computer_scores: int):
        """
        Assert complete game scenario results.
        
        Args:
            game: Game object after scenario
            player_scores: Number of times player should score
            computer_scores: Number of times computer should score
        """
        expected_player_score = player_scores
        expected_computer_score = computer_scores
        expected_losses = computer_scores
        expected_level_increase = player_scores
        
        GameAssertions.assert_score_progression(
            game, expected_player_score, expected_computer_score, 
            expected_losses, expected_level_increase + 1  # Starting from level 1
        )
    
    @staticmethod
    def assert_boundary_collision_scenario(ball, boundary_type: str, initial_velocity: Tuple[int, int]):
        """
        Assert boundary collision scenario results.
        
        Args:
            ball: Ball object after collision
            boundary_type: Type of boundary that should have been hit
            initial_velocity: Initial velocity before collision
        """
        # Check ball is at boundary
        GameAssertions.assert_ball_at_boundary(ball, boundary_type)
        
        # Check velocity was reversed in appropriate direction
        if boundary_type in ['top', 'bottom']:
            # Vertical velocity should be reversed
            expected_vy = -initial_velocity[1]
            message = f"Expected vertical velocity {expected_vy}, got {ball.velocity_y}"
            assert abs(ball.velocity_y - expected_vy) <= TestTolerances.VELOCITY_TOLERANCE, message
