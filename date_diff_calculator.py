#!/usr/bin/env python3
import argparse
from datetime import datetime

def parse_date(date_str):
    try:
        return datetime.strptime(date_str, "%d%m%Y")
    except ValueError:
        raise argparse.ArgumentTypeError(
            f"Invalid date format for '{date_str}'. Expected format is ddmmyyyy."
        )

class DateDifferenceCalculator:
    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date

    def calculate(self):
        # Compute the difference in days as a float
        delta = self.end_date - self.start_date
        total_days = float(delta.days)
        total_weeks = total_days / 7.0
        # Using 30.44 as an average month length:
        total_months = total_days / 30.44
        return total_days, total_weeks, total_months

    def combined_output(self, total_days, total_weeks, total_months):
        return (f"Total difference: {total_days:.2f} days, "
                f"{total_weeks:.2f} weeks, {total_months:.2f} months.")

def main():
    parser = argparse.ArgumentParser(
        description="Calculate the difference between two dates (format ddmmyyyy) in days, weeks, and months."
    )
    parser.add_argument("--from", dest="from_date", type=parse_date, required=True,
                        help="Start date in ddmmyyyy format")
    parser.add_argument("--to", dest="to_date", type=parse_date, required=True,
                        help="End date in ddmmyyyy format")
    args = parser.parse_args()

    calculator = DateDifferenceCalculator(args.from_date, args.to_date)
    days, weeks, months = calculator.calculate()

    print("Detailed Difference:")
    print(f"Total days  : {days:.2f}")
    print(f"Total weeks : {weeks:.2f}")
    print(f"Total months: {months:.2f}")
    print(calculator.combined_output(days, weeks, months))

if __name__ == "__main__":
    main()
