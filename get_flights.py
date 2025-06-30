"""
Flight tracking module using ADS-B data.

This module provides functionality to retrieve nearby aircraft information
using the ADS-B Exchange API.
"""

import requests
from typing import Dict, Any, Optional, List

# Configuration handling
try:
    from config import LATITUDE, LONGITUDE, RADIUS
except ImportError:
    # Default values if config.py is not available
    LATITUDE = 38.89580240857114
    LONGITUDE = -77.09308316546287
    RADIUS = 10
    _CONFIG_WARNING = "config.py not found. Using default coordinates (Washington DC area)."
else:
    _CONFIG_WARNING = None


def get_config_warning() -> Optional[str]:
    """
    Get the configuration warning message if config.py was not found.
    
    Returns:
        Optional[str]: Warning message or None if config was loaded successfully.
    """
    return _CONFIG_WARNING


def get_closest_flights(lat: float = None, lon: float = None, radius: int = None) -> Optional[Dict[str, Any]]:
    """
    Retrieve information about aircraft closest to the specified coordinates.
    
    Args:
        lat (float, optional): Latitude. Defaults to config value.
        lon (float, optional): Longitude. Defaults to config value.
        radius (int, optional): Search radius in nautical miles. Defaults to config value.
    
    Returns:
        Dict[str, Any]: JSON response from the API containing flight information,
                       or None if the request fails.
    """
    # Use provided parameters or fall back to config values
    latitude = lat if lat is not None else LATITUDE
    longitude = lon if lon is not None else LONGITUDE
    search_radius = radius if radius is not None else RADIUS
    
    url = f"https://api.adsb.lol/v2/closest/{latitude}/{longitude}/{search_radius}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching flight data: {e}")
        return None


def parse_aircraft_data(flight_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Parse and extract aircraft data from the API response.
    
    Args:
        flight_data (Dict[str, Any]): Raw flight data from the API response.
    
    Returns:
        List[Dict[str, Any]]: List of aircraft data dictionaries.
    """
    if not flight_data:
        return []
    
    # Handle different possible response structures
    if isinstance(flight_data, dict):
        if 'aircraft' in flight_data:
            aircraft_list = flight_data['aircraft']
        elif 'ac' in flight_data:
            aircraft_list = flight_data['ac']
        else:
            return []
    else:
        aircraft_list = flight_data
    
    return aircraft_list if isinstance(aircraft_list, list) else []


def format_aircraft_info(aircraft: Dict[str, Any]) -> str:
    """
    Format aircraft information into a readable string.
    
    Args:
        aircraft (Dict[str, Any]): Aircraft data dictionary.
    
    Returns:
        str: Formatted aircraft information string.
    """
    callsign = aircraft.get('flight', 'Unknown')
    altitude = aircraft.get('alt_baro', 'Unknown')
    speed = aircraft.get('gs', 'Unknown')
    model = aircraft.get('t', 'Unknown')
    registration = aircraft.get('r', 'Unknown')
    
    return f"Callsign: {callsign}, Altitude: {altitude} ft, Speed: {speed} knots, Model: {model}, Registration: {registration}"


def print_flight_info(flight_data: Dict[str, Any], show_raw: bool = False, max_aircraft: int = 10) -> None:
    """
    Print formatted flight information.
    
    Args:
        flight_data (Dict[str, Any]): Flight data from the API response.
        show_raw (bool, optional): Whether to show raw JSON data. Defaults to False.
        max_aircraft (int, optional): Maximum number of aircraft to display. Defaults to 10.
    """
    if not flight_data:
        print("No flight data available.")
        return
    
    print("Nearby Aircraft:")
    print("-" * 50)
    
    if show_raw:
        print("Raw JSON data:")
        print(flight_data)
        print("-" * 50)
    
    aircraft_list = parse_aircraft_data(flight_data)
    
    if not aircraft_list:
        print("No aircraft found in the specified area.")
        return
    
    for aircraft in aircraft_list[:max_aircraft]:
        print(format_aircraft_info(aircraft))


def main():
    """Main function for standalone script execution."""
    # Show config warning only when running as standalone script
    if _CONFIG_WARNING:
        print(f"Warning: {_CONFIG_WARNING}")
    
    print(f"Searching for aircraft near coordinates: {LATITUDE}, {LONGITUDE}")
    print(f"Search radius: {RADIUS} nautical miles")
    print()
    
    flight_data = get_closest_flights()
    print_flight_info(flight_data)


if __name__ == "__main__":
    main()
