import requests
from appium import webdriver
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import importlib
import session.config as cfg

def get_element_by_classtext_helper(driver, class_name, text):
    elements = driver.find_elements_by_class_name(class_name)
    for element in elements:
        if element.get_attribute('text') == text:
            return element

class TestClass:
    def test_one(self):
        # Test one: 9-Day forecast navigation
        app_path = os.path.abspath(cfg.app_name)

        desired_cap = cfg.desired_cap
        desired_cap["app"] = app_path

        # Create the driver instance
        driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_cap)
        wait = WebDriverWait(driver, 30)

        # Navigate through app
        driver.find_element_by_id('btn_agree').click()
        driver.find_element_by_id('btn_agree').click()

        # wait until pop-up appears and click through
        wait.until(EC.presence_of_element_located((By.ID, 'android:id/button1')))
        driver.find_element_by_id('android:id/button1').click()
        driver.find_element_by_id('com.android.permissioncontroller:id/permission_allow_always_button').click()

        # wait until pop-up apepars and click through
        wait.until(EC.presence_of_element_located((By.ID, 'btn_friendly_reminder_skip')))
        driver.find_element_by_id('btn_friendly_reminder_skip').click()
        driver.find_element_by_id('hko.MyObservatory_v1_0:id/btn_friendly_reminder_skip').click()
        driver.find_element_by_accessibility_id('Navigate up').click()

        # wait 2 seconds for navigation menu animation to complete
        time.sleep(2)
        driver.swipe(100, 800, 150, 200, 1000)

        # Locate the 9-days forecast menu and click
        nine_day_menu = get_element_by_classtext_helper(driver,'android.widget.TextView', cfg.nine_day)
        nine_day_menu.click()

        # Obtaining tomorrow's forecast
        nine_day_list = driver.find_elements_by_id('hko.MyObservatory_v1_0:id/sevenDayLinearLayout')
        content = nine_day_list[0].get_attribute('content-desc')

        # Check if content is extracted
        assert len(content) > 0

    def test_two(self):
        # test two: 9-day forecast API request and relative humidity

        response = requests.get(cfg.weather_api_url, params=cfg.weather_parameters)

        # Check response is successful
        assert (response.status_code == 200)

        day_after_tomorrow = response.json().get('weatherForecast')[2]

        # obtain minimum and maximum relative humidity
        minrh = day_after_tomorrow['forecastMinrh']['value']
        maxrh = day_after_tomorrow['forecastMaxrh']['value']
        day = day_after_tomorrow['week']

        # Check min relative humidity is equal or above 0 and max is equal or above min relative humidity
        assert float(minrh) >= 0
        assert float(maxrh) >= float(minrh)

        print("{}'s relative humidity will be: {}% - {}%".format(day, minrh, maxrh))





