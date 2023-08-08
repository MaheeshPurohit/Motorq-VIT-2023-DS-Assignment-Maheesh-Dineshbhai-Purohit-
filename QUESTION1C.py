import pandas as pd

# Load datasets
telemetry_data = pd.read_csv('telemetry_data.csv')
triggers_soc = pd.read_csv('triggers_soc.csv')
vehicle_pnid_mapping = pd.read_csv('vehicle_pnid_mapping.csv')
ignition_off_data = pd.read_json('artificial_ign_off_data.json')

# Merge mapping to telemetry data
telemetry_data = telemetry_data.merge(vehicle_pnid_mapping, left_on='VEHICLE_ID', right_on='ID', how='left')

# Create ignition event table
ignition_events = pd.DataFrame(columns=['vehicle_id', 'timestamp', 'event'])

for idx, row in triggers_soc.iterrows():
    if row['NAME'] == 'IGN_CYL':
        event = 'ignitionOn' if row['VAL'] == 'ON' else 'ignitionOff'
        matching_rows = telemetry_data[telemetry_data['IDS'] == row['PNID']]
        if not matching_rows.empty:
            vehicle_id = matching_rows.iloc[0]['VEHICLE_ID']
            timestamp = row['CTS']
            ignition_events = ignition_events.append({'vehicle_id': vehicle_id, 'timestamp': timestamp, 'event': event}, ignore_index=True)

# Generate ignitionOff events from artificial_ign_off_data.json
for _, off_event in ignition_off_data.iterrows():
    ignition_events = ignition_events.append({'vehicle_id': off_event['vehicleId'], 'timestamp': off_event['timestamp'], 'event': 'ignitionOff'}, ignore_index=True)

# Perform additional analysis and insights
# ...

# Save results or export tables
ignition_events.to_csv('ignition_events.csv', index=False)
