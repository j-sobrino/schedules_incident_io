import argparse


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

if __name__ == "__main__":
    main()