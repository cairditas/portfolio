"""
Test Data Builders

Builder pattern implementation for creating complex test scenarios with fluent interface.
Simplifies test setup and makes test scenarios more readable and maintainable.
"""

from typing import Optional, List, Tuple, Dict, Any
from unittest.mock import patch
import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from pong.game import Paddle, Ball, PongGame
from pong.core.config import config, Colors

# Get constants for test convenience
GAME_AREA_X = config.game_area.x
GAME_AREA_Y = config.game_area.y
GAME_AREA_WIDTH = config.game_area.width
GAME_AREA_HEIGHT = config.game_area.height
PADDLE_WIDTH = config.paddle.width
PADDLE_HEIGHT = config.paddle.height
PADDLE_SPEED = config.paddle.y_amount
BALL_SIZE = config.ball.size
INITIAL_BALL_SPEED = config.ball.initial_speed
MAX_LOSSES = config.rules.max_losses
from tests.fixtures.test_config import TestDataRanges, ScoringScenarios, IntegrationScenarios


class PaddleBuilder:
    """Builder for creating paddle test configurations."""
    
    def __init__(self):
        self.x = GAME_AREA_X + 20
        self.y = GAME_AREA_Y + GAME_AREA_HEIGHT // 2 - PADDLE_HEIGHT // 2
        self.color = Colors.BLUE
        self.y_amount = PADDLE_SPEED
    
    def with_position(self, x: int, y: int) -> 'PaddleBuilder':
        """Set paddle position."""
        self.x = x
        self.y = y
        return self
    
    def with_color(self, color: Tuple[int, int, int]) -> 'PaddleBuilder':
        """Set paddle color."""
        self.color = color
        return self
    
    def with_speed(self, speed: int) -> 'PaddleBuilder':
        """Set paddle speed."""
        self.speed = speed
        return self
    
    def at_top_boundary(self) -> 'PaddleBuilder':
        """Position paddle at top boundary."""
        self.y = GAME_AREA_Y
        return self
    
    def at_bottom_boundary(self) -> 'PaddleBuilder':
        """Position paddle at bottom boundary."""
        self.y = GAME_AREA_Y + GAME_AREA_HEIGHT - PADDLE_HEIGHT
        return self
    
    def near_top_boundary(self, margin: int = 5) -> 'PaddleBuilder':
        """Position paddle near top boundary."""
        self.y = GAME_AREA_Y + margin
        return self
    
    def near_bottom_boundary(self, margin: int = 5) -> 'PaddleBuilder':
        """Position paddle near bottom boundary."""
        self.y = GAME_AREA_Y + GAME_AREA_HEIGHT - PADDLE_HEIGHT - margin
        return self
    
    def build(self) -> Paddle:
        """Build the paddle."""
        paddle = Paddle(self.x, self.y, self.color)
        paddle.y_amount = self.y_amount
        return paddle


class BallBuilder:
    """Builder for creating ball test configurations."""
    
    def __init__(self):
        self.x = GAME_AREA_X + GAME_AREA_WIDTH // 2 - BALL_SIZE // 2
        self.y = GAME_AREA_Y + GAME_AREA_HEIGHT // 2 - BALL_SIZE // 2
        self.velocity_x = 5
        self.velocity_y = 5
        self.base_speed = INITIAL_BALL_SPEED
    
    def with_position(self, x: int, y: int) -> 'BallBuilder':
        """Set ball position."""
        self.x = x
        self.y = y
        return self
    
    def with_velocity(self, vx: int, vy: int) -> 'BallBuilder':
        """Set ball velocity."""
        self.velocity_x = vx
        self.velocity_y = vy
        return self
    
    def with_speed(self, speed: float) -> 'BallBuilder':
        """Set ball base speed."""
        self.base_speed = speed
        return self
    
    def moving_up(self) -> 'BallBuilder':
        """Set ball moving upward."""
        self.velocity_y = -abs(self.velocity_y)
        return self
    
    def moving_down(self) -> 'BallBuilder':
        """Set ball moving downward."""
        self.velocity_y = abs(self.velocity_y)
        return self
    
    def moving_left(self) -> 'BallBuilder':
        """Set ball moving leftward."""
        self.velocity_x = -abs(self.velocity_x)
        return self
    
    def moving_right(self) -> 'BallBuilder':
        """Set ball moving rightward."""
        self.velocity_x = abs(self.velocity_x)
        return self
    
    def at_top_boundary(self, margin: int = 2) -> 'BallBuilder':
        """Position ball near top boundary."""
        self.y = GAME_AREA_Y + margin
        return self
    
    def at_bottom_boundary(self, margin: int = 2) -> 'BallBuilder':
        """Position ball near bottom boundary."""
        self.y = GAME_AREA_Y + GAME_AREA_HEIGHT - BALL_SIZE - margin
        return self
    
    def past_left_paddle(self) -> 'BallBuilder':
        """Position ball past left paddle (for scoring)."""
        self.x = GAME_AREA_X - 10
        return self
    
    def past_right_paddle(self) -> 'BallBuilder':
        """Position ball past right paddle (for scoring)."""
        self.x = GAME_AREA_X + GAME_AREA_WIDTH + 10
        return self
    
    def at_center(self) -> 'BallBuilder':
        """Position ball at game center."""
        self.x = GAME_AREA_X + GAME_AREA_WIDTH // 2 - BALL_SIZE // 2
        self.y = GAME_AREA_Y + GAME_AREA_HEIGHT // 2 - BALL_SIZE // 2
        return self
    
    def build(self) -> Ball:
        """Build the ball."""
        ball = Ball()
        ball.rect.x = self.x
        ball.rect.y = self.y
        ball.velocity_x = self.velocity_x
        ball.velocity_y = self.velocity_y
        ball.base_speed = self.base_speed
        return ball


class GameStateBuilder:
    """Builder for creating game state scenarios."""
    
    def __init__(self):
        self.player_score = 0
        self.computer_score = 0
        self.losses = 0
        self.level = 1
        self.high_score = 0
        self.game_over = False
        self.countdown_active = False
        self.show_continue_prompt = False
        self.ball_position = None
        self.ball_velocity = None
        self.paddle_positions = {}
    
    def with_scores(self, player: int, computer: int) -> 'GameStateBuilder':
        """Set game scores."""
        self.player_score = player
        self.computer_score = computer
        return self
    
    def with_losses(self, losses: int) -> 'GameStateBuilder':
        """Set losses."""
        self.losses = losses
        return self
    
    def with_level(self, level: int) -> 'GameStateBuilder':
        """Set game level."""
        self.level = level
        return self
    
    def with_high_score(self, high_score: int) -> 'GameStateBuilder':
        """Set high score."""
        self.high_score = high_score
        return self
    
    def game_over_state(self) -> 'GameStateBuilder':
        """Set game to over state."""
        self.game_over = True
        self.show_continue_prompt = True
        return self
    
    def countdown_state(self) -> 'GameStateBuilder':
        """Set game to countdown state."""
        self.countdown_active = True
        self.countdown_value = 3
        return self
    
    def with_ball_at(self, x: int, y: int) -> 'GameStateBuilder':
        """Set ball position."""
        self.ball_position = (x, y)
        return self
    
    def with_ball_velocity(self, vx: int, vy: int) -> 'GameStateBuilder':
        """Set ball velocity."""
        self.ball_velocity = (vx, vy)
        return self
    
    def with_paddle_position(self, paddle_type: str, x: int, y: int) -> 'GameStateBuilder':
        """Set paddle position."""
        self.paddle_positions[paddle_type] = (x, y)
        return self
    
    def player_winning(self, score: int) -> 'GameStateBuilder':
        """Set up player winning scenario."""
        self.player_score = score
        self.level = score + 1
        return self
    
    def computer_winning(self, score: int) -> 'GameStateBuilder':
        """Set up computer winning scenario."""
        self.computer_score = score
        self.losses = score
        return self
    
    def at_max_losses(self) -> 'GameStateBuilder':
        """Set game at maximum losses."""
        self.losses = MAX_LOSSES
        self.game_over = True
        self.show_continue_prompt = True
        return self
    
    def build(self, game: PongGame) -> PongGame:
        """Apply the built state to a game object."""
        game.game_state.player_score = self.player_score
        game.game_state.computer_score = self.computer_score
        game.game_state.losses = self.losses
        game.game_state.level = self.level
        game.game_state.high_score = self.high_score
        game.game_state.game_over = self.game_over
        game.game_state.countdown_active = self.countdown_active
        game.game_state.show_continue_prompt = self.show_continue_prompt
        
        if self.ball_position:
            game.game_objects['ball'].rect.x, game.game_objects['ball'].rect.y = self.ball_position
        
        if self.ball_velocity:
            game.game_objects['ball'].velocity_x, game.game_objects['ball'].velocity_y = self.ball_velocity
        
        for paddle_type, position in self.paddle_positions.items():
            paddle = game.game_objects[f"{paddle_type}_paddle"]
            paddle.rect.x, paddle.rect.y = position
        
        return game


class GameScenarioBuilder:
    """Builder for creating complete game test scenarios."""
    
    def __init__(self):
        self.game = None
        self.actions = []
    
    def create_game(self) -> 'GameScenarioBuilder':
        """Create a new game instance."""
        with patch('pygame.display.set_mode'):
            with patch('pygame.font.Font'):
                self.game = PongGame()
        return self
    
    def player_scores(self, times: int = 1) -> 'GameScenarioBuilder':
        """Add player scoring action."""
        for _ in range(times):
            self.actions.append(('player_score', None))
        return self
    
    def computer_scores(self, times: int = 1) -> 'GameScenarioBuilder':
        """Add computer scoring action."""
        for _ in range(times):
            self.actions.append(('computer_score', None))
        return self
    
    def move_ball_to(self, x: int, y: int) -> 'GameScenarioBuilder':
        """Add ball positioning action."""
        self.actions.append(('move_ball', (x, y)))
        return self
    
    def set_ball_velocity(self, vx: int, vy: int) -> 'GameScenarioBuilder':
        """Add ball velocity action."""
        self.actions.append(('set_velocity', (vx, vy)))
        return self
    
    def move_paddle(self, paddle_type: str, direction: str) -> 'GameScenarioBuilder':
        """Add paddle movement action."""
        self.actions.append(('move_paddle', (paddle_type, direction)))
        return self
    
    def trigger_collision(self, paddle_type: str) -> 'GameScenarioBuilder':
        """Add paddle collision action."""
        self.actions.append(('collision', paddle_type))
        return self
    
    def reset_game(self) -> 'GameScenarioBuilder':
        """Add game reset action."""
        self.actions.append(('reset', None))
        return self
    
    def execute(self) -> PongGame:
        """Execute all actions and return the game state."""
        if not self.game:
            raise ValueError("Must call create_game() first")
        
        for action, data in self.actions:
            if action == 'player_score':
                self.game.game_objects['ball'].rect.left = GAME_AREA_X + GAME_AREA_WIDTH + 1
                self.game.handle_scoring()
            
            elif action == 'computer_score':
                self.game.game_objects['ball'].rect.right = GAME_AREA_X - 1
                self.game.handle_scoring()
            
            elif action == 'move_ball':
                x, y = data
                self.game.game_objects['ball'].rect.x, self.game.game_objects['ball'].rect.y = x, y
            
            elif action == 'set_velocity':
                vx, vy = data
                self.game.game_objects['ball'].velocity_x, self.game.game_objects['ball'].velocity_y = vx, vy
            
            elif action == 'move_paddle':
                paddle_type, direction = data
                paddle = self.game.game_objects[f"{paddle_type}_paddle"]
                if direction == 'up':
                    paddle.move_up()
                elif direction == 'down':
                    paddle.move_down()
            
            elif action == 'collision':
                paddle_type = data
                paddle = self.game.game_objects[f"{paddle_type}_paddle"]
                self.game.game_objects['ball'].rect.centerx = paddle.rect.centerx
                self.game.game_objects['ball'].rect.centery = paddle.rect.centery
                self.game.handle_paddle_collision()
            
            elif action == 'reset':
                self.game.reset_game()
        
        return self.game


class TestDataFactory:
    """Factory for creating common test data configurations."""
    
    @staticmethod
    def create_paddle(x: int = 100, y: int = 200, color: Tuple[int, int, int] = Colors.BLUE) -> Paddle:
        """Create a paddle with default or specified parameters."""
        return PaddleBuilder().with_position(x, y).with_color(color).build()
    
    @staticmethod
    def create_ball() -> Ball:
        """Create a ball with default parameters."""
        return BallBuilder().build()
    
    @staticmethod
    def create_game() -> PongGame:
        """Create a game instance with mocked display to avoid overhead."""
        with patch('pygame.display.set_mode'):
            with patch('pygame.font.Font'):
                return PongGame()
    
    @staticmethod
    def create_paddle_at_boundary(boundary: str, color: Tuple[int, int, int] = Colors.BLUE) -> Paddle:
        """Create paddle at specified boundary."""
        builder = PaddleBuilder().with_color(color)
        
        if boundary == 'top':
            return builder.at_top_boundary().build()
        elif boundary == 'bottom':
            return builder.at_bottom_boundary().build()
        else:
            raise ValueError(f"Unknown boundary: {boundary}")
    
    @staticmethod
    def create_paddle_near_boundary(boundary: str, margin: int = 5, 
                                  color: Tuple[int, int, int] = Colors.BLUE) -> Paddle:
        """Create paddle near specified boundary."""
        builder = PaddleBuilder().with_color(color)
        
        if boundary == 'top':
            return builder.near_top_boundary(margin).build()
        elif boundary == 'bottom':
            return builder.near_bottom_boundary(margin).build()
        else:
            raise ValueError(f"Unknown boundary: {boundary}")
    
    @staticmethod
    def create_ball_at_boundary(boundary: str, velocity: Tuple[int, int] = (5, 5)) -> Ball:
        """Create ball at specified boundary."""
        builder = BallBuilder().with_velocity(*velocity)
        
        if boundary == 'top':
            return builder.at_top_boundary().build()
        elif boundary == 'bottom':
            return builder.at_bottom_boundary().build()
        elif boundary == 'left':
            return builder.past_left_paddle().build()
        elif boundary == 'right':
            return builder.past_right_paddle().build()
        else:
            raise ValueError(f"Unknown boundary: {boundary}")
    
    @staticmethod
    def create_scoring_scenario(scoring_type: str) -> Tuple[PongGame, Dict[str, Any]]:
        """Create a scoring scenario."""
        with patch('pygame.display.set_mode'):
            with patch('pygame.font.Font'):
                game = PongGame()
        
        if scoring_type == 'player_scores':
            game.ball.rect.left = GAME_AREA_X + GAME_AREA_WIDTH + 1
            expected = {'player_score': 1, 'computer_score': 0, 'losses': 0, 'level': 2}
        elif scoring_type == 'computer_scores':
            game.ball.rect.right = GAME_AREA_X - 1
            expected = {'player_score': 0, 'computer_score': 1, 'losses': 1, 'level': 1}
        else:
            raise ValueError(f"Unknown scoring type: {scoring_type}")
        
        return game, expected
    
    @staticmethod
    def create_boundary_collision_scenario(boundary: str) -> Tuple[PongGame, Dict[str, Any]]:
        """Create a boundary collision scenario."""
        with patch('pygame.display.set_mode'):
            with patch('pygame.font.Font'):
                game = PongGame()
        
        if boundary == 'top':
            game.ball.rect.y = GAME_AREA_Y + 2
            game.ball.velocity_y = -5
            expected = {'boundary': 'top', 'initial_velocity': (0, -5)}
        elif boundary == 'bottom':
            game.ball.rect.y = GAME_AREA_Y + GAME_AREA_HEIGHT - BALL_SIZE - 2
            game.ball.velocity_y = 5
            expected = {'boundary': 'bottom', 'initial_velocity': (0, 5)}
        else:
            raise ValueError(f"Unknown boundary: {boundary}")
        
        return game, expected
    
    @staticmethod
    def create_complete_game_scenario() -> PongGame:
        """Create a complete game scenario."""
        return (GameScenarioBuilder()
                .create_game()
                .player_scores(3)
                .computer_scores(2)
                .execute())
    
    @staticmethod
    def create_ai_test_scenario(mistake: bool = False) -> Tuple[Paddle, Dict[str, Any]]:
        """Create AI movement test scenario."""
        paddle = PaddleBuilder().build()
        
        if mistake:
            ball_y = paddle.rect.centery + 50
            expected_direction = 'up'
        else:
            ball_y = paddle.rect.centery + 50
            expected_direction = 'down'
        
        scenario = {
            'ball_y': ball_y,
            'ball_velocity_y': 0,
            'make_mistake': mistake,
            'expected_direction': expected_direction
        }
        
        return paddle, scenario


# Convenience functions for common patterns
def create_paddle() -> Paddle:
    """Create a standard paddle."""
    return PaddleBuilder().build()

def create_ball() -> Ball:
    """Create a standard ball."""
    return BallBuilder().build()

def create_game() -> PongGame:
    """Create a standard game."""
    with patch('pygame.display.set_mode'):
        with patch('pygame.font.Font'):
            return PongGame()

def create_game_with_state(player_score: int = 0, computer_score: int = 0, 
                          losses: int = 0, level: int = 1) -> PongGame:
    """Create game with specific state."""
    game = create_game()
    return (GameStateBuilder()
            .with_scores(player_score, computer_score)
            .with_losses(losses)
            .with_level(level)
            .build(game))
