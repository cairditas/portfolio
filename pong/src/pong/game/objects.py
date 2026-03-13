"""
Game objects module

Contains all game objects with clean separation of concerns.
"""

import pygame
import math
from pong.core.config import config
from pong.physics import MovementController, BallPhysics, BoundaryChecker
from pong.physics.vectors import adjust_speed_to_target, calculate_speed_from_velocity
from pong.ai import AIController


class Paddle:
    """
    Represents a paddle in the game with boundary-safe movement.
    
    Separates movement logic from boundary checking and rendering.
    """
    
    # Movement constants
    X_IS_ZERO = 0
    
    def __init__(self, x: int, y: int, color: tuple, paddle_config=None):
        """
        Initialize paddle with position, color, and configuration.
        
        Args:
            x: Initial X position
            y: Initial Y position
            color: RGB color tuple
            paddle_config: Optional paddle configuration
        """
        self.config = paddle_config or config.paddle
        self.rect = pygame.Rect(x, y, self.config.width, self.config.height)
        self.color = color
        self.y_amount = self.config.y_amount
    
    def move_up(self) -> None:
        """Move paddle up with boundary protection."""
        MovementController.move_with_boundary_protection(
            self.rect, 
            self.X_IS_ZERO,
            -self.y_amount, 
            config.game_area
        )
    
    def move_down(self) -> None:
        """Move paddle down with boundary protection."""
        MovementController.move_with_boundary_protection(
            self.rect, 
            self.X_IS_ZERO,
            self.y_amount, 
            config.game_area
        )
    
    def move_up_by_amount(self, y_amount: float) -> None:
        """
        Move paddle up by a specific amount with boundary protection.
        
        Args:
            amount: Distance to move up in pixels
        """
        MovementController.move_with_boundary_protection(
            self.rect, 
            self.X_IS_ZERO,
            -y_amount, 
            config.game_area
        )
    
    def move_down_by_amount(self, y_amount: float) -> None:
        """
        Move paddle down by a specific amount with boundary protection.
        
        Args:
            y_amount: Distance to move down in pixels
        """
        MovementController.move_with_boundary_protection(
            self.rect, 
            self.X_IS_ZERO,
            y_amount, 
            config.game_area
        )
    
    def ai_move(self, ball_y: int, ball_velocity_y: float, make_mistake: bool = False) -> None:
        """
        Move paddle using AI logic.
        
        Args:
            ball_y: Current Y position of the ball
            ball_velocity_y: Current Y velocity of the ball
            make_mistake: If True, AI will intentionally move away from ball
        """
        controller = AIController()
        target_y = controller.calculate_target_position(
            ball_y, ball_velocity_y, self.rect.centery, make_mistake
        )
        
        if not MovementController.is_within_threshold(self.rect.centery, target_y, controller.config.movement_threshold):
            movement_amount = MovementController.calculate_movement_distance(
                self.rect.centery, target_y, self.y_amount
            )
            
            if movement_amount > 0:
                self.move_down_by_amount(movement_amount)
            else:
                self.move_up_by_amount(abs(movement_amount))
    
    def draw(self, screen: pygame.Surface) -> None:
        """Draw the paddle on the screen."""
        pygame.draw.rect(screen, self.color, self.rect)


class Ball:
    """
    Represents the ball with physics-based movement and collision detection.
    
    Separates physics calculations from rendering and state management.
    """
    
    def __init__(self, ball_config=None):
        """
        Initialize ball with configuration.
        
        Args:
            ball_config: Optional ball configuration
        """
        self.config = ball_config or config.ball
        self.rect = pygame.Rect(0, 0, self.config.size, self.config.size)
        self.velocity_x = 0.0
        self.velocity_y = 0.0
        self.base_speed = self.config.initial_speed
        self.reset()
    
    def reset(self) -> None:
        """Reset ball to center position with random angled velocity."""
        # Position ball at game area center
        self.rect.x = config.ball_center_x
        self.rect.y = config.ball_center_y
        
        # Generate random angle and calculate velocity
        angle = BallPhysics.generate_random_angle()
        self.velocity_x, self.velocity_y = BallPhysics.calculate_velocity(
            self.base_speed, angle
        )
    
    def move(self) -> None:
        """Update ball position and handle wall collisions."""
        # Update position
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y
        
        # Handle vertical wall collisions only (ball can go outside horizontally for scoring)
        collision_occurred, boundary_type = BoundaryChecker.check_vertical_boundaries(self.rect, config.game_area)
        if collision_occurred:
            if boundary_type == 'top':
                self.rect.top = config.game_area.y
            else:  # bottom
                self.rect.bottom = config.game_area.bottom_edge
            self.velocity_y = -self.velocity_y
    
    def increase_speed(self) -> None:
        """Increase ball speed for next level while maintaining direction."""
        self.base_speed += self.config.speed_increment
        
        # Update current velocity to match new speed while preserving direction
        self.velocity_x, self.velocity_y = adjust_speed_to_target(
            self.velocity_x, self.velocity_y, self.base_speed
        )
    
    def draw(self, screen: pygame.Surface) -> None:
        """Draw the ball on the screen."""
        pygame.draw.rect(screen, config.colors.BALL, self.rect)
    
    @property
    def speed(self) -> float:
        """Get current speed magnitude."""
        return calculate_speed_from_velocity(self.velocity_x, self.velocity_y)
    
    @property
    def angle(self) -> float:
        """Get current movement angle in degrees."""
        return math.degrees(math.atan2(self.velocity_y, self.velocity_x))


class GameState:
    """
    Manages game state and scoring logic.
    
    Separates state management from rendering and game objects.
    """
    
    def __init__(self, game_rules_config=None):
        """
        Initialize game state.
        
        Args:
            game_rules_config: Optional game rules configuration
        """
        self.config = game_rules_config or config.rules
        self.player_score = 0
        self.computer_score = 0
        self.losses = 0
        self.level = 1
        self.high_score = 0
        self.game_over = False
        self.countdown_active = False
        self.show_continue_prompt = False
        self.countdown_timer = 0
        self.last_countdown_tick = 0
    
    def reset(self) -> None:
        """Reset game state to initial values."""
        self.player_score = 0
        self.computer_score = 0
        self.losses = 0
        self.level = 1
        self.game_over = False
        self.countdown_active = False
        self.show_continue_prompt = False
        self.countdown_timer = 0
        self.last_countdown_tick = 0
    
    def increment_player_score(self) -> None:
        """Increment player score and update high score."""
        self.player_score += 1
        self.level += 1
        if self.player_score > self.high_score:
            self.high_score = self.player_score
    
    def increment_computer_score(self) -> None:
        """Increment computer score and losses."""
        self.computer_score += 1
        self.losses += 1
    
    def is_game_over(self) -> bool:
        """Check if game should end based on losses."""
        return self.losses >= self.config.max_losses
    
    def start_countdown(self) -> None:
        """Start the countdown timer."""
        self.countdown_active = True
        self.countdown_timer = self.config.countdown_duration
        self.last_countdown_tick = pygame.time.get_ticks()
    
    def update_countdown(self) -> bool:
        """
        Update countdown timer.
        
        Returns:
            True if countdown completed
        """
        if not self.countdown_active:
            return False
        
        current_tick = pygame.time.get_ticks()
        if current_tick - self.last_countdown_tick >= self.config.countdown_tick_interval:
            self.countdown_timer -= 1
            self.last_countdown_tick = current_tick
            
            if self.countdown_timer <= 0:
                self.countdown_active = False
                return True
        
        return False
