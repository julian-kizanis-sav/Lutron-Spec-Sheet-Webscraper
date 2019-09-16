from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import pandas as pd
import time

driver = webdriver.Chrome() #sets the browser driver

driver.get("http://www.lutron.com/en-US/Service-Support/Pages/Technical/ProductSpecification.aspx") #opens Lutron's website
                                                                        #the models are only accesable when the coraspoding popup is active (hovered over)
Alphabet = driver.find_element_by_xpath("(//li[@class='hasMore'])[1]")  #Alphabet finds the letters that the mouse has to hover over to open a popup box

hover = ActionChains(driver).move_to_element(Alphabet)  #hover hovers the mouse over the current letter
hover.perform()    #executes the hover command

modelCounter = 1    #every model has a unique number (starting with 1) that can be used to find it
letterCounter = 1   #keeps track of the current letter
stopCounter = 0      #allows a small batch to be performed
STOPNUMBER = 9999   #final number of the batch
ModelCategory = []  #list of categories
ModelName = []      #list of Model Names
ModelLanguage = []  #list of data sheet languages
ModelPdf = []       #list of datasheet links
pdf = ""            #temporaraly stores the link
languagePdf = ""    #temporaraly stores the language
nameCheck = 0       #used for logic
row = 0             #keeps track of the row
done = 0

#this section uses Selenium to access different parts of Lutron's dynamic website
try:
    while stopCounter < STOPNUMBER: #allows a small batch to be performed
        ProductCategory = driver.find_element_by_xpath(f"(//a[@class='step1Done'])[{modelCounter}]")    #finds the next model category
    
        while ProductCategory.is_displayed() == 0:  #is the next model category hidden
#            print(f"{modelCounter}    {letterCounter}")
            Alphabet = driver.find_element_by_xpath(f"(//li[@class='hasMore'])[{letterCounter}]")       #Alphabet finds the letters that the mouse has to hover over to open a popup box
            hover = ActionChains(driver).move_to_element(Alphabet)                                      #hover hovers the mouse over the current letter
            hover.perform()                                                                             #executes the hover command
            letterCounter += 1      #adds one to the current letter
        ProductCategory = driver.find_element_by_xpath(f"(//a[@class='step1Done'])[{modelCounter}]")    #finds the next model category
        ProductCategory.click()     #clicks the link
        modelCounter += 1
        letterCounter = 1
        stopCounter += 1
    
        
        time.sleep(10)      #sleeps to allow the webpage to buffer/load
    

    page_source = driver.page_source            #this section uses beautifulSoup to find the data we want
    soup = BeautifulSoup(page_source, 'lxml')   #creates a beautifulSoup object called soup
    
    category = soup.find_all("div", {"class":"lnkCategory"})    #finds all instances that the class 'InkCategory' occurs, this is the section where the category is stored


    for cat in category:    #cycles through every category found
#        print(cat)
        tempCategory = cat.find('a')    #finds the subsection of the current category directory that stores the category's name
 #       print(tempCategory['name'])
        
        nameList1 = cat.parent.find_all("td", {"style":"width:15%;"})   #finds all the model numbers and pdfs within the current category
  
        for name in nameList1:          #cycles through the model numbers and pdf links
            tempLink = name.find('a')   #finds the subsection of the current pdf directory that stores the pdf link's url
            if tempLink == None:        #if there is no subsection, then we are looking at a model number's directory
                if nameCheck == 0:      #we were previously looknig at a pdf's directory
                    nameCheck = 1       #we just looked at a model number's directory
                else:                   #we were previously looknig at a model number's directory
                    ModelLanguage.insert(row, languagePdf)  #this model's language is the same as the last models
                    ModelPdf.insert(row, pdf)               #this model's pdf link is the same as the last models
                row += 1        #next row
                ModelName.insert(row, name.get_text())          #extracts the model's name from the model's directory
                ModelCategory.insert(row, tempCategory['name']) #inserts the model's name
            else:   #we are looking at a pdf's directory
                languagePdf = name.get_text()
                pdf = tempLink['href']
                ModelLanguage.insert(row, languagePdf)   
                ModelPdf.insert(row, pdf)
                nameCheck = 0

except NoSuchElementException:    
    print("End of List")
    
print(4)
df = pd.DataFrame(list(zip(ModelCategory, ModelName, ModelPdf)), columns =['Category', 'Name', 'Url'])
export_csv = df.to_csv (r'C:\Users\Julian.Kizanis\Documents\Lutron Data Sheets\Category.csv', header=True) #Don't forget to add '.csv' at the end of the path
