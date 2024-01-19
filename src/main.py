# drives program and handles selenium code
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from madcalendar import loadCourses, createCalendar

headless = True

def fill_form_value(element_id, value):
    element = driver.find_element(By.ID, element_id)
    element.send_keys(value)    

if headless:
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('log-level=3')
    driver = webdriver.Chrome(options=chrome_options)
else:
    driver = webdriver.Chrome()

driver.get("https://go.wisc.edu/76k189")

wait = WebDriverWait(driver, 10)
timeout = 20

print("Welcome to mad_calendar! This is a tool to import your class schedule into Google Calendar.")
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
        print("Username and password correct. Sending Duo Push...")
        break
    except TimeoutException:
        print("Wrong username or password, try again.")
    finally:
        pass
try:
    element_on_next_page = WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located((By.ID, "trust-browser-button"))
    )
    print("Duo Mobile request approved. Loading Course Schedule page...")
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
    print("Schedule page has loaded successfully. Loading courses...")
    courses = loadCourses(driver)
    createCalendar(courses)
except TimeoutException:
    print("Timed out waiting for the schedule page to load.")
    driver.quit()
finally:
    pass