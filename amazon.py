import pandas as pd
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from itertools import permutations
import pdb
import sys

# Intializing selenium webdriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))


# Processing input file
filename= r"E:\AMAZON_URL\amazon5000inputs_formatted.csv"
prod_tracker = pd.read_csv(filename)

# pdb.set_trace()

# Create required columns in dataframe
prod_tracker["Price"] = None
prod_tracker["Title"] = None
prod_tracker["Rating"] = None
prod_tracker["Description"] = None
# print(prod_tracker.head())
#Iterationg over input and scraping the data
start = 2
end=3

def get_product_information(url):    
    driver.get(url)
    
    #  set conditional sleep
    title= None
    Rating= None
    description=None
    
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#productTitle")))
        title = driver.find_element(By.ID, 'productTitle').text
    except:
        print("Error in field title")
    
    try:
        Rating = driver.find_element(By.CSS_SELECTOR,"#acrPopover span").text
    except:
        print("Error in field rating")
    try:
        description = driver.find_element(By.CSS_SELECTOR,"div#productOverview_feature_div").text
    except:
        print("Error in field description for div#productOverview_feature_div")

    try:
        if not description:
            description_dropdown = driver.find_element(By.CSS_SELECTOR,"#nic-po-expander i")
            if description_dropdown:
                description_dropdown.click()
                description_list = driver.find_elements(By.CSS_SELECTOR,"#nic-po-expander-content span" )
                description= ""
                for element in description_list:
                    description= description + " " + element.text
    except Exception as msg:
        print("Error in field description for #nic-po-expander i:-", msg)

        
    return {"Title": title,"Rating":Rating,"Price":None, "Description":description}

for index,row in prod_tracker[start:end].iterrows():
    value = row['url']
    url = value[9:-2]
    product_information = get_product_information(url)
    prod_tracker.at[index, 'Title'] = product_information['Title']
    prod_tracker.at[index,'Rating'] = product_information['Rating']
    prod_tracker.at[index, 'Price'] = product_information['Price']
    prod_tracker.at[index, 'Description'] = product_information['Description']
   
pdb.set_trace()   
prod_tracker.to_excel("output.xlsx")

