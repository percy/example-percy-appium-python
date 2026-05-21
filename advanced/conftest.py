"""PER-8195 — pytest fixtures: BrowserStack App Automate Android driver."""

import os
import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options


@pytest.fixture(scope="session")
def driver():
    caps = {
        "platformName": "Android",
        "deviceName": os.environ.get("DEVICE", "Google Pixel 6"),
        "app": os.environ["APP"],
        "bstack:options": {
            "userName": os.environ["AA_USERNAME"],
            "accessKey": os.environ["AA_ACCESS_KEY"],
            "projectName": os.environ.get("PERCY_PROJECT", "Percy Appium Python Advanced"),
            "buildName": os.environ.get("PERCY_BUILD", "Advanced Python Appium"),
        },
        "appium:percyOptions": {"enabled": True, "ignoreErrors": True},
    }
    options = UiAutomator2Options().load_capabilities(caps)
    drv = webdriver.Remote("https://hub-cloud.browserstack.com/wd/hub", options=options)
    yield drv
    drv.quit()
