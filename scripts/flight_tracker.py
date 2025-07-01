#!/usr/bin/env python3
import sys
import os
import argparse

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.services.flight_service import FlightService
from src.config.settings import get_settings


def main():
    parser = argparse.ArgumentParser(
        description="Fetch and display nearby aircraft information",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                           # Use default coordinates
  %(prog)s --lat 40.7128 --lon -74.0060  # New York City
  %(prog)s --radius 20               # 20 nautical mile radius
  %(prog)s --raw                     # Show raw data
        """
    )
    
    parser.add_argument(
        '--lat', '--latitude',
        type=float,
        help='Latitude for search center'
    )
    parser.add_argument(
        '--lon', '--longitude',
        type=float,
        help='Longitude for search center'
    )
    parser.add_argument(
        '--radius',
        type=int,
        help='Search radius in nautical miles'
    )
    parser.add_argument(
        '--raw',
        action='store_true',
        help='Show raw flight data'
    )
    parser.add_argument(
        '--quiet',
        action='store_true',
        help='Suppress configuration warnings'
    )
    
    args = parser.parse_args()
    
    try:
        # Initialize service
        settings = get_settings()
        service = FlightService(settings)
        
        # Get flight data
        flight_data = service.get_flight_data(
            lat=args.lat,
            lon=args.lon,
            radius=args.radius,
            show_warning=not args.quiet
        )
        
        # Print results
        service.print_flight_info(flight_data, show_raw=args.raw)
        
        if flight_data:
            sys.exit(0)
        else:
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 