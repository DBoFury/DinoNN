from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from time import sleep
from win32api import GetSystemMetrics


class Chrome:
    def __init__(self, url, class_name, acceleration=False, no_window=False):
        """
        :rtype: object
        """
        chrome_options = Options()
        if no_window:
            chrome_options.add_argument("--headless")
        self.chrome = webdriver.Chrome("chromedriver.exe", chrome_options=chrome_options)
        self.chrome.maximize_window()
        self.chrome.get(url)
        self.class_name = class_name
        self.element = self.chrome.find_element_by_class_name(self.class_name)
        self.coords = self.get_coord()

        sleep(1)

        self.press_up()

        if not acceleration:
            self.chrome.execute_script("Runner.config.ACCELERATION=0")

    def get_coord(self):
        location = self.element.location
        size = self.element.size
        left = location['x']
        top = location['y']
        right = location['x'] + size['width']
        bottom = location['y'] + size['height']
        return left + (right - left) * 0.125, top + GetSystemMetrics(1) / 10, \
               right - int((right - left) / 2), bottom + GetSystemMetrics(1) / 10

    def get_crashed(self):
        return self.chrome.execute_script("return Runner.instance_.crashed")

    def get_playing(self):
        return self.chrome.execute_script("return Runner.instance_.playing")

    def restart(self):
        self.chrome.execute_script("Runner.instance_.restart()")
        sleep(0.25)

    def press_up(self):
        self.chrome.find_element_by_tag_name("body").send_keys(Keys.ARROW_UP)

    def quit(self):
        self.chrome.quit()
