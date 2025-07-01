import asyncio
from typing import Optional

from ..config.settings import Settings, get_settings
from ..flight.models import FlightData
from ..display.html_image_generator import HTMLImageGenerator
from .flight_service import FlightService


class RadarService:
    def __init__(self, settings: Optional[Settings] = None):
        self.settings = settings or get_settings()
        self.flight_service = FlightService(self.settings)
        self.image_generator = HTMLImageGenerator(self.settings)

    def get_flight_data(self, **kwargs) -> Optional[FlightData]:
        return self.flight_service.get_flight_data(**kwargs)

    async def generate_display_async(
        self, flight_data: Optional[FlightData] = None, **kwargs
    ) -> bool:
        if flight_data is None:
            flight_data = self.flight_service.get_flight_data(**kwargs)

        if not flight_data:
            print("❌ No flight data available for display generation")
            return False

        return await self.image_generator.generate_image(flight_data)

    def generate_display(
        self, flight_data: Optional[FlightData] = None, **kwargs
    ) -> bool:
        return asyncio.run(self.generate_display_async(flight_data, **kwargs))

    def run_full_cycle(self, **kwargs) -> bool:
        print("🎯 Starting Radar Pi Flight Display System")
        print("=" * 50)
        print("This will:")
        print("1. Fetch live flight data from nearby aircraft")
        print("2. Generate a visual display image")
        print(f"3. Save the result as '{self.settings.output_image_file}'")
        print()

        try:
            flight_data = self.flight_service.get_flight_data(**kwargs)
            if not flight_data:
                return False

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