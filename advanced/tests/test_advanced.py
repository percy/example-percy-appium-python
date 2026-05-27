"""PER-8195 Phase 2 — appium-python advanced example.

Each test exercises one row of the App Percy / Appium Native matrix.
See ../matrix.yml for the canonical mapping.

Run against the BrowserStack App Automate hub. Requires AA_USERNAME,
AA_ACCESS_KEY, APP env vars. See ../README.md.
"""

import time
from appium.webdriver.common.appiumby import AppiumBy
from percy import percy_screenshot
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def test_exercises_baseline_screenshot(driver):
    time.sleep(5)
    percy_screenshot(driver, "Wikipedia Home")


def test_exercises_device_name_and_orientation(driver):
    percy_screenshot(
        driver,
        "Wikipedia Home — landscape",
        device_name="Google Pixel 6",
        orientation="landscape",
    )


def test_exercises_fullscreen_and_bars(driver):
    percy_screenshot(
        driver,
        "Wikipedia Home — fullscreen",
        fullscreen=True,
        status_bar_height=24,
        nav_bar_height=0,
    )


def test_exercises_ignore_regions_xpaths(driver):
    percy_screenshot(
        driver,
        "Wikipedia Home — ignore via xpath",
        ignore_regions_xpaths=['//android.widget.TextView[@text="Search Wikipedia"]'],
    )


def test_exercises_ignore_region_appium_elements(driver):
    el = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "Search Wikipedia"))
    )
    percy_screenshot(
        driver,
        "Wikipedia Home — ignore via appium element",
        ignore_region_appium_elements=[el],
    )


def test_exercises_custom_ignore_regions(driver):
    percy_screenshot(
        driver,
        "Wikipedia Home — custom ignore region",
        custom_ignore_regions=[{"top": 0, "bottom": 100, "left": 0, "right": 300}],
    )


def test_exercises_consider_regions_xpaths(driver):
    percy_screenshot(
        driver,
        "Wikipedia Home — consider via xpath",
        consider_regions_xpaths=['//android.widget.TextView[@text="Search Wikipedia"]'],
    )


def test_exercises_sync_mode(driver):
    # sync=True blocks until Percy returns the comparison result for this
    # screenshot, so percy_screenshot hands back that result instead of None.
    result = percy_screenshot(driver, "Wikipedia Home — sync", sync=True)
    print(f"sync screenshot comparison result: {result}")
    assert result is not None


def test_exercises_test_case_and_labels(driver):
    percy_screenshot(
        driver,
        "Wikipedia Home — test_case + labels",
        test_case="home-smoke",
        labels="smoke,appium-python",
    )
