from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
from pathlib import Path
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.remote.webdriver import WebElement

import time

class SeleniumUtils:
    def __init__(self):
        self.driver = self.initialize_driver()
        
    def get_actions(self):
        self.actions = ActionChains(self.driver)
        return self.actions
        
    def initialize_driver(self):
        
        print("Initializing... ")
        
        chrome_options = webdriver.ChromeOptions()

        # Add a user-agent to prevent getting blocked
        chrome_options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        )

        driver = webdriver.Chrome(options=chrome_options)
        return driver
    
    def get_with_wait(self, wait= 10):
        return WebDriverWait(self.driver, wait)
    
    def get_element(self, tag_name, element_name):
        return EC.presence_of_element_located((tag_name, element_name))
    
    def retrieve_attribute(self, attribute: WebElement):
        return attribute.text if attribute.is_displayed() else ''