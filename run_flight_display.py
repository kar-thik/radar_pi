#!/usr/bin/env python3
"""
Simple runner script for the Integrated Flight Display Generator
"""

import sys
import os

# Add the current directory to Python path so we can import our modules
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Import and run the main application
from integrated_flight_display import main
import asyncio

if __name__ == "__main__":
    print("🎯 Starting Radar Pi Flight Display System")
    print("=" * 50)
    print("This will:")
    print("1. Fetch live flight data from nearby aircraft")
    print("2. Generate a visual display image")
    print("3. Save the result as 'curr_flight.png'")
    print()
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1) 