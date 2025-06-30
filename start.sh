#!/bin/bash

# Flight Display Image Generator - Start Script
# This script handles the complete workflow for generating flight display images

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

print_status "🎯 Flight Display Image Generator"
echo "=========================================="

# Check if we're in the right directory
if [ ! -f "generate_image.py" ]; then
    print_error "generate_image.py not found. Please run this script from the radar_pi directory."
    exit 1
fi

# Check Python
if ! command_exists python3 && ! command_exists python; then
    print_error "Python not found. Please install Python 3.7 or higher."
    exit 1
fi

# Use python3 if available, otherwise python
PYTHON_CMD="python"
if command_exists python3; then
    PYTHON_CMD="python3"
fi

print_status "Using Python: $($PYTHON_CMD --version)"

# Check Node.js and npm
if ! command_exists node; then
    print_error "Node.js not found. Please install Node.js 16 or higher."
    exit 1
fi

if ! command_exists npm; then
    print_error "npm not found. Please install npm."
    exit 1
fi

print_status "Using Node.js: $(node --version)"
print_status "Using npm: $(npm --version)"

# Check if virtual environment is activated
if [ -z "$VIRTUAL_ENV" ]; then
    print_warning "No virtual environment detected. Consider using a virtual environment."
    if [ -d ".venv" ]; then
        print_status "Found .venv directory. You can activate it with: source .venv/bin/activate"
    fi
fi

# Install Python dependencies if needed
print_status "📦 Checking Python dependencies..."
if ! $PYTHON_CMD -c "import playwright, requests" 2>/dev/null; then
    print_status "Installing Python dependencies..."
    $PYTHON_CMD -m pip install -r requirements.txt
    print_success "Python dependencies installed"
else
    print_success "Python dependencies already installed"
fi

# Check Playwright browsers
print_status "🌐 Checking Playwright browsers..."
if ! $PYTHON_CMD -c "from playwright.sync_api import sync_playwright; sync_playwright().start().chromium.launch()" 2>/dev/null; then
    print_status "Installing Playwright browsers..."
    $PYTHON_CMD -m playwright install chromium
    print_success "Playwright browsers installed"
else
    print_success "Playwright browsers already installed"
fi

# Install npm dependencies if needed
if [ ! -d "node_modules" ]; then
    print_status "📦 Installing npm dependencies..."
    npm install
    print_success "npm dependencies installed"
else
    print_success "npm dependencies already installed"
fi

# Generate the image
print_status "🚀 Generating flight display image..."
$PYTHON_CMD generate_image.py

# Check if image was created successfully
if [ -f "image.png" ]; then
    print_success "🎉 Image generated successfully!"
    
    # Show file info
    if command_exists file; then
        FILE_INFO=$(file image.png)
        print_status "📁 File info: $FILE_INFO"
    fi
    
    # Show file size
    if command_exists ls; then
        SIZE=$(ls -lh image.png | awk '{print $5}')
        print_status "📏 File size: $SIZE"
    fi
    
    # Show location
    print_status "📍 Location: $(pwd)/image.png"
    
    # Open image if possible (macOS)
    if command_exists open && [ "$(uname)" = "Darwin" ]; then
        read -p "Would you like to open the image? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            open image.png
        fi
    fi
    
else
    print_error "💥 Image generation failed. Check the output above for errors."
    exit 1
fi

echo
print_success "✅ All done! Your flight display image is ready." 