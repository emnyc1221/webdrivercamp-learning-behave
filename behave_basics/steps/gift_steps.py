from behave import *
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from behave_basics.components.base import Base
from behave_basics.components.gift_page import GiftPage
import time

# Step to navigate to a URL and print it
@step('Navigate to {url}')
def step_impl(context, url):
    context.browser.get(url)
    print(context.browser.current_url)


# Step to perform a search operation
@step("Search for {search_item}")
def step_impl(context, search_item):
    main_page = Base(context.browser)
    search_field_xpath = "//input[@name='searchTerm']"
    search_field = WebDriverWait(context.browser, 10).until(
        EC.presence_of_element_located((By.XPATH, search_field_xpath)))
    search_field.send_keys(search_item + Keys.RETURN)

    # Handle specific case for 'iphone' search
    if search_item == 'iphone':
        link1 = "//p[contains(text(),'Explore all iPhone')]//ancestor::a"
        frame1 = "//div[@id='slpespot']//child::iframe[@title='3rd party ad content']"
        context.browser.switch_to.frame(main_page.find_element((By.XPATH, frame1)))
        element = main_page.find_element((By.XPATH, link1))
        element.click()
        context.browser.switch_to.default_content()
        time.sleep(1)


# Step to verify the header of the page
@step("Verify header of the page contains {search_item}")
def step_impl(context, search_item):
    header_xpath = "//h1"
    header_text = WebDriverWait(context.browser, 10).until(
        EC.presence_of_element_located((By.XPATH, header_xpath))).text
    assert search_item in header_text


# Step to select an option in a specific section
@step("Select {option} in {section} section")
def step_impl(context, option, section):
    context.gift_page = GiftPage(context.browser)
    context.gift_page.select_option(option, section)


# Step to collect items from the first page
@step("Collect all items on the first page into {var} on the {level} level")
def step_impl(context, var, level=None):
    items = context.gift_page.collect_item_features()
    if level == 'feature':
        setattr(context.feature, var, items)
    else:
        setattr(context, var, items)


# Step to verify collected results
@then("Verify all collected results' {parameter} is {condition}")
def step_impl(context, parameter, condition):
    for item in getattr(context, 'collected_items', []):
        value = item.get(parameter, '')
        if parameter == 'price':
            assert any(eval(f'{price} {condition}') for price in value.replace("$", "").split(" - "))
        else:
            assert condition in value
