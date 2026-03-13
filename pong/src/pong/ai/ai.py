"""
AI Module

Handles AI opponent logic and decision making.
Separates AI concerns from game objects.
"""

from typing import Tuple
from pong.core.config import config


class AIController:
    """Controls AI paddle movement and decision making."""
    
    def __init__(self, ai_config=None):
        """Initialize AI controller with configuration."""
        self.config = ai_config or config.ai
    
    def calculate_target_position(self, ball_y: int, ball_velocity_y: float, 
                                paddle_center_y: int, make_mistake: bool = False) -> int:
        """
        Calculate the target Y position for the AI paddle.
        
        Args:
            ball_y: Current Y position of the ball
            ball_velocity_y: Current Y velocity of the ball
            paddle_center_y: Current Y position of the paddle center
            make_mistake: If True, AI will intentionally move away from ball
        
        Returns:
            Target Y position for the paddle
        """
        if make_mistake:
            # Intentionally move away from the ball
            mistake_direction = 1 if ball_y < paddle_center_y else -1
            return ball_y + (self.config.mistake_distance * mistake_direction)
        else:
            # Track ball with prediction based on velocity
            prediction = ball_velocity_y * self.config.prediction_factor
            return ball_y + prediction
    
    def should_move(self, current_y: int, target_y: int) -> bool:
        """
        Determine if AI should move based on threshold.
        
        Args:
            current_y: Current Y position
            target_y: Target Y position
        
        Returns:
            True if movement should occur
        """
        return abs(target_y - current_y) > self.config.movement_threshold
    
    def calculate_movement_amount(self, current_y: int, target_y: int, speed: int) -> int:
        """
        Calculate how much the paddle should move.
        
        Args:
            current_y: Current Y position
            target_y: Target Y position
            speed: Maximum movement speed
        
        Returns:
            Movement amount (positive for down, negative for up)
        """
        diff = target_y - current_y
        return min(speed, abs(diff)) * (1 if diff > 0 else -1)
    
    def should_make_mistake(self) -> bool:
        """
        Determine if AI should make a mistake this frame.
        
        Returns:
            True if AI should make a mistake
        """
        import random
        return random.random() < self.config.error_chance
    
    def get_movement_direction(self, movement_amount: int) -> str:
        """
        Get movement direction from movement amount.
        
        Args:
            movement_amount: Movement amount (can be positive or negative)
        
        Returns:
            'up', 'down', or 'none'
        """
        if movement_amount > 0:
            return 'down'
        elif movement_amount < 0:
            return 'up'
        return 'none'


class AIStrategy:
    """Base class for AI strategies."""
    
    def calculate_move(self, ball_y: int, ball_velocity_y: int, paddle_center_y: int) -> Tuple[int, bool]:
        """
        Calculate AI movement.
        
        Args:
            ball_y: Current ball Y position
            ball_velocity_y: Current ball Y velocity
            paddle_center_y: Current paddle center Y position
        
        Returns:
            Tuple of (movement_amount, should_make_mistake)
        """
        raise NotImplementedError


class BasicAIStrategy(AIStrategy):
    """Basic AI strategy with simple tracking."""
    
    def __init__(self, ai_config=None):
        self.controller = AIController(ai_config)
    
    def calculate_move(self, ball_y: int, ball_velocity_y: int, paddle_center_y: int) -> Tuple[int, bool]:
        """Calculate basic AI movement."""
        make_mistake = self.controller.should_make_mistake()
        target_y = self.controller.calculate_target_position(
            ball_y, ball_velocity_y, paddle_center_y, make_mistake
        )
        
        if not self.controller.should_move(paddle_center_y, target_y):
            return 0, False
        
        movement_amount = self.controller.calculate_movement_amount(
            paddle_center_y, target_y, 7  # Default paddle speed
        )
        
        return movement_amount, make_mistake


class SmartAIStrategy(AIStrategy):
    """Advanced AI strategy with better prediction."""
    
    def __init__(self, ai_config=None):
        self.controller = AIController(ai_config)
        self.prediction_history = []
    
    def calculate_move(self, ball_y: int, ball_velocity_y: int, paddle_center_y: int) -> Tuple[int, bool]:
        """Calculate smart AI movement with improved prediction."""
        make_mistake = self.controller.should_make_mistake()
        
        # Store prediction history for learning
        self.prediction_history.append((ball_y, ball_velocity_y))
        if len(self.prediction_history) > 10:
            self.prediction_history.pop(0)
        
        # Enhanced prediction based on history
        enhanced_velocity = self._calculate_enhanced_velocity(ball_velocity_y)
        target_y = self.controller.calculate_target_position(
            ball_y, enhanced_velocity, paddle_center_y, make_mistake
        )
        
        if not self.controller.should_move(paddle_center_y, target_y):
            return 0, False
        
        movement_amount = self.controller.calculate_movement_amount(
            paddle_center_y, target_y, 7  # Default paddle speed
        )
        
        return movement_amount, make_mistake
    
    def _calculate_enhanced_velocity(self, current_velocity: float) -> float:
        """Calculate enhanced velocity prediction based on history."""
        if len(self.prediction_history) < 3:
            return current_velocity
        
        # Simple momentum calculation based on recent history
        recent_velocities = [vel for _, vel in self.prediction_history[-3:]]
        avg_velocity = sum(recent_velocities) / len(recent_velocities)
        
        # Weight current velocity more heavily
        return (current_velocity * 0.7 + avg_velocity * 0.3)
