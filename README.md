# Metro Management System

A highly customizable, command-line transit simulation and ticketing tool.

> This program simulates a metro system featuring station and line management, interactive ticketing, and map visualization.
>
> This project is built to be **highly flexible**, allowing you to create and manage your own metro system just by editing simple CSV files. It uses graph-based algorithms to find routes, manages persistent ticket storage, and provides clear route guidance, making it perfect for educational projects, prototyping, or simple transit simulations.

## ✨ Core Features

* 🚉 **Station & Line Browser:** View all available stations, neatly grouped by their respective metro lines.
* 🗺️ **Interactive Map:** Automatically generates and opens an interactive HTML map of your metro network.
* 🎫 **Ticket Management:** Purchase tickets between any two stations, view a list of all issued tickets, and delete old tickets.
* ↪️ **Route Guidance:** Get clear, step-by-step instructions for your journey, including line changes.
* 💾 **Persistent Data:** All stations, lines, and purchased tickets are saved to and loaded from CSV files.
* 🔧 **Extensible Design:** Easily add new features or modify existing ones. The system is built to be extended.
* ⚠️ **Robust Error Handling:** Gracefully handles missing files, formatting errors, and invalid user input.

## 🚀 Getting Started

### 1. Prerequisites
* Python 3.x
* `pip` (Python package installer)

### 2. Installation

1.  Clone this repository (or download the source code).
2.  Navigate to the project directory:
    ```bash
    cd /path/to/metro-management-system
    ```
3.  Install the required Python dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### 3. Running the Program

Execute the main script from your terminal:
```bash
python metro.py

You will be greeted by the interactive main menu. From there, you can explore stations, buy tickets, view the map, and manage your purchased tickets.

🛠️ How to Customize Your Metro

This system is fully data-driven. You can create your own metro network without touching the Python code.

1. Editing Network Data (CSV Files)

All network data is stored in the /data folder:

    data/stations.csv: Define all your stations and their direct connections (neighbors).

    data/lines.csv: Create metro lines (e.g., "Red Line") and list the stations that belong to each line in order.

    data/tickets.csv: This file stores purchased tickets. You can clear it to reset the ticket history.

2. Configuring Application Behavior (Config Class)

All application settings are located in the Config class within metro.py. You can easily change file paths, pricing, and terminal appearance.

Example: Config class in metro.py

Python

class Config:

    # Paths to CSV data files
    STATIONSFILE = "data/stations.csv"
    LINESFILE = "data/lines.csv"
    TICKETSFILE = "data/tickets.csv"
    MAPFILE = "maps/metro.html"

    # CSV formatting options
    DELIMITER = ","
    LISTDELIMITER = ";"
    NEWLINE = "\n"

    # Ticket pricing factor (price per station hop)
    PRICEFACTOR = 3

    # Menu and screen clear delay in seconds
    DELAY = 1.2

    # Terminal text colors (ANSI escape sequences)
    LINECOLORS = {
        "Red Line": "\033[91m",
        "Yellow Line": "\033[93m",
        "Blue Line": "\033[94m",
        "Green Line": "\033[92m",
        # add or customize colors per line
    }

    # Text style ANSI codes
    ANSI = {
        "reset": "\033[0m",
        "bold": "\033[1m",
        "underline": "\033[4m",
        # add styles as required
    }

Configuration Options Explained

    File Paths: STATIONSFILE, LINESFILE, TICKETSFILE (data sources), MAPFILE (output path for the HTML map).

    CSV Formatting: DELIMITER and LISTDELIMITER (change if your CSVs use tabs or pipes).

    Pricing: PRICEFACTOR is the multiplier used to calculate a ticket's price based on the number of stations in the route.

    UX: DELAY is the pause time (in seconds) between menus for a smoother user experience.

    Appearance: LINECOLORS and ANSI dictionaries map line names and styles to ANSI escape codes for colorful and styled terminal output.

📂 Repository Structure

Bash

.
├── data/
│   ├── stations.csv    # Station definitions and connections
│   ├── lines.csv       # Metro lines and their stations
│   └── tickets.csv     # Persistent storage of purchased tickets
├── maps/
│   └── .gitkeep        # Folder to save generated map html files
├── versions/
│   └── v1.0.0.zip      # Program release versions
├── metro.py            # Main program code
├── requirements.txt    # Python dependencies
├── LICENSE             # Apache License 2.0
├── .gitignore          # Git ignore file
└── README.md           # This file

📜 License

This project is licensed under the Apache License 2.0. See the LICENSE file for details.