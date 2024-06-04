import os
import time
import logging
import undetected_chromedriver as uc
import pyperclip
import platform
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.core.utils import ChromeType
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException


class LeetCodeAutomation:
    def __init__(self,
                 driver_path: str = None,
                 driver_options: str = None,
                 use_headless: bool = False,
                 user_name: str = None,
                 user_password: str = None,
                 website_url: str = None,
                 is_verbose: bool = False,
                 use_incognito: bool = False,
                 bypass_login: bool = False,
                 chrome_user_data: str = None,
                 auth_method: str = 'normal'):
        self.use_headless = use_headless

        if not bypass_login:
            if not user_name or not user_password:
                logging.warning(
                    "Username and password are necessary unless bypassing login."
                )
                raise ValueError(
                    'Please supply both username and password.'
                )
            user_name = user_name
            user_password = user_password

        self.website_url = website_url or "https://leetcode.com/accounts/login"
        self.problem_url = "https://leetcode.com/problems/"
        if is_verbose:
            logging.getLogger().setLevel(logging.INFO)
            logging.info('Verbose mode is on')

        chrome_options = uc.ChromeOptions()
        chrome_options.headless = self.use_headless
        if use_incognito:
            chrome_options.add_argument('--incognito')
        if driver_options:
            for option in driver_options:
                chrome_options.add_argument(option)

        logging.info('Starting undetected Chrome Driver')
        self.driver = uc.Chrome(
            user_data_dir=chrome_user_data,
            driver_executable_path=driver_path,
            options=chrome_options,
            headless=use_headless,
            log_level=logging.INFO,
        )
        user_agent = self.driver.execute_script("return navigator.userAgent")
        self.driver.execute_cdp_cmd(
            'Network.setUserAgentOverride',
            {"userAgent": user_agent.replace('Headless', '')}
        )
        self.driver.set_page_load_timeout(15)

        logging.info('Opening LeetCode website')
        self.driver.get(self.website_url)

        if not bypass_login and auth_method == 'normal':
            self.standard_login(user_name, user_password)
        elif not bypass_login and auth_method == 'manually':
            self.manual_login(user_name, user_password)

    def standard_login(self, username, password):
        time.sleep(2)
        email_input = self.wait_find_element(By.ID, 'id_login')
        email_input.send_keys(username)
        logging.info('Username entered')

        password_input = self.wait_find_element(By.ID, 'id_password')
        password_input.send_keys(password)
        logging.info('Password entered')

        login_button = self.wait_find_element(By.ID, 'signin_btn')
        login_button.click()
        logging.info('Clicked on login button')
        time.sleep(1)

    def manual_login(self, username, password, timeout: int = 15):
        if "login" in self.driver.current_url:
            time.sleep(2)
            email_input = self.wait_find_element(By.ID, 'id_login')
            email_input.send_keys(username)
            logging.info('Username entered manually')

            password_input = self.wait_find_element(B
