# test_simulation.py
from src import (
    AirportDepartureTerminal,
    passenger,
    COUNTER_TRANSIT_TIME,
    choose_shortest_counter,
    passenger_log,
)

def test_simulation():
    import simpy
    env = simpy.Environment()
    airport = AirportDepartureTerminal(env, 2, 2, 1, 1)

    env.process(passenger(env, "Test_Passenger", airport))
    env.run(until=50)

    assert len(passenger_log) > 0, "No passengers were logged!"
    print("Test passed.")
