"""PER-8195 Phase 2 — appium-python advanced example.

Each test exercises one row of the App Percy / Appium Native matrix.
See ../matrix.yml for the canonical mapping.

Run against the BrowserStack App Automate hub. Requires AA_USERNAME,
AA_ACCESS_KEY, APP env vars. See ../README.md.
"""

import os
import time

import pytest
from appium.webdriver.common.appiumby import AppiumBy
from percy import percy_screenshot
from percy.lib.ignore_region import IgnoreRegion
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


PLATFORM = os.environ.get("PLATFORM", "android").lower()
IS_IOS = PLATFORM == "ios"


def _set_orientation(driver, target, attempts=3):
    """Best-effort physical device rotation.

    The iOS XCUITest driver on remote hubs intermittently rejects rotation
    with "Unable To Rotate Device" (a known transient server-side error),
    so retry a few times. If it still won't rotate we return False and let
    the caller take the snapshot anyway with the `orientation` metadata —
    the row's intent is to exercise the snapshot option, and we never want a
    flaky rotation to fail the build.
    """
    last_err = None
    for _ in range(attempts):
        try:
            driver.orientation = target
            return True
        except WebDriverException as err:
            last_err = err
            time.sleep(2)
    print(f"warning: could not rotate device to {target}: {last_err}")
    return False

# Robust on-screen selectors per platform. On Android we target the Wikipedia
# feed's search bar by resource-id — resource-ids are locale-independent and
# present on the home screen, unlike content-desc/text which vary by locale
# and app build (e.g. there is no content-desc="Wikipedia" element). On iOS
# the app is the BrowserStack "Sample iOS" app; its first list row is a button
# whose accessibility id (name) is "Text Button" (label "Text"), so target
# that — `@name="Text"` matches nothing and silently yields an empty region.
ANDROID_REGION_XPATH = '//*[@resource-id="org.wikipedia.alpha:id/search_container"]'
IOS_REGION_XPATH = '//XCUIElementTypeButton[@name="Text Button"]'
REGION_XPATH = IOS_REGION_XPATH if IS_IOS else ANDROID_REGION_XPATH

# Accessibility id for the appium-element ignore-region row (Android only —
# the iOS XCUITest path can't read the element's "class" attribute, so that
# row is skipped on iOS). Android Wikipedia exposes "Search Wikipedia".
A11Y_ID = "Search Wikipedia"


def test_exercises_baseline_screenshot(driver):
    time.sleep(5)
    percy_screenshot(driver, "Wikipedia Home")


def test_exercises_device_name_and_orientation(driver):
    # Actually rotate the device — passing orientation="landscape" alone
    # is just metadata; without rotating, the snapshot would be identical to
    # the portrait baseline. Rotation is best-effort (see _set_orientation):
    # the snapshot is always captured so the row passes even when the iOS
    # hub transiently refuses to rotate.
    rotated = _set_orientation(driver, "LANDSCAPE")
    try:
        percy_screenshot(
            driver,
            "Wikipedia Home — landscape",
            device_name=os.environ.get("DEVICE", "Google Pixel 6"),
            orientation="landscape",
        )
    finally:
        if rotated:
            _set_orientation(driver, "PORTRAIT")


def test_exercises_fullscreen_and_bars(driver):
    # SDK key is `full_screen` (underscore); `fullscreen` is silently dropped.
    percy_screenshot(
        driver,
        "Wikipedia Home — fullscreen",
        full_screen=True,
        status_bar_height=24,
        nav_bar_height=0,
    )


def test_exercises_fullpage_with_bottom_scroll_offset(driver):
    # Full-page (scroll-and-stitch) capture — App Automate only. The device's
    # bottom navigation/system bar is sticky, so the scroll engine sees it as
    # the end of the page and captures a single tile (no scroll). Telling Percy
    # to ignore the bottom `bottom_scrollview_offset` pixels lets the scroll
    # advance past the fixed bar and stitch the real content into many tiles.
    # Verified on Pixel 6: without the offset = 1 tile, with offset = ~7 tiles.
    # The default matches the Pixel 6 nav-bar height (160 device px); override
    # via BOTTOM_SCROLLVIEW_OFFSET for other devices. iOS uses the same option.
    bottom_offset = int(os.environ.get("BOTTOM_SCROLLVIEW_OFFSET", "160"))
    percy_screenshot(
        driver,
        "Wikipedia Home — fullpage",
        fullpage=True,
        screen_lengths=4,
        bottom_scrollview_offset=bottom_offset,
    )


def test_exercises_ignore_regions_xpaths(driver):
    percy_screenshot(
        driver,
        "Wikipedia Home — ignore via xpath",
        ignore_regions_xpaths=[REGION_XPATH],
    )


def test_exercises_ignore_region_appium_elements(driver):
    if IS_IOS:
        # percy-appium-app builds the ignore region from element.get_attribute
        # ("class"), but the XCUITest driver has no "class" attribute (it uses
        # "type"), so this raises "The attribute 'class' is unknown" on iOS.
        # The other ignore/consider rows (xpath-based) cover iOS already.
        pytest.skip("ignore_region_appium_elements is unsupported on iOS XCUITest (no 'class' attribute)")
    el = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, A11Y_ID))
    )
    percy_screenshot(
        driver,
        "Wikipedia Home — ignore via appium element",
        ignore_region_appium_elements=[el],
    )


def test_exercises_custom_ignore_regions(driver):
    # App Percy's custom_ignore_regions expects IgnoreRegion objects (top,
    # bottom, left, right) — NOT plain dicts. A dict raises
    # "'dict' object has no attribute 'is_valid'" inside the SDK, which is
    # then swallowed (ignore_errors) and the snapshot is silently dropped.
    # (Only the Percy-on-Automate path accepts dicts.)
    percy_screenshot(
        driver,
        "Wikipedia Home — custom ignore region",
        custom_ignore_regions=[IgnoreRegion(top=0, bottom=100, left=0, right=300)],
    )


def test_exercises_consider_regions_xpaths(driver):
    percy_screenshot(
        driver,
        "Wikipedia Home — consider via xpath",
        consider_regions_xpaths=[REGION_XPATH],
    )


def test_exercises_sync_mode(driver):
    # sync=True blocks until Percy returns the comparison result for this
    # screenshot. With a full-access PERCY_TOKEN the SDK hands back the
    # comparison payload (a dict); with a write-only token (common in CI)
    # Percy responds 403 and percy-appium-app returns None. Both are valid
    # outcomes, so don't couple the assertion to token scope — just exercise
    # the option and, when a payload is returned, sanity-check it's a dict.
    result = percy_screenshot(driver, "Wikipedia Home — sync", sync=True)
    print(f"sync screenshot comparison result: {result}")
    assert result is None or isinstance(result, dict)


def test_exercises_test_case_and_labels(driver):
    percy_screenshot(
        driver,
        "Wikipedia Home — test_case + labels",
        test_case="home-smoke",
        labels="smoke,appium-python",
    )
