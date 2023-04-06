import os
import unittest
from appium.options.android import UiAutomator2Options
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from os import path
from time import sleep
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.pointer_input import PointerInput
import base64
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.support.events import AbstractEventListener, EventFiringWebDriver
import logging
import pytest

class MyListener(AbstractEventListener):
    def before_find(self, by, value, driver):
        logging.getLogger().info(f'Finding by {by} value {value}')


@pytest.hookimpl
def pytest_configure(config):
    logging_plugin = config.pluginmanager.get_plugin("logging-plugin")

    # Change color on existing log level
    logging_plugin.log_cli_handler.formatter.add_color_level(logging.INFO, "cyan")

    # Add color to a custom log level (a custom log level `SPAM` is already set up)
    logging_plugin.log_cli_handler.formatter.add_color_level(logging.SPAM, "blue")

class GalleryAppTest(unittest.TestCase):
    def setUp(self):
        options = UiAutomator2Options()
        options.app = path.realpath(".") + "/packagenameviewer.apk"
        remote_driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", options=options)
        self.driver = EventFiringWebDriver(remote_driver, MyListener())
        # sample: upload test files to gallery
        # for a in os.listdir("gallery"):
        #     with open("gallery/" + a, "rb") as file:
        #         rd = file.read()
        #         self.driver.push_file(
        #             "/storage/emulated/0/Pictures/" + a, base64.b64encode(rd).decode('utf-8')
        #         )
        #         self.driver.push_file(
        #             "/storage/emulated/0/Pictures/.thumbnails/" + a, base64.b64encode(rd).decode('utf-8')
        #         )
        #         print(a)

    def tearDown(self):
        self.driver.quit()

    def test_swipe(self):
        system_tab = self.driver.find_element(AppiumBy.XPATH, '//android.widget.LinearLayout[@content-desc="system apps"]')
        system_tab.click()
        # some synchronization
        sleep(1)

        recycler = self.driver.find_element(AppiumBy.ID, "com.csdroid.pkg:id/recycler")
        elements = recycler.find_elements(AppiumBy.ID, "com.csdroid.pkg:id/tv_title")
        beforeScroll = elements[0].text

        gesture = ActionChains(self.driver)
        # gesture.drag_and_drop(elements[-1], elements[0])

        touch_input = PointerInput(interaction.POINTER_TOUCH, "touch")
        gesture.w3c_actions = ActionBuilder(self.driver, mouse=touch_input)

        gesture.w3c_actions.pointer_action.move_to_location(0,elements[-1].rect['y'])
        gesture.w3c_actions.pointer_action.pointer_down()
        gesture.w3c_actions.pointer_action.move_to_location(0,elements[0].rect['y'])
        gesture.w3c_actions.pointer_action.release()
        gesture.perform()

        recycler = self.driver.find_element(AppiumBy.ID, "com.csdroid.pkg:id/recycler")
        elements = recycler.find_elements(AppiumBy.ID, "com.csdroid.pkg:id/tv_title")
        afterScroll = elements[0].text
        assert beforeScroll!=afterScroll

        # drag to last visible list item
        # gesture.w3c_actions.pointer_action.move_to(elements[-1])
        # gesture.w3c_actions.pointer_action.pointer_down()
        # gesture.w3c_actions.pointer_action.move_to(elements[1])
        # gesture.w3c_actions.pointer_action.release()
        # gesture.perform()

