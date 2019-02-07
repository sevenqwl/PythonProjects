#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Seven"


import selenium.webdriver.remote.webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time


driver = selenium.webdriver.remote.webdriver.WebDriver(command_executor="http://10.6.25.82:4444/wd/hub", desired_capabilities=DesiredCapabilities.CHROME)

# driver = webdriver.Chrome(chrome_options=optons)

driver.implicitly_wait(30)
driver.get("http://10.6.39.241")
# driver.maximize_window()
driver.find_element_by_css_selector(".gwt-TextBox").send_keys("admin")
driver.find_element_by_css_selector(".gwt-PasswordTextBox").send_keys("ywznboy")
driver.find_element_by_css_selector(".gwt-PasswordTextBox").send_keys(Keys.ENTER)
# 账号1
ActionChains(driver).move_to_element(driver.find_element_by_id("gwt-uid-64")).perform()
ActionChains(driver).move_to_element(driver.find_element_by_id("gwt-uid-50")).perform()
driver.find_element_by_id("gwt-uid-38").click()
time.sleep(3)
elem_Sip1_Enable = driver.find_element_by_xpath("//input[@name='P271']" and "//input[@value='0']") # 0表示关闭注册，1表示启用注册
elem_Sip1_Enable.click()
# ele = driver.find_element_by_xpath("//input[@name='P271']" and "//input[@value='0']")  # 点击否关闭注册
# ele.click()

Grandstream_options = ["P270", "P47", "P48", "P35", "P36", "P34", "P3"]
elem = driver.find_element_by_name("P270")
elem.clear()
elem.send_keys()

elem_Sip1_Label = driver.find_element_by_name("P47")
elem_Sip1_Label.clear()
elem_Sip1_Label.send_keys()

