from datetime import datetime
import pytz
from django.utils import timezone

class DateFormatter:
    def __init__(self, input_date, format_date=''):
        self.date = input_date
        self.format = format_date

    def format_date_make_aware(self):
        print(f'RECEIVED DATE FOR TIMEZONE AWARE: {self.date}\n\n')
        naive_datetime = datetime.strptime(self.date, str(self.format))
        return timezone.make_aware(naive_datetime, timezone=pytz.UTC)

    def format_date(self):
        try:
            print(f'RECEIVED DATE: {self.date}\n\n')
            # Parse the input date string to a datetime object
            input_datetime = datetime.strptime(self.date, "%Y-%m-%dT%H:%M:%SZ")

            # Format the datetime object as "YYYY-MM-dd"
            return input_datetime.strftime("%Y-%m-%d %H:%M:%S")

        except ValueError as e:
            print(f"Error: {e}")
            return self.date

    def date_formatter2(self):
        try:
            # Parse the input date string to a datetime object
            input_datetime = datetime.strptime(self.date, "%Y-%m-%dT%H:%M:%S%z")

            # Format the datetime object as "YYYY-MM-dd HH:mm:ss"
            return input_datetime.strftime("%Y-%m-%d %H:%M:%S")

        except ValueError as e:
            print(f'An error occurred: {str(e)}')
            return self.date


if __name__ == '__main__':
    date = "2023-10-23T06:28:00Z"
    process_date = DateFormatter(date)
    formatted_date = process_date.date_formatter2()
    print(f"Original date: {date}")
    print(f"Formatted date: {formatted_date}")
