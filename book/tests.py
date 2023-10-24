from datetime import datetime

def format_date(input_date):
    try:
        # Parse the input date string to a datetime object
        input_datetime = datetime.strptime(input_date, "%Y-%m-%dT%H:%M:%SZ")

        # Format the datetime object as "YYYY-MM-dd"
        formatted_date = input_datetime.strftime("%Y-%m-%d")

        return formatted_date
    except ValueError as e:
        return f"Error: {e}"


if __name__ == '__main__':
    date = "2023-10-23T06:28:00Z"
    formatted_date = format_date(date)
    print(f"Original date: {date}")
    print(f"Formatted date: {formatted_date}")
