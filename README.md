# Metro Management System

A command-line based Metro transit management program for exploring stations, viewing metro routes, purchasing tickets, and visualizing network maps. Designed for flexibility, it allows users to customize metro data and appearance easily by modifying CSV files and configuration settings.

## Project Description

This program simulates a metro system featuring station and line management, interactive ticketing, and map visualization. It reads all its data from CSV files, enabling you to tailor the metro network by adding or editing stations, lines, and pricing rules. The application uses graph-based algorithms to compute routes and supports persistent ticket storage, making it ideal for educational projects, prototyping, or simple transit simulations.

## Core Features

- **Metro Station Browser:** View a list of metro stations grouped by lines.
- **Interactive Metro Map:** Generate and display an interactive map of the metro network.
- **Ticket Purchase & Management:** Buy tickets between two stations, view issued tickets, and delete tickets.
- **Route Guidance:** Clear step-by-step instructions show the path between stations.
- **Persistent Data Storage:** All tickets, stations, and lines are saved and loaded from CSV files.
- **Robust Error Handling:** Graceful handling of missing files, format errors, and invalid input.
- **Extensible Design:** Easily extend functionality by modifying source code or data files.

## Customizable and Optional Behaviors

- Modify the metro network by editing CSV files:
  - `stations.csv`: Define stations and their connections.
  - `lines.csv`: Define metro lines and assign stations to lines.
- Customize pricing, display colors, and terminal behaviors through the `Config` class.
- Adjust delay timings for menu navigation and screen clearing.
- Use your preferred color schemes for each metro line to enhance terminal output.
- Change delimiters used in CSV files if necessary.
- Map visualization output location and filename can be configured.
  
## Example Config Class

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

### Explanation of Config Options

- `STATIONSFILE`, `LINESFILE`, `TICKETSFILE`: File paths to CSV data files; replace these to load different datasets.
- `MAPFILE`: Output HTML file showing the generated metro map visualization.
- `DELIMITER` and `LISTDELIMITER`: CSV field and list item separators; useful if your CSV uses different separators.
- `PRICEFACTOR`: Multiplier applied to the number of stations in a ticket route to calculate price.
- `DELAY`: Pause time between menu display updates for better user experience.
- `LINECOLORS`: Maps line names to terminal color codes to customize colored output.
- `ANSI`: Dictionary holding terminal text formatting codes to style text in menus and outputs.

## Repository Structure

.
├── data/
│ ├── stations.csv # Station definitions and connections
│ ├── lines.csv # Metro lines and their stations
│ ├── tickets.csv # Persistent storage of purchased tickets
├── maps/
│ └── .gitkeep # Folder to save generated map html files
├── versions/
│ └── v1.0.0.zip # Program release versions
├── metro.py # Main program code
├── requirements.txt # Python dependencies
├── LICENSE # Apache License 2.0
├── .gitignore # Git ignore file
└── README.md # This file


## Getting Started

1. Install dependencies with:
pip install -r requirements.txt

2. Run the program:
python metro.py

3. Use the interactive menu to explore stations, buy tickets, view the metro map, and manage your tickets.

4. Customize your metro experience by editing CSV data files or adjusting configuration options in the `Config` class.

## License

This project is licensed under the Apache License 2.0. See LICENSE for details.
