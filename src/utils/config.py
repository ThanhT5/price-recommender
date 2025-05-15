"""
Configuration utilities for the Handmade Goods Pricing Assistant
"""

import json
import os
from pathlib import Path

# Default configuration values
DEFAULT_CONFIG = {
    "pricing": {
        "uniqueness_weight": 0.05,
        "demand_weight": 0.04,
        "economy_modifier": 0.85,
        "premium_modifier": 1.25,
        "suggested_price_multiplier": 2.0
    },
    "ui": {
        "theme": "default",
        "currency_symbol": "$",
        "decimal_places": 2
    },
    "defaults": {
        "material_cost": 10.0,
        "hours_worked": 2.0,
        "labor_rate": 15.0,
        "uniqueness": 5,
        "demand": 5,
        "selling_price": 0.0  # Default to 0 (automatic calculation)
    }
}

class Config:
    """Configuration manager for the application"""
    
    def __init__(self, config_dir=None):
        """
        Initialize the configuration manager
        
        Args:
            config_dir: Directory to store configuration files (default: 'config')
        """
        # Set up the configuration directory
        if config_dir is None:
            # Use the config directory relative to the project root
            self.config_dir = Path(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))) / "config"
        else:
            self.config_dir = Path(config_dir)
        
        # Create the config directory if it doesn't exist
        self.config_dir.mkdir(exist_ok=True)
        
        # Configuration file path
        self.config_file = self.config_dir / "settings.json"
        
        # Load configuration (or create default if it doesn't exist)
        self.config = self._load_config()
    
    def _load_config(self):
        """
        Load configuration from file or create default
        
        Returns:
            Dictionary containing configuration values
        """
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    
                # Merge with defaults in case new settings were added
                self._merge_with_defaults(config)
                return config
            except (json.JSONDecodeError, IOError):
                # If there's an error loading, use defaults
                return DEFAULT_CONFIG.copy()
        else:
            # Create a new config file with default values
            config = DEFAULT_CONFIG.copy()
            self._save_config(config)
            return config
    
    def _save_config(self, config):
        """
        Save configuration to file
        
        Args:
            config: Configuration dictionary to save
        """
        try:
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=4)
        except IOError:
            # Just log the error for now
            print(f"Error: Could not save configuration to {self.config_file}")
    
    def _merge_with_defaults(self, config):
        """
        Ensure all default keys exist in the config
        
        Args:
            config: Configuration dictionary to update
        """
        for section, values in DEFAULT_CONFIG.items():
            if section not in config:
                config[section] = values
            else:
                for key, value in values.items():
                    if key not in config[section]:
                        config[section][key] = value
    
    def get(self, section, key, default=None):
        """
        Get a configuration value
        
        Args:
            section: Configuration section
            key: Configuration key
            default: Default value if not found
        
        Returns:
            Configuration value
        """
        try:
            return self.config[section][key]
        except KeyError:
            return default
    
    def set(self, section, key, value):
        """
        Set a configuration value
        
        Args:
            section: Configuration section
            key: Configuration key
            value: Value to set
        """
        # Ensure section exists
        if section not in self.config:
            self.config[section] = {}
        
        # Set the value
        self.config[section][key] = value
        
        # Save the configuration
        self._save_config(self.config)
    
    def get_pricing_settings(self):
        """
        Get all pricing-related settings
        
        Returns:
            Dictionary of pricing settings
        """
        return self.config["pricing"].copy()
    
    def get_ui_settings(self):
        """
        Get all UI-related settings
        
        Returns:
            Dictionary of UI settings
        """
        return self.config["ui"].copy()
    
    def get_default_values(self):
        """
        Get default input values
        
        Returns:
            Dictionary of default values
        """
        return self.config["defaults"].copy()
    
    def save(self):
        """Save the current configuration to file"""
        self._save_config(self.config) 