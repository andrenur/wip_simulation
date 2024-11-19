import streamlit as st
from src.simulation import run_simulation
from src.config import setup_parameters

# Streamlit app interface
st.title("Airport Passenger Movement Simulation")

# Inputs for simulation parameters
NUM_PASSENGERS = st.number_input("Number of Passengers", value=setup_parameters['NUM_PASSENGERS'])
SIM_TIME = st.number_input("Simulation Time (minutes)", value=setup_parameters['SIM_TIME'])

# Run the simulation
if st.button("Run Simulation"):
    result_df = run_simulation(NUM_PASSENGERS, SIM_TIME)
    st.write(result_df)
    st.line_chart(result_df[['time', 'event']])  # Customize as needed
