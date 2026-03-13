"""
Main Pong Game Implementation
"""

import pygame
from pong.core.config import config
from pong.ui import GameRenderer, InputHandler
from pong.ai import BasicAIStrategy
from pong.physics import BallPhysics, BoundaryChecker
from .objects import Paddle, Ball, GameState


class PongGame:
    """
    Main game class that orchestrates all game components.
    """
    
    def __init__(self):
        """Initialize the game with all components."""
        pygame.init()
        
        # Initialize display
        self.screen = pygame.display.set_mode((config.window.width, config.window.height))
        pygame.display.set_caption(config.window.caption)
        self.clock = pygame.time.Clock()
        
        # Initialize game components
        self.renderer = GameRenderer(self.screen)
        self.input_handler = InputHandler()
        self.ai_strategy = BasicAIStrategy()
        self.game_state = GameState()
        
        # Initialize game objects
        self._create_game_objects()
        
        # Game control flags
        self.running = True
        self.paused = False
    
    def _create_game_objects(self) -> None:
        """Create and initialize all game objects."""
        # Calculate paddle Y position to be vertically centered
        paddle_y = config.game_area.y + config.game_area.height // 2 - config.paddle.height // 2
        
        self.game_objects = {
            'player_paddle': Paddle(
                config.player_paddle_x, 
                paddle_y,
                config.colors.PADDLE_PLAYER
            ),
            'computer_paddle': Paddle(
                config.computer_paddle_x,
                paddle_y,
                config.colors.PADDLE_COMPUTER
            ),
            'ball': Ball()
        }
    
    def reset_game(self) -> None:
        """Reset the game to initial state."""
        self.game_state.reset()
        self._create_game_objects()
    
    def handle_scoring(self) -> bool:
        """
        Handle scoring when ball goes out of bounds.
        
        Returns:
            True if scoring occurred
        """
        ball = self.game_objects['ball']
        scored, scorer = BoundaryChecker.check_scoring(ball.rect, config.game_area)
        
        if scored:
            if scorer == 'player':
                self.game_state.increment_player_score()
                ball.increase_speed()
            else:  # computer
                self.game_state.increment_computer_score()
                self.game_state.game_over = self.game_state.is_game_over()
            
            ball.reset()
            return True
        
        return False
    
    def handle_paddle_collision(self) -> bool:
        """
        Handle ball collision with paddles.
        
        Returns:
            True if collision occurred
        """
        ball = self.game_objects['ball']
        player_paddle = self.game_objects['player_paddle']
        computer_paddle = self.game_objects['computer_paddle']
        
        collision_occurred = False
        
        # Player paddle collision
        if BoundaryChecker.check_paddle_collision(ball.rect, player_paddle.rect, ball.velocity_x):
            ball.velocity_x = -ball.velocity_x
            ball.velocity_y = BallPhysics.add_spin(ball.velocity_y)
            collision_occurred = True
        
        # Computer paddle collision
        elif BoundaryChecker.check_paddle_collision(ball.rect, computer_paddle.rect, ball.velocity_x):
            ball.velocity_x = -ball.velocity_x
            ball.velocity_y = BallPhysics.add_spin(ball.velocity_y)
            collision_occurred = True
        
        return collision_occurred
    
    def update_game_state(self) -> None:
        """Update all game objects and state."""
        if self.game_state.countdown_active:
            if self.game_state.update_countdown():
                self.game_state.countdown_active = False
            return
        
        # Update ball
        self.game_objects['ball'].move()
        
        # Handle collisions
        self.handle_paddle_collision()
        self.handle_scoring()
        
        # Update AI paddle
        self._update_ai_paddle()
    
    def _update_ai_paddle(self) -> None:
        """Update AI paddle movement."""
        ball = self.game_objects['ball']
        computer_paddle = self.game_objects['computer_paddle']
        
        movement_amount, _ = self.ai_strategy.calculate_move(
            ball.rect.centery, ball.velocity_y, computer_paddle.rect.centery
        )
        
        if movement_amount > 0:
            computer_paddle.move_down_by_amount(movement_amount)
        elif movement_amount < 0:
            computer_paddle.move_up_by_amount(abs(movement_amount))
    
    def handle_input(self) -> bool:
        """
        Handle user input.
        
        Returns:
            True if game should quit
        """
        should_quit, input_data = self.input_handler.handle_events()
        
        if should_quit:
            return True
        
        # Handle keyboard input for paddle movement
        keyboard = input_data['keyboard']
        player_paddle = self.game_objects['player_paddle']
        
        if keyboard['up']:
            player_paddle.move_up()
        if keyboard['down']:
            player_paddle.move_down()
        
        # Handle game over screen buttons
        if self.game_state.game_over and self.game_state.show_continue_prompt:
            return self._handle_game_over_input(input_data)
        
        return False
    
    def _handle_game_over_input(self, input_data) -> bool:
        """Handle input during game over screen."""
        mouse_pos = input_data['mouse_pos']
        mouse_click = input_data['mouse_click']
        
        if hasattr(self, 'continue_buttons'):
            yes_button, no_button = self.continue_buttons
            
            if yes_button.is_clicked(mouse_pos, mouse_click):
                self.reset_game()
                self.game_state.start_countdown()
                self.game_state.show_continue_prompt = False
            elif no_button.is_clicked(mouse_pos, mouse_click):
                return True
        
        return False
    
    def render(self) -> None:
        """Render the current game state."""
        if not self.game_state.game_over:
            self.renderer.render_complete_frame(self.game_objects, self.game_state)
        else:
            # Handle game over screen
            if not self.game_state.show_continue_prompt:
                self.game_state.show_continue_prompt = True
                self.continue_buttons = self.renderer.draw_game_over_screen()
            elif hasattr(self, 'continue_buttons'):
                yes_button, no_button = self.continue_buttons
                mouse_pos = pygame.mouse.get_pos()
                yes_button.update(mouse_pos)
                no_button.update(mouse_pos)
                yes_button.draw(self.screen)
                no_button.draw(self.screen)
                pygame.display.flip()
    
    def run(self) -> None:
        """Main game loop."""
        # Don't start with countdown - let player start immediately
        # self.game_state.start_countdown()
        
        while self.running:
            # Handle input
            if self.handle_input():
                break
            
            # Update game state
            self.update_game_state()
            
            # Render
            self.render()
            
            # Control frame rate
            self.clock.tick(config.window.fps)
        
        pygame.quit()
