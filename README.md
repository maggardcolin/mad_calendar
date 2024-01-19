# mad_calendar
Python tool to access UW-Madison Course Schedule app and create an .ics file that can be loaded into a wide variety of calendar apps.

## How it works
- mad_calender uses Selenium, a Python web driver package, to access your Course Schedule app and filters through the page content to find the data about your classes.
- It then filters through the data and puts it into a format called iCal, in an .ics file.
- This file can be uploaded into the calendar app of your choice, provided it supports iCal format.

## Usage
- Download the source code from the GitHub repository, then run main.py in the src folder. Your .ics file will be generated in the "output" folder.

### I need testers for this program, please let me know if you run into any issues with it.
