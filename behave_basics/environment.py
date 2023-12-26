from selenium import webdriver


def before_feature(context, feature):
    context.browser = webdriver.Chrome()
    context.browser.maximize_window()


def after_feature(context, feature):
    context.browser.close()


def before_scenario(context, scenario):
    if '@no_background' in scenario.effective_tags:
        scenario.feature.background = None