class Flight:
    """ A flight with a particular aircraft"""
    def __init__(self,fno,aircraft):
        if not fno[:2].isalpha():
             raise ValueError("No Airline code in '{}'".format(fno))
        if not fno[:2].isupper():
             raise ValueError("Invalid airline code {}".format(fno))
        if not(fno[2:].isdigit() and int(fno[2:])<=9999):
            raise ValueError("Invalid route number'{}'".format(fno))
        self._fno=fno
        self._aircraft=aircraft
        rows,seats=self.getSeatingplan()
        print(rows,seats)
        self._seating=[None]+[{letter:None for letter in seats} for _ in rows]

    def getNumber(self):
        return self._fno[:2]

    def getModel(self):
        return self._aircraft.model()

    def getSeatingplan(self):
        return self._aircraft.seatingplan()

    def relocate_passenger(self,from_seat,to_seat):
        """ Relocate a passenger to a different seat
        Args:
            from_seat: The existing seat designator for the
            passenger to be moved

            to_seat: The new seat designator
        """

        torow,toletter = self.parse_seat(to_seat)

        if self._seating[torow][toletter] is not None:
            raise ValueError("Seat {} already occupied".format(to_seat))

        fromRow, fromLetter = self.parse_seat(from_seat)

        self._seating[torow][toletter]=self._seating[fromRow][fromLetter]
        self._seating[fromRow][fromLetter]=None



    def parse_seat(self,seat):
        """ parse s seat designer into a valid row and letter

            Args:
                seat: A seat designator such as 12F

            Returns:
                A tuple containing an integer and a string for row and seat.
        """
        letter=seat[-1]
        row_numbers, seat_letter=self._aircraft.seatingplan()
        if letter not in seat_letter:
            raise ValueError("Invalid seat letter {}".format(letter))
        row_text=seat[:-1]
        try:
            row=int(row_text)
        except ValueError:
            raise ValueError("Invalid seat row {}".format(row_text))

        if row not in row_numbers:
            raise ValueError("Invalid row number{}".format(row))

        return row,letter

    def allocate_seat(self,seat,passenger):
        """
        Allocate a seat to a passenger.
        Raises:
            valueError: if the seat is unavailable
        """
        rows,seat_letters=self._aircraft.seatingplan()
        row,letter=self.parse_seat(seat)

        if self._seating[row][letter] is not None:
            raise ValueError("Seat {} already occupied".format(seat))

        self._seating[row][letter]=passenger

    def make_boarding_cards(self,console_card_printer):
        for passenger, seat in sorted(self._passenger_seats()):
            console_card_printer(passenger,seat,self.getNumber(),self.getModel())


    def _passenger_seats(self):
        row_numbers,seat_letters=self._aircraft.seatingplan()
        for row in row_numbers:
            for letter in seat_letters:
                passenger=self._seating[row][letter]
                if passenger is not None:
                    yield (passenger, "{}{}".format(row,letter))


class SuperC:
    def __init__(self):
        print('Super Class')
        self._registration

class Aircraft:

    def totalSeats(self):
        rows,seats=self.seatingplan()
        return len(rows)*len(seats)

    def __init__(self,registration):
        self._registration=registration

    def registration(self):
        return self._registration

class Airbus319(Aircraft,SuperC):

    def model(self):
        return "Air Bus A319"

    def seatingplan(self):
        return range(1,23), "ABCDEF"

class Boeing777(Aircraft,SuperC):

    def model(self):
        return "Boeing 777"

    def seatingplan(self):
        return range(1,56),"ABCDEFGHJK"



def make_flights():
    ab = Flight("BA758", Airbus319("G-EUPT"))
    ab.allocate_seat('12A', 'Aryan Bhardwaj')
    ab.allocate_seat('12B', 'Gargie Bhardwaj')
    ab.allocate_seat('12C', 'Deep Mala')
    ab.allocate_seat('1A', 'Ravi Datt Sharma')
    ab.allocate_seat('2F', 'J N Sharma')
    ab.allocate_seat('2A', 'Rekha Kumari')

    bo = Flight("AF72", Boeing777("F-GSPS"))
    bo.allocate_seat('12A', 'Aryan Bhardwaj')
    bo.allocate_seat('12B', 'Gargie Bhardwaj')
    bo.allocate_seat('12C', 'Deep Mala')
    bo.allocate_seat('1A', 'Ravi Datt Sharma')
    bo.allocate_seat('2F', 'J N Sharma')
    bo.allocate_seat('2A', 'Rekha Kumari')

    return ab,bo

def console_card_printer(passenger, seat, flight_number, aircraft):
    output="|Name:{0} " \
        " Flight: {1} "\
        "Seat: {2} " \
        "Aircraft: {3} "\
        "|".format(passenger, flight_number,seat,aircraft)

    banner='+'+'-'*(len(output)-2)+'+'
    border='|'+' '*(len(output)-2)+'|'
    lines=[banner,border,output,border,banner]
    card='\n'.join(lines)
    print(card)
    print()


