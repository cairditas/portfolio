"""
Physics module

Handles all physics calculations and movement logic.
"""

from .vectors import Vector2D, calculate_velocity_from_angle, calculate_speed_from_velocity, adjust_speed_to_target
from .ball_physics import BallPhysics
from .collision import BoundaryChecker
from .movement import MovementController

__all__ = [
    'Vector2D', 'calculate_velocity_from_angle', 'calculate_speed_from_velocity', 'adjust_speed_to_target',
    'BallPhysics', 'BoundaryChecker', 'MovementController'
]
