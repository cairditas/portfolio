"""
UI Module

Handles all user interface rendering and interaction.
Separates UI concerns from game logic.
"""

import pygame
from typing import Optional, Tuple
from pong.core.config import config


class TextRenderer:
    """Handles text rendering with different fonts and styles."""
    
    def __init__(self):
        """Initialize text renderer with fonts."""
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
    
    def render_text(self, text: str, color: tuple, use_small_font: bool = False) -> pygame.Surface:
        """
        Render text to a surface.
        
        Args:
            text: Text to render
            color: RGB color tuple
            use_small_font: Whether to use small font
        
        Returns:
            Rendered text surface
        """
        font = self.small_font if use_small_font else self.font
        return font.render(text, True, color)
    
    def render_text_at(self, screen: pygame.Surface, text: str, position: Tuple[int, int], 
                      color: tuple, use_small_font: bool = False) -> None:
        """
        Render text at a specific position on screen.
        
        Args:
            screen: Surface to draw on
            text: Text to render
            position: (x, y) position
            color: RGB color tuple
            use_small_font: Whether to use small font
        """
        text_surface = self.render_text(text, color, use_small_font)
        screen.blit(text_surface, position)


class Button:
    """Interactive button for UI elements."""
    
    def __init__(self, x: int, y: int, width: int, height: int, text: str, 
                 text_color: tuple, button_color: tuple, text_renderer: TextRenderer):
        """
        Initialize button.
        
        Args:
            x, y: Button position
            width, height: Button dimensions
            text: Button text
            text_color: Text color
            button_color: Button color
            text_renderer: Text renderer instance
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.text_color = text_color
        self.button_color = button_color
        self.text_renderer = text_renderer
        self.hovered = False
    
    def update(self, mouse_pos: Tuple[int, int]) -> None:
        """Update button hover state based on mouse position."""
        self.hovered = self.rect.collidepoint(mouse_pos)
    
    def is_clicked(self, mouse_pos: Tuple[int, int], mouse_click: bool) -> bool:
        """
        Check if button was clicked.
        
        Args:
            mouse_pos: Mouse position
            mouse_click: Whether mouse was clicked
        
        Returns:
            True if button was clicked
        """
        return self.rect.collidepoint(mouse_pos) and mouse_click
    
    def draw(self, screen: pygame.Surface) -> None:
        """Draw the button on screen."""
        # Draw button background
        color = self.button_color if not self.hovered else tuple(min(255, c + 50) for c in self.button_color)
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, config.colors.TEXT, self.rect, 2)  # Border
        
        # Draw text
        text_surface = self.text_renderer.render_text(self.text, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)


class GameRenderer:
    """Handles all game rendering operations."""
    
    def __init__(self, screen: pygame.Surface):
        """
        Initialize game renderer.
        
        Args:
            screen: Pygame display surface
        """
        self.screen = screen
        self.text_renderer = TextRenderer()
        self.buttons = []
    
    def clear_screen(self) -> None:
        """Clear the screen with background color."""
        self.screen.fill(config.colors.BACKGROUND)
    
    def draw_game_area(self) -> None:
        """Draw the game area boundaries."""
        # Draw game area border in blue
        pygame.draw.rect(self.screen, config.colors.BLUE, 
                        (config.game_area.x, config.game_area.y, 
                         config.game_area.width, config.game_area.height), 2)
        
        # Draw dashed middle dividing line
        middle_x = config.game_area.x + config.game_area.width // 2
        dash_length = 10
        gap_length = 5
        y_start = config.game_area.y
        y_end = config.game_area.y + config.game_area.height
        
        current_y = y_start
        while current_y < y_end:
            # Draw dash
            dash_end = min(current_y + dash_length, y_end)
            pygame.draw.line(self.screen, config.colors.WHITE,
                           (middle_x, current_y),
                           (middle_x, dash_end), 2)
            current_y += dash_length + gap_length
    
    def draw_scores(self, game_state) -> None:
        """
        Draw player and computer scores.
        
        Args:
            game_state: Current game state
        """
        self.text_renderer.render_text_at(
            self.screen, f"Player: {game_state.player_score}", 
            config.ui.player_score_pos, config.colors.TEXT
        )
        
        self.text_renderer.render_text_at(
            self.screen, f"Computer: {game_state.computer_score}", 
            config.ui.computer_score_pos, config.colors.TEXT
        )
    
    def draw_game_info(self, game_state) -> None:
        """
        Draw game information (high score, level, losses).
        
        Args:
            game_state: Current game state
        """
        self.text_renderer.render_text_at(
            self.screen, f"High Score: {game_state.high_score}", 
            config.ui.high_score_pos, config.colors.TEXT
        )
        
        self.text_renderer.render_text_at(
            self.screen, f"Level: {game_state.level}", 
            config.ui.level_pos, config.colors.TEXT, use_small_font=True
        )
        
        self.text_renderer.render_text_at(
            self.screen, f"Losses: {game_state.losses}/{config.rules.max_losses}", 
            config.ui.losses_pos, config.colors.TEXT, use_small_font=True
        )
    
    def draw_countdown(self, countdown_timer: int) -> None:
        """
        Draw countdown timer.
        
        Args:
            countdown_timer: Current countdown value
        """
        if countdown_timer > 0:
            # Create much larger font for countdown
            large_font = pygame.font.Font(None, 120)  # Much larger font
            countdown_text = str(countdown_timer)
            text_surface = large_font.render(countdown_text, True, config.colors.GREEN)
            text_rect = text_surface.get_rect(center=(config.window.width // 2, config.window.height // 2))
            
            # Draw a background circle for better visibility
            circle_radius = 80
            pygame.draw.circle(self.screen, config.colors.BLACK, 
                             (config.window.width // 2, config.window.height // 2), 
                             circle_radius)
            pygame.draw.circle(self.screen, config.colors.WHITE, 
                             (config.window.width // 2, config.window.height // 2), 
                             circle_radius, 3)
            
            # Draw the countdown number
            self.screen.blit(text_surface, text_rect)
    
    def draw_game_over_screen(self) -> Tuple[Optional[Button], Optional[Button]]:
        """
        Draw game over screen with continue buttons.
        
        Returns:
            Tuple of (yes_button, no_button)
        """
        # Create semi-transparent overlay
        overlay = pygame.Surface((config.window.width, config.window.height))
        overlay.set_alpha(128)
        overlay.fill(config.colors.BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Draw game over text
        game_over_text = "Game Over! Continue?"
        text_surface = self.text_renderer.render_text(game_over_text, config.colors.WHITE)
        text_rect = text_surface.get_rect(center=(config.window.width // 2, config.window.height // 2 - 50))
        self.screen.blit(text_surface, text_rect)
        
        # Create buttons
        button_y = config.window.height // 2 + 20
        yes_button = Button(
            config.window.width // 2 + config.ui.yes_button_offset, button_y,
            config.ui.button_width, config.ui.button_height, "Yes",
            config.colors.BLACK, config.colors.GREEN, self.text_renderer
        )
        
        no_button = Button(
            config.window.width // 2 + config.ui.no_button_offset, button_y,
            config.ui.button_width, config.ui.button_height, "No",
            config.colors.BLACK, config.colors.RED, self.text_renderer
        )
        
        # Draw buttons
        yes_button.draw(self.screen)
        no_button.draw(self.screen)
        
        return yes_button, no_button
    
    def render_complete_frame(self, game_objects, game_state) -> None:
        """
        Render a complete game frame.
        
        Args:
            game_objects: Dictionary containing game objects
            game_state: Current game state
        """
        self.clear_screen()
        self.draw_game_area()
        
        # Draw game objects
        game_objects['player_paddle'].draw(self.screen)
        game_objects['computer_paddle'].draw(self.screen)
        game_objects['ball'].draw(self.screen)
        
        # Draw UI elements
        self.draw_scores(game_state)
        self.draw_game_info(game_state)
        
        if game_state.countdown_active:
            self.draw_countdown(game_state.countdown_timer)
        
        pygame.display.flip()


class InputHandler:
    """Handles user input processing."""
    
    @staticmethod
    def get_keyboard_state() -> dict:
        """
        Get current keyboard state.
        
        Returns:
            Dictionary with keyboard state
        """
        keys = pygame.key.get_pressed()
        return {
            'up': keys[pygame.K_UP] or keys[pygame.K_w],
            'down': keys[pygame.K_DOWN] or keys[pygame.K_s],
            'escape': keys[pygame.K_ESCAPE],
            'space': keys[pygame.K_SPACE]
        }
    
    @staticmethod
    def handle_events() -> Tuple[bool, dict]:
        """
        Handle pygame events.
        
        Returns:
            Tuple of (should_quit, event_data)
        """
        should_quit = False
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                should_quit = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    mouse_click = True
        
        return should_quit, {
            'mouse_pos': mouse_pos,
            'mouse_click': mouse_click,
            'keyboard': InputHandler.get_keyboard_state()
        }
