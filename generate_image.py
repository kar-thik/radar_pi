#!/usr/bin/env python3
"""
Flight Display Image Generator

This script starts a Next.js server with the flight information display components
and uses Playwright to capture a screenshot at exactly 800x480 pixels.
"""

import asyncio
import subprocess
import time
import os
import sys
from pathlib import Path
from playwright.async_api import async_playwright

class FlightDisplayImageGenerator:
    def __init__(self, output_filename="image.png"):
        self.output_filename = output_filename
        self.server_process = None
        self.port = 3000
        self.url = f"http://localhost:{self.port}"
        
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
            max_wait = 30  # seconds
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
    
    async def generate_image(self):
        """Main method to generate the flight display image"""
        try:
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

def check_dependencies():
    """Check if required dependencies are available"""
    try:
        import playwright
        print("✅ Playwright is available")
    except ImportError:
        print("❌ Playwright not found. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "playwright", "requests"])
        subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"])
        print("✅ Playwright installed")
    
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
    print("🎯 Flight Display Image Generator")
    print("=" * 40)
    
    # Check dependencies
    if not check_dependencies():
        return
    
    # Generate the image
    generator = FlightDisplayImageGenerator()
    success = await generator.generate_image()
    
    if success:
        print("\n🎉 Image generated successfully!")
        print(f"📁 Output file: {generator.output_filename}")
    else:
        print("\n💥 Failed to generate image")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main()) 