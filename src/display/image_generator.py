"""
Image generation module for flight displays.

This module uses Playwright to capture screenshots of the flight display
web interface and generate images for e-ink displays.
"""

import asyncio
import subprocess
import sys
import json
import os
from typing import Optional
from pathlib import Path
from playwright.async_api import async_playwright

from ..config.settings import Settings
from ..flight.models import FlightData
from .server_manager import NextJSServerManager


class ImageGenerator:
    """Generates flight display images using web scraping."""
    
    def __init__(self, settings: Settings):
        """
        Initialize the image generator.
        
        Args:
            settings: Configuration settings object
        """
        self.settings = settings
        self.server_manager = NextJSServerManager(settings)
        self._playwright_installed = False
    
    def _check_dependencies(self) -> bool:
        """
        Check if required dependencies are available and install if needed.
        
        Returns:
            bool: True if dependencies are available, False otherwise
        """
        # Check Playwright
        try:
            import playwright
            print("✅ Playwright is available")
            self._playwright_installed = True
        except ImportError:
            print("❌ Playwright not found. Installing...")
            try:
                subprocess.run([
                    sys.executable, "-m", "pip", "install", 
                    "playwright", "requests"
                ], check=True, capture_output=True)
                subprocess.run([
                    sys.executable, "-m", "playwright", "install", "chromium"
                ], check=True, capture_output=True)
                print("✅ Playwright installed successfully")
                self._playwright_installed = True
            except subprocess.CalledProcessError as e:
                print(f"❌ Failed to install Playwright: {e}")
                return False
        
        return True
    
    def _save_flight_data(self, flight_data: FlightData) -> bool:
        """
        Save flight data to JSON file for Next.js app to consume.
        
        Args:
            flight_data: FlightData object to save
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            data = flight_data.to_json_dict()
            with open(self.settings.flight_data_file, 'w') as f:
                json.dump(data, f, indent=2)
            return True
        except Exception as e:
            print(f"❌ Failed to save flight data: {e}")
            return False
    
    def _cleanup_temp_files(self) -> None:
        """Clean up temporary files."""
        try:
            if os.path.exists(self.settings.flight_data_file):
                os.remove(self.settings.flight_data_file)
        except Exception as e:
            print(f"⚠️  Failed to clean up temp files: {e}")
    
    async def _capture_screenshot(self) -> bool:
        """
        Capture a screenshot of the flight display.
        
        Returns:
            bool: True if successful, False otherwise
        """
        print("📸 Capturing screenshot...")
        
        async with async_playwright() as p:
            try:
                # Launch browser in headless mode
                browser = await p.chromium.launch(headless=True)
                
                # Create a new page with exact viewport size
                page = await browser.new_page(viewport={
                    'width': self.settings.display_width, 
                    'height': self.settings.display_height
                })
                
                # Navigate to the page
                await page.goto(self.server_manager.url, wait_until='networkidle')
                
                # Wait for any animations to complete
                await page.wait_for_timeout(2000)
                
                # Find the flight display component and screenshot it
                display_selector = f'div[class*="w-[{self.settings.display_width}px] h-[{self.settings.display_height}px]"]'
                flight_display = page.locator(display_selector)
                
                # Take screenshot of just the component
                await flight_display.screenshot(path=self.settings.output_image_file)
                
                print(f"✅ Screenshot saved as {self.settings.output_image_file}")
                return True
                
            except Exception as e:
                print(f"❌ Failed to capture screenshot: {e}")
                return False
                
            finally:
                if 'browser' in locals():
                    await browser.close()
    
    async def generate_image(self, flight_data: FlightData) -> bool:
        """
        Generate flight display image from flight data.
        
        Args:
            flight_data: FlightData object containing aircraft information
        
        Returns:
            bool: True if image was generated successfully, False otherwise
        """
        print("🎯 Generating flight display image...")
        
        try:
            # Check dependencies
            if not self._check_dependencies():
                return False
            
            # Save flight data for Next.js app
            if not self._save_flight_data(flight_data):
                return False
            
            # Use server manager as context manager
            with self.server_manager:
                # Setup and start server
                if not self.server_manager.setup_project():
                    return False
                
                if not self.server_manager.start_server():
                    return False
                
                # Capture screenshot
                success = await self._capture_screenshot()
                
                return success
        
        except KeyboardInterrupt:
            print("\n⚠️  Process interrupted by user")
            return False
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return False
        finally:
            # Always clean up
            self._cleanup_temp_files()
    
    def generate_image_sync(self, flight_data: FlightData) -> bool:
        """
        Synchronous wrapper for generate_image.
        
        Args:
            flight_data: FlightData object containing aircraft information
        
        Returns:
            bool: True if image was generated successfully, False otherwise
        """
        return asyncio.run(self.generate_image(flight_data)) 