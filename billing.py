
from datetime import datetime
import math

from validators import validate_ticket_id
from storage import save_parking_slots, save_tickets


# ParkSmart - Billing System

# Parking charges in rupees
HOURLY_RATES = {
    "two_wheeler": {
        "first_hour": 20,
        "additional_hour": 10
    },
    "car": {
        "first_hour": 40,
        "additional_hour": 20
    },
    "ev": {
        "first_hour": 30,
        "additional_hour": 15
    }
}

# Optional feature charges
EV_CHARGING_RATE = 30
LOST_TICKET_PENALTY = 100


def calculate_duration_hours(entry_time, exit_time):
    """
    Calculates parking duration.
    Every started hour is counted as a full hour.
    """

    try:
        entry = datetime.fromisoformat(entry_time)
        exit = datetime.fromisoformat(exit_time)

    except (TypeError, ValueError):
        raise ValueError("Invalid entry or exit time.")

    duration = (exit - entry).total_seconds()

    if duration < 0:
        raise ValueError("Exit time cannot be before entry time.")

    charged_hours = max(1, math.ceil(duration / 3600))

    return charged_hours


def calculate_parking_fee(vehicle_type, entry_time, exit_time):
    """
    Calculates parking fee based on vehicle type
    and charged hours.
    """

    if vehicle_type not in HOURLY_RATES:
        raise ValueError("Invalid vehicle type.")

    charged_hours = calculate_duration_hours(
        entry_time,
        exit_time
    )

    rates = HOURLY_RATES[vehicle_type]

    first_hour_charge = rates["first_hour"]

    additional_hour_charge = (
        charged_hours - 1
    ) * rates["additional_hour"]

    total_fee = first_hour_charge + additional_hour_charge

    return charged_hours, total_fee


def process_vehicle_exit(
    parking_slots,
    tickets,
    ticket_id,
    exit_time=None
):
    """
    Processes normal vehicle exit and calculates fees.
    """

    ticket_id = validate_ticket_id(ticket_id)

    if ticket_id not in tickets:
        raise ValueError("Ticket ID not found.")

    ticket = tickets[ticket_id]

    if ticket["status"] != "active":
        raise ValueError("This vehicle has already exited.")

    if exit_time is None:
        exit_time = datetime.now().isoformat(timespec="seconds")

    charged_hours, parking_fee = calculate_parking_fee(
        ticket["vehicle_type"],
        ticket["entry_time"],
        exit_time
    )

    charging_fee = 0

    if ticket.get("ev_charging", False):

        if ticket["vehicle_type"] != "ev":
            raise ValueError(
                "EV charging is available only for EV vehicles."
            )

        charging_fee = charged_hours * EV_CHARGING_RATE

    total_fee = parking_fee + charging_fee

    matching_slot = None

    for slot in parking_slots:
        if slot["slot_id"] == ticket["slot_id"]:
            matching_slot = slot
            break

    if matching_slot is None:
        raise ValueError("Parking slot record not found.")

    if (
        matching_slot["status"] != "occupied"
        or matching_slot["ticket_id"] != ticket_id
    ):
        raise ValueError("Parking slot record is inconsistent.")

    ticket["exit_time"] = exit_time
    ticket["fee"] = total_fee
    ticket["charging_fee"] = charging_fee
    ticket["parking_fee"] = parking_fee
    ticket["lost_ticket_penalty"] = 0
    ticket["status"] = "completed"
    ticket["charged_hours"] = charged_hours

    matching_slot["status"] = "available"
    matching_slot["ticket_id"] = None

    save_parking_slots(parking_slots)
    save_tickets(tickets)

    return ticket


def process_lost_ticket_exit(
    parking_slots,
    tickets,
    vehicle_number,
    exit_time=None
):
    """
    Processes vehicle exit when the customer has lost
    their parking ticket. Adds a fixed penalty.
    """

    vehicle_number = (
        vehicle_number.strip()
        .upper()
        .replace(" ", "")
        .replace("-", "")
    )

    if not vehicle_number:
        raise ValueError("Vehicle number cannot be empty.")

    matching_ticket = None

    for ticket in tickets.values():

        if (
            ticket["vehicle_number"] == vehicle_number
            and ticket["status"] == "active"
        ):
            matching_ticket = ticket
            break

    if matching_ticket is None:
        raise ValueError(
            "No active parking record found for this vehicle."
        )

    if exit_time is None:
        exit_time = datetime.now().isoformat(timespec="seconds")

    charged_hours, parking_fee = calculate_parking_fee(
        matching_ticket["vehicle_type"],
        matching_ticket["entry_time"],
        exit_time
    )

    charging_fee = 0

    if matching_ticket.get("ev_charging", False):

        if matching_ticket["vehicle_type"] != "ev":
            raise ValueError(
                "EV charging is available only for EV vehicles."
            )

        charging_fee = charged_hours * EV_CHARGING_RATE

    penalty = LOST_TICKET_PENALTY

    total_fee = parking_fee + charging_fee + penalty

    matching_slot = None

    for slot in parking_slots:

        if slot["slot_id"] == matching_ticket["slot_id"]:
            matching_slot = slot
            break

    if matching_slot is None:
        raise ValueError("Parking slot record not found.")

    if (
        matching_slot["status"] != "occupied"
        or matching_slot["ticket_id"] != matching_ticket["ticket_id"]
    ):
        raise ValueError("Parking slot information is inconsistent.")

    matching_ticket["exit_time"] = exit_time
    matching_ticket["parking_fee"] = parking_fee
    matching_ticket["charging_fee"] = charging_fee
    matching_ticket["lost_ticket_penalty"] = penalty
    matching_ticket["fee"] = total_fee
    matching_ticket["charged_hours"] = charged_hours
    matching_ticket["status"] = "completed"

    matching_slot["status"] = "available"
    matching_slot["ticket_id"] = None

    save_parking_slots(parking_slots)
    save_tickets(tickets)

    return matching_ticket


def display_bill(ticket):
    """
    Displays the final parking bill.
    """

    print("\n" + "=" * 45)
    print("              PARKSMART BILL")
    print("=" * 45)

    print(f"Ticket ID       : {ticket['ticket_id']}")
    print(f"Vehicle Number  : {ticket['vehicle_number']}")

    print(
        f"Vehicle Type    : "
        f"{ticket['vehicle_type'].replace('_', ' ').title()}"
    )

    print(f"Parking Level   : {ticket['level']}")
    print(f"Slot ID         : {ticket['slot_id']}")
    print(f"Entry Time      : {ticket['entry_time']}")
    print(f"Exit Time       : {ticket['exit_time']}")
    print(f"Charged Hours   : {ticket['charged_hours']}")

    print("-" * 45)

    print(
        f"Parking Fee     : "
        f"Rs. {ticket.get('parking_fee', ticket['fee']):.2f}"
    )

    print(
        f"EV Charging Fee : "
        f"Rs. {ticket.get('charging_fee', 0):.2f}"
    )

    print(
        f"Lost Ticket Fee : "
        f"Rs. {ticket.get('lost_ticket_penalty', 0):.2f}"
    )

    print("-" * 45)

    print(f"TOTAL FEE       : Rs. {ticket['fee']:.2f}")

    print("=" * 45)
    print("       Thank you for using ParkSmart!")
    print("=" * 45)


if __name__ == "__main__":

    print("\nPARKSMART BILLING TEST")
    print("-" * 40)

    sample_entry = "2026-11-10T10:00:00"
    sample_exit = "2026-11-10T12:20:00"

    hours, fee = calculate_parking_fee(
        "car",
        sample_entry,
        sample_exit
    )

    print("Vehicle Type  : Car")
    print(f"Charged Hours : {hours}")
    print(f"Parking Fee   : Rs. {fee:.2f}")

    print("\nBilling calculation completed successfully!")
