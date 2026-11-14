
from parking import (
    create_parking_lot,
    register_vehicle,
    display_ticket,
    display_live_occupancy,
    get_vehicle_details
)

from billing import (
    process_vehicle_exit,
    process_lost_ticket_exit,
    display_bill
)

from reports import (
    generate_daily_report,
    display_daily_report
)

from storage import (
    save_parking_slots,
    load_parking_slots,
    save_tickets,
    load_tickets
)

from validators import validate_ticket_id


def display_menu():
    print("\n" + "=" * 45)
    print("             PARKSMART SYSTEM")
    print("       Multi-Level Parking Management")
    print("=" * 45)

    print("\n1. Park a Vehicle")
    print("2. Remove a Vehicle")
    print("3. View Parking Availability")
    print("4. Generate Daily Report")
    print("5. Exit")
    print("6. Lost Ticket Exit")

    print("\n" + "=" * 45)


def get_user_choice():
    while True:
        try:
            choice = input("Enter your choice (1-6): ").strip()

            if not choice:
                print("Error: Input cannot be empty.")
                continue

            if not choice.isdigit():
                print("Error: Please enter numbers only.")
                continue

            choice = int(choice)

            if choice < 1 or choice > 6:
                print("Error: Please enter a number between 1 and 6.")
                continue

            return choice

        except (EOFError, KeyboardInterrupt):
            print("\nInput interrupted. Exiting safely.")
            return 5


def main():

    # Welcome screen
    print("\n" + "=" * 45)
    print("             WELCOME TO PARKSMART")
    print("       Multi-Level Parking Management")
    print("=" * 45)

    # Load saved data
    parking_slots = load_parking_slots()
    tickets = load_tickets()

    # Create parking lot if no saved data exists
    if parking_slots is None:
        parking_slots = create_parking_lot()
        save_parking_slots(parking_slots)

    print("\nParking data loaded successfully!")
    print(f"Total parking slots : {len(parking_slots)}")
    print(f"Total ticket records: {len(tickets)}")

    # Main application loop
    while True:

        display_menu()

        choice = get_user_choice()

        # Option 1: Park a vehicle
        if choice == 1:

            try:
                vehicle_number, vehicle_type, ev_charging = get_vehicle_details()

                ticket = register_vehicle(
                    parking_slots,
                    tickets,
                    vehicle_number,
                    vehicle_type,
                    ev_charging
                )

                print("\nVehicle parked successfully!")
                display_ticket(ticket)
                display_live_occupancy(parking_slots)

            except ValueError as error:
                print(f"\nParking Error: {error}")

        # Option 2: Normal vehicle exit
        elif choice == 2:

            try:
                ticket_id = input(
                    "\nEnter your parking ticket ID: "
                )

                ticket_id = validate_ticket_id(ticket_id)

                completed_ticket = process_vehicle_exit(
                    parking_slots,
                    tickets,
                    ticket_id
                )

                print("\nVehicle exit completed successfully!")
                display_bill(completed_ticket)
                display_live_occupancy(parking_slots)

            except ValueError as error:
                print(f"\nExit Error: {error}")

        # Option 3: Parking availability
        elif choice == 3:

            display_live_occupancy(parking_slots)

        # Option 4: Daily report
        elif choice == 4:

            report = generate_daily_report(tickets)
            display_daily_report(report)

        # Option 5: Exit application
        elif choice == 5:

            save_parking_slots(parking_slots)
            save_tickets(tickets)

            print("\nParking data saved successfully!")
            print("Thank you for using ParkSmart!")
            print("Have a safe journey!")
            break

        # Option 6: Lost ticket exit
        elif choice == 6:

            try:
                vehicle_number = input(
                    "\nEnter your vehicle registration number: "
                ).strip()

                completed_ticket = process_lost_ticket_exit(
                    parking_slots,
                    tickets,
                    vehicle_number
                )

                print("\nLost ticket exit completed successfully!")
                display_bill(completed_ticket)
                display_live_occupancy(parking_slots)

            except ValueError as error:
                print(f"\nLost Ticket Error: {error}")


if __name__ == "__main__":
    main()
