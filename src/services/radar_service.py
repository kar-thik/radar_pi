"""
Main radar service that orchestrates the entire flight tracking system.

This service combines flight data fetching with display image generation
to provide a complete radar tracking solution.
"""

import asyncio
from typing import Optional

from ..config.settings import Settings, get_settings
from ..flight.models import FlightData
from ..display.image_generator import ImageGenerator
from .flight_service import FlightService


class RadarService:
    """Main service that orchestrates the radar tracking system."""
    
    def __init__(self, settings: Optional[Settings] = None):
        """
        Initialize the radar service.
        
        Args:
            settings: Configuration settings. If None, will load from config.
        """
        self.settings = settings or get_settings()
        self.flight_service = FlightService(self.settings)
        self.image_generator = ImageGenerator(self.settings)
    
    def get_flight_data(self, **kwargs) -> Optional[FlightData]:
        """
        Get flight data using the flight service.
        
        Args:
            **kwargs: Arguments passed to flight service.
        
        Returns:
            FlightData object or None if no data available.
        """
        return self.flight_service.get_flight_data(**kwargs)
    
    async def generate_display_async(
        self,
        flight_data: Optional[FlightData] = None,
        **kwargs
    ) -> bool:
        """
        Generate flight display image asynchronously.
        
        Args:
            flight_data: Flight data to display. If None, will fetch new data.
            **kwargs: Additional arguments passed to get_flight_data.
        
        Returns:
            bool: True if image was generated successfully, False otherwise.
        """
        # Get flight data if not provided
        if flight_data is None:
            flight_data = self.flight_service.get_flight_data(**kwargs)
        
        if not flight_data:
            print("❌ No flight data available for display generation")
            return False
        
        # Generate image
        return await self.image_generator.generate_image(flight_data)
    
    def generate_display(
        self,
        flight_data: Optional[FlightData] = None,
        **kwargs
    ) -> bool:
        """
        Generate flight display image synchronously.
        
        Args:
            flight_data: Flight data to display. If None, will fetch new data.
            **kwargs: Additional arguments passed to get_flight_data.
        
        Returns:
            bool: True if image was generated successfully, False otherwise.
        """
        return asyncio.run(self.generate_display_async(flight_data, **kwargs))
    
    def run_full_cycle(self, **kwargs) -> bool:
        """
        Run a complete radar cycle: fetch data and generate display.
        
        Args:
            **kwargs: Additional arguments passed to get_flight_data.
        
        Returns:
            bool: True if successful, False otherwise.
        """
        print("🎯 Starting Radar Pi Flight Display System")
        print("=" * 50)
        print("This will:")
        print("1. Fetch live flight data from nearby aircraft")
        print("2. Generate a visual display image")
        print(f"3. Save the result as '{self.settings.output_image_file}'")
        print()
        
        try:
            # Get flight data
            flight_data = self.flight_service.get_flight_data(**kwargs)
            if not flight_data:
                return False
            
            # Generate display
            success = self.generate_display(flight_data)
            
            if success:
                print("\n🎉 Flight display generated successfully!")
                print(f"📁 Output file: {self.settings.output_image_file}")
            else:
                print("\n💥 Failed to generate flight display")
            
            return success
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            return False
        except Exception as e:
            print(f"\n❌ Error: {e}")
            return False 