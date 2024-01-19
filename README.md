# mad_calendar
Python tool to access UW-Madison Course Schedule app and create an .ics file that can be loaded into a wide variety of calendar apps.

## How it works
- mad_calender uses Selenium, a Python web driver package, to access your Course Schedule app and filters through the page content to find the data about your classes.
- It then filters through the data and puts it into a format called iCal, in an .ics file.
- This file can be uploaded into the calendar app of your choice, provided it supports iCal format.

## Usage
### Prerequisites
- Selenium
- Python3
## How to use
- Download the source code from the GitHub repository, and upzip the folder
- Navigate into the src folder, and install Selenium using (pip install selenium)
- Run main.py in the src folder (python main.py on Windows). Your .ics file will be generated in the "output" folder.

### I need testers for this program, please let me know if you run into any issues with it.
