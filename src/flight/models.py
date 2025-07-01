"""
Data models for flight information.

This module defines the data structures used throughout the flight tracking system.
"""

from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from datetime import datetime


@dataclass
class Aircraft:
    """Represents a single aircraft with its flight information."""
    
    flight_number: str
    model: str
    registration: str
    ground_speed: float
    altitude: Optional[str] = None
    hex_code: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    heading: Optional[float] = None
    vertical_rate: Optional[float] = None
    squawk: Optional[str] = None
    
    @classmethod
    def from_api_data(cls, data: Dict[str, Any]) -> 'Aircraft':
        """Create Aircraft instance from API response data."""
        # Handle flight number - use hex code if flight is empty/None
        flight = data.get('flight', '').strip() if data.get('flight') else ''
        if not flight:
            hex_code = data.get('hex', 'XXXX')
            flight = f"AC{hex_code[-4:]}" if hex_code else "UNKNOWN"
        
        return cls(
            flight_number=flight,
            model=data.get('t', 'Unknown'),
            registration=data.get('r', 'Unknown'),
            ground_speed=float(data.get('gs', 0)) if data.get('gs') is not None else 0.0,
            altitude=data.get('alt_baro'),
            hex_code=data.get('hex'),
            latitude=data.get('lat'),
            longitude=data.get('lon'),
            heading=data.get('track'),
            vertical_rate=data.get('baro_rate'),
            squawk=data.get('squawk')
        )
    
    def to_display_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format suitable for display components."""
        return {
            "flightNumber": self.flight_number,
            "model": self.model,
            "registration": self.registration,
            "groundSpeed": self.ground_speed,
            "altitude": self.altitude or "Unknown"
        }
    
    def format_info(self) -> str:
        """Format aircraft information as a readable string."""
        return (
            f"Callsign: {self.flight_number}, "
            f"Altitude: {self.altitude or 'Unknown'} ft, "
            f"Speed: {self.ground_speed} knots, "
            f"Model: {self.model}, "
            f"Registration: {self.registration}"
        )


@dataclass
class FlightData:
    """Represents flight data response with multiple aircraft."""
    
    aircraft: List[Aircraft]
    timestamp: datetime
    total_count: int
    search_latitude: float
    search_longitude: float
    search_radius: int
    
    @property
    def primary_aircraft(self) -> Optional[Aircraft]:
        """Get the primary (first) aircraft for display."""
        return self.aircraft[0] if self.aircraft else None
    
    def to_json_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format for JSON serialization."""
        primary = self.primary_aircraft
        if not primary:
            return {
                "error": "No aircraft data available",
                "flightNumber": "NO DATA",
                "model": "Unknown",
                "registration": "Unknown",
                "groundSpeed": 0,
                "altitude": "Unknown",
                "lastUpdated": self.timestamp.isoformat(),
                "totalAircraft": 0
            }
        
        data = primary.to_display_dict()
        data.update({
            "lastUpdated": self.timestamp.isoformat(),
            "totalAircraft": self.total_count
        })
        return data 