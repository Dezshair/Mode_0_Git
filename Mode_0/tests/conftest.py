import pytest
import sys
import os

# Add the parent directory to path so Python can find the mode_0 package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture
def config_manager():
    from mode_0.config.config_manager import ConfigManager
    return ConfigManager()

@pytest.fixture
def mock_db():
    from unittest.mock import MagicMock, AsyncMock
    mock = MagicMock()
    mock.get_user_profile = AsyncMock(return_value={})
    mock.update_user_profile = AsyncMock()
    return mock
