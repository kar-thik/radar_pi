#!/usr/bin/env python3
"""
DEPRECATED: Legacy flight tracking module.

This module has been refactored into the new modular structure.
Please use scripts/flight_tracker.py instead.

For backwards compatibility, this script now uses the new modules.
"""

import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from src.services.flight_service import FlightService
from src.config.settings import get_settings, get_config_warning

# Keep original function signatures for backwards compatibility
def get_closest_flights(lat=None, lon=None, radius=None):
    """Legacy function - use FlightService instead."""
    service = FlightService(get_settings())
    flight_data = service.get_flight_data(lat, lon, radius, show_warning=False)
    return flight_data.to_json_dict() if flight_data else None


def parse_aircraft_data(flight_data):
    """Legacy function - kept for backwards compatibility."""
    if not flight_data or not isinstance(flight_data, dict):
        return []
    
    if 'aircraft' in flight_data:
        return flight_data['aircraft']
    elif 'ac' in flight_data:
        return flight_data['ac']
    else:
        return []


def format_aircraft_info(aircraft):
    """Legacy function - kept for backwards compatibility."""
    callsign = aircraft.get('flight', 'Unknown')
    altitude = aircraft.get('alt_baro', 'Unknown')
    speed = aircraft.get('gs', 'Unknown')
    model = aircraft.get('t', 'Unknown')
    registration = aircraft.get('r', 'Unknown')
    
    return f"Callsign: {callsign}, Altitude: {altitude} ft, Speed: {speed} knots, Model: {model}, Registration: {registration}"


def print_flight_info(flight_data, show_raw=False, max_aircraft=10):
    """Legacy function - kept for backwards compatibility."""
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
    """Main function - now uses new service architecture."""
    print("⚠️  This script is deprecated. Please use 'scripts/flight_tracker.py' instead.")
    print("   Running with new architecture for backwards compatibility...\n")
    
    try:
        service = FlightService(get_settings())
        flight_data = service.get_flight_data()
        service.print_flight_info(flight_data)
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
