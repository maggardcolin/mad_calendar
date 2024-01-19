class Course():
    def __init__(self, class_name: str, lecture_num: str, location: str, start_date: str, 
                 end_date: str, year: str, start_time: str, end_time: str, day_of_week: str = ""):
        self.class_name = class_name
        self.lecture_num = lecture_num
        self.location = location
        self.start_date = start_date
        self.end_date = end_date
        self.year = year
        self.start_time = start_time
        self.end_time = end_time
        self.day_of_week = []
        self.day_of_week.append(day_of_week)
    
    def add_day(self, day_of_week):
        self.day_of_week.append(day_of_week)