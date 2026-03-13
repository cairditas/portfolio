"""
Game Configuration Module

Centralized configuration for all game constants and settings.
Follows DRY principles by providing single source of truth for configuration.
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
    speed: int = 10  # Increased from 7 to 10 for faster movement
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
    error_chance: float = 0.15  # 15% chance of mistake
    prediction_factor: int = 10  # How far AI predicts ball movement
    movement_threshold: int = 5  # Minimum difference to trigger movement
    mistake_distance: int = 100  # Distance to move away when making mistake


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
    
    # Text positions - centered over game area
    player_score_pos: Tuple[int, int] = None  # Will be calculated dynamically
    computer_score_pos: Tuple[int, int] = None  # Will be calculated dynamically
    high_score_pos: Tuple[int, int] = (1000 // 2 - 100, 30)  # Centered at top
    level_pos: Tuple[int, int] = (50, 60)
    losses_pos: Tuple[int, int] = (950, 60)
    
    def __post_init__(self):
        """Calculate dynamic positions based on game area."""
        # These will be calculated when we have access to game area config
        pass


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
        self._calculate_ui_positions()
    
    def _calculate_ui_positions(self):
        """Calculate UI positions based on game area."""
        # Player score - left aligned over game area
        self.ui.player_score_pos = (self.game_area.x, 30)
        
        # Computer score - right aligned over game area
        computer_score_x = self.game_area.x + self.game_area.width - 200
        self.ui.computer_score_pos = (computer_score_x, 30)
        
        # High score - centered at top
        self.ui.high_score_pos = (self.window.width // 2 - 100, 30)
        
        # Level and losses - positioned within window bounds
        self.ui.level_pos = (50, 60)
        self.ui.losses_pos = (self.window.width - 200, 60)  # Adjusted for 1000px width
    
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
