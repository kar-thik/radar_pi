# Radar Pi - Flight Tracking Display System

A modern, modular flight tracking system that fetches live ADS-B data and generates visual displays for radar monitoring. Perfect for aviation enthusiasts and Raspberry Pi projects.

## ✨ Features

- **Live Flight Data**: Fetches real-time aircraft information from ADS-B Exchange
- **Visual Display**: Generates beautiful flight information displays
- **Modular Architecture**: Clean, well-organized codebase with separate concerns
- **Multiple Interfaces**: Command-line tools and web-based displays
- **Configurable**: Easy to customize coordinates, display settings, and more
- **Raspberry Pi Ready**: Optimized for e-ink displays and GPIO controls

## 🏗️ Architecture

The system is built with a clean modular architecture:

```
src/
├── config/          # Configuration management
├── flight/          # Flight data handling
│   ├── data_fetcher.py    # API communication
│   ├── data_parser.py     # Data processing
│   └── models.py          # Data structures
├── display/         # Display generation
│   ├── image_generator.py # Screenshot capture
│   └── server_manager.py  # Next.js server management
└── services/        # High-level services
    ├── flight_service.py  # Flight operations
    └── radar_service.py   # Complete radar system
```

## 🚀 Quick Start

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd radar_pi
   ```

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Node.js dependencies**:
   ```bash
   npm install
   ```

4. **Configure your location** (optional):
   ```bash
   cp config.py.example config.py
   # Edit config.py with your coordinates
   ```

### Usage

#### Command Line Interface

**Fetch flight data only**:
```bash
python scripts/flight_tracker.py
python scripts/flight_tracker.py --lat 40.7128 --lon -74.0060 --radius 20
```

**Generate complete radar display**:
```bash
python scripts/radar_display.py
python scripts/radar_display.py --output my_radar.png
```

#### Legacy Scripts (Backwards Compatible)

```bash
python get_flights.py              # Still works!
python run_flight_display.py       # Still works!
python generate_image.py           # Still works!
```

## ⚙️ Configuration

### Environment Variables

- `RADAR_LATITUDE`: Override default latitude
- `RADAR_LONGITUDE`: Override default longitude  
- `RADAR_RADIUS`: Override search radius (nautical miles)
- `RADAR_PORT`: Override Next.js server port (default: 3000)

### Configuration File

Create `config.py` from the example:

```python
# Coordinates for flight search
LATITUDE = 40.7128
LONGITUDE = -74.0060
RADIUS = 15  # nautical miles
```

## 🔧 API Reference

### Python Services

```python
from src.services.radar_service import RadarService
from src.services.flight_service import FlightService

# Get flight data
flight_service = FlightService()
flight_data = flight_service.get_flight_data(lat=40.7128, lon=-74.0060)

# Generate complete display
radar_service = RadarService()
success = radar_service.run_full_cycle()
```

### REST API

The Next.js application provides a REST API:

```
GET /api/flight-data
```

Returns:
```json
{
  "flightNumber": "UAL123",
  "model": "B737",
  "registration": "N12345",
  "groundSpeed": 250.5,
  "altitude": "35000",
  "lastUpdated": "2024-01-01T12:00:00Z",
  "totalAircraft": 5
}
```

## 🎨 Display Customization

The display system generates 800x480 pixel images perfect for e-ink displays. Customize the appearance by modifying:

- **Colors**: Edit `components/flight-info-display.tsx`
- **Layout**: Modify the React component structure
- **Size**: Adjust settings in `src/config/settings.py`

## 🏗️ Development

### Project Structure

```
radar_pi/
├── src/                 # New modular Python architecture
├── scripts/             # Command-line interfaces
├── app/                 # Next.js frontend
├── components/          # React components
├── types/               # TypeScript definitions
├── *.py                 # Legacy scripts (backwards compatible)
└── README.md           # This file
```

### Adding New Features

1. **Flight Data Processing**: Extend `src/flight/data_parser.py`
2. **Display Components**: Add React components in `components/`
3. **Configuration**: Update `src/config/settings.py`
4. **Services**: Create new services in `src/services/`

### Testing

```bash
# Test flight data fetching
python scripts/flight_tracker.py --data-only

# Test display generation
python scripts/radar_display.py --data-only

# Test with custom coordinates
python scripts/flight_tracker.py --lat 51.4700 --lon -0.4543 --radius 25
```

## 🔄 Migration Guide

### From Legacy Scripts

The old scripts still work but are deprecated:

| Old Script | New Script | Notes |
|------------|------------|-------|
| `get_flights.py` | `scripts/flight_tracker.py` | Enhanced CLI options |
| `run_flight_display.py` | `scripts/radar_display.py` | Better error handling |
| `generate_image.py` | `scripts/radar_display.py` | Integrated workflow |

### API Changes

Legacy functions are preserved for backwards compatibility:

```python
# Old way (still works)
from get_flights import get_closest_flights
data = get_closest_flights()

# New way (recommended)
from src.services.flight_service import FlightService
service = FlightService()
flight_data = service.get_flight_data()
```

## 🛠️ Hardware Integration

### Raspberry Pi Setup

For physical displays:

1. **Install system dependencies**:
   ```bash
   sudo apt update
   sudo apt install python3-pip nodejs npm
   ```

2. **Enable GPIO** (for e-ink displays):
   ```bash
   # Uncomment GPIO dependencies in requirements.txt
   pip install gpiod pillow inky
   ```

3. **Run on boot**:
   ```bash
   # Add to crontab
   @reboot cd /path/to/radar_pi && python scripts/radar_display.py
   ```

### E-ink Display Integration

The system works with Pimoroni Inky displays:

```python
# disp_curr_flight.py handles e-ink display
python disp_curr_flight.py
```

## 📊 Performance

- **API Response Time**: ~1-3 seconds
- **Display Generation**: ~10-15 seconds
- **Memory Usage**: ~100MB during generation
- **Storage**: Generated images are ~50KB

## 🐛 Troubleshooting

### Common Issues

**"No aircraft found"**:
- Check your coordinates and radius
- Verify internet connection
- Try a different location

**"npm not found"**:
- Install Node.js and npm
- Verify PATH configuration

**"Playwright browser not found"**:
- Run `python -m playwright install chromium`

**"Config warning"**:
- Create `config.py` from the example
- Or use command-line arguments

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Follow the existing code structure
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is open source. See the license file for details.

## 🙏 Acknowledgments

- **ADS-B Exchange** for providing free flight data
- **Pimoroni** for excellent e-ink display hardware
- **Next.js** and **React** for the web interface
- **Playwright** for reliable screenshot generation