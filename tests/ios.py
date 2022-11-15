import time

from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from percy import percy_screenshot

USER_NAME = "App Automate User Name"
ACCESS_KEY = "App Automate Access key"


def run_session(capability):
    driver = webdriver.Remote("https://" + USER_NAME + ":" + ACCESS_KEY + "@hub-cloud.browserstack.com/wd/hub",
                              capability)
    time.sleep(2)
    percy_screenshot(driver, 'screenshot 1')
    text_button = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "Text Button"))
    )
    text_button.click()
    text_input = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "Text Input"))
    )
    text_input.send_keys("hello@browserstack.com" + "\n")
    time.sleep(2)
    percy_screenshot(driver, 'screenshot 2')
    driver.quit()


if __name__ == '__main__':
    ios_capability = {
        "build": "ios-builds",
        "deviceName": "iPhone 14",
        "os_version": "16",
        "app":  '<APP URL>',
        "percy:options": {
            "enabled": True
        },
        "platformName": "ios",
        "sessionName": "v0.0.1"
    }

    capabilities_list = [ios_capability]
    list(map(run_session, capabilities_list))
