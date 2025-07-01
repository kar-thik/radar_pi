import requests
from typing import Optional, Dict, Any
from datetime import datetime
import time

from ..config.settings import Settings


class FlightDataFetcher:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.session = requests.Session()
        self.session.timeout = settings.api_timeout
    
    def get_closest_flights(
        self, 
        lat: Optional[float] = None, 
        lon: Optional[float] = None, 
        radius: Optional[int] = None
    ) -> Optional[Dict[str, Any]]:
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
        if hasattr(self, 'session'):
            self.session.close()