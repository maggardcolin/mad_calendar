import re, csv
from course import Course
from conversions import shorten_day, time_code, next_matching_day, month_to_number

def load_courses(driver):
    html = driver.page_source
    courses = []
    pattern = r'(<div class="tt-activity".*?>.*?<\/div>\s*<\/div>\s*<\/div>)|(role="rowheader">(Sun|Mon|Tue|Wed|Thu|Fri|Sat))'
    match_results = re.finditer(pattern, html, re.DOTALL)
    output = ""
    for match in match_results:
        text = match.group()
        text = re.sub("<.*?>", "\"", text)
        text = re.sub("role=\"rowheader\">", "", text)
        text = re.sub("&nbsp;", " ", text)
        text = re.sub("\"\"\"", "\"", text)
        text = re.sub("\"\"", "\",\"", text)
        output += text + "\n"

    lines = output.strip().split("\n")
    line_index = 1
    day_of_week = ""
    line_index = 0
    already_done = False

    while line_index < len(lines):
        line = lines[line_index]
        if line in ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]:
            day_of_week = line
            line_index += 1
            continue
        else:
            fields = next(csv.reader([line]))
            class_name = fields[0]
            for course in courses: 
                if class_name == course.class_name:
                    course.add_day(day_of_week)
                    already_done = True
            event_day = day_of_week
            lecture_num = fields[1]
            location = fields[2]
            date_string = fields[3].split(", ")
            dates = date_string[0].split(" - ")
            start_date = dates[0]
            end_date = dates[1]
            year = date_string[1]
            times = fields[4].split(" to ")
            start_time = times[0]
            end_time = times[1]
            line_index += 1
            course = Course(class_name, lecture_num, location, start_date, end_date, year, start_time, end_time, day_of_week)
            if not already_done:
                courses.append(course)
            else:
                already_done = False
    print("Courses loaded. Creating .ics file...")
    return courses

def create_calendar(classes):
    with open('./output/calendar.ics', 'w') as file:
        file.write("BEGIN:VCALENDAR\n")
        file.write("VERSION:2.0\n")
        file.write("PRODID:-//Colin Maggard//mad_calendar//EN\n") 
        file.write("CALSCALE:GREGORIAN\n")
        for course in classes:
            file.write("BEGIN:VEVENT\n")
            file.write("SUMMARY:" + course.class_name + " " + course.lecture_num + "\n")
            days = ""
            day_codes = ""
            for day in course.day_of_week:
                days += day
                day_codes += shorten_day(day)
                if day != course.day_of_week[-1]:
                    days += ", "
                    day_codes += ","
            file.write("DESCRIPTION:\n")
            end_code = course.year + month_to_number(course.end_date[:3]) + course.end_date[4:6]
            file.write("RRULE:FREQ=WEEKLY;UNTIL=" + end_code + "T234500Z;BYDAY=" + day_codes + "\n")
            datecode = next_matching_day(course.year + month_to_number(course.start_date[:3]) + course.start_date[4:6], course.day_of_week)
            file.write("DTSTART;TZID=America/Chicago:" + datecode + "T" + time_code(course.start_time) + "\n")
            file.write("DTEND;TZID=America/Chicago:" + datecode + "T" + time_code(course.end_time) + "\n")
            file.write("LOCATION:" + course.location + "\n")
            file.write("SEQUENCE:0\n")
            file.write("STATUS:CONFIRMED\n")
            file.write("TRANSP:OPAQUE\n")
            file.write("END:VEVENT\n")
        file.write("END:VCALENDAR\n")
        print("Schedule uploaded to .ics file.\nUpload this to Google Calendar or other calendars that support .ics format to see your classes. Go Badgers!")
        print("Google Calendar: https://calendar.google.com/calendar/u/0/r/settings/export")
