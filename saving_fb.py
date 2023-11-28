import selenium

import json
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import requests
import time

s = requests.Session()

email = "chriseric351@gmail.com"
password = "CHriseric255"

def get_driver():
    driver = webdriver.Chrome(executable_path = '/home/talha/Documents/scrapper/chromedriver')
    driver.wait = WebDriverWait(driver, 3)
    return driver

def get_url_cookie(driver):
    driver.get('https://facebook.com')
    driver.find_element("name",'email').send_keys(email)
    driver.find_element("name",'pass').send_keys(password)
    driver.find_element("name",'login').click()
    cookies_list= driver.get_cookies()
    script = open('facebook_cookie.json','w')
    json.dump(cookies_list,script)

driver = get_driver()
get_url_cookie(driver)
