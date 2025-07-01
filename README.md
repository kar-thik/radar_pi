# Radar Pi

![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-in_development-orange.svg)

I built this app because I had a Raspberry Pi and an E-ink display lying around, and I'm a huge plane nerd. From my apartment, I can see planes landing at DCA, and this app uses a waypoint I've set on the approach path. It finds the closest plane to those coordinates, and by the time the painfully slow e-ink display updates, I can look out my window and see the actual plane. It's basically magic, but with more Python and API calls.

The flight data comes from the nice people at [adsb.lol](https://adsb.lol/about).

## Hardware

- A Raspberry Pi (any model with a 40-pin header should work).
- An Inky Impression 7.3" e-paper display. You can get one [here](https://shop.pimoroni.com/products/inky-impression-7-3?variant=55186435244411).
- The necessary drivers for the display, which you can find [here](https://github.com/pimoroni/inky).

## Getting Started

### Prerequisites

This guide assumes you've already set up your Raspberry Pi and have installed the Pimoroni Inky library in the default path (`~/.virtualenvs/pimoroni/`). If you haven't, please follow the instructions on the [Pimoroni Inky GitHub page](https://github.com/pimoroni/inky).

### Installation & Running

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/radar-pi.git
    cd radar-pi
    ```

2.  **Activate the Pimoroni virtual environment:**
    ```bash
    source ~/.virtualenvs/pimoroni/bin/activate
    ```

3.  **Install the Python dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    
4.  **(Optional) Configure your location:**
    
    If you don't want to track planes landing at DCA, you can create a `config.py` file in the root directory and set your own coordinates.
    
    ```bash
    cp config.py.example config.py
    ```
    
    Then edit `config.py` with your desired latitude, longitude, and search radius.

5.  **Run the script:**
    
    The main script will fetch flight data, generate an image, and display it on the Inky screen.
    
    ```bash
    ./run_radar.sh
    ```

That's it. Now you can also stare out your window at planes, but with more steps. 