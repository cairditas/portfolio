"""
Test package initialization

Configures test environment and provides common imports.
"""

import sys
import os
import warnings

# Add the src directory to the Python path for all tests
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# Suppress pygame warnings
warnings.filterwarnings("ignore", category=DeprecationWarning, module="pkg_resources")
