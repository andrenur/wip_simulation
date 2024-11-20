# analyze_results.py
from src import passenger_log

# Example: analyze the log
def analyze_logs(log):
    for entry in log:
        print(f"Passenger: {entry['Passenger']}, Check-in Finish Time: {entry['Check-in Finish Time']}")

# Call the analysis function
analyze_logs(passenger_log)
