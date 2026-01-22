"""
ConfigManager - Centralized settings management with JSON persistence.

Handles loading, saving, and providing defaults for user preferences.
"""

import json
import logging
from pathlib import Path
from typing import Any, Dict

logger = logging.getLogger(__name__)


class ConfigManager:
    """Manages application configuration with JSON file persistence."""
    
    DEFAULT_SETTINGS: Dict[str, Any] = {
        "language": "en",      # 'en' or 'bn'
        "interval": 60,        # 15, 30, or 60 (minutes)
        "muted": False
    }
    
    def __init__(self, config_path: Path):
        """
        Initialize the ConfigManager.
        
        Args:
            config_path: Path to the JSON configuration file.
        """
        self.config_path = Path(config_path)
        self._settings: Dict[str, Any] = {}
        self.load()
    
    def load(self) -> Dict[str, Any]:
        """
        Load settings from JSON file.
        
        Creates default config if file doesn't exist.
        Resets to defaults if file is corrupted.
        
        Returns:
            The loaded settings dictionary.
        """
        if not self.config_path.exists():
            logger.info(f"Config file not found, creating defaults at {self.config_path}")
            self._settings = self.DEFAULT_SETTINGS.copy()
            self.save(self._settings)
            return self._settings
        
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                loaded = json.load(f)
            
            # Merge with defaults to handle missing keys (forward compatibility)
            self._settings = {**self.DEFAULT_SETTINGS, **loaded}
            logger.info(f"Config loaded from {self.config_path}")
            
        except (json.JSONDecodeError, IOError) as e:
            logger.warning(f"Failed to load config ({e}), resetting to defaults")
            self._settings = self.DEFAULT_SETTINGS.copy()
            self.save(self._settings)
        
        return self._settings
    
    def save(self, settings: Dict[str, Any] = None) -> bool:
        """
        Save settings to JSON file.
        
        Args:
            settings: Optional settings dict. If None, saves current settings.
            
        Returns:
            True if save successful, False otherwise.
        """
        if settings is not None:
            self._settings = settings
        
        try:
            # Ensure parent directory exists
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self._settings, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Config saved to {self.config_path}")
            return True
            
        except IOError as e:
            logger.error(f"Failed to save config: {e}")
            return False
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value.
        
        Args:
            key: The setting key to retrieve.
            default: Default value if key not found.
            
        Returns:
            The setting value or default.
        """
        return self._settings.get(key, default)
    
    def set(self, key: str, value: Any, auto_save: bool = True) -> None:
        """
        Set a configuration value.
        
        Args:
            key: The setting key to update.
            value: The new value.
            auto_save: If True, immediately persist to disk.
        """
        self._settings[key] = value
        if auto_save:
            self.save()
    
    @property
    def settings(self) -> Dict[str, Any]:
        """Return a copy of current settings."""
        return self._settings.copy()
