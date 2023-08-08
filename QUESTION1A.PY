import pandas as pd
import json

# Read telemetry_data.csv
telemetry_data = pd.read_csv('telemetry_data.csv')

# Initialize previous ignition status
prev_ignition_status = None

# Initialize lists to store generated ignition events
ignition_events = []

# Iterate through telemetry data
for index, row in telemetry_data.iterrows():
    current_ignition_status = row['IGNITION_STATUS']
    
    if prev_ignition_status is not None and current_ignition_status != prev_ignition_status:
        if current_ignition_status == 'Off':
            ignition_events.append({'Previous state': 'On', 'Current state': 'Off', 'Event': 'ignitionOff'})
        elif current_ignition_status == 'On':
            ignition_events.append({'Previous state': 'Off', 'Current state': 'On', 'Event': 'ignitionOn'})
    
    prev_ignition_status = current_ignition_status

# Read triggers_soc.csv
triggers_data = pd.read_csv('triggers_soc.csv')

# Filter and process IGN_CYL events
ignition_triggers = triggers_data[triggers_data['NAME'] == 'IGN_CYL']
for index, row in ignition_triggers.iterrows():
    ignition_events.append({'Previous state': row['VAL'], 'Current state': row['VAL'], 'Event': f'ignition{row["VAL"]}'})
    
# Read artificial_ign_off_data.json
with open('artificial_ign_off_data.json', 'r') as json_file:
    ign_off_data = json.load(json_file)

# Process artificial ignitionOff events
for entry in ign_off_data:
    ignition_events.append({'Previous state': 'On', 'Current state': 'Off', 'Event': 'ignitionOff', 'Timestamp': entry['timestamp']})

# Create a DataFrame with generated ignition events
ignition_events_df = pd.DataFrame(ignition_events)

# Save generated ignition events to a CSV file
ignition_events_df.to_csv('generated_ignition_events.csv', index=False)