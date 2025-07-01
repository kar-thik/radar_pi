#!/usr/bin/env python3
"""
DEPRECATED: Legacy runner script.

This script has been refactored. Please use scripts/radar_display.py instead.
For backwards compatibility, this now uses the new service architecture.
"""

import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from src.services.radar_service import RadarService

if __name__ == "__main__":
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
        print(f"\n❌ Error: {e}")
        sys.exit(1) 