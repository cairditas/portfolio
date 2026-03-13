"""
Movement control module

Handles movement with boundary protection.
"""

from typing import Tuple
from pong.core.config import config


class MovementController:
    """Controls movement with boundary protection."""
    
    @staticmethod
    def move_with_boundary_protection(rect, delta_x: float, delta_y: float, 
                                    game_area_config) -> Tuple[float, float]:
        """
        Move a rect by delta amounts with boundary protection.
        
        Args:
            rect: Pygame rect to move
            delta_x: X movement amount
            delta_y: Y movement amount
            game_area_config: Game area configuration
        
        Returns:
            Tuple of (actual_delta_x, actual_delta_y) after boundary constraints
        """
        actual_delta_x = delta_x
        actual_delta_y = delta_y
        
        # Check X boundaries
        new_x = rect.x + delta_x
        if new_x < game_area_config.x:
            actual_delta_x = game_area_config.x - rect.x
        elif new_x + rect.width > game_area_config.right_edge:
            actual_delta_x = game_area_config.right_edge - rect.width - rect.x
        
        # Check Y boundaries
        new_y = rect.y + delta_y
        if new_y < game_area_config.y:
            actual_delta_y = game_area_config.y - rect.y
        elif new_y + rect.height > game_area_config.bottom_edge:
            actual_delta_y = game_area_config.bottom_edge - rect.height - rect.y
        
        rect.x += actual_delta_x
        rect.y += actual_delta_y
        
        return actual_delta_x, actual_delta_y
    
    @staticmethod
    def calculate_movement_distance(current_pos: int, target_pos: int, max_speed: int) -> int:
        """
        Calculate movement distance towards target.
        
        Args:
            current_pos: Current position
            target_pos: Target position
            max_speed: Maximum movement speed
        
        Returns:
            Movement amount (positive for down/right, negative for up/left)
        """
        diff = target_pos - current_pos
        return min(max_speed, abs(diff)) * (1 if diff > 0 else -1)
    
    @staticmethod
    def is_within_threshold(current_pos: int, target_pos: int, threshold: int) -> bool:
        """
        Check if position is within threshold of target.
        
        Args:
            current_pos: Current position
            target_pos: Target position
            threshold: Threshold distance
        
        Returns:
            True if within threshold
        """
        return abs(target_pos - current_pos) <= threshold
