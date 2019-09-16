from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import pandas as pd
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


   
ModelName = []
ModelLanguage = []
ModelPdf = []
pdf = ""
languagePdf = ""
nameCheck = 0
row = 0
p = 0
nameList1 = soup.find_all("td", {"style":"width:15%;"})
for name in nameList1:    
    p += 1
    if p%10 == 0:
        print(p)
    tempLink = name.find('a')
    if tempLink == None:
        if nameCheck == 0:
            nameCheck = 1
        else:
            ModelLanguage.insert(row, languagePdf)
            ModelPdf.insert(row, pdf)
        row += 1
        ModelName.insert(row, name.get_text())
    else:
        languagePdf = name.get_text()
        pdf = tempLink['href']
        ModelLanguage.insert(row, languagePdf)   
        ModelPdf.insert(row, pdf)
        nameCheck = 0

for elem in range(len(ModelName)):
    print(ModelName[elem])
    print(ModelLanguage[elem])
    print(ModelPdf[elem])
    print("New Model!!")
    
df = pd.DataFrame(list(zip(ModelName, ModelLanguage, ModelPdf)), columns =['Name', 'Language' , 'Url'])

export_csv = df.to_csv (r'C:\Users\Julian.Kizanis\Documents\Lutron Data Sheets\All Data Sheets.csv', header=True) #Don't forget to add '.csv' at the end of the path
