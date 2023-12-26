import time
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from behave_basics.components.base import Base


class GiftPage(Base):

    def select_option(self, option, section):
        xpath = f"//span[contains(text(), '{section}')]//ancestor::div//span[contains(text(), '{option}')]//ancestor::a"
        locator = (By.XPATH, xpath)
        element = self.safe_find_element(locator)
        if element:
            element.click()

    def get_item_name(self, parent):
        item_name_locator = (By.XPATH, f"//{parent}a[@data-test='product-title']")
        return self.get_text(item_name_locator)

    def get_item_price(self, parent):
        item_price_locator = (By.XPATH, f"//{parent}span[@data-test='current-price']/span[1]")
        return self.get_text(item_price_locator)

    def get_item_shipping(self, parent):
        item_shipping_locator = (By.XPATH, f"//{parent}span[@data-test='LPFulfillmentSectionShippingFA_standardShippingMessage']/span")
        try:
            return self.get_text(item_shipping_locator)
        except TimeoutException:
            return "Shipping info not available"

    def get_items(self):
        item_xpath = (By.XPATH, "//div[@class='styles__StyledCol-sc-fw90uk-0 dOpyUp']")
        WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located(item_xpath))
        return self.driver.find_elements(*item_xpath)

    def collect_item_features(self):
        items = self.get_items()
        item_features = []
        for i, item in enumerate(items, start=1):
            xpath = f"div[@class='styles__StyledCol-sc-fw90uk-0 dOpyUp'][{i}]//"
            item_name = self.get_item_name(xpath)
            item_price = self.get_item_price(xpath)
            item_shipping = self.get_item_shipping(xpath)
            item_features.append({"name": item_name, "price": item_price, "shipment": item_shipping})
        return item_features
