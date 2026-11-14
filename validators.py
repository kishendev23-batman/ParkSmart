
import re


# ParkSmart - Input Validation


def normalize_vehicle_number(vehicle_number):
    """
    Removes spaces and hyphens and converts
    the registration number to uppercase.
    """

    if not isinstance(vehicle_number, str):
        raise ValueError("Vehicle number must be text.")

    vehicle_number = vehicle_number.strip().upper()
    vehicle_number = re.sub(r"[\s-]+", "", vehicle_number)

    if not vehicle_number:
        raise ValueError("Vehicle number cannot be empty.")

    return vehicle_number


def validate_vehicle_number(vehicle_number):
    """
    Validates the basic structure of an
    Indian vehicle registration number.
    """

    vehicle_number = normalize_vehicle_number(vehicle_number)

    pattern = r"^[A-Z]{2}\d{1,2}[A-Z]{1,3}\d{1,4}$"

    if not re.fullmatch(pattern, vehicle_number):
        raise ValueError(
            "Invalid registration number. "
            "Example: KA03AB1234"
        )

    return vehicle_number


def validate_vehicle_type(vehicle_type):
    """
    Accepts supported vehicle type names
    and common alternatives.
    """

    if not isinstance(vehicle_type, str):
        raise ValueError("Vehicle type must be text.")

    vehicle_type = vehicle_type.strip().lower()

    valid_types = {
        "1": "two_wheeler",
        "2": "car",
        "3": "ev",
        "two_wheeler": "two_wheeler",
        "two wheeler": "two_wheeler",
        "bike": "two_wheeler",
        "motorcycle": "two_wheeler",
        "car": "car",
        "ev": "ev",
        "electric": "ev",
        "electric vehicle": "ev"
    }

    if vehicle_type not in valid_types:
        raise ValueError(
            "Invalid vehicle type. "
            "Choose Two-wheeler, Car or EV."
        )

    return valid_types[vehicle_type]


def validate_ticket_id(ticket_id):
    """
    Checks the format of a ParkSmart ticket ID.
    """

    if not isinstance(ticket_id, str):
        raise ValueError("Ticket ID must be text.")

    ticket_id = ticket_id.strip().upper()

    if not ticket_id:
        raise ValueError("Ticket ID cannot be empty.")

    if not re.fullmatch(r"PS\d{6}", ticket_id):
        raise ValueError(
            "Invalid ticket format. Example: PS000001"
        )

    return ticket_id


def validate_menu_choice(choice, minimum, maximum):
    """
    Validates a numeric menu selection.
    """

    if not isinstance(choice, str):
        raise ValueError("Menu choice must be text.")

    choice = choice.strip()

    if not choice:
        raise ValueError("Menu choice cannot be empty.")

    if not choice.isdigit():
        raise ValueError("Please enter numbers only.")

    choice = int(choice)

    if choice < minimum or choice > maximum:
        raise ValueError(
            f"Please enter a number between {minimum} and {maximum}."
        )

    return choice



if __name__ == "__main__":

    def test_invalid_input(test_name, test_function, value, *args):

        try:
            test_function(value, *args)
            print(f"FAIL: {test_name} was accepted.")

        except ValueError:
            print(f"PASS: {test_name} was rejected correctly.")

    print("\nPARKSMART ERROR HANDLING TEST")
    print("-" * 45)

    test_invalid_input(
        "Empty vehicle number",
        validate_vehicle_number,
        ""
    )

    test_invalid_input(
        "Invalid vehicle number",
        validate_vehicle_number,
        "ABC123"
    )

    test_invalid_input(
        "Invalid vehicle type",
        validate_vehicle_type,
        "bus"
    )

    test_invalid_input(
        "Empty ticket ID",
        validate_ticket_id,
        ""
    )

    test_invalid_input(
        "Invalid ticket ID",
        validate_ticket_id,
        "ABC123"
    )

    test_invalid_input(
        "Alphabetic menu choice",
        validate_menu_choice,
        "hello", 1, 5
    )

    test_invalid_input(
        "Menu choice outside range",
        validate_menu_choice,
        "9", 1, 5
    )

    test_invalid_input(
        "Empty menu choice",
        validate_menu_choice,
        "", 1, 5
    )

    print("-" * 45)
    print("Error handling tests completed.")
