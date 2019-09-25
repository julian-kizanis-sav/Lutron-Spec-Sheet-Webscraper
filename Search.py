#SAV Digital Enviroments
#Julian Kizanis

from selenium import webdriver
#from selenium.webdriver.common.keys import Keys

#from selenium import webdriver
#from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
#from selenium.common.exceptions import StaleElementReferenceException
from bs4 import BeautifulSoup
#from pandas import DataFrame
import pandas as pd
#import os
import time


modelIndex = 0
imageURL = []
specURL = []
CadURL = []
RvtURL = []
tempURL =""
attempts = 0
modelNumber = ""
noSpec = 0
noCAD = 0
noRVT = 0
shortDelay = .5


import csv

with open('LutronModelList.csv', 'r') as f:
    reader = csv.reader(f)
    OriginalModelNumbersTemp = list(reader)
OriginalModelNumbers = [j for sub in OriginalModelNumbersTemp for j in sub]

for model in OriginalModelNumbers:
    model.replace("'", "")
    model.replace("'", "")

ModelNumbers = OriginalModelNumbers
i = -1
for model in ModelNumbers:
    i += 1    
    model = model.replace("CHOOSE COLOR'", "")
#    if model[-2:-1] == 'XX':
    model = model.replace("-XX", "")
#    if model[-2:-1] == 'WH':
    model =  model.replace("-WH", "")
#    if model[-2:-1] == 'IV':
    model =  model.replace("-IV", "")
#    if model[-2:-1] == 'AL':
    model =  model.replace("-AL", "")
#    if model[-2:-1] == 'LA':
    model =  model.replace("-LA", "")
#    if model[-2:-1] == 'GR':
    model =  model.replace("-GR", "")
#    if model[-2:-1] == 'BR':
    model =  model.replace("-BR", "")    
#    if model[-2:-1] == 'BL':
    model =  model.replace("-BL", "")
#    if model[-2:-1] == 'HT':
    model =  model.replace("-HT", "")
#    if model[-2:-1] == 'MR':
    model =  model.replace("-MR", "")
#    if model[-2:-1] == 'PL':
    model =  model.replace("-PL", "")
#    if model[-2:-1] == 'LS':
    model =  model.replace("-LS", "")
#    if model[-2:-1] == 'TP':
    model =  model.replace("-TP", "")
#    if model[-2:-1] == 'ES':
    model =  model.replace("-ES", "")
#    if model[-2:-1] == 'BI':
    model =  model.replace("-BI", "")    
#    if model[-2:-1] == 'SW':
    model =  model.replace("-SW", "")
#    if model[-2:-1] == 'PD':
    model =  model.replace("-PD", "")
#    if model[-2:-1] == 'MN':
    model =  model.replace("-MN", "")
#    if model[-2:-1] == 'SI':
    model =  model.replace("-SI", "")
#    if model[-2:-1] == 'BE':
    model =  model.replace("-BE", "")
#    if model[-2:-1] == 'TP':
    model =  model.replace("-TP", "")
#    if model[-2:-1] == 'TC':
    model =  model.replace("-TC", "")
#    if model[-2:-1] == 'GB':
    model =  model.replace("-GB", "")
#    if model[-2:-1] == 'BG':
    model =  model.replace("-BG", "")
#    if model[-2:-1] == 'MS':
    model =  model.replace("-MS", "")
#    if model[-2:-1] == 'GS':
    model =  model.replace("-GS", "")
#    if model[-2:-1] == 'DS':
    model =  model.replace("-DS", "")
#    if model[-2:-1] == 'ST':
    model =  model.replace("-ST", "")

    model =  model.replace("-CHOOSE COLOR", "")
    model =  model.replace("-*", "")
    model =  model.replace(", Specify Color", "")
    model =  model.replace("-CHOOSE COLOR", "")
    model =  model.replace("?CHOOSE COLOR", "")
    model =  model.replace("(CHOOSE COLOR)", "")
    model =  model.replace(" SELECT COLOR", "")
    model =  model.replace("(CHOOSE FINISH)", "")
    model =  model.replace("  ***SPECIFY COLOR", "")
#    print(model)
    ModelNumbers[i] = model
    #time.sleep(.3)
    
#print(ModelNumbers)
    
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome()    
for model in ModelNumbers:
    print(model)
#    driver = webdriver.Chrome() 
    modelURL = f"http://www.lutron.com/en-US/pages/supportCenter/support.aspx?modelNumber={model}&&SECTION=Documents"
    driver.get(modelURL)
    
    time.sleep(20)
    while attempts < 3:
        try:
            soup = BeautifulSoup(driver.page_source, 'lxml')   #creates a beautifulSoup object called soup
            imageURL.insert(modelIndex, soup.find("img", {"class":"img-responsive center-block"})['src'])
            attempts = 3
        except NoSuchElementException:
            attempts += 1
            imageURL.insert(modelIndex, "")
            time.sleep(shortDelay)
        except TypeError:
            attempts += 1
            imageURL.insert(modelIndex, "")
            time.sleep(5)
    print(f"imageURL[{modelIndex}]:\t{imageURL[modelIndex]}")
    attempts = 0
    
    while attempts < 3:
        try:
            driver.find_element_by_xpath("(//a[@title='Product Specification Submittals'])").click()    #Product Specification Submittals
            time.sleep(shortDelay)
            if noSpec == 0:
                
                try:
                    tempURL = soup.find("a", {"title":"English  (.pdf)"})['href']
                    specURL.insert(modelIndex, f"http://www.lutron.com{tempURL}")  
                    noSpec = -1
#                    print("Spec")
                except TypeError:
                    specURL.insert(modelIndex, "")
                    noSpec = 1
#                    print("No Spec")
            
           
            driver.find_element_by_xpath("(//a[@title='CAD Downloads'])").click()    #CAD Downloads
            time.sleep(shortDelay)
            if noCAD == 0:
                try:
                    tempURL = soup.find("a", {"title":"English  (.dwg)"})['href']
                    CadURL.insert(modelIndex, f"http://www.lutron.com{tempURL}")
                    noCAD = -1
#                    print("CAD")
                except TypeError:
                    CadURL.insert(modelIndex, "")
                    noCAD = 1
#                    print("No CAD")    
            time.sleep(shortDelay)
            if noRVT == 0:               
                try:
                    tempURL = soup.find("a", {"title":"English  (.rvt)"})['href']
                    RvtURL.insert(modelIndex, f"http://www.lutron.com{tempURL}")
                    noRVT = -1
#                    print("RVT")
                except TypeError:
                    RvtURL.insert(modelIndex, "")
                    noRVT = 1
#                    print("No RVT")
            
            attempts = 3
        except NoSuchElementException:
            attempts += 1
            time.sleep(shortDelay)  
            
    if noSpec == 0:
        specURL.insert(modelIndex, "")
    if noCAD == 0:
        CadURL.insert(modelIndex, "")
    if noRVT == 0:
        RvtURL.insert(modelIndex, "")
    noSpec = 0
    noCAD = 0
    noRVT = 0
    print(f"specURL[{modelIndex}]:\t{specURL[modelIndex]}")
    print(f"CadURL[{modelIndex}]:\t{CadURL[modelIndex]}")
    print(f"RvtURL[{modelIndex}]:\t{RvtURL[modelIndex]}")
    attempts = 0
    modelIndex += 1
    
    df = pd.DataFrame(list(zip(OriginalModelNumbers, ModelNumbers, imageURL, specURL, CadURL, RvtURL)), columns =['Model Number', 'Adj Model Number', 'imageURL', 'specURL', 'CadURL', 'RvtURL'])  
    #df is a panda object that contains: ModelCategory, ModelName, ModelPdf
    export_csv = df.to_csv ('LutronSpecSheetCADRVT.csv', header=True) #Don't forget to add '.csv' at the end of the path
    
#    driver.quit()
    
df = pd.DataFrame(list(zip(OriginalModelNumbers, ModelNumbers, imageURL, specURL, CadURL, RvtURL)), columns =['Model Number', 'Adj Model Number', 'imageURL', 'specURL', 'CadURL', 'RvtURL'])  
#df is a panda object that contains: ModelCategory, ModelName, ModelPdf
export_csv = df.to_csv ('Lutron SpecSheet CAD RVT.csv', header=True) #Don't forget to add '.csv' at the end of the path

