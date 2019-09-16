from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import pandas as pd
import time

driver = webdriver.Chrome()

driver.get("http://www.lutron.com/en-US/Service-Support/Pages/Technical/ProductSpecification.aspx")

Alphabet = driver.find_element_by_xpath("(//li[@class='hasMore'])[1]")

hover = ActionChains(driver).move_to_element(Alphabet)
hover.perform()

modelCounter = 1
ModelName = []
ModelLanguage = []
ModelPdf = []
pdf = ""
languagePdf = ""
nameCheck = 0
row = 0
done = 0
print("0")

while done == 0:
    ProductCategory = driver.find_element_by_xpath("(//a[@class='step1Done'])[11]")

    while ProductCategory.is_displayed() == 0:
        print("1")
        Alphabet = driver.find_element_by_xpath("(//li[@class='hasMore'])[1]")
        hover = ActionChains(driver).move_to_element(Alphabet)
        hover.perform()
    print("2")
    ProductCategory = driver.find_element_by_xpath("(//a[@class='step1Done'])[modelCounter]")
    ProductCategory.click()
    modelCounter += 1

    
    time.sleep(10)
    

    page_source = driver.page_source
    
    soup = BeautifulSoup(page_source, 'lxml')
    
    
       
    
    nameList1 = soup.find_all("td", {"style":"width:15%;"})
    for name in nameList1:    
    
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

#except NoSuchElementException:    
print(4)
df = pd.DataFrame(list(zip(ModelName, ModelPdf)), columns =['Name', 'Url'])
export_csv = df.to_csv (r'C:\Users\Julian.Kizanis\Documents\Lutron Data Sheets\Ballasts.csv', header=True) #Don't forget to add '.csv' at the end of the path
