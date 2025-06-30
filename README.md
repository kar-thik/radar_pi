# Radar Pi - Flight Tracking & Display Module

A comprehensive Python module for tracking nearby aircraft using ADS-B data from the ADS-B Exchange API and generating visual flight information displays.

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
   # For flight tracking only
   pip install requests
   
   # For flight tracking + image generation
   pip install -r requirements.txt
   ```

## Usage

### Flight Tracking

#### As a standalone script:
```bash
python get_flights.py
```

#### As a module in your code:
```python
import get_flights

# Use default config values
flight_data = get_flights.get_closest_flights()
get_flights.print_flight_info(flight_data)

# Or specify custom coordinates
flight_data = get_flights.get_closest_flights(lat=40.7128, lon=-74.0060, radius=15)
```

### Integrated Flight Display Generation (Recommended)

Generate a live flight information display with real-time data:

```bash
python run_flight_display.py
```

Or use the integrated module directly:
```bash
python integrated_flight_display.py
```

This will:
- Fetch live flight data from nearby aircraft using ADS-B Exchange API
- Create a Next.js project with dynamic React components
- Pass real flight data to the display components
- Start a local development server
- Render the live flight information display using headless Chrome
- Capture a screenshot as `curr_flight.png`
- Automatically clean up temporary files and server

### Static Flight Display Image Generation

Generate a visual 800×480px flight information display with static data:

```bash
python generate_image.py
```

This will:
- Create a Next.js project with React components
- Start a local development server
- Render the flight information display using headless Chrome
- Capture a screenshot as `image.png`
- Automatically clean up the server

The generated image includes:
- Flight number, aircraft model, and registration
- Ground speed in knots
- Number of nearby aircraft
- Data timestamp and current time
- Clean, modern light-themed interface
- Exact 800×480 pixel dimensions

## Features

### Flight Tracking
- **Configurable location**: Set your coordinates in a separate config file
- **Modular design**: Can be used as both a script and importable module  
- **Error handling**: Graceful handling of API errors and missing config
- **Formatted output**: Clean display of aircraft information
- **Type hints**: Full type annotations for better code clarity

### Flight Display Generation
- **Visual flight displays**: Generate 800×480px images of flight information
- **React components**: Modern, responsive UI built with Next.js and Tailwind CSS
- **Headless rendering**: Uses Playwright for automated screenshot capture
- **Light theme**: Clean, professional appearance optimized for displays
- **Automated workflow**: Complete setup, rendering, and cleanup process
- **Customizable data**: Easy to modify flight information through React props

## Project Structure

```
radar_pi/
├── get_flights.py                    # Flight tracking module
├── generate_image.py                 # Static image generation script
├── integrated_flight_display.py     # Live flight display generator
├── run_flight_display.py            # Simple runner script
├── config.py.example                # Configuration template
├── requirements.txt                  # Python dependencies
├── package.json                      # Node.js dependencies
├── app/                              # Next.js application
│   ├── layout.tsx                    # Root layout component
│   ├── page.tsx                      # Dynamic home page
│   ├── globals.css                   # Global styles
│   └── api/                          # API routes
│       └── flight-data/
│           └── route.ts              # Flight data API endpoint
└── components/                       # React components
    └── flight-info-display.tsx      # Enhanced flight display component
```

## Dependencies

### Python Dependencies
- `requests`: For API calls to ADS-B Exchange
- `playwright`: For headless browser automation
- `asyncio`: For asynchronous operations

### Node.js Dependencies
- `next`: React framework for the web interface
- `react`: User interface library
- `tailwindcss`: Utility-first CSS framework
- `lucide-react`: Icon library
- `typescript`: Type safety for JavaScript

## Security

The `config.py` file is automatically ignored by git to prevent accidentally committing location data. Use `config.py.example` as a template for your configuration.