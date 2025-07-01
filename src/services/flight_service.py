from typing import Optional
from ..config.settings import Settings, get_config_warning
from ..flight.data_fetcher import FlightDataFetcher
from ..flight.data_parser import FlightDataParser
from ..flight.models import FlightData


class FlightService:
    def __init__(self, settings: Optional[Settings] = None):
        self.settings = settings or Settings()
        self.fetcher = FlightDataFetcher(self.settings)
        self.parser = FlightDataParser(self.settings)
    
    def get_flight_data(
        self,
        lat: Optional[float] = None,
        lon: Optional[float] = None,
        radius: Optional[int] = None,
        show_warning: bool = True
    ) -> Optional[FlightData]:
        # Show config warning if requested
        if show_warning:
            warning = get_config_warning()
            if warning:
                print(f"⚠️  {warning}")
        
        # Use provided parameters or fall back to settings
        search_lat = lat if lat is not None else self.settings.latitude
        search_lon = lon if lon is not None else self.settings.longitude
        search_radius = radius if radius is not None else self.settings.radius
        
        print(f"🔍 Searching for aircraft near {search_lat}, {search_lon}")
        print(f"   Search radius: {search_radius} nautical miles")
        
        # Fetch raw data
        raw_data = self.fetcher.get_closest_flights(search_lat, search_lon, search_radius)
        if not raw_data:
            return None
        
        # Parse into structured data
        flight_data = self.parser.parse_api_response(
            raw_data, search_lat, search_lon, search_radius
        )
        
        if flight_data:
            print(f"✅ Found {len(flight_data.aircraft)} aircraft")
            if flight_data.primary_aircraft:
                primary = flight_data.primary_aircraft
                print(f"   Primary: {primary.flight_number} ({primary.model})")
                print(f"   Speed: {primary.ground_speed} knots")
        else:
            print("❌ No aircraft found in the specified area")
        
        return flight_data
    
    def print_flight_info(
        self,
        flight_data: Optional[FlightData] = None,
        show_raw: bool = False,
        **kwargs
    ) -> None:
        if flight_data is None:
            flight_data = self.get_flight_data(**kwargs)
        
        if flight_data:
            self.parser.print_flight_info(flight_data, show_raw)
        else:
            print("No flight data available.")