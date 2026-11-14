
import csv
import os

DATA_FOLDER = "data"

PARKING_FILE = os.path.join(DATA_FOLDER, "parking_slots.csv")
TICKETS_FILE = os.path.join(DATA_FOLDER, "tickets.csv")


def ensure_data_folder():
    os.makedirs(DATA_FOLDER, exist_ok=True)


def save_parking_slots(parking_slots):
    ensure_data_folder()

    fieldnames = [
        "slot_id",
        "level",
        "type",
        "status",
        "ticket_id"
    ]

    with open(PARKING_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(parking_slots)


def load_parking_slots():
    ensure_data_folder()

    if not os.path.exists(PARKING_FILE):
        return None

    with open(PARKING_FILE, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        parking_slots = []

        for row in reader:
            parking_slots.append({
                "slot_id": row["slot_id"],
                "level": int(row["level"]),
                "type": row["type"],
                "status": row["status"],
                "ticket_id": row["ticket_id"] or None
            })

    return parking_slots


def save_tickets(tickets):
    ensure_data_folder()


    fieldnames = [
    "ticket_id",
    "vehicle_number",
    "vehicle_type",
    "slot_id",
    "level",
    "entry_time",
    "exit_time",
    "fee",
    "status",
    "charged_hours",
    "ev_charging",
    "charging_fee",
    "parking_fee",
    "lost_ticket_penalty"
    ]
    

    with open(TICKETS_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames,
            extrasaction="ignore"
        )

        writer.writeheader()

        for ticket in tickets.values():
            writer.writerow(ticket)


def load_tickets():
    ensure_data_folder()

    if not os.path.exists(TICKETS_FILE):
        return {}

    tickets = {}

    with open(TICKETS_FILE, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            ticket_id = row["ticket_id"]

            tickets[ticket_id] = {
                "ticket_id": ticket_id,
                "vehicle_number": row["vehicle_number"],
                "vehicle_type": row["vehicle_type"],
                "slot_id": row["slot_id"],
                "level": int(row["level"]),
                "entry_time": row["entry_time"],
                "exit_time": row["exit_time"] or None,
                "fee": float(row["fee"] or 0),
                "status": row["status"],
                "charged_hours": (
                    int(row["charged_hours"])
                    if row.get("charged_hours")
                    else 0
                ),
                "ev_charging": (
                    row.get("ev_charging", "").strip().lower() == "true"
                ),
                "charging_fee": float(row.get("charging_fee") or 0),
                "parking_fee": float(row.get("parking_fee") or 0),
                "lost_ticket_penalty": float(
                    row.get("lost_ticket_penalty") or 0
                    )
            }

    return tickets

if __name__ == "__main__":

    from parking import create_parking_lot

    print("\nPARKSMART CSV STORAGE TEST")
    print("-" * 40)

    # Create sample parking slots
    parking_slots = create_parking_lot()

    # Create sample ticket
    tickets = {
        "PS000001": {
            "ticket_id": "PS000001",
            "vehicle_number": "KA03AB1234",
            "vehicle_type": "car",
            "slot_id": "L1-C01",
            "level": 1,
            "entry_time": "2026-11-10T10:00:00",
            "exit_time": None,
            "fee": 0.0,
            "status": "active",
            "charged_hours": 0
        }
    }

    # Mark the sample slot as occupied
    parking_slots[5]["status"] = "occupied"
    parking_slots[5]["ticket_id"] = "PS000001"

    # Save data
    save_parking_slots(parking_slots)
    save_tickets(tickets)

    print("PASS: Parking slots saved.")
    print("PASS: Tickets saved.")

    # Load saved data
    loaded_slots = load_parking_slots()
    loaded_tickets = load_tickets()

    # Verify loaded data
    assert len(loaded_slots) == 39
    assert loaded_tickets["PS000001"]["vehicle_number"] == "KA03AB1234"
    assert loaded_slots[5]["status"] == "occupied"
    assert loaded_slots[5]["ticket_id"] == "PS000001"

    print("PASS: 39 parking slots loaded.")
    print("PASS: Ticket details loaded.")
    print("PASS: Occupied slot status restored.")

    print("\nAll CSV storage tests passed!")
