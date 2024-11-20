# Import main classes from the simulation module
from .simulation import (
    AirportDepartureTerminal,
    passenger,
    passenger_arrivals,
)

# Import constants, configurations, and timing functions from the config module
from .config import (
    COUNTER_TRANSIT_TIME,
    KIOSK_TRANSIT_TIME,
    SC_TRANSIT_TIME,
    IM_TRANSIT_TIME,
    DEPARTURE_TRANSIT_TIME,
    ARRIVAL_WINDOW,
    get_checkin_time_counter,
    get_checkin_time_kiosk,
    get_security_check_time,
    get_immigration_time,
)

# Import utility functions for resource selection
from .utils import (
    get_checkin_time_counter,
    get_checkin_time_kiosk,
    get_security_time,
    get_immigration_time,
    choose_shortest_counter,
    choose_shortest_kiosk,
    choose_shortest_security_line,
    choose_shortest_immigration_line,
)

# Expose the passenger log (if managed globally within the simulation)
from .simulation import passenger_log

# Define package-level exports
__all__ = [
    # Classes
    "AirportDepartureTerminal",
    # Passenger and arrival functions
    "passenger",
    "passenger_arrivals",
    # Configuration constants and functions
    "COUNTER_TRANSIT_TIME",
    "KIOSK_TRANSIT_TIME",
    "SC_TRANSIT_TIME",
    "IM_TRANSIT_TIME",
    "DEPARTURE_TRANSIT_TIME",
    "ARRIVAL_WINDOW",
    "get_checkin_time_counter",
    "get_checkin_time_kiosk",
    "get_security_check_time",
    "get_immigration_time",
    # Utility functions
    "choose_shortest_counter",
    "choose_shortest_kiosk",
    "choose_shortest_security_line",
    "choose_shortest_immigration_line",
    # Logs
    "passenger_log",
]
