#!/usr/bin/env python3
"""
DEPRECATED: Legacy image generator.

This script has been refactored into the new modular structure.
Please use scripts/radar_display.py instead.

For backwards compatibility, this script now uses the new modules.
"""

import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from services.radar_service import RadarService
from display.image_generator import ImageGenerator
from config.settings import get_settings

# Legacy class kept for backwards compatibility
class FlightDisplayImageGenerator:
    """Legacy class - use ImageGenerator from src.display instead."""
    
    def __init__(self, output_filename="image.png"):
        print("⚠️  FlightDisplayImageGenerator is deprecated.")
        print("   Use ImageGenerator from src.display.image_generator instead.")
        self.output_filename = output_filename
        self.settings = get_settings()
        self.settings.output_image_file = output_filename
        self.generator = ImageGenerator(self.settings)
    
    async def generate_image(self):
        """Legacy method - now uses new ImageGenerator."""
        # Create dummy flight data for the display
        from services.flight_service import FlightService
        flight_service = FlightService(self.settings)
        flight_data = flight_service.get_flight_data()
        
        if not flight_data:
            print("❌ No flight data available")
            return False
        
        return await self.generator.generate_image(flight_data)


def main():
    """Main function - now uses new service architecture."""
    print("⚠️  This script is deprecated. Please use 'scripts/radar_display.py' instead.")
    print("   Running with new architecture for backwards compatibility...\n")
    
    try:
        service = RadarService()
        success = service.run_full_cycle()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 