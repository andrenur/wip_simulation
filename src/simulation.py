import simpy
import random
from src.config import *
from src.utils import *

class AirportDepartureTerminal:
    def __init__(self, env, num_counters, num_kiosks, num_sc_lines, num_immigration):
        self.env = env
        self.counters = [simpy.Resource(env, capacity=1) for _ in range(num_counters)]  # Check-in counters
        self.kiosks = [simpy.Resource(env, capacity=1) for _ in range(num_kiosks)]  # Self-service kiosks
        self.security_lines = [simpy.Resource(env, capacity=1) for _ in range(num_sc_lines)]  # Security lines
        self.immigration = [simpy.Resource(env, capacity=1) for _ in range(num_immigration)]  # Immigration checkers

        self.counter_id = [f'Counter {i+1}' for i in range(num_counters)]
        self.kiosk_id = [f'Kiosk {i+1}' for i in range(num_kiosks)]
        self.sc_id = [f'SC Line {i+1}' for i in range(num_sc_lines)]
        self.im_id = [f'Immigration {i+1}' for i in range(num_immigration)]

    def check_in_counter(self, passenger, has_baggage, log_row):
        counter_choice = choose_shortest_counter(self)
        counter_index = self.counters.index(counter_choice)
        log_row['Counter Choiced ID'] = self.counter_id[counter_index]
        log_row['Time at Counter Choice'] = self.env.now

        with counter_choice.request() as request:
            yield request
            log_row['Counter Used'] = True
            log_row['Counter Start'] = self.env.now
            log_row['Counter Used ID'] = self.counter_id[counter_index]

            # Exponential service time for check-in counter
            yield self.env.timeout(get_checkin_time_counter())

            if has_baggage:
                yield self.env.timeout(get_checkin_time_counter())  # Additional time for baggage drop

            log_row['Counter Finish Time'] = self.env.now
            log_row['Counter Used Length'] = log_row['Counter Finish Time'] - log_row['Counter Start']

            yield self.env.timeout(COUNTER_TO_EXIT_TRANSIT_TIME)
            log_row['Check-in Finish Time'] = self.env.now
            yield self.env.process(self.security_check(passenger, log_row))

    def check_in_kiosk(self, passenger, has_baggage, log_row):
        kiosk_choice = choose_shortest_kiosk(self)
        kiosk_index = self.kiosks.index(kiosk_choice)
        log_row['Kiosk Choiced ID'] = self.kiosk_id[kiosk_index]
        log_row['Time at Kiosk Choice'] = self.env.now

        with kiosk_choice.request() as request:
            yield request
            log_row['Kiosk Used'] = True
            log_row['Kiosk Start'] = self.env.now
            log_row['Kiosk Used ID'] = self.kiosk_id[kiosk_index]

            # Exponential service time for kiosk check-in
            yield self.env.timeout(get_checkin_time_kiosk())
            log_row['Kiosk Finish Time'] = self.env.now
            log_row['Kiosk Used Length'] = log_row['Kiosk Finish Time'] - log_row['Kiosk Start']

            if has_baggage:
                yield self.env.timeout(KIOSK_TO_COUNTER_TRANSIT_TIME)
                yield self.env.process(self.check_in_counter(passenger, has_baggage, log_row))
                yield self.env.timeout(COUNTER_TO_EXIT_TRANSIT_TIME)
            else:
                yield self.env.timeout(KIOSK_TO_EXIT_TRANSIT_TIME)
                log_row['Check-in Finish Time'] = self.env.now

    def security_check(self, passenger, log_row):
        sc_choice = choose_shortest_security_line(self)
        sc_index = self.security_lines.index(sc_choice)
        log_row['SC Line Choiced ID'] = self.sc_id[sc_index]
        log_row['Time at SC Line Choice'] = self.env.now

        with sc_choice.request() as request:
            yield request
            log_row['SC Start'] = self.env.now
            log_row['SC Line Used ID'] = self.sc_id[sc_index]

            # Exponential service time for security check
            yield self.env.timeout(get_security_check_time())
            log_row['SC Finish Time'] = self.env.now
            log_row['SC Used Length'] = log_row['SC Finish Time'] - log_row['SC Start']

    def immigration_check(self, passenger, log_row):
        im_choice = choose_shortest_immigration_line(self)
        im_index = self.immigration.index(im_choice)
        log_row['IM Line Choiced ID'] = self.im_id[im_index]
        log_row['Time at IM Line Choice'] = self.env.now

        with im_choice.request() as request:
            yield request
            log_row['IM Line Start'] = self.env.now
            log_row['IM Line Used ID'] = self.im_id[im_index]

            # Exponential service time for immigration check
            yield self.env.timeout(get_immigration_time())
            log_row['IM Line Finish Time'] = self.env.now
            log_row['IM Used Length'] = log_row['IM Line Finish Time'] - log_row['IM Line Start']

            yield self.env.timeout(DEPARTURE_TRANSIT_TIME)
            log_row['Departure Area Arrival Time'] = self.env.now



###
def passenger(env, name, airport_departure_system):
    # Choose a check-in method with probabilities for online, kiosk, or counter check-in
    check_in_choice = random.choices(['online', 'kiosk', 'counter'], weights=[0.2, 0.3, 0.5], k=1)[0]
    has_baggage = random.choice([True, False])

    # Initialize the log row to record times and details
    log_row = {
        'Passenger': name,
        'Arrival Time': env.now,
        'Check-in Type': check_in_choice,
        'Has Baggage': has_baggage,
        'Online Check-in Used': False,
        'Kiosk Used': False,
        'Kiosk Choiced ID': None,
        'Time at Kiosk Choice': None,
        'Kiosk Used ID': None,
        'Kiosk Start': None,
        'Kiosk Finish Time': None,
        'Kiosk Used Length': None,
        'Counter Used': False,
        'Counter Choiced ID': None,
        'Time at Counter Choice': None,
        'Counter Used ID': None,
        'Counter Start': None,
        'Counter Finish Time': None,
        'Counter Used Length': None,
        'Check-in Finish Time': None,
        'Check In Length': None,
        'SC Line Choiced ID': None,
        'Time at SC Line Choice': None,
        'SC Line Used ID': None,
        'SC Start': None,
        'SC Finish Time': None,
        'SC Line Used Length': None,
        'IM Line Choiced ID': None,
        'Time at IM Line Choice': None,
        'IM Line Used ID': None,
        'IM Line Start': None,
        'IM Line Finish Time': None,
        'IM Line Used Length': None,
        'Departure Area Arrival Time': None
    }

    # Start the check-in process based on choice
    if check_in_choice == 'online':
        log_row['Online Check-in Used'] = True

        # If the passenger has baggage, they still need to go to a counter to drop it off
        if has_baggage:
            yield env.timeout(COUNTER_TRANSIT_TIME)  # Transit time to counter
            yield env.process(airport_departure_system.check_in_counter(name, has_baggage, log_row))
        else:
            yield env.timeout(PASS_THROUGH_TRANSIT_TIME)  # Transit time for passengers with no baggage

        log_row['Check-in Finish Time'] = env.now  # Record check-in finish time

    elif check_in_choice == 'kiosk':
        yield env.timeout(KIOSK_TRANSIT_TIME)  # Transit time to reach kiosk
        yield env.process(airport_departure_system.check_in_kiosk(name, has_baggage, log_row))

    else:  # 'counter' check-in
        yield env.timeout(COUNTER_TRANSIT_TIME)  # Transit time to reach counter
        yield env.process(airport_departure_system.check_in_counter(name, has_baggage, log_row))

    # Calculate total check-in length
    log_row['Check In Length'] = log_row['Check-in Finish Time'] - log_row['Arrival Time']

    # Proceed to security check
    yield env.timeout(SC_TRANSIT_TIME)  # Transit time to reach security
    yield env.process(airport_departure_system.security_check(name, log_row))

    # Proceed to immigration check
    yield env.timeout(IM_TRANSIT_TIME)  # Transit time to reach immigration
    yield env.process(airport_departure_system.immigration_check(name, log_row))

    # Log the final arrival time at the departure area
    log_row['Departure Area Arrival Time'] = env.now

    # Append the passenger log once the entire process is complete
    passenger_log.append(log_row)

def passenger_arrivals(env, num_passengers, airport_departure_system):
    """Simulates passengers arriving within the first n minutes."""
    for i in range(num_passengers):
        passenger_name = f"Passenger_{i+1}"

        # Start a new passenger process
        env.process(passenger(env, passenger_name, airport_departure_system))

        # Time between arrivals (n minutes / number of passengers to ensure all arrive in first 10 minutes)
        yield env.timeout(ARRIVAL_WINDOW / num_passengers)  # This will spread passengers evenly across the n-minute window
