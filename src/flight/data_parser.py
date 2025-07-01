"""
Flight data parser for processing raw API responses.

This module handles parsing and validation of flight data from various
API response formats.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime

from .models import Aircraft, FlightData
from ..config.settings import Settings


class FlightDataParser:
    """Handles parsing and validation of flight data from API responses."""
    
    def __init__(self, settings: Settings):
        """
        Initialize the flight data parser.
        
        Args:
            settings: Configuration settings object
        """
        self.settings = settings
    
    def parse_api_response(
        self, 
        response_data: Dict[str, Any],
        search_lat: float,
        search_lon: float,
        search_radius: int
    ) -> Optional[FlightData]:
        """
        Parse API response and return structured flight data.
        
        Args:
            response_data: Raw API response data
            search_lat: Search latitude used
            search_lon: Search longitude used  
            search_radius: Search radius used
        
        Returns:
            FlightData object or None if parsing fails
        """
        if not response_data:
            return None
        
        aircraft_list = self._extract_aircraft_list(response_data)
        if not aircraft_list:
            return None
        
        # Parse aircraft data
        aircraft = []
        for aircraft_data in aircraft_list[:self.settings.max_aircraft_display]:
            try:
                aircraft.append(Aircraft.from_api_data(aircraft_data))
            except Exception as e:
                print(f"⚠️  Failed to parse aircraft data: {e}")
                continue
        
        if not aircraft:
            return None
        
        return FlightData(
            aircraft=aircraft,
            timestamp=datetime.now(),
            total_count=len(aircraft_list),
            search_latitude=search_lat,
            search_longitude=search_lon,
            search_radius=search_radius
        )
    
    def _extract_aircraft_list(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Extract aircraft list from API response, handling different formats.
        
        Args:
            data: API response data
        
        Returns:
            List of aircraft data dictionaries
        """
        if not isinstance(data, dict):
            return []
        
        # Handle different possible response structures
        if 'aircraft' in data:
            aircraft_list = data['aircraft']
        elif 'ac' in data:
            aircraft_list = data['ac']
        else:
            return []
        
        return aircraft_list if isinstance(aircraft_list, list) else []
    
    def format_aircraft_info(self, aircraft: Aircraft) -> str:
        """
        Format aircraft information into a readable string.
        
        Args:
            aircraft: Aircraft object to format
        
        Returns:
            Formatted aircraft information string
        """
        return aircraft.format_info()
    
    def print_flight_info(
        self, 
        flight_data: FlightData, 
        show_raw: bool = False
    ) -> None:
        """
        Print formatted flight information to console.
        
        Args:
            flight_data: FlightData object to display
            show_raw: Whether to show raw data
        """
        print("✈️  Nearby Aircraft:")
        print("-" * 50)
        
        if show_raw:
            print("Raw data available - use flight_data.aircraft for details")
            print("-" * 50)
        
        if not flight_data.aircraft:
            print("No aircraft found in the specified area.")
            return
        
        for aircraft in flight_data.aircraft:
            print(self.format_aircraft_info(aircraft))
        
        print(f"\nTotal aircraft nearby: {flight_data.total_count}")
        print(f"Search area: {flight_data.search_latitude}, {flight_data.search_longitude} "
              f"(radius: {flight_data.search_radius} nm)")
        print(f"Last updated: {flight_data.timestamp.strftime('%Y-%m-%d %H:%M:%S')}") 