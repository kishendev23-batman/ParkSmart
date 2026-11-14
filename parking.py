
# ParkSmart - Parking Configuration and Vehicle Entry

from datetime import datetime
from storage import save_parking_slots, save_tickets

from validators import (
    validate_vehicle_number,
    validate_vehicle_type
)


PARKING_LEVELS = 3

SLOT_CAPACITY = {
    "two_wheeler": 5,
    "car": 5,
    "ev": 3
}


def create_parking_lot():

    parking_slots = []

    slot_prefix = {
        "two_wheeler": "T",
        "car": "C",
        "ev": "E"
    }

    for level in range(1, PARKING_LEVELS + 1):

        for vehicle_type, capacity in SLOT_CAPACITY.items():

            for slot_number in range(1, capacity + 1):

                slot = {
                    "slot_id": (
                        f"L{level}-"
                        f"{slot_prefix[vehicle_type]}"
                        f"{slot_number:02d}"
                    ),
                    "level": level,
                    "type": vehicle_type,
                    "status": "available",
                    "ticket_id": None
                }

                parking_slots.append(slot)

    return parking_slots


def display_parking_configuration(parking_slots):

    print("\n" + "=" * 55)
    print("             PARKSMART PARKING CONFIGURATION")
    print("=" * 55)

    for level in range(1, PARKING_LEVELS + 1):

        print(f"\nLEVEL {level}")
        print("-" * 55)

        for vehicle_type in SLOT_CAPACITY:

            level_slots = [
                slot for slot in parking_slots
                if slot["level"] == level
                and slot["type"] == vehicle_type
            ]

            print(
                f"{vehicle_type.replace('_', ' ').title():15}"
                f" : {len(level_slots)} slots"
            )

    print("\n" + "=" * 55)
    print(f"TOTAL PARKING SLOTS : {len(parking_slots)}")
    print("=" * 55)


def display_live_occupancy(parking_slots):
    """
    Displays live parking occupancy by level
    and vehicle type.
    """

    vehicle_types = {
        "two_wheeler": "Two-wheelers",
        "car": "Cars",
        "ev": "EVs"
    }

    print("\n" + "=" * 65)
    print("                  PARKSMART LIVE OCCUPANCY")
    print("=" * 65)

    overall_total = 0
    overall_occupied = 0

    for level in range(1, PARKING_LEVELS + 1):

        print(f"\nLEVEL {level}")
        print("-" * 65)
        print(
            f"{'Vehicle Type':20}"
            f"{'Total':10}"
            f"{'Occupied':12}"
            f"{'Available':12}"
            f"{'Usage':10}"
        )

        print("-" * 65)

        level_slots = [
            slot for slot in parking_slots
            if slot["level"] == level
        ]

        level_total = len(level_slots)

        level_occupied = sum(
            1 for slot in level_slots
            if slot["status"] == "occupied"
        )

        level_available = level_total - level_occupied

        for vehicle_type, display_name in vehicle_types.items():

            matching_slots = [
                slot for slot in level_slots
                if slot["type"] == vehicle_type
            ]

            total = len(matching_slots)

            occupied = sum(
                1 for slot in matching_slots
                if slot["status"] == "occupied"
            )

            available = total - occupied

            percentage = (
                (occupied / total) * 100
                if total > 0 else 0
            )

            print(
                f"{display_name:20}"
                f"{total:<10}"
                f"{occupied:<12}"
                f"{available:<12}"
                f"{percentage:.1f}%"
            )

        level_percentage = (
            (level_occupied / level_total) * 100
            if level_total > 0 else 0
        )

        print("-" * 65)

        print(
            f"{'LEVEL TOTAL':20}"
            f"{level_total:<10}"
            f"{level_occupied:<12}"
            f"{level_available:<12}"
            f"{level_percentage:.1f}%"
        )

        overall_total += level_total
        overall_occupied += level_occupied

    overall_available = overall_total - overall_occupied

    overall_percentage = (
        (overall_occupied / overall_total) * 100
        if overall_total > 0 else 0
    )

    print("\n" + "=" * 65)
    print("                    OVERALL PARKING STATUS")
    print("=" * 65)

    print(f"Total Slots       : {overall_total}")
    print(f"Occupied Slots    : {overall_occupied}")
    print(f"Available Slots   : {overall_available}")
    print(f"Occupancy Rate    : {overall_percentage:.2f}%")

    print("=" * 65)


def generate_ticket_id(tickets):

    ticket_number = 1

    while True:

        ticket_id = f"PS{ticket_number:06d}"

        if ticket_id not in tickets:
            return ticket_id

        ticket_number += 1


def register_vehicle(parking_slots, tickets,
                     vehicle_number, vehicle_type,
                     ev_charging=False):

    # Step 1: Validate vehicle details

    if ev_charging and vehicle_type != "ev":
        raise ValueError(
            "EV charging is available only for electric vehicles."
    )

    # Step 2: Prevent duplicate active parking

    for ticket in tickets.values():

        if (
            ticket["vehicle_number"] == vehicle_number
            and ticket["status"] == "active"
        ):
            raise ValueError(
                "This vehicle is already parked."
            )

    # Step 3: Find the first available suitable slot

    available_slot = None

    for slot in parking_slots:

        if (
            slot["type"] == vehicle_type
            and slot["status"] == "available"
            and slot["ticket_id"] is None
        ):
            available_slot = slot
            break

    if available_slot is None:
        raise ValueError(
            f"No available {vehicle_type.replace('_', ' ')} slots."
        )

    # Step 4: Generate a unique ticket

    ticket_id = generate_ticket_id(tickets)

    # Step 5: Create the vehicle ticket

    ticket = {
    "ticket_id": ticket_id,
    "vehicle_number": vehicle_number,
    "vehicle_type": vehicle_type,
    "slot_id": available_slot["slot_id"],
    "level": available_slot["level"],
    "entry_time": datetime.now().isoformat(timespec="seconds"),
    "exit_time": None,
    "fee": 0.0,
    "status": "active",
    "ev_charging": ev_charging,
    "charging_fee": 0.0
}

    # Step 6: Update parking information

    available_slot["status"] = "occupied"
    available_slot["ticket_id"] = ticket_id

    tickets[ticket_id] = ticket

    # Save updated parking information
    save_parking_slots(parking_slots)
    save_tickets(tickets)

    return ticket


def display_ticket(ticket):

    print("\n" + "=" * 45)
    print("             PARKSMART TICKET")
    print("=" * 45)

    print(f"Ticket ID     : {ticket['ticket_id']}")
    print(f"Vehicle No.   : {ticket['vehicle_number']}")
    print(f"Vehicle Type  : {ticket['vehicle_type']}")
    print(f"Parking Level : {ticket['level']}")
    print(f"Slot ID       : {ticket['slot_id']}")
    print(f"Entry Time    : {ticket['entry_time']}")
    print(f"Status        : {ticket['status'].upper()}")

    print("=" * 45)



def get_vehicle_details():

    while True:
        vehicle_number = input(
            "\nEnter vehicle registration number: "
        )

        try:
            vehicle_number = validate_vehicle_number(vehicle_number)
            break

        except ValueError as error:
            print(f"Error: {error}")

    while True:
        print("\nSelect Vehicle Type:")
        print("1. Two Wheeler")
        print("2. Car")
        print("3. Electric Vehicle (EV)")

        vehicle_type_choice = input("Enter your choice (1-3): ").strip()

        try:
            vehicle_type = validate_vehicle_type(vehicle_type_choice)
            break

        except ValueError as error:
            print(f"Error: {error}")

    # Default value
    ev_charging = False

    # Ask about charging only for EV vehicles
    if vehicle_type == "ev":

        while True:
            print("\nDo you need EV charging?")
            print("1. Yes")
            print("2. No")

            charging_choice = input("Enter your choice (1-2): ").strip()

            if charging_choice == "1":
                ev_charging = True
                break

            elif charging_choice == "2":
                ev_charging = False
                break

            else:
                print("Invalid choice. Please enter 1 or 2.")

    return vehicle_number, vehicle_type, ev_charging
