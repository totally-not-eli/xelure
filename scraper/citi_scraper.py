from utils.selenium_helper import *

class CitiScraper(SeleniumUtils):
    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date
