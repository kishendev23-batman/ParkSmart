# 🚗 ParkSmart – Multi-Level Parking Allocation and Billing System

ParkSmart is a Python-based parking management system designed to automate vehicle parking allocation, ticket generation, parking fee calculation, and occupancy monitoring across multiple parking levels.

## 📌 Project Overview

ParkSmart manages a multi-level parking facility with dedicated parking spaces for two-wheelers, cars, and electric vehicles (EVs). It automatically allocates the nearest available suitable parking slot and maintains parking records using CSV file storage.

## ✨ Features

- **Multi-Level Parking Setup:** Three parking levels with 39 total slots.
- **Automatic Slot Allocation:** Assigns the nearest available suitable slot.
- **Ticket Generation:** Generates unique parking ticket IDs.
- **Automated Billing:** Calculates parking fees based on hourly slabs.
- **EV Charging:** Supports optional EV charging fees.
- **Lost Ticket Management:** Allows vehicle exit using registration number with a ₹100 penalty.
- **Live Occupancy:** Displays occupied and available slots by level and vehicle type.
- **Daily Reports:** Displays vehicle counts and parking revenue.
- **Data Persistence:** Stores parking and ticket records using CSV files.
- **Input Validation:** Handles invalid inputs and prevents duplicate active vehicle registrations.

## 🛠️ Technologies Used

- Python 3
- CSV File Handling
- Datetime Module
- Visual Studio Code
- Git and GitHub

## 📂 Project Structure

```text
ParkSmart/
│
├── main.py
├── parking.py
├── billing.py
├── reports.py
├── storage.py
├── validators.py
├── README.md
├── .gitignore
│
└── data/
    ├── parking_slots.csv
    └── tickets.csv
```

The CSV files are generated locally when the application runs and are excluded from Git tracking.

## 🚘 Parking Configuration

| Vehicle Type | Slots per Level | Total Slots |
|---|---:|---:|
| Two Wheeler | 5 | 15 |
| Car | 5 | 15 |
| Electric Vehicle | 3 | 9 |
| **Total** | **13** | **39** |

## 💰 Parking Charges

| Vehicle Type | First Hour | Each Additional Hour |
|---|---:|---:|
| Two Wheeler | ₹20 | ₹10 |
| Car | ₹40 | ₹20 |
| EV | ₹30 | ₹15 |

Additional EV charging fee: ₹30 per charged hour.

Lost ticket penalty: ₹100.

## ⚙️ Installation and Execution

**1. Clone the repository**

```bash
git clone https://github.com/kishendev23-batman/ParkSmart.git
```

**2. Navigate to the project folder**

```bash
cd ParkSmart
```

**3. Run the application**

```bash
python main.py
```

Make sure Python 3 is installed on your computer.

## 👨‍💻 Author

**Kishen Dev**

GitHub: [@kishendev23-batman](https://github.com/kishendev23-batman)

## 🎓 Project Information

**Project:** CP-043 – ParkSmart  
**Category:** Python-Based Parking Management System

---

*ParkSmart – Making parking smarter, simpler, and more efficient.*