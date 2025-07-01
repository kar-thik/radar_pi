#!/usr/bin/env python3

import gpiod
import gpiodevice
from gpiod.line import Bias, Direction, Edge
import os
from PIL import Image
from inky.auto import auto

# GPIO pins for each button (use actual pin numbers)
BUTTONS = ["5", "6", "16", "24"]  # Replace with actual GPIO pin numbers

# Corresponding labels for the buttons
LABELS = ["A", "B", "C", "D"]

# Create settings for all the input pins
INPUT = gpiod.LineSettings(direction=Direction.INPUT, bias=Bias.PULL_UP, edge_detection=Edge.FALLING)

# Find the gpiochip device
chip = gpiodevice.find_chip_by_platform()

# Build config for each pin/line
OFFSETS = [chip.line_offset_from_id(pin) for pin in BUTTONS]
line_config = dict.fromkeys(OFFSETS, INPUT)

# Request the lines
request = chip.request_lines(consumer="button-capture", config=line_config)

# Set up the Inky display
try:
    inky_display = auto(ask_user=True, verbose=True)
except TypeError:
    raise TypeError("You need to update the Inky library to >= v1.1.0")

try:
    inky_display.set_border(inky_display.WHITE)
except NotImplementedError:
    pass

# Display the curr_flight.png image
img = Image.open("./curr_flight.png")
img = img.resize(inky_display.resolution)
inky_display.set_image(img)
inky_display.show()
