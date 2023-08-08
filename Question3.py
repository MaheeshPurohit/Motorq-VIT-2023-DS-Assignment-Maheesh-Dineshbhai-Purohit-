import pandas as pd

# Load generated_ignition_events.csv and ev_trigger_events.csv
ignition_events = pd.read_csv('generated_ignition_events.csv')
ev_trigger_events = pd.read_csv('ev_trigger_events.csv')

# Concatenate ignition and EV trigger events
combined_events = pd.concat([ignition_events, ev_trigger_events], ignore_index=True)

# Save combined events table
combined_events.to_csv('combined_events.csv', index=False)
