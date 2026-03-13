"""
Collision detection module

Handles boundary checking and collision response.
"""

from typing import Tuple
from pong.core.config import config


class BoundaryChecker:
    """Handles boundary collision detection and response."""
    
    @staticmethod
    def check_vertical_boundaries(rect, game_area_config) -> Tuple[bool, str]:
        """
        Check if rect has collided with vertical boundaries.
        
        Args:
            rect: Pygame rect to check
            game_area_config: Game area configuration
        
        Returns:
            Tuple of (collision_occurred, boundary_type)
        """
        if rect.top <= game_area_config.y:
            return True, 'top'
        elif rect.bottom >= game_area_config.bottom_edge:
            return True, 'bottom'
        return False, ''
    
    @staticmethod
    def handle_wall_collision(rect, velocity_y: float, game_area_config) -> float:
        """
        Handle wall collision by adjusting position and reversing velocity.
        
        Args:
            rect: Pygame rect to adjust
            velocity_y: Current Y velocity
            game_area_config: Game area configuration
        
        Returns:
            New Y velocity after collision
        """
        collision_occurred, boundary_type = BoundaryChecker.check_vertical_boundaries(rect, game_area_config)
        
        if collision_occurred:
            if boundary_type == 'top':
                rect.top = game_area_config.y
            else:  # bottom
                rect.bottom = game_area_config.bottom_edge
            return -velocity_y
        
        return velocity_y
    
    @staticmethod
    def check_paddle_collision(ball_rect, paddle_rect, velocity_x: float) -> bool:
        """
        Check if ball has collided with paddle.
        
        Args:
            ball_rect: Ball rectangle
            paddle_rect: Paddle rectangle
            velocity_x: Ball X velocity
        
        Returns:
            True if collision occurred
        """
        return (ball_rect.colliderect(paddle_rect) and 
                ((velocity_x < 0 and paddle_rect.centerx < config.game_area.width // 2) or
                 (velocity_x > 0 and paddle_rect.centerx > config.game_area.width // 2)))
    
    @staticmethod
    def check_scoring(ball_rect, game_area_config) -> Tuple[bool, str]:
        """
        Check if ball has scored (gone past paddles).
        
        Args:
            ball_rect: Ball rectangle
            game_area_config: Game area configuration
        
        Returns:
            Tuple of (scored, scorer) where scorer is 'player' or 'computer'
        """
        if ball_rect.left > game_area_config.right_edge:
            return True, 'player'
        elif ball_rect.right <= game_area_config.x:
            return True, 'computer'
        return False, ''
