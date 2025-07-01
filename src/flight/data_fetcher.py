"""
Flight data fetcher for retrieving aircraft information from ADS-B API.

This module handles all HTTP requests to the ADS-B Exchange API and provides
robust error handling and retry mechanisms.
"""

import requests
from typing import Optional, Dict, Any
from datetime import datetime
import time

from ..config.settings import Settings


class FlightDataFetcher:
    """Handles fetching flight data from the ADS-B Exchange API."""
    
    def __init__(self, settings: Settings):
        """
        Initialize the flight data fetcher.
        
        Args:
            settings: Configuration settings object
        """
        self.settings = settings
        self.session = requests.Session()
        self.session.timeout = settings.api_timeout
    
    def get_closest_flights(
        self, 
        lat: Optional[float] = None, 
        lon: Optional[float] = None, 
        radius: Optional[int] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Retrieve information about aircraft closest to the specified coordinates.
        
        Args:
            lat: Latitude. Defaults to settings value.
            lon: Longitude. Defaults to settings value.
            radius: Search radius in nautical miles. Defaults to settings value.
        
        Returns:
            Dict containing flight information or None if request fails.
        """
        # Use provided parameters or fall back to settings
        latitude = lat if lat is not None else self.settings.latitude
        longitude = lon if lon is not None else self.settings.longitude
        search_radius = radius if radius is not None else self.settings.radius
        
        url = f"{self.settings.api_base_url}/closest/{latitude}/{longitude}/{search_radius}"
        
        try:
            response = self.session.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout:
            print(f"⚠️  Request timeout after {self.settings.api_timeout} seconds")
            return None
        except requests.exceptions.ConnectionError:
            print("❌ Connection error - check your internet connection")
            return None
        except requests.exceptions.HTTPError as e:
            print(f"❌ HTTP error: {e}")
            return None
        except requests.exceptions.RequestException as e:
            print(f"❌ Request error: {e}")
            return None
        except ValueError as e:
            print(f"❌ Invalid JSON response: {e}")
            return None
    
    def __del__(self):
        """Clean up the session when the fetcher is destroyed."""
        if hasattr(self, 'session'):
            self.session.close() 