#!/bin/bash

# Radar Pi Setup Script
# Installs Node.js, npm, and project dependencies

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

print_status "🔧 Radar Pi Setup Script"
echo "=========================="

# Check if we're in the right directory
if [ ! -f "package.json" ]; then
    print_error "package.json not found. Please run this script from the radar_pi directory."
    exit 1
fi

# Detect system architecture and OS
ARCH=$(uname -m)
OS=$(uname -s)
print_status "System: $OS $ARCH"

# Check if running as root (not recommended for Pi user)
if [ "$EUID" -eq 0 ]; then
    print_warning "Running as root. Consider running as regular user (pi) instead."
fi

# Update package lists
print_status "📦 Updating package lists..."
sudo apt update

# Install curl if not present (needed for NodeSource setup)
if ! command_exists curl; then
    print_status "Installing curl..."
    sudo apt install -y curl
fi

# Check Node.js installation
NODE_VERSION_REQUIRED="16"
if command_exists node; then
    NODE_VERSION=$(node --version | sed 's/v//' | cut -d. -f1)
    print_status "Found Node.js version: v$(node --version | sed 's/v//')"
    
    if [ "$NODE_VERSION" -ge "$NODE_VERSION_REQUIRED" ]; then
        print_success "Node.js version is sufficient (>= v$NODE_VERSION_REQUIRED)"
    else
        print_warning "Node.js version is too old (< v$NODE_VERSION_REQUIRED). Will update..."
        NEED_NODE_INSTALL=true
    fi
else
    print_status "Node.js not found. Will install..."
    NEED_NODE_INSTALL=true
fi

# Install or update Node.js if needed
if [ "$NEED_NODE_INSTALL" = true ]; then
    print_status "🟢 Installing Node.js LTS..."
    
    # Remove old Node.js installations if they exist
    if command_exists node; then
        print_status "Removing old Node.js installation..."
        sudo apt remove -y nodejs npm 2>/dev/null || true
    fi
    
    # Install Node.js from NodeSource repository (works for ARM64 and ARMv7)
    print_status "Adding NodeSource repository..."
    curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
    
    print_status "Installing Node.js LTS..."
    sudo apt install -y nodejs
    
    print_success "Node.js installed: $(node --version)"
fi

# Verify npm is available
if ! command_exists npm; then
    print_error "npm not found after Node.js installation. Something went wrong."
    exit 1
fi

print_success "npm available: $(npm --version)"

# Update npm to latest version
print_status "📦 Updating npm to latest version..."
sudo npm install -g npm@latest

# Install npm dependencies
print_status "📦 Installing project npm dependencies..."
npm install

print_success "npm dependencies installed"

# Optional: Install Python dependencies if requirements.txt exists
if [ -f "requirements.txt" ]; then
    print_status "🐍 Python dependencies setup..."
    
    # Check if we have Python
    PYTHON_CMD="python"
    if command_exists python3; then
        PYTHON_CMD="python3"
    elif ! command_exists python; then
        print_warning "Python not found. Installing Python 3..."
        sudo apt install -y python3 python3-pip python3-venv
        PYTHON_CMD="python3"
    fi
    
    print_status "Using Python: $($PYTHON_CMD --version)"
    
    # Check if in virtual environment
    if [ -z "$VIRTUAL_ENV" ]; then
        print_warning "No virtual environment detected."
        print_status "Creating virtual environment..."
        $PYTHON_CMD -m venv .venv
        print_status "To activate: source .venv/bin/activate"
        print_status "Installing Python deps in virtual environment..."
        .venv/bin/pip install -r requirements.txt
        .venv/bin/python -m playwright install chromium
    else
        print_status "Installing Python dependencies in current environment..."
        $PYTHON_CMD -m pip install -r requirements.txt
        $PYTHON_CMD -m playwright install chromium
    fi
    
    print_success "Python dependencies installed"
fi

# Make start.sh executable if it exists
if [ -f "start.sh" ]; then
    chmod +x start.sh
    print_success "Made start.sh executable"
fi

echo
print_success "🎉 Setup complete!"
echo
print_status "Next steps:"
echo "1. If you created a virtual environment, activate it: source .venv/bin/activate"
echo "2. Copy config.py.example to config.py and set your coordinates"
echo "3. Run the flight display: ./start.sh"
echo
print_status "Node.js: $(node --version)"
print_status "npm: $(npm --version)"
if [ -f "requirements.txt" ]; then
    print_status "Python deps: Installed"
fi 