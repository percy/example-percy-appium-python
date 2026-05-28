"""PER-8195 — pytest fixtures: BrowserStack App Automate Android/iOS driver.

Platform is selected via the PLATFORM env var ("android" | "ios"). Default
is "android" so existing CI rows keep working unchanged. The iOS pathway
points at the BStackSampleApp (or any iOS .ipa supplied via APP); the
Android pathway targets the Wikipedia app.
"""

import os
import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.options.ios import XCUITestOptions


@pytest.fixture(scope="session")
def driver():
    platform = os.environ.get("PLATFORM", "android").lower()
    if platform == "ios":
        caps = {
            "platformName": "iOS",
            "deviceName": os.environ.get("DEVICE", "iPhone 13"),
            "platformVersion": os.environ.get("OS_VERSION", "15"),
            "app": os.environ["APP"],
            "bstack:options": {
                "userName": os.environ["AA_USERNAME"],
                "accessKey": os.environ["AA_ACCESS_KEY"],
                "projectName": os.environ.get("BROWSERSTACK_PROJECT_NAME", "Percy Appium Python Advanced"),
                "buildName": os.environ.get("BROWSERSTACK_BUILD_NAME", "Advanced Python Appium iOS"),
            },
            "appium:percyOptions": {"enabled": True, "ignoreErrors": True},
        }
        options = XCUITestOptions().load_capabilities(caps)
    else:
        caps = {
            "platformName": "Android",
            "deviceName": os.environ.get("DEVICE", "Google Pixel 6"),
            "app": os.environ["APP"],
            "bstack:options": {
                "userName": os.environ["AA_USERNAME"],
                "accessKey": os.environ["AA_ACCESS_KEY"],
                "projectName": os.environ.get("BROWSERSTACK_PROJECT_NAME", "Percy Appium Python Advanced"),
                "buildName": os.environ.get("BROWSERSTACK_BUILD_NAME", "Advanced Python Appium Android"),
            },
            "appium:percyOptions": {"enabled": True, "ignoreErrors": True},
        }
        options = UiAutomator2Options().load_capabilities(caps)

    drv = webdriver.Remote("https://hub-cloud.browserstack.com/wd/hub", options=options)
    yield drv
    drv.quit()
