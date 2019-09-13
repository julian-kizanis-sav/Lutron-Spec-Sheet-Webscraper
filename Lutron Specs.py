from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementNotInteractableException
from bs4 import BeautifulSoup


import re
import time

driver = webdriver.Chrome()

driver.get("http://www.lutron.com/en-US/Service-Support/Pages/Technical/ProductSpecification.aspx")

Alphabet = driver.find_element_by_xpath("(//li[@class='hasMore'])[1]")

hover = ActionChains(driver).move_to_element(Alphabet)
hover.perform()


ProductCategory = driver.find_element_by_xpath("(//a[@class='step1Done'])[11]")
if ProductCategory.is_displayed():
    ProductCategory.click()
else:
    Alphabet = driver.find_element_by_xpath("(//li[@class='hasMore'])[1]")
    hover = ActionChains(driver).move_to_element(Alphabet)
    hover.perform()
    ProductCategory = driver.find_element_by_xpath("(//a[@class='step1Done'])[11]")
    ProductCategory.click()


time.sleep(10)


page_source = driver.page_source

soup = BeautifulSoup(page_source, 'lxml')
nameList = soup.find_all("td", {"style":"width:15%;"})
for name in nameList:
    print(nameList)
    #print(nameList.get('href'))


aaa = driver.find_element_by_xpath("//td[@class='wrapword']/preceding::td")
print(aaa.find_element_by_css_selector('td').get_attribute('style'))
if aaa:
    parenta = aaa.find_element_by_xpath('..')
print(parenta)
    
    
#Alphabet3 = driver.find_elements_by_xpath("//td[@class='wrapword']")
#for ii in Alphabet3:
#    print(ii.find_element_by_css_selector('a').get_attribute('href'))
