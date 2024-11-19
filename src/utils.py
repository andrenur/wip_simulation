import random
from src.config import setup_parameters

def get_checkin_time_counter():
    return random.expovariate(1.0 / setup_parameters['CHECKIN_TIME']['counter'])

def get_checkin_time_kiosk():
    return random.expovariate(1.0 / setup_parameters['CHECKIN_TIME']['kiosk'])

def get_security_time():
    return random.expovariate(1.0 / setup_parameters['SECURITY_TIME'])

def get_immigration_time():
    return random.expovariate(1.0 / setup_parameters['IMMIGRATION_TIME'])

def choose_shortest_counter(airport_departure_system):
    # Select the counter with the shortest queue or a completely free counter
    return min(airport_departure_system.counters, key=lambda counter: (len(counter.queue), counter.count))

def choose_shortest_kiosk(airport_departure_system):
    # Select the kiosk with the shortest queue or a completely free kiosk
    return min(airport_departure_system.kiosks, key=lambda kiosk: (len(kiosk.queue), kiosk.count))

def choose_shortest_security_line(airport_departure_system):
    # Select the security line with the shortest queue or a completely free line
    return min(airport_departure_system.security_lines, key=lambda security_line: (len(security_line.queue), security_line.count))

def choose_shortest_immigration_line(airport_departure_system):
    # Select the immigration line with the shortest queue or a completely free line
    return min(airport_departure_system.immigration, key=lambda immigration_line: (len(immigration_line.queue), immigration_line.count))
