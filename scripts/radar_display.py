#!/usr/bin/env python3
"""
Radar Pi Flight Display System - Main Entry Point

This script runs the complete radar system: fetches flight data and generates
visual display images for e-ink displays.
"""

import sys
import os
import argparse
import asyncio

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.services.radar_service import RadarService
from src.config.settings import get_settings


def main():
    """Main entry point for radar display system."""
    parser = argparse.ArgumentParser(
        description="Generate flight display images for radar monitoring",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                           # Use default coordinates
  %(prog)s --lat 40.7128 --lon -74.0060  # New York City
  %(prog)s --radius 20               # 20 nautical mile radius
  %(prog)s --output flight.png       # Custom output filename
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
        '--output', '-o',
        help='Output image filename'
    )
    parser.add_argument(
        '--data-only',
        action='store_true',
        help='Only fetch and display data, do not generate image'
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
        if args.output:
            settings.output_image_file = args.output
            
        service = RadarService(settings)
        
        if args.data_only:
            # Just fetch and display data
            flight_data = service.get_flight_data(
                lat=args.lat,
                lon=args.lon,
                radius=args.radius,
                show_warning=not args.quiet
            )
            service.flight_service.print_flight_info(flight_data)
            sys.exit(0 if flight_data else 1)
        else:
            # Run full cycle
            success = service.run_full_cycle(
                lat=args.lat,
                lon=args.lon,
                radius=args.radius,
                show_warning=not args.quiet
            )
            sys.exit(0 if success else 1)
            
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 