class Flight:
    """Represents a passenger flight with a specific type of aircraft"""

    def __init__(self, number, aircraft):
        if not number[:2].isalpha():
            raise ValueError(f'No airline code in {number}')
        if not number[:2].isupper():
            raise ValueError(f'Invalid airline code {number}')
        if not (number[2:].isdigit() and len(number[2:]) in (3, 4)):
            raise ValueError(f'Invalid route number {number}')
        self._number = number
        self._aircraft = aircraft
        rows, seats = self._aircraft.get_seating_plan()
        self._seating = [None] + [{letter: None for letter in seats} for _ in rows]

    def _parse_seat(self, seat):
        row_numbers, seat_letters = self._aircraft.get_seating_plan()

        letter = seat[-1]
        if letter not in seat_letters:
            raise ValueError(f'Invalid seat letter {letter}')

        row_text = seat[:-1]
        try:
            row = int(row_text)
        except ValueError:
            raise ValueError(f'Invalid seat row {row_text}')

        if row not in row_numbers:
            raise ValueError(f'Invalid row number {row}')

        return row, letter

    def get_number(self):
        return self._number

    def get_aircraft_model(self):
        return self._aircraft.get_model()

    def allocate_seat(self, seat, passenger):
        """
        Allocate a seat to a passenger.

        Args:
            seat (str): A seat reference, such as '12C'.
            passenger (str): The name of a passenger, such as 'Guido van Rossum'.

        Raises:
            ValueError: If the seat is already occupied.
        """
        row, letter = self._parse_seat(seat)

        # Check if the seat is already occupied
        if self._seating[row][letter] is not None:
            raise ValueError(f'Seat {seat} is already occupied')

        # Allocate the seat to the passenger
        self._seating[row][letter] = passenger

    def print_seating(self):
        """Helper method to print the seating plan for testing purposes"""
        for row_num, row in enumerate(self._seating):
            if row is not None:  # Skip the `None` at index 0
                print(f'Row {row_num}: {row}')

    def relocate_passenger(self, from_seat, to_seat):
        # Parse the from_seat and to_seat to get row and letter
        from_row, from_letter = self._parse_seat(from_seat)
        to_row, to_letter = self._parse_seat(to_seat)

        # Check if the from_seat is occupied
        if self._seating[from_row][from_letter] is None:
            raise ValueError(f'Seat {from_seat} is not occupied')

        # Check if the to_seat is free
        if self._seating[to_row][to_letter] is not None:
            raise ValueError(f'Seat {to_seat} is already occupied')

        # Move the passenger from from_seat to to_seat
        self._seating[to_row][to_letter] = self._seating[from_row][from_letter]
        self._seating[from_row][from_letter] = None

    def get_available_seats(self):
        """
        Count the number of available seats.

        Returns:
            int: The total number of available seats.
        """
        # Initialize the counter for available seats
        available_seats = 0

        # Iterate over the seating plan, skipping the first `None` entry
        for row in self._seating:
            if row is not None:  # Ignore the first `None` at index 0
                # Count unoccupied seats (None values in the dictionary)
                available_seats += sum(1 for seat in row.values() if seat is None)

        return available_seats


# Define the Aircraft class
class Aircraft:
    """Represents a specific type of aircraft"""

    def __init__(self, registration, model, num_rows, num_seats_per_row):
        self._registration = registration
        self._model = model
        self._num_rows = num_rows
        self._num_seats_per_row = num_seats_per_row

    def get_model(self):
        return self._model

    def get_seating_plan(self):
        return range(1, self._num_rows + 1), 'ABCDEFGHJK'[:self._num_seats_per_row]