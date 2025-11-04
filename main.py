import argparse
import json
from datetime import datetime, timedelta

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

def format_date(dt):
    # Format datetime to ISO 8601 with 'Z' suffix
    iso_str = dt.isoformat()
    # Replace +00:00 with Z for UTC
    if iso_str.endswith('+00:00'):
        return iso_str[:-6] + 'Z'
    return iso_str

def generate_base_schedule(schedule, from_date, until_date):
    users = schedule['users']
    handover_start_at = parse_date(schedule['handover_start_at'])
    handover_interval_days = schedule['handover_interval_days']
    schedule_entries = []
    
    current_handover = handover_start_at
    
    # If from_date is after handover_start_at then calculate the current handover
    if from_date > handover_start_at:
        days_since_start = (from_date - handover_start_at).days
        intervals_passed = days_since_start // handover_interval_days
        current_handover = handover_start_at + timedelta(days=intervals_passed * handover_interval_days)
        if current_handover > from_date:
            current_handover -= timedelta(days=handover_interval_days)
    
    # generaate schedule entries until we reach the until date
    while current_handover < until_date:
        intervals_since_start = (current_handover - handover_start_at).days // handover_interval_days
        user_index = intervals_since_start % len(users)
        
        next_handover = current_handover + timedelta(days=handover_interval_days)
        
        entry = {
            'user': users[user_index],
            'start_at': current_handover,
            'end_at': next_handover
        }
        schedule_entries.append(entry)
        
        current_handover = next_handover
    
    return schedule_entries

def apply_overrides(base_schedule, overrides):
    # Convert override dates to datetime objects
    parsed_overrides = []
    for override in overrides:
        parsed_overrides.append({
            'user': override['user'],
            'start_at': parse_date(override['start_at']),
            'end_at': parse_date(override['end_at'])
        })
    
    # Process each override
    schedule_entries = base_schedule
    for override in parsed_overrides:
        override_start = override['start_at']
        override_end = override['end_at']
        
        new_entries = []
        
        for entry in schedule_entries:
            entry_start = entry['start_at']
            entry_end = entry['end_at']
            
            if entry_end <= override_start or entry_start >= override_end:
                new_entries.append(entry)
            else:
                if entry_start < override_start:
                    new_entries.append({
                        'user': entry['user'],
                        'start_at': entry_start,
                        'end_at': override_start
                    })
                if entry_end > override_end:
                    new_entries.append({
                        'user': entry['user'],
                        'start_at': override_end,
                        'end_at': entry_end
                    })
        
        new_entries.append({
            'user': override['user'],
            'start_at': override_start,
            'end_at': override_end
        })
        
        schedule_entries = sorted(new_entries, key=lambda x: x['start_at'])
    
    return schedule_entries


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
    print(base_schedule)
    # Apply overrides to modify the schedule entries
    overridden_schedule = apply_overrides(base_schedule, parsed_overrides)

    # Convert datetime objects to strings for JSON output
    result = []
    for entry in overridden_schedule:
        result.append({
            'user': entry['user'],
            'start_at': format_date(entry['start_at']),
            'end_at': format_date(entry['end_at'])
        })
    
    # Output the final schedule as JSON
    print(json.dumps(result))
    

if __name__ == "__main__":
    main()