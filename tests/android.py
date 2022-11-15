from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from percy import percy_screenshot

USER_NAME = "App Automate User Name"
ACCESS_KEY = "App Automate Access key"


def run_session(capability):
    driver = webdriver.Remote(f'https://{USER_NAME}:{ACCESS_KEY}@hub-cloud.browserstack.com/wd/hub', capability)
    percy_screenshot(driver, 'screenshot 1')

    search_element = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "Search Wikipedia"))
    )
    search_element.click()
    search_input = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable(
            (AppiumBy.ID, "org.wikipedia.alpha:id/search_src_text")
        )
    )
    search_input.send_keys("BrowserStack")
    percy_screenshot(driver, 'screenshot 2')

    driver.quit()


if __name__ == '__main__':
    galaxy_s8_capability = {
        "build": "android-builds",
        "deviceName": "Google Pixel 4",
        "app": '<APP URL>',
        "percy:options": {
            "enabled": True
        },
        "platformName": "android",
        "sessionName": "first-session"
    }

    capabilities_list = [galaxy_s8_capability]
    print(list(map(run_session, capabilities_list)))
