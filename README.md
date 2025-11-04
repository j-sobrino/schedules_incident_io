Run with Python:
python3 render-schedule --schedule=schedule.json --overrides=overrides.json --from='2025-11-07T17:00:00Z' --until='2025-11-21T17:00:00Z'

On Unix/Linux/macOS (after chmod +x render-schedule):
./render-schedule --schedule=schedule.json --overrides=overrides.json --from='2025-11-07T17:00:00Z' --until='2025-11-21T17:00:00Z'

Example files are included: schedule.json and overrides.json

All parameters have default values, so you can run with just:
python3 render-schedule
or
./render-schedule