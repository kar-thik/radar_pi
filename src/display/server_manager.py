"""
Next.js server management for the flight display system.

This module handles starting, stopping, and monitoring the Next.js development
server used for generating flight display images.
"""

import subprocess
import time
import os
import requests
from typing import Optional
from pathlib import Path

from ..config.settings import Settings


class NextJSServerManager:
    """Manages the Next.js development server lifecycle."""
    
    def __init__(self, settings: Settings):
        """
        Initialize the server manager.
        
        Args:
            settings: Configuration settings object
        """
        self.settings = settings
        self.server_process: Optional[subprocess.Popen] = None
        self.url = f"http://localhost:{settings.server_port}"
    
    def setup_project(self) -> bool:
        """
        Set up the Next.js project by installing dependencies if needed.
        
        Returns:
            bool: True if setup was successful, False otherwise
        """
        print("📦 Setting up Next.js project...")
        
        if not Path("node_modules").exists():
            print("Installing npm dependencies...")
            try:
                result = subprocess.run(
                    ["npm", "install"], 
                    capture_output=True, 
                    text=True,
                    timeout=300  # 5 minute timeout
                )
                if result.returncode != 0:
                    print(f"❌ Failed to install npm dependencies: {result.stderr}")
                    return False
                print("✅ Dependencies installed successfully")
            except subprocess.TimeoutExpired:
                print("❌ npm install timed out")
                return False
            except FileNotFoundError:
                print("❌ npm not found. Please install Node.js and npm first.")
                return False
        else:
            print("✅ Dependencies already installed")
        
        return True
    
    def start_server(self) -> bool:
        """
        Start the Next.js development server.
        
        Returns:
            bool: True if server started successfully, False otherwise
        """
        print(f"🚀 Starting Next.js server on port {self.settings.server_port}...")
        
        try:
            # Set environment variable for port
            env = os.environ.copy()
            env['PORT'] = str(self.settings.server_port)
            
            # Start the server in development mode
            self.server_process = subprocess.Popen(
                ["npm", "run", "dev"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                env=env
            )
            
            # Wait for server to start
            return self._wait_for_server_ready()
            
        except FileNotFoundError:
            print("❌ npm not found. Please install Node.js and npm first.")
            return False
        except Exception as e:
            print(f"❌ Failed to start server: {e}")
            return False
    
    def _wait_for_server_ready(self) -> bool:
        """
        Wait for the server to become ready.
        
        Returns:
            bool: True if server is ready, False if timeout
        """
        start_time = time.time()
        
        while time.time() - start_time < self.settings.server_timeout:
            try:
                response = requests.get(self.url, timeout=1)
                if response.status_code == 200:
                    print("✅ Next.js server is ready!")
                    return True
            except requests.RequestException:
                # Server not ready yet, continue waiting
                pass
            
            time.sleep(1)
        
        print("❌ Server failed to start within timeout")
        return False
    
    def stop_server(self) -> None:
        """Stop the Next.js server."""
        if self.server_process:
            print("🛑 Stopping Next.js server...")
            self.server_process.terminate()
            try:
                self.server_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                print("⚠️  Server didn't stop gracefully, forcing shutdown...")
                self.server_process.kill()
                self.server_process.wait()
            print("✅ Server stopped")
            self.server_process = None
    
    def is_running(self) -> bool:
        """
        Check if the server is currently running.
        
        Returns:
            bool: True if server is running, False otherwise
        """
        if not self.server_process:
            return False
        
        return self.server_process.poll() is None
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - ensures server is stopped."""
        self.stop_server() 