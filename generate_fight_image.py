#!/usr/bin/env python3
"""
Integrated Flight Display Generator

This script fetches live flight data and generates a visual display image.
It combines the flight data fetching from get_flights.py with image generation
from generate_image.py to create a dynamic flight information display.
"""

import asyncio
import subprocess
import time
import os
import sys
import json
from pathlib import Path
from playwright.async_api import async_playwright
from get_flights import get_closest_flights, parse_aircraft_data, get_config_warning


class IntegratedFlightDisplayGenerator:
    def __init__(self, output_filename="curr_flight.png"):
        self.output_filename = output_filename
        self.server_process = None
        self.port = 3000
        self.url = f"http://localhost:{self.port}"
        self.flight_data_file = "flight_data.json"
        
    def fetch_flight_data(self):
        """Fetch flight data and save to JSON file for the Next.js app"""
        print("✈️  Fetching live flight data...")
        
        # Show config warning if needed
        config_warning = get_config_warning()
        if config_warning:
            print(f"⚠️  {config_warning}")
        
        # Get flight data
        flight_data = get_closest_flights()
        
        if not flight_data:
            print("❌ No flight data available")
            return False
        
        # Parse aircraft data
        aircraft_list = parse_aircraft_data(flight_data)
        
        if not aircraft_list:
            print("❌ No aircraft found in the specified area")
            return False
        
        # Get the first aircraft for display
        aircraft = aircraft_list[0]
        
        # Extract required fields for the display component
        display_data = {
            "flightNumber": aircraft.get('flight', 'Unknown').strip() or f"AC{aircraft.get('hex', 'XXXX')[-4:]}",
            "model": aircraft.get('t', 'Unknown'),
            "registration": aircraft.get('r', 'Unknown'),
            "groundSpeed": float(aircraft.get('gs', 0)) if aircraft.get('gs') else 0.0,
            "altitude": aircraft.get('alt_baro', 'Unknown'),
            "lastUpdated": time.strftime("%Y-%m-%d %H:%M:%S"),
            "totalAircraft": len(aircraft_list)
        }
        
        # Save to JSON file
        try:
            with open(self.flight_data_file, 'w') as f:
                json.dump(display_data, f, indent=2)
            
            print(f"✅ Flight data saved: {display_data['flightNumber']} ({display_data['model']})")
            print(f"   Speed: {display_data['groundSpeed']} knots")
            print(f"   Total aircraft nearby: {display_data['totalAircraft']}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to save flight data: {e}")
            return False
    
    def setup_nextjs_project(self):
        """Install npm dependencies if needed"""
        print("📦 Setting up Next.js project...")
        
        if not Path("node_modules").exists():
            print("Installing npm dependencies...")
            result = subprocess.run(["npm", "install"], capture_output=True, text=True)
            if result.returncode != 0:
                print(f"❌ Failed to install npm dependencies: {result.stderr}")
                return False
            print("✅ Dependencies installed successfully")
        else:
            print("✅ Dependencies already installed")
        
        return True
    
    def start_nextjs_server(self):
        """Start the Next.js development server"""
        print(f"🚀 Starting Next.js server on port {self.port}...")
        
        try:
            # Start the server in development mode
            self.server_process = subprocess.Popen(
                ["npm", "run", "dev"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Wait for server to start
            max_wait = 140  # seconds
            start_time = time.time()
            
            while time.time() - start_time < max_wait:
                try:
                    import requests
                    response = requests.get(self.url, timeout=1)
                    if response.status_code == 200:
                        print("✅ Next.js server is ready!")
                        return True
                except:
                    time.sleep(1)
                    continue
            
            print("❌ Server failed to start within timeout")
            return False
            
        except Exception as e:
            print(f"❌ Failed to start server: {e}")
            return False
    
    def stop_nextjs_server(self):
        """Stop the Next.js server"""
        if self.server_process:
            print("🛑 Stopping Next.js server...")
            self.server_process.terminate()
            try:
                self.server_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.server_process.kill()
            print("✅ Server stopped")
    
    async def capture_screenshot(self):
        """Capture a screenshot of the flight display"""
        print("📸 Capturing screenshot...")
        
        async with async_playwright() as p:
            # Launch browser in headless mode
            browser = await p.chromium.launch(headless=True)
            
            # Create a new page with exact viewport size
            page = await browser.new_page(viewport={'width': 800, 'height': 480})
            
            try:
                # Navigate to the page
                await page.goto(self.url, wait_until='networkidle')
                
                # Wait a bit for any animations to complete
                await page.wait_for_timeout(2000)
                
                # Find the flight display component and screenshot it
                flight_display = page.locator('div[class*="w-[800px] h-[480px]"]')
                
                # Take screenshot of just the component
                await flight_display.screenshot(path=self.output_filename)
                
                print(f"✅ Screenshot saved as {self.output_filename}")
                return True
                
            except Exception as e:
                print(f"❌ Failed to capture screenshot: {e}")
                return False
                
            finally:
                await browser.close()
    
    def cleanup_temp_files(self):
        """Clean up temporary files"""
        try:
            if os.path.exists(self.flight_data_file):
                os.remove(self.flight_data_file)
                print("🧹 Cleaned up temporary files")
        except Exception as e:
            print(f"⚠️  Failed to clean up temp files: {e}")
    
    async def generate_flight_display(self):
        """Main method to generate the flight display image"""
        try:
            # Fetch flight data
            if not self.fetch_flight_data():
                return False
            
            # Setup the project
            if not self.setup_nextjs_project():
                return False
            
            # Start the server
            if not self.start_nextjs_server():
                return False
            
            # Capture the screenshot
            success = await self.capture_screenshot()
            
            return success
            
        except KeyboardInterrupt:
            print("\n⚠️  Process interrupted by user")
            return False
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return False
        finally:
            # Always clean up
            self.stop_nextjs_server()
            self.cleanup_temp_files()


def check_dependencies():
    """Check if required dependencies are available"""
    try:
        import playwright
        import requests
        print("✅ Python dependencies are available")
    except ImportError as e:
        print(f"❌ Missing Python dependencies: {e}")
        print("Installing required packages...")
        subprocess.run([sys.executable, "-m", "pip", "install", "playwright", "requests"])
        subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"])
        print("✅ Python dependencies installed")
    
    # Check if npm is available
    try:
        subprocess.run(["npm", "--version"], capture_output=True, check=True)
        print("✅ npm is available")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ npm not found. Please install Node.js and npm first.")
        return False
    
    return True


async def main():
    """Main entry point"""
    print("🎯 Integrated Flight Display Generator")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        return
    
    # Generate the image
    generator = IntegratedFlightDisplayGenerator()
    success = await generator.generate_flight_display()
    
    if success:
        print("\n🎉 Flight display generated successfully!")
        print(f"📁 Output file: {generator.output_filename}")
    else:
        print("\n💥 Failed to generate flight display")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main()) 
