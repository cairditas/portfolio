"""
Vector mathematics module

Provides vector operations for physics calculations.
"""

import math
from typing import Tuple


class Vector2D:
    """Simple 2D vector class for physics calculations."""
    
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
    
    @property
    def magnitude(self) -> float:
        """Get the magnitude (length) of the vector."""
        return math.sqrt(self.x ** 2 + self.y ** 2)
    
    def normalize(self) -> 'Vector2D':
        """Return a normalized copy of this vector."""
        mag = self.magnitude
        if mag > 0:
            return Vector2D(self.x / mag, self.y / mag)
        return Vector2D(0, 0)
    
    def __mul__(self, scalar: float) -> 'Vector2D':
        """Multiply vector by scalar."""
        return Vector2D(self.x * scalar, self.y * scalar)
    
    def __add__(self, other: 'Vector2D') -> 'Vector2D':
        """Add two vectors."""
        return Vector2D(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other: 'Vector2D') -> 'Vector2D':
        """Subtract two vectors."""
        return Vector2D(self.x - other.x, self.y - other.y)
    
    def __repr__(self) -> str:
        return f"Vector2D({self.x}, {self.y})"


def calculate_velocity_from_angle(speed: float, angle_degrees: float) -> Tuple[float, float]:
    """
    Calculate velocity components from speed and angle.
    
    Args:
        speed: Ball speed in pixels per frame
        angle_degrees: Angle in degrees (0 = right, 90 = up)
    
    Returns:
        Tuple of (velocity_x, velocity_y)
    """
    angle_radians = math.radians(angle_degrees)
    velocity_x = speed * math.cos(angle_radians)
    velocity_y = speed * math.sin(angle_radians)
    return velocity_x, velocity_y


def calculate_speed_from_velocity(velocity_x: float, velocity_y: float) -> float:
    """Calculate speed magnitude from velocity components."""
    return math.sqrt(velocity_x ** 2 + velocity_y ** 2)


def adjust_speed_to_target(current_velocity_x: float, current_velocity_y: float, 
                          target_speed: float) -> Tuple[float, float]:
    """
    Adjust velocity to match target speed while preserving direction.
    
    Args:
        current_velocity_x: Current X velocity
        current_velocity_y: Current Y velocity
        target_speed: Desired speed
    
    Returns:
        Adjusted velocity components
    """
    current_speed = calculate_speed_from_velocity(current_velocity_x, current_velocity_y)
    if current_speed > 0:
        speed_ratio = target_speed / current_speed
        return current_velocity_x * speed_ratio, current_velocity_y * speed_ratio
    return current_velocity_x, current_velocity_y
