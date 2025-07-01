#!/bin/bash
# Complete Radar Pi Workflow
# Usage: ./run_radar.sh

echo "🎯 Starting Complete Radar Pi Workflow..."
echo "=" * 50

# Step 0: Activate the Pimoroni virtual environment
echo "🔄 Activating Pimoroni virtual environment..."
source $HOME/.virtualenvs/pimoroni/bin/activate

# Step 1: Generate flight display
echo "📡 Fetching flight data and generating display..."
python scripts/radar_display.py

# Check if image generation was successful
if [ $? -eq 0 ]; then
    echo "✅ Display image generated successfully!"
    
    # Step 2: Display on e-ink
    echo "📺 Displaying on e-ink screen..."
    python disp_curr_flight.py
    
    if [ $? -eq 0 ]; then
        echo "🎉 Complete! Flight display is now showing on e-ink screen."
    else
        echo "❌ Failed to display on e-ink screen."
        exit 1
    fi
else
    echo "❌ Failed to generate flight display image."
    exit 1
fi 