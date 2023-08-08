import pandas as pd

# Load triggers_soc.csv
triggers_soc = pd.read_csv('triggers_soc.csv')

# Filter EV trigger events (Active, Abort, Completed)
ev_trigger_events = triggers_soc[triggers_soc['NAME'] == 'EV_CHARGE_STATE']

# Select necessary columns and rename the 'Val' column to 'Event'
ev_trigger_events = ev_trigger_events[['CTS', 'VAL']].rename(columns={'VAL': 'Event'})

# Save results or export the EV trigger events table
ev_trigger_events.to_csv('ev_trigger_events.csv', index=False)
