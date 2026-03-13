"""
Pytest configuration and shared fixtures

Provides common setup for all tests including path configuration
and warning suppression.
"""

import sys
import os
import warnings
from unittest.mock import patch
import pytest

# Add the src directory to the Python path for all tests
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


def pytest_configure():
    """Configure pytest with custom markers."""
    pytest.mark.unit = pytest.mark.unit("Unit tests for individual components")
    pytest.mark.integration = pytest.mark.integration("Integration tests for component interactions")
    pytest.mark.performance = pytest.mark.performance("Performance and memory tests")


@pytest.fixture(scope="session")
def pygame_display_mock():
    """Mock pygame display for all tests to avoid actual window creation."""
    with patch('pygame.display.set_mode'):
        with patch('pygame.font.Font'):
            yield


@pytest.fixture(scope="session")
def test_constants():
    """Provide access to commonly used test constants."""
    from tests.fixtures.test_config import TestDataRanges, TestTolerances, PerformanceBenchmarks
    return {
        'ranges': TestDataRanges,
        'tolerances': TestTolerances,
        'benchmarks': PerformanceBenchmarks
    }
