# main.py
import sys
import os
from pathlib import Path

# Add the src directory to sys.path
sys.path.append(os.path.join(os.getcwd(), "src"))
print("sys.path:", sys.path)

from src import (
    AirportDepartureTerminal,
    passenger,
    COUNTER_TRANSIT_TIME,
    choose_shortest_counter,
    passenger_log,
)
import simpy  # If using SimPy for simulation

# Initialize the simulation environment
env = simpy.Environment()

# Configure and initialize the airport terminal
num_counters = 5
num_kiosks = 3
num_sc_lines = 4
num_immigration = 2

airport = AirportDepartureTerminal(env, num_counters, num_kiosks, num_sc_lines, num_immigration)

# Run the simulation
env.process(passenger(env, "Passenger_1", airport))
env.run(until=100)  # Run for 100 time units

# Output the passenger log
print(passenger_log)
