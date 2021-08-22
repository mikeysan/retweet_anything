from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait


browser = webdriver.Firefox()


# Bare minimum to test that the driver and selenium works
browser.get("https://google.com")
wait = WebDriverWait(browser, 600)

