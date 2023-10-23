import datetime


def insert_to_date_place_omission(params):
    try:
        print('Inserting data into the Offense Violation Library...')

        for place in params["place_of_omission"]:
            print(place)

        # omission = PlaceOfOmission(place=place['place_of_omission'])
        # omission.save()

    except Exception as e:
       print(f'An error occurred: {e}')


def get_format_date():
    try:
        cur_date = datetime.datetime.now()
        # Format the current date and time as "YYYY-MM-DD HH:MM"
        formatted_datetime = cur_date.strftime('%Y-%m-%d %H:%M')
        print(f'\n\nFORMATTED DATE: {formatted_datetime}\n\n')
        return formatted_datetime
    except Exception as e:
        return f"Error: {e}"


if __name__ == '__main__':
    data = {
        "offense": "Violation of R.A 7877 (Anti-Sexual Harassment Act of 1995) and R.A 11313 (Safe Spaces Act)",
        "place_of_omission": ["CJVAB, Pasay City", get_format_date()],
        "punishment": "Restriction within CJVAB and to certain specified limits without suspension from duty and/or any activities for sixty (60) consecutive days.",
        "rank": "AM",
        "afpsn": "987960",
        "last": "Bulahan",
        "first": "Eugene",
        "middle": "Lugatiman"
    }

    # self.insert_to_punishment(data)
    # self.insert_to_offense(data)
    insert_to_date_place_omission(data)
    # self.insert_to_afp_personnel(data)
