"""
HTML-based image generation module for flight displays.

This module uses simple HTML templates and Playwright to generate
images for e-ink displays without the complexity of Next.js.
"""

import asyncio
import subprocess
import sys
import os
import tempfile
from typing import Optional
from pathlib import Path
from playwright.async_api import async_playwright

from ..config.settings import Settings
from ..flight.models import FlightData


class HTMLImageGenerator:
    """Generates flight display images using HTML templates."""
    
    def __init__(self, settings: Settings):
        """
        Initialize the HTML image generator.
        
        Args:
            settings: Configuration settings object
        """
        self.settings = settings
        self._playwright_installed = False
        self.template_path = Path(__file__).parent.parent.parent / "templates" / "flight_display.html"
    
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
                    "playwright"
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
    
    def _load_template(self) -> str:
        """
        Load the HTML template from file.
        
        Returns:
            str: HTML template content
        
        Raises:
            FileNotFoundError: If template file doesn't exist
        """
        if not self.template_path.exists():
            raise FileNotFoundError(f"Template not found: {self.template_path}")
        
        with open(self.template_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def _populate_template(self, template: str, flight_data: FlightData) -> str:
        """
        Populate the HTML template with flight data.
        
        Args:
            template: HTML template string
            flight_data: FlightData object containing aircraft information
        
        Returns:
            str: HTML with populated data
        """
        # Get primary aircraft
        aircraft = flight_data.primary_aircraft
        
        if not aircraft:
            # Handle case where no aircraft data is available
            flight_number = "NO DATA"
            model = "Unknown"
            registration = "Unknown"
            ground_speed = "N/A"
            altitude = "N/A"
        else:
            # Handle missing data gracefully
            flight_number = aircraft.flight_number or "N/A"
            model = aircraft.model or "Unknown"
            registration = aircraft.registration or "Unknown"
            
            # Format ground speed
            if aircraft.ground_speed is not None:
                ground_speed = f"{aircraft.ground_speed:.1f}"
            else:
                ground_speed = "N/A"
            
            # Format altitude
            if aircraft.altitude is not None:
                # Handle string altitude (remove 'ft' if present)
                alt_str = str(aircraft.altitude).replace('ft', '').strip()
                try:
                    altitude = f"{int(float(alt_str))}"
                except (ValueError, TypeError):
                    altitude = "N/A"
            else:
                altitude = "N/A"
        
        # Replace template placeholders
        populated_html = template.replace("{{flight_number}}", flight_number)
        populated_html = populated_html.replace("{{model}}", model)
        populated_html = populated_html.replace("{{registration}}", registration)
        populated_html = populated_html.replace("{{ground_speed}}", ground_speed)
        populated_html = populated_html.replace("{{altitude}}", altitude)
        
        return populated_html
    
    def _create_temp_html(self, populated_html: str) -> str:
        """
        Create a temporary HTML file with populated data.
        
        Args:
            populated_html: HTML content with flight data
        
        Returns:
            str: Path to temporary HTML file
        """
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as f:
            f.write(populated_html)
            return f.name
    
    async def _capture_screenshot(self, html_file_path: str) -> bool:
        """
        Capture a screenshot of the HTML file.
        
        Args:
            html_file_path: Path to the HTML file to capture
        
        Returns:
            bool: True if successful, False otherwise
        """
        print("📸 Capturing screenshot from HTML template...")
        
        async with async_playwright() as p:
            try:
                # Launch browser in headless mode
                browser = await p.chromium.launch(headless=True)
                
                # Create a new page with exact viewport size
                page = await browser.new_page(viewport={
                    'width': self.settings.display_width, 
                    'height': self.settings.display_height
                })
                
                # Navigate to the HTML file
                file_url = f"file://{os.path.abspath(html_file_path)}"
                await page.goto(file_url, wait_until='networkidle')
                
                # Wait for fonts to load
                await page.wait_for_timeout(1000)
                
                # Take screenshot of the entire page
                await page.screenshot(
                    path=self.settings.output_image_file,
                    full_page=False
                )
                
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
        Generate flight display image from flight data using HTML template.
        
        Args:
            flight_data: FlightData object containing aircraft information
        
        Returns:
            bool: True if image was generated successfully, False otherwise
        """
        print("🎯 Generating flight display image from HTML template...")
        
        temp_html_path = None
        
        try:
            # Check dependencies
            if not self._check_dependencies():
                return False
            
            # Load template
            print("📄 Loading HTML template...")
            template = self._load_template()
            
            # Populate template with flight data
            print("📝 Populating template with flight data...")
            populated_html = self._populate_template(template, flight_data)
            
            # Create temporary HTML file
            temp_html_path = self._create_temp_html(populated_html)
            print(f"📁 Created temporary HTML file: {temp_html_path}")
            
            # Capture screenshot
            success = await self._capture_screenshot(temp_html_path)
            
            return success
        
        except FileNotFoundError as e:
            print(f"❌ Template file not found: {e}")
            return False
        except KeyboardInterrupt:
            print("\n⚠️  Process interrupted by user")
            return False
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return False
        finally:
            # Clean up temporary file
            if temp_html_path and os.path.exists(temp_html_path):
                try:
                    os.unlink(temp_html_path)
                    print("🧹 Cleaned up temporary files")
                except Exception as e:
                    print(f"⚠️  Failed to clean up temp file: {e}")
    
    def generate_image_sync(self, flight_data: FlightData) -> bool:
        """
        Synchronous wrapper for generate_image.
        
        Args:
            flight_data: FlightData object containing aircraft information
        
        Returns:
            bool: True if image was generated successfully, False otherwise
        """
        return asyncio.run(self.generate_image(flight_data)) 