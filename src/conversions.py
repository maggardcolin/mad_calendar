from datetime import datetime, timedelta

def shorten_day(day):
    days = {
        'Sun': 'SU',
        'Mon': 'MO',
        'Tue': 'TU',
        'Wed': 'WE',
        'Thu': 'TH',
        'Fri': 'FR',
        'Sat': 'SA',
    }
    return days.get(day, 'Invalid Day')

def time_code(original_time):
    timecode = ""
    timefields = original_time.split(" ")
    hour = timefields[0].split(":")[0]
    minutes = timefields[0].split(":")[1]
    if timefields[1] == "PM":
        hour = str(int(hour) + 12)
    else:
        if int(hour) < 10:
            hour = "0" + hour
    timecode = hour+minutes+"00"
    return timecode

def next_matching_day(datecode: str, days):
    current_date = datetime.strptime(datecode, "%Y%m%d")
    full_names = {
        'Sun': 'Sunday',
        'Mon': 'Monday',
        'Tue': 'Tuesday',
        'Wed': 'Wednesday',
        'Thu': 'Thursday',
        'Fri': 'Friday',
        'Sat': 'Saturday',
    }

    weekdays = [full_names[code] for code in days]

    day_codes_set = set(weekdays)

    while True:
        day_of_week = current_date.strftime('%A')

        if day_of_week in day_codes_set:
            return current_date.strftime("%Y%m%d")

        current_date += timedelta(days=1)

def month_to_number(month):
    months_dict = {
        'Jan': '01',
        'Feb': '02',
        'Mar': '03',
        'Apr': '04',
        'May': '05',
        'Jun': '06',
        'Jul': '07',
        'Aug': '08',
        'Sep': '09',
        'Oct': '10',
        'Nov': '11',
        'Dec': '12'
    }
    return months_dict.get(month, 'Invalid Month')