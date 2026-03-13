"""
Ball physics module

Handles ball-specific physics calculations.
"""

import random
from typing import Tuple
from pong.core.config import config
from .vectors import calculate_velocity_from_angle


class BallPhysics:
    """Handles ball physics calculations."""
    
    @staticmethod
    def calculate_velocity(speed: float, angle_degrees: float) -> Tuple[float, float]:
        """
        Calculate velocity components from speed and angle.
        
        Args:
            speed: Ball speed in pixels per frame
            angle_degrees: Angle in degrees (0 = right, 90 = up)
        
        Returns:
            Tuple of (velocity_x, velocity_y)
        """
        return calculate_velocity_from_angle(speed, angle_degrees)
    
    @staticmethod
    def generate_random_angle() -> float:
        """
        Generate a random angle that ensures the ball moves at an angle (never purely vertical).
        
        Returns:
            Random angle in degrees between the allowed ranges
        """
        angle_ranges = config.ball.angle_ranges
        chosen_range = random.choice(angle_ranges)
        return random.uniform(chosen_range[0], chosen_range[1])
    
    @staticmethod
    def add_spin(ball_velocity_y: float, spin_amount: float = 2.0) -> float:
        """
        Add spin to ball velocity.
        
        Args:
            ball_velocity_y: Current Y velocity
            spin_amount: Amount of spin to add
        
        Returns:
            New Y velocity with spin
        """
        return ball_velocity_y + random.uniform(-spin_amount, spin_amount)
