"""
Game Configuration Module

Centralized configuration for all game constants and settings.
"""

from dataclasses import dataclass
from typing import Tuple


@dataclass
class WindowConfig:
    """Window and display configuration."""
    width: int = 1000
    height: int = 700
    fps: int = 60
    caption: str = "Pong Game"


@dataclass
class GameAreaConfig:
    """Game area configuration."""
    width: int = 900
    height: int = 500
    x: int = 50
    y: int = 100
    
    @property
    def right_edge(self) -> int:
        """Get the right edge coordinate."""
        return self.x + self.width
    
    @property
    def bottom_edge(self) -> int:
        """Get the bottom edge coordinate."""
        return self.y + self.height


@dataclass
class PaddleConfig:
    """Paddle configuration."""
    width: int = 10
    height: int = 60
    y_amount: int = 10
    player_offset_x: int = 20  # Distance from left edge
    computer_offset_x: int = 30  # Distance from right edge


@dataclass
class BallConfig:
    """Ball configuration."""
    size: int = 10
    initial_speed: float = 8.0
    speed_increment: float = 0.25
    min_angle: float = 30.0  # degrees
    max_angle: float = 60.0  # degrees
    
    @property
    def angle_ranges(self) -> list[Tuple[float, float]]:
        """Get allowed angle ranges for ball movement."""
        return [
            (self.min_angle, self.max_angle),
            (180 - self.max_angle, 180 - self.min_angle)
        ]


@dataclass
class AIConfig:
    """AI opponent configuration."""
    error_chance: float = 0.10  # 10% chance of mistake
    prediction_factor: int = 20  # Increased prediction distance for better tracking
    movement_threshold: int = 2  # Very responsive movement
    mistake_distance: int = 30  # Smaller mistake distance so mistakes are less severe


@dataclass
class GameRulesConfig:
    """Game rules and progression configuration."""
    max_losses: int = 5
    countdown_duration: int = 3  # seconds
    countdown_tick_interval: int = 1000  # milliseconds


@dataclass
class UIConfig:
    """UI elements configuration."""
    button_width: int = 100
    button_height: int = 40
    yes_button_offset: int = -120
    no_button_offset: int = 20
    
    # Text positions - will be calculated dynamically
    player_score_pos: Tuple[int, int] = None
    computer_score_pos: Tuple[int, int] = None
    high_score_pos: Tuple[int, int] = (500, 30)
    level_pos: Tuple[int, int] = (50, 60)
    losses_pos: Tuple[int, int] = (800, 60)
    
    def calculate_positions(self, window_width: int, game_area_x: int, game_area_width: int):
        """Calculate dynamic positions based on window and game area."""
        # Update high score position to center of window
        self.high_score_pos = (window_width // 2 - 100, 30)
        
        # Update losses position to be within window bounds
        self.losses_pos = (window_width - 200, 60)
        
        # Calculate score positions over game area
        self.player_score_pos = (game_area_x, 30)
        computer_score_x = game_area_x + game_area_width - 200
        self.computer_score_pos = (computer_score_x, 30)


class Colors:
    """Color palette for the game."""
    
    # Basic colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    GRAY = (128, 128, 128)
    
    # Game-specific colors
    PADDLE_PLAYER = BLUE
    PADDLE_COMPUTER = RED
    BALL = WHITE
    TEXT = WHITE
    BACKGROUND = BLACK
    GAME_AREA_BORDER = GREEN


class GameConfig:
    """Main configuration container that aggregates all game settings."""
    
    def __init__(self):
        self.window = WindowConfig()
        self.game_area = GameAreaConfig()
        self.paddle = PaddleConfig()
        self.ball = BallConfig()
        self.ai = AIConfig()
        self.rules = GameRulesConfig()
        self.ui = UIConfig()
        self.colors = Colors()
        
        # Calculate dynamic UI positions
        self.ui.calculate_positions(
            self.window.width, 
            self.game_area.x, 
            self.game_area.width
        )
    
    @property
    def player_paddle_x(self) -> int:
        """Get player paddle starting X position."""
        return self.game_area.x + self.paddle.player_offset_x
    
    @property
    def computer_paddle_x(self) -> int:
        """Get computer paddle starting X position."""
        return self.game_area.right_edge - self.paddle.computer_offset_x
    
    @property
    def ball_center_x(self) -> int:
        """Get ball center X position."""
        return self.game_area.x + self.game_area.width // 2 - self.ball.size // 2
    
    @property
    def ball_center_y(self) -> int:
        """Get ball center Y position."""
        return self.game_area.y + self.game_area.height // 2 - self.ball.size // 2


# Global configuration instance
config = GameConfig()
