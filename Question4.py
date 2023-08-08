import pandas as pd
import json

# Load telemetry_data.csv
telemetry_data = pd.read_csv('telemetry_data.csv')

# Load combined_events.csv
combined_events = pd.read_csv('combined_events.csv')

# Function to find closest timestamp within a time range
def find_closest_timestamp(df, target_timestamp, time_range_seconds):
    closest_row = df.iloc[(df['timestamp'] - target_timestamp).abs().idxmin()]
    time_difference = abs(pd.Timestamp(target_timestamp) - pd.Timestamp(closest_row['timestamp'])).total_seconds()
    if time_difference <= time_range_seconds:
        return closest_row
    return None

# Match EV battery level for each trigger event
matched_events = []
time_range_seconds = 300  # 300 seconds (5 minutes)

for idx, row in combined_events.iterrows():
    closest_telemetry_row = find_closest_timestamp(telemetry_data, row['TIMESTAMP'], time_range_seconds)
    if closest_telemetry_row is not None:
        matched_events.append({'vehicle_id': closest_telemetry_row['vehicle id'], 'timestamp': row['timestamp'], 'event': row['event'], 'charge': closest_telemetry_row['EV battery level']})

# Create DataFrame from matched events
final_dataset = pd.DataFrame(matched_events)

# Save final dataset
final_dataset.to_csv('final_dataset.csv', index=False)
