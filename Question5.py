import pandas as pd
import json

# Load final_dataset.csv
final_dataset = pd.read_csv('final_dataset.csv')

# Function to generate charging events based on battery level increase
def generate_charging_events(row, ignition_state):
    if row['event'] == 'ignitionOff':
        percentage_threshold = 1 if ignition_state == 'Off' else 3
        battery_increase = row['charge'] - prev_charge
        if battery_increase >= percentage_threshold:
            return 'charging'
    return 'not charging'

prev_charge = None
prev_ignition_state = None
charging_events = []

for idx, row in final_dataset.iterrows():
    if prev_charge is not None and prev_ignition_state is not None:
        charging_state = generate_charging_events(row, prev_ignition_state)
        charging_events.append({'vehicle_id': row['vehicle_id'], 'timestamp': row['timestamp'], 'charging_state': charging_state})
    prev_charge = row['charge']
    prev_ignition_state = prev_ignition_state if row['event'] == 'ignitionOff' else 'On'

# Create DataFrame from charging events
charging_events_df = pd.DataFrame(charging_events)

# Save charging events table
charging_events_df.to_csv('charging_events.csv', index=False)
