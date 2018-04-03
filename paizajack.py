# -*- coding: utf-8 -*-
import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.chrome.options import Options
import unittest, time, re

class JackPaiza(unittest.TestCase):
    def setUp(self):
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.binary_location = 'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(30)
        self.base_url = "https://paiza.jp/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_jack_paiza(self):
        wait = WebDriverWait(self.driver, 300)
        driver = self.driver
        driver.get(self.base_url + "/paizajack/")
        driver.find_element_by_css_selector("#lp_login_btn > img").click()
        wait.until(expected_conditions.element_to_be_clickable((By.ID, "user_email")))
        driver.find_element_by_id("user_email").click()
        driver.find_element_by_id("user_email").clear()
        driver.find_element_by_id("user_email").send_keys("XXX")
        driver.find_element_by_id("user_password").clear()
        driver.find_element_by_id("user_password").send_keys("XXX")
        driver.find_element_by_name("commit").click()
        print("START")
        driver.find_element_by_css_selector("#game_start_btn_wrap > a > img").click()
        driver.find_element_by_css_selector("p.program_execution_btn > a > img").click()
        self.assertEqual(u"コードを提出してもよろしいですか？", self.close_alert_and_get_its_text())
        while True:
            wait.until(expected_conditions.url_contains("summary") or expected_conditions.url_contains("error"))
            print("----------SUMMARY----------")
            time.sleep(3)
            driver.find_element_by_css_selector("#page_game_btn > p.page_game_retry_btn > a > img").click()
            driver.find_element_by_css_selector("p.program_execution_btn > a > img").click()
            self.assertEqual(u"コードを提出してもよろしいですか？", self.close_alert_and_get_its_text())
    
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException as e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
