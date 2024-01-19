# hours logged: 7:00 PM - 3:00 AM 7 hours
import re, csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from conversions import *
from course import Course

headless = True

def fill_form_value(element_id, value):
    element = driver.find_element(By.ID, element_id)
    element.send_keys(value)    

def loadCourses():
    print("Loading courses...")
    html = driver.page_source
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
            for course in classes: 
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
                classes.append(course)
            else:
                already_done = False
    print("Courses loaded.")

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

def createCalendar():
    with open('./output/calendar.ics', 'w') as file:
        file.write("BEGIN:VCALENDAR\n")
        file.write("VERSION:2.0\n")
        file.write("PRODID:-//Colin Maggard//MadCalendar//EN\n") 
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
        print("Schedule made. Go Badgers!")

if headless:
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
else:
    driver = webdriver.Chrome()

classes = []

driver.get("https://go.wisc.edu/76k189")

wait = WebDriverWait(driver, 10)
timeout = 20

while True:
    username = str(input("What is your username? "))
    password = str(input("What is your password? "))
    fill_form_value("j_username", username)
    fill_form_value("j_password", password)
    submit_button = driver.find_element(By.NAME, "_eventId_proceed")
    submit_button.click()
    try:
        element_on_next_page = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "auth-view-wrapper"))
        )
        print("Username and password correct.")
        break
    except TimeoutException:
        print("Wrong username or password, try again.")
    finally:
        pass
try:
    element_on_next_page = WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located((By.ID, "trust-browser-button"))
    )
    print("Duo Mobile request accepted.")
    trust_button = driver.find_element(By.ID, "trust-browser-button")
    trust_button.click()
except TimeoutException:
    print("Timed out waiting for Duo Mobile request to be approved.")
    driver.quit()
finally:
    pass
try:
    element_on_next_page = WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located((By.ID, "portalPageBody"))
    )
    print("Schedule page has loaded successfully.")
    loadCourses()
    createCalendar()
except TimeoutException:
    print("Timed out waiting for the schedule page to load.")
    driver.quit()
finally:
    pass