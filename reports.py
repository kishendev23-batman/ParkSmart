
from datetime import date, datetime


# ParkSmart - Daily Reports


def generate_daily_report(tickets, report_date=None):
    """
    Generates daily parking and revenue statistics.

    Vehicles parked:
    Counted using their entry date.

    Revenue:
    Counted using their exit date, because
    payment is collected when a vehicle exits.
    """

    if report_date is None:
        report_date = date.today()

    if not isinstance(report_date, date):
        raise ValueError("Invalid report date.")

    vehicle_counts = {
        "two_wheeler": 0,
        "car": 0,
        "ev": 0
    }

    revenue_by_type = {
        "two_wheeler": 0.0,
        "car": 0.0,
        "ev": 0.0
    }

    total_vehicles_parked = 0
    completed_exits_today = 0
    total_revenue = 0.0
    active_vehicles = 0

    for ticket in tickets.values():

        try:
            entry_date = datetime.fromisoformat(
                ticket["entry_time"]
            ).date()

        except (ValueError, TypeError, KeyError):
            raise ValueError(
                "A ticket contains an invalid entry time."
            )

        vehicle_type = ticket["vehicle_type"]

        if vehicle_type not in vehicle_counts:
            raise ValueError("A ticket contains an invalid vehicle type.")

        # Count vehicles that entered on the selected date
        if entry_date == report_date:

            total_vehicles_parked += 1
            vehicle_counts[vehicle_type] += 1

        # Count currently active vehicles
        if ticket["status"] == "active":
            active_vehicles += 1

        # Count revenue collected on the selected date
        if ticket["status"] == "completed":

            try:
                exit_date = datetime.fromisoformat(
                    ticket["exit_time"]
                ).date()

                fee = float(ticket["fee"])

            except (ValueError, TypeError, KeyError):
                raise ValueError(
                    "A completed ticket contains invalid billing data."
                )

            if fee < 0:
                raise ValueError("Ticket fee cannot be negative.")

            if exit_date == report_date:

                completed_exits_today += 1
                total_revenue += fee
                revenue_by_type[vehicle_type] += fee

    return {
        "report_date": report_date.isoformat(),
        "total_vehicles_parked": total_vehicles_parked,
        "vehicle_counts": vehicle_counts,
        "active_vehicles": active_vehicles,
        "completed_exits_today": completed_exits_today,
        "total_revenue": total_revenue,
        "revenue_by_type": revenue_by_type
    }


def display_daily_report(report):

    vehicle_names = {
        "two_wheeler": "Two-wheelers",
        "car": "Cars",
        "ev": "EVs"
    }

    print("\n" + "=" * 60)
    print("                 PARKSMART DAILY REPORT")
    print("=" * 60)

    print(f"Report Date             : {report['report_date']}")

    print("-" * 60)
    print("VEHICLE PARKING DETAILS")
    print("-" * 60)

    print(
        f"Total Vehicles Parked   : "
        f"{report['total_vehicles_parked']}"
    )

    for vehicle_type, name in vehicle_names.items():

        print(
            f"{name:23}: "
            f"{report['vehicle_counts'][vehicle_type]}"
        )

    print("-" * 60)
    print("EXIT AND REVENUE DETAILS")
    print("-" * 60)

    print(
        f"Currently Active        : "
        f"{report['active_vehicles']}"
    )

    print(
        f"Completed Exits Today   : "
        f"{report['completed_exits_today']}"
    )

    for vehicle_type, name in vehicle_names.items():

        print(
            f"{name + ' Revenue':23}: "
            f"Rs. {report['revenue_by_type'][vehicle_type]:.2f}"
        )

    print("-" * 60)

    print(
        f"TOTAL REVENUE           : "
        f"Rs. {report['total_revenue']:.2f}"
    )

    print("=" * 60)
    print("             END OF DAILY REPORT")
    print("=" * 60)


def main():
    """
    Temporary test for the daily report.
    """

    today = date.today()

    today_text = today.isoformat()

    sample_tickets = {
        "PS000001": {
            "ticket_id": "PS000001",
            "vehicle_number": "KA03AB1234",
            "vehicle_type": "car",
            "entry_time": f"{today_text}T09:00:00",
            "exit_time": f"{today_text}T11:00:00",
            "fee": 60.0,
            "status": "completed"
        },

        "PS000002": {
            "ticket_id": "PS000002",
            "vehicle_number": "KA03CD5678",
            "vehicle_type": "two_wheeler",
            "entry_time": f"{today_text}T10:00:00",
            "exit_time": f"{today_text}T12:00:00",
            "fee": 30.0,
            "status": "completed"
        },

        "PS000003": {
            "ticket_id": "PS000003",
            "vehicle_number": "KA03EF9012",
            "vehicle_type": "ev",
            "entry_time": f"{today_text}T13:00:00",
            "exit_time": None,
            "fee": 0.0,
            "status": "active"
        }
    }

    report = generate_daily_report(sample_tickets)

    display_daily_report(report)


if __name__ == "__main__":
    main()
