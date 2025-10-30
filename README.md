# 🚇 Metro Ticketing System

A command-line **Metro Network Simulation and Ticketing Program** that allows users to view stations, visualize metro maps, purchase tickets, and calculate travel routes — all while being fully customizable through editable data files and configuration settings.

---

## 📂 Repository Structure

```plaintext
├── data/
│   ├── stations.csv        # List of stations and connections
│   ├── lines.csv           # Metro lines and associated stations
│   ├── tickets.csv         # Purchased tickets (auto-generated)
│
├── maps/
│   ├── .gitkeep            # Keeps folder structure in git
│
├── versions/
│   ├── v1.0.0.zip          # Program archive (first release)
│
├── metro.py                # Main program source code
├── requirements.txt        # Python dependencies
├── LICENSE                 # Apache 2.0 License
├── .gitignore              # Ignored files
└── README.md               # This file
```

---

## ✨ Features

### 🧭 Interactive Command-Line Menu
Navigate through options such as:
- 🏙️ View Metro Stations  
- 🗺️ View Metro Map  
- 🎫 Purchase Tickets  
- 📄 View Tickets  
- ❌ Delete Tickets  
- 🚪 Exit Program  

### 🌐 Dynamic Metro Map Generation
- Generates a **visual network graph** of all stations and connections.  
- Uses [**NetworkX**](https://networkx.org/) and [**PyVis**](https://pyvis.readthedocs.io/) to render an interactive map viewable in any browser.  

### 💳 Ticket Management
- Purchase, view, and delete tickets easily.
- Tickets are automatically saved to `tickets.csv` and persist between runs.

### 🚉 Shortest Route Calculation
- Computes the **shortest path** between any two stations.  
- Provides **step-by-step transfer instructions** between lines.

### ⚙️ Configurable Design
Fully data-driven and user-customizable:
- Edit `stations.csv` and `lines.csv` to add or modify metro data.
- Adjust runtime behavior in the `Config` class, including:
  - `DELAY` (UI timing)
  - `PRICE_FACTOR` (ticket pricing)
  - Custom color themes and formatting.

### 🔐 Data Integrity & Caching
- Metro map filenames are **hashed using SHA256** to reflect changes in data.  
- Ensures cached versions stay unique to the dataset.

---

## 🧰 Installation

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>
```

### 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Run the Program
```bash
python metro.py
```

---

## 🧩 Configuration and Customization

| Component | Description | Editable |
|------------|-------------|-----------|
| **`Config` Class** | Contains runtime settings like delays, paths, pricing, and colors | ✅ |
| **`stations.csv`** | Defines station IDs, names, and neighbor relationships | ✅ |
| **`lines.csv`** | Defines metro lines and connected stations | ✅ |
| **`tickets.csv`** | Stores purchased tickets (auto-managed) | ⚠️ Avoid manual edits |

Example of editing line colors or pricing in `Config`:
```python
PRICE_FACTOR = 5  # Increases ticket price multiplier
LINE_COLORS["Blue Line"] = "[94m"  # Custom ANSI color
```

---

## 🧠 Example Usage

**Main Menu:**
```
=============[ MAIN MENU ]=============
[1] View Metro Stations
[2] View Metro Map
[3] Purchase Tickets
[4] View Tickets
[5] Delete Tickets
[0] Exit
```

**Purchasing a Ticket:**
```
Enter starting Station ID (ENTER -> abort): 1
Enter destination Station ID (ENTER -> abort): 8
Purchase this ticket? (y/n)
```

**Viewing the Metro Map:**
- Automatically opens in your default web browser as an interactive HTML visualization.

---

## 📦 Dependencies

The project relies on:
- [networkx](https://networkx.org/)
- [pyvis](https://pyvis.readthedocs.io/)

Install them with:
```bash
pip install -r requirements.txt
```

---

## 🧾 License

Licensed under the **Apache License 2.0**.  
See the [LICENSE](./LICENSE) file for full details.

---

## 🕒 Version History

| Version | Date | Notes |
|----------|------|-------|
| **v1.0.0** | Initial Release | 🎉 First public version |

---

## 💡 Notes & Tips

- Generated maps are stored in the `maps/` directory as `.html` files.  
- Filenames include **unique SHA256 hashes** of metro data.  
- Always back up your `data/` directory before editing CSVs manually.  

---

**🚆 Enjoy exploring and customizing your metro network simulation!**
