#SAV Digital Environments
#Julian Kizanis

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
#from selenium.common.exceptions import StaleElementReferenceException
from bs4 import BeautifulSoup
#from pandas import DataFrame
import pandas as pd
#import os
import random
import time
import csv
import re

modelIndex = 0
MSRP = []
Cost = []
CadURL = []
RvtURL = []
tempURL =""
attempts = 0
modelNumber = ""
noSpec = 0
noCAD = 0
noRVT = 0
shortDelay = .5

with open('LutronModelList.csv', 'r') as f:
    reader = csv.reader(f)
    ModelNumbersTemp = list(reader)
ModelNumbers = [j for sub in ModelNumbersTemp for j in sub]

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome() 
modelURL = f"https://mylutron.com/shop#addProduct/byModel"        
driver.get(modelURL)   

time.sleep(1 + random.random())
username = driver.find_element_by_xpath("(//input[@data-val-email='Enter a valid email address'])")
username.send_keys("scott.green@savinc.net")
username.send_keys(Keys.RETURN)

time.sleep(1 + random.random())
password = driver.find_element_by_xpath("(//input[@data-val-required='The Password field is required.'])")
password.send_keys("Seg123!e")
password.send_keys(Keys.RETURN)
time.sleep(12 + random.random())

modelBox = driver.find_element_by_xpath("(//input[@class='search-models typeahead tt-input'])")
modelBox.send_keys("model")

time.sleep(1 + random.random())
qtyBox = driver.find_element_by_xpath("(//input[@class='quantity input-qty'])")
qtyBox.send_keys("1")
qtyBox.send_keys(Keys.RETURN)

for model in ModelNumbers:
    time.sleep(1 + random.random())
#    print("looped")
    modelBox = driver.find_element_by_xpath("(//input[@data-rowid='0'])")
#    print("found")
    modelBox.clear()
#    print("cleared")
    time.sleep(1 + random.random())
    modelBox = driver.find_element_by_xpath("(//input[@data-rowid='0'])")
#    print("found again")
    modelBox.send_keys(model)
#    print("typed")
    time.sleep(1 + random.random())
    modelBox = driver.find_element_by_xpath("(//input[@data-rowid='0'])")
    modelBox.send_keys(Keys.RETURN)
#    print("returned")
    time.sleep(9 + random.random())
    
    
    soup = BeautifulSoup(driver.page_source, 'lxml')   #creates a beautifulSoup object called soup
    try:
        Prices = soup.findAll("span", {"class":"unit-price"})
        i = 0
        for price in Prices:
            #print(price.text)
            if i == 0:
                Cost.insert(modelIndex, price.text)
                i = 1
            else:
                MSRP.insert(modelIndex, price.text)
                i = 0
            
    except:
        print("No Price data!")
        MSRP.insert(modelIndex, "")
        Cost.insert(modelIndex, "")
    
    print(f"MSRP:  {MSRP[modelIndex]}")
    print(f"Cost:  {Cost[modelIndex]}")
    modelIndex += 1
    
    
    df = pd.DataFrame(list(zip(ModelNumbers, MSRP, Cost)), columns =['Model Number', 'MSRP', 'Cost'])  
    #df is a panda object that contains: ModelCategory, ModelName, ModelPdf
    export_csv = df.to_csv ('LutronPriceSheet.csv', header=True) #Don't forget to add '.csv' at the end of the path
    
df = pd.DataFrame(list(zip(ModelNumbers, MSRP, Cost)), columns =['Model Number', 'MSRP', 'Cost'])  
#df is a panda object that contains: ModelCategory, ModelName, ModelPdf
export_csv = df.to_csv ('Lutron Price Sheet Complete.csv', header=True) #Don't forget to add '.csv' at the end of the path
    
    
