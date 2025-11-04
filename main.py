import argparse
import json
from datetime import datetime

def parse_schedule(schedule_file):
    with open(schedule_file, 'r') as f:
        schedule_data = json.load(f)
    
    return schedule_data

def parse_overrides(overrides_file):
    with open(overrides_file, 'r') as f:
        overrides_data = json.load(f)
    
    return overrides_data

def parse_date(date_string):
    # Replace 'Z' with '+00:00' for UTC timezone compatibility
    if date_string.endswith('Z'):
        date_string = date_string[:-1] + '+00:00'
    
    return datetime.fromisoformat(date_string)

def generate_base_schedule(schedule, from_date, until_date):
    pass

def apply_overrides(base_schedule, overrides):
    pass


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--schedule", default="schedule.json")
    parser.add_argument("--overrides", default="overrides.json")
    parser.add_argument("--from", dest='from_date', default='2025-11-07T17:00:00Z')
    parser.add_argument("--until", dest='until_date', default='2025-11-21T17:00:00Z')
    return parser.parse_args()


def main():
    args = parse_args()

    print("Schedule file:", args.schedule)
    print("Overrides file:", args.overrides)
    print("From:", args.from_date)
    print("Until:", args.until_date)

    # Load and parse the schedule JSON file
    parsed_schedule = parse_schedule(args.schedule)
    print(parsed_schedule)
    # Load and parse the overrides JSON file
    parsed_overrides = parse_overrides(args.overrides)
    print(parsed_overrides)
    # Parse the from and until date strings into datetime objects
    from_date = parse_date(args.from_date)
    until_date = parse_date(args.until_date)
    print(from_date)
    print(until_date)
    # Generate base schedule entries from the schedule configuration
    base_schedule = generate_base_schedule(parsed_schedule, from_date, until_date)

    # Apply overrides to modify the schedule entries
    overridden_schedule = apply_overrides(base_schedule, parsed_overrides)

    # Output the final schedule as JSON
    print(json.dumps(overridden_schedule))
    

if __name__ == "__main__":
    main()