"""
Test Configuration Management

Centralized configuration for test parameters, performance benchmarks,
and test data ranges. Eliminates magic numbers and makes tests easier to maintain.
"""

import os
from typing import List, Tuple

# Game area constants (from main game)
GAME_AREA_X = 50
GAME_AREA_Y = 100
GAME_AREA_WIDTH = 700
GAME_AREA_HEIGHT = 400
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 60
BALL_SIZE = 10

# Performance benchmarks
class PerformanceBenchmarks:
    """Performance targets for test validation."""
    MAX_GAME_LOOP_TIME = 0.1  # seconds for 10 iterations
    MAX_MEMORY_GROWTH = 1000   # maximum object growth
    MAX_TEST_EXECUTION_TIME = 2.0  # seconds for full test suite
    
    # Allowable performance degradation (10%)
    PERFORMANCE_DEGRADATION_THRESHOLD = 1.1

# Test data ranges and positions
class TestDataRanges:
    """Valid ranges for test data generation."""
    
    # Valid paddle positions (x, y)
    PADDLE_POSITIONS = [
        (GAME_AREA_X + 20, GAME_AREA_Y + 50),
        (GAME_AREA_X + 100, GAME_AREA_Y + 200),
        (GAME_AREA_X + 300, GAME_AREA_Y + 150),
        (GAME_AREA_X + 500, GAME_AREA_Y + 300),
    ]
    
    # Ball velocities for testing (vx, vy)
    BALL_VELOCITIES = [
        (5, 5), (-5, 5), (5, -5), (-5, -5),
        (3, 7), (-3, 7), (3, -7), (-3, -7),
        (8, 2), (-8, 2), (8, -2), (-8, -2),
    ]
    
    # Boundary test positions
    BOUNDARY_POSITIONS = {
        'top_near': (GAME_AREA_X + 100, GAME_AREA_Y + 2),
        'bottom_near': (GAME_AREA_X + 100, GAME_AREA_Y + GAME_AREA_HEIGHT - 2 - BALL_SIZE),
        'left_far': (GAME_AREA_X - 100, GAME_AREA_Y + GAME_AREA_HEIGHT // 2),
        'right_far': (GAME_AREA_X + GAME_AREA_WIDTH + 100, GAME_AREA_Y + GAME_AREA_HEIGHT // 2),
    }
    
    # AI test scenarios
    AI_TEST_SCENARIUM = [
        {'ball_y': 200, 'ball_velocity_y': 0, 'make_mistake': False, 'expected_direction': 'down'},
        {'ball_y': 150, 'ball_velocity_y': 0, 'make_mistake': False, 'expected_direction': 'up'},
        {'ball_y': 200, 'ball_velocity_y': 0, 'make_mistake': True, 'expected_direction': 'up'},
        {'ball_y': 150, 'ball_velocity_y': 0, 'make_mistake': True, 'expected_direction': 'down'},
    ]

# Test margins and tolerances
class TestTolerances:
    """Margins and tolerances for test assertions."""
    
    # Boundary collision tolerances
    BOUNDARY_MARGIN = 5  # pixels
    POSITION_TOLERANCE = 1  # pixels
    
    # Velocity tolerances
    VELOCITY_TOLERANCE = 0.1
    
    # Performance tolerances
    TIME_TOLERANCE = 0.01  # seconds
    PERFORMANCE_DEGRADATION_THRESHOLD = 1.1  # 10% degradation allowed
    MAX_MEMORY_GROWTH = 1000  # maximum object growth
    
    # Visual testing tolerances
    PIXEL_DIFFERENCE_THRESHOLD = 100  # maximum different pixels
    COLOR_TOLERANCE = 5  # RGB value difference

# Scoring test scenarios
class ScoringScenarios:
    """Predefined scoring scenarios for testing."""
    
    PLAYER_SCORES = [
        ((GAME_AREA_X + GAME_AREA_WIDTH + 10, GAME_AREA_Y + 50), 1, 0, 0),  # First score
    ]
    
    COMPUTER_SCORES = [
        ((GAME_AREA_X - 10, GAME_AREA_Y + 50), 0, 1, 1),  # First score
    ]

# Integration test scenarios
class IntegrationScenarios:
    """Complex integration test scenarios."""
    
    COMPLETE_GAME = {
        'player_scores': 3,
        'computer_scores': 2,
        'expected_final_player_score': 3,
        'expected_final_computer_score': 2,
        'expected_final_losses': 2,
        'expected_level_increase': 3,
    }
    
    BOUNDARY_COLLISIONS = [
        {'position': 'top_near', 'velocity': (5, -5), 'expected_bounce': 'top'},
        {'position': 'bottom_near', 'velocity': (5, 5), 'expected_bounce': 'bottom'},
    ]

# CI/CD configuration
class CIConfig:
    """Configuration for continuous integration testing."""
    
    # Performance reporting
    ENABLE_PERFORMANCE_REPORTING = os.getenv('CI') is not None
    PERFORMANCE_REPORT_FILE = 'ci_metrics.json'
    
    # Test coverage
    MINIMUM_TEST_COVERAGE = 85  # percentage
    
    # Test execution limits
    MAX_TEST_RETRIES = 3
    TEST_TIMEOUT = 300  # seconds

# Development configuration
class DevConfig:
    """Configuration for development environment."""
    
    # Verbose output
    VERBOSE_TEST_OUTPUT = True
    
    # Debug mode
    DEBUG_TESTS = os.getenv('DEBUG_TESTS', 'false').lower() == 'true'
    
    # Test data persistence
    SAVE_TEST_ARTIFACTS = os.getenv('SAVE_TEST_ARTIFACTS', 'false').lower() == 'true'
    
    # Performance profiling
    ENABLE_PROFILING = os.getenv('PROFILE_TESTS', 'false').lower() == 'true'

# Utility functions
def get_paddle_positions() -> List[Tuple[int, int]]:
    """Get all valid paddle test positions."""
    return TestDataRanges.PADDLE_POSITIONS

def get_ball_velocities() -> List[Tuple[int, int]]:
    """Get all ball velocity test cases."""
    return TestDataRanges.BALL_VELOCITIES

def get_boundary_position(boundary_type: str) -> Tuple[int, int]:
    """Get a specific boundary test position."""
    return TestDataRanges.BOUNDARY_POSITIONS[boundary_type]

def is_ci_environment() -> bool:
    """Check if running in CI environment."""
    return CIConfig.ENABLE_PERFORMANCE_REPORTING

def should_save_artifacts() -> bool:
    """Check if test artifacts should be saved."""
    return DevConfig.SAVE_TEST_ARTIFACTS or is_ci_environment()
