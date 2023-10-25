from datetime import datetime

def format_date(input_date):
    try:
        print(f'RECEIVED DATE: {input_date}\n\n')
        # Parse the input date string to a datetime object
        input_datetime = datetime.strptime(input_date, "%Y-%m-%dT%H:%M:%SZ")

        # Format the datetime object as "YYYY-MM-dd"
        return input_datetime.strftime("%Y-%m-%d %H:%M:%S")

    except ValueError as e:
        print(f"Error: {e}")
        return input_date


def date_formatter2(input_date):
    try:
        # Parse the input date string to a datetime object
        input_datetime = datetime.strptime(input_date, "%Y-%m-%dT%H:%M:%S%z")

        # Format the datetime object as "YYYY-MM-dd HH:mm:ss"
        return input_datetime.strftime("%Y-%m-%d %H:%M:%S")

    except ValueError as e:
        print(f'An error occurred: {str(e)}')
        return input_date


if __name__ == '__main__':
    date = "2023-10-23T06:28:00Z"
    formatted_date = format_date(date)
    print(f"Original date: {date}")
    print(f"Formatted date: {formatted_date}")
