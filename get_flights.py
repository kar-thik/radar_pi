"""
Flight tracking module using ADS-B data.

This module provides functionality to retrieve nearby aircraft information
using the ADS-B Exchange API.
"""

import requests
from typing import Dict, Any, Optional

try:
    from config import LATITUDE, LONGITUDE, RADIUS
except ImportError:
    # Default values if config.py is not available
    LATITUDE = 38.89580240857114
    LONGITUDE = -77.09308316546287
    RADIUS = 10
    print("Warning: config.py not found. Using default coordinates (Washington DC area).")


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


def print_flight_info(flight_data: Dict[str, Any]) -> None:
    """
    Print formatted flight information.
    
    Args:
        flight_data (Dict[str, Any]): Flight data from the API response.
    """
    if not flight_data:
        print("No flight data available.")
        return
    
    print("Nearby Aircraft:")
    print("-" * 50)
    
    # Handle different possible response structures
    if isinstance(flight_data, dict):
        if 'aircraft' in flight_data:
            aircraft_list = flight_data['aircraft']
        elif 'ac' in flight_data:
            aircraft_list = flight_data['ac']
        else:
            print(flight_data)
            return
    else:
        aircraft_list = flight_data
    
    if not aircraft_list:
        print("No aircraft found in the specified area.")
        return
    
    for aircraft in aircraft_list[:10]:  # Show first 10 aircraft
        callsign = aircraft.get('flight', 'Unknown')
        altitude = aircraft.get('alt_baro', 'Unknown')
        speed = aircraft.get('gs', 'Unknown')
        print(f"Callsign: {callsign}, Altitude: {altitude} ft, Speed: {speed} knots")


def main():
    """Main function for standalone script execution."""
    print(f"Searching for aircraft near coordinates: {LATITUDE}, {LONGITUDE}")
    print(f"Search radius: {RADIUS} nautical miles")
    print()
    
    flight_data = get_closest_flights()
    print_flight_info(flight_data)


if __name__ == "__main__":
    main()
