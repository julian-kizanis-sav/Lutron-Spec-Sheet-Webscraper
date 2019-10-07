#SAV Digital Enviroments
#Julian Kizanis
print("Commpany:\tSAV Digital Environments\nDeveloper:\tJulian Kizanis\n\
Powered By:\tAnaconda\n\n")

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
#converts the csv file to a python list
with open('LutronModelList.csv', 'r') as f:
    reader = csv.reader(f)
    OriginalModelNumbersTemp = list(reader)
OriginalModelNumbers = [j for sub in OriginalModelNumbersTemp for j in sub]

#removes some artifacts
for model in OriginalModelNumbers:
    model.replace("'", "")
    model.replace("'", "")

ModelNumbers = OriginalModelNumbers
#lutron doesn't include color information on their spec sheet names
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
driver = webdriver.Chrome()    #opens a chrome browser
for model in ModelNumbers:	#cycles through the the models 
    print(model)
#    driver = webdriver.Chrome() 
	#opens the website of the model_______________________________________________________{here}__________________
    modelURL = f"http://www.lutron.com/en-US/pages/supportCenter/support.aspx?modelNumber={model}&&SECTION=Documents"
    driver.get(modelURL)
    
    time.sleep(20)	#lutron is a very slow website
    while attempts < 3:	#improves stability
        try:
            soup = BeautifulSoup(driver.page_source, 'lxml')   #creates a beautifulSoup object called soup
            imageURL.insert(modelIndex, soup.find("img", {"class":"img-responsive center-block"})['src'])	#finds the model's image and inserts it in the imageURL list
            attempts = 3	#found it!!
        except NoSuchElementException:	#can't find it
            attempts += 1	
            imageURL.insert(modelIndex, "")	#insert a blank entry for now
            time.sleep(shortDelay)#chances are the lutron website isn't loaded yet
        except TypeError:
            attempts += 1
            imageURL.insert(modelIndex, "")
            time.sleep(5)
    print(f"imageURL[{modelIndex}]:\t{imageURL[modelIndex]}")
    attempts = 0	#reset attempts
    
    while attempts < 3:
        try:
            driver.find_element_by_xpath("(//a[@title='Product Specification Submittals'])").click()    #finds and clicks Product Specification Submittals
            time.sleep(shortDelay)
            if noSpec == 0:	#We don't know if there is a spec sheet
                
                try:
                    tempURL = soup.find("a", {"title":"English  (.pdf)"})['href']	#look for a spec sheet
                    specURL.insert(modelIndex, f"http://www.lutron.com{tempURL}")  #found one, record it
                    noSpec = -1	#we already found one
#                    print("Spec")
                except TypeError:	#there is no spec sheet
                    specURL.insert(modelIndex, "")	#insert a blank cell
                    noSpec = 1	#there is no spec sheet
#                    print("No Spec")
            
           
            driver.find_element_by_xpath("(//a[@title='CAD Downloads'])").click()    #finds and clicks CAD Downloads
            time.sleep(shortDelay)
			#looking for a DWG file, process the same as for spec sheet
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
			#looking for a RVT file, process the same as for spec sheet
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
    #resetting for the next model        
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
    
	#creates a csv file of everything we've gathered
    df = pd.DataFrame(list(zip(OriginalModelNumbers, ModelNumbers, imageURL, specURL, CadURL, RvtURL)), columns =['Model Number', 'Adj Model Number', 'imageURL', 'specURL', 'CadURL', 'RvtURL'])  
    #df is a panda object that contains: ModelCategory, ModelName, ModelPdf
    export_csv = df.to_csv ('LutronSpecSheetCADRVT.csv', header=True)
    
#    driver.quit()
#creates a csv file of everything we've gathered   
df = pd.DataFrame(list(zip(OriginalModelNumbers, ModelNumbers, imageURL, specURL, CadURL, RvtURL)), columns =['Model Number', 'Adj Model Number', 'imageURL', 'specURL', 'CadURL', 'RvtURL'])  
#df is a panda object that contains: ModelCategory, ModelName, ModelPdf
export_csv = df.to_csv ('Lutron SpecSheet CAD RVT.csv', header=True)

