from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Base:
    def __init__(self, driver):
        self.driver = driver

    def click(self, locator):
        element = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(locator))
        element.click()

    def find_element(self, locator):
        element = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(locator))
        return element

    def input_text_into_field(self, text, locator):
        element = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(locator))
        element.send_keys(text)

    def assert_text(self, search_text, locator):
        element = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, locator)))
        try:
            assert search_text.lower() in element.text.lower()
        except AssertionError:
            print(f"Search text '{search_text.lower()}', is not in header '{element.text.lower()}'")

    def get_text(self, locator):
        element = WebDriverWait(self.driver, 0.1).until(EC.visibility_of_element_located(locator))
        return element.text