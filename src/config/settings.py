"""
Configuration settings for the Radar Pi system.

This module handles all configuration including coordinates, API settings,
and display parameters.
"""

import os
from typing import Optional
from dataclasses import dataclass


@dataclass
class Settings:
    """Configuration settings for the Radar Pi system."""
    
    # Default coordinates (Washington DC area)
    latitude: float = 38.89580240857114
    longitude: float = -77.09308316546287
    radius: int = 10  # nautical miles
    
    # Server settings
    server_port: int = 3000
    server_timeout: int = 140  # seconds
    
    # Display settings
    display_width: int = 800
    display_height: int = 480
    max_aircraft_display: int = 10
    
    # File paths
    flight_data_file: str = "flight_data.json"
    output_image_file: str = "curr_flight.png"
    
    # API settings
    api_base_url: str = "https://api.adsb.lol/v2"
    api_timeout: int = 10  # seconds


def get_settings() -> Settings:
    """
    Get configuration settings.
    
    Attempts to load from config.py file first, then falls back to defaults.
    Environment variables can override specific settings.
    
    Returns:
        Settings: Configured settings object
    """
    settings = Settings()
    
    # Try to load from config.py
    try:
        import config
        settings.latitude = getattr(config, 'LATITUDE', settings.latitude)
        settings.longitude = getattr(config, 'LONGITUDE', settings.longitude)
        settings.radius = getattr(config, 'RADIUS', settings.radius)
    except ImportError:
        print("Warning: config.py not found. Using default coordinates (Washington DC area).")
    
    # Override with environment variables if available
    settings.latitude = float(os.getenv('RADAR_LATITUDE', settings.latitude))
    settings.longitude = float(os.getenv('RADAR_LONGITUDE', settings.longitude))
    settings.radius = int(os.getenv('RADAR_RADIUS', settings.radius))
    settings.server_port = int(os.getenv('RADAR_PORT', settings.server_port))
    
    return settings


def get_config_warning() -> Optional[str]:
    """
    Get configuration warning message if config.py was not found.
    
    Returns:
        Optional[str]: Warning message or None if config was loaded successfully.
    """
    try:
        import config
        return None
    except ImportError:
        return "config.py not found. Using default coordinates (Washington DC area)." 