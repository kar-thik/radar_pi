# Radar Pi - Flight Tracking Module

A Python module for tracking nearby aircraft using ADS-B data from the ADS-B Exchange API.

## Setup

1. **Create configuration file**: Copy `config.py.example` to `config.py` and update with your desired coordinates:
   ```bash
   cp config.py.example config.py
   ```

2. **Edit coordinates**: Open `config.py` and set your latitude, longitude, and search radius:
   ```python
   LATITUDE = 38.89580240857114    # Your latitude
   LONGITUDE = -77.09308316546287  # Your longitude
   RADIUS = 10                     # Search radius in nautical miles
   ```

3. **Install dependencies**:
   ```bash
   pip install requests
   ```

## Usage

### As a standalone script:
```bash
python get_flights.py
```

### As a module in your code:
```python
import get_flights

# Use default config values
flight_data = get_flights.get_closest_flights()
get_flights.print_flight_info(flight_data)

# Or specify custom coordinates
flight_data = get_flights.get_closest_flights(lat=40.7128, lon=-74.0060, radius=15)
```

## Features

- **Configurable location**: Set your coordinates in a separate config file
- **Modular design**: Can be used as both a script and importable module  
- **Error handling**: Graceful handling of API errors and missing config
- **Formatted output**: Clean display of aircraft information
- **Type hints**: Full type annotations for better code clarity

## Security

The `config.py` file is automatically ignored by git to prevent accidentally committing location data. Use `config.py.example` as a template for your configuration.