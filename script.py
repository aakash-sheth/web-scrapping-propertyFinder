# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
import pandas as pd
from selenium import webdriver
from pandas import ExcelWriter
from selenium.common.exceptions import NoSuchElementException
from requests import ReadTimeout, ConnectTimeout, HTTPError, Timeout, ConnectionError


"""source url"""
url=r'https://m.propertyfinder.ae/en/commercial-rent/properties-for-rent.html'

#List 
sr_no=[]
description_list=[] 
price_list=[]
address_list=[] 
category_list=[]
area_list=[]
status_list=[]
NumBath_list=[]
#next - 'pagination__link pagination__link--next
#Get the url for search by email
source_code=requests.get(url)
plain_text=source_code.text
soup= BeautifulSoup(plain_text, 'html.parser')
propertyNumber=soup.find_all('a', class_="property-card__title-link")
driver=webdriver.Chrome()
sr=0
n=1
while True:
        page_url=r'https://www.propertyfinder.ae/en/commercial-rent/properties-for-rent.html?page='+str(n)
        
        source_code=requests.get(page_url)
        plain_text=source_code.text
        soup=BeautifulSoup(plain_text,'html.parser')
        class_card=soup.find_all('h2', class_="card__title card__title-link")
        driver.get(page_url)
        if len(class_card)==0:
            print("I am done at page {0}".format(n))
            break
        count=1
        p=1
        while True:
             print("here")
            
             try:
                 #Property 
                 description_xpath=r'/html/body/main/div/div[2]/div[5]/div[1]/div[2]/div/div/div['+str(p+1)+']/a/div[2]/div[1]/h2'
                 description=driver.find_element_by_xpath(description_xpath).text
                 description_list.append(description)
                 #Price Description
                 price_xpath=r'/html/body/main/div/div[2]/div[5]/div[1]/div[2]/div/div/div['+str(p+1)+']/a/div[2]/div[2]/div[1]/div[1]/p/span'
                 price=driver.find_element_by_xpath(price_xpath).text
                 price_list.append(price)
                 print(price_list)
                 #Address Description
                 address_xpath=r'/html/body/main/div/div[2]/div[5]/div[1]/div[2]/div/div/div['+str(p+1)+']/a/div[2]/div[1]/p'
                 address=driver.find_element_by_xpath(address_xpath).text
                 address_list.append(address)
                 #Category Description
                 category_xpath=r'/html/body/main/div/div[2]/div[5]/div[1]/div[2]/div/div/div['+str(p+1)+']/a/div[2]/div[2]/div[1]/div[2]/p[1]'
                 category=driver.find_element_by_xpath(category_xpath).text
                 category_list.append(category)
                 #Area Description
                 area_xpath=r'/html/body/main/div/div[2]/div[5]/div[1]/div[2]/div/div/div['+str(p+1)+']/a/div[2]/div[2]/div[1]/div[2]/p[2]'
                 area=driver.find_element_by_xpath(area_xpath).text
                 if area[-4:]!='sqrt':
                     area_list.append(area)
                 else:            
                     #Number of bathrooms 
                     NumBath_xpath=r'/html/body/main/div/div[2]/div[5]/div[1]/div[2]/div/div/div['+str(p+1)+']/a/div[2]/div[2]/div[1]/div[2]/p[2]'
                     NumBath=driver.find_element_by_xpath(NumBath_xpath).text
                     NumBath_list.append(NumBath)
                     #Area Description
                     area_xpath=r'/html/body/main/div/div[2]/div[5]/div[1]/div[2]/div/div/div['+str(p+1)+']/a/div[2]/div[2]/div[1]/div[2]/p[3]'
                     area=driver.find_element_by_xpath(area_xpath).text
                     area_list.append(area)
                 #Status of property Description
                 Status_xpath=r'/html/body/main/div/div[2]/div[5]/div[1]/div[2]/div/div/div['+str(p+1)+']/a/div[2]/p'
                 Status=driver.find_element_by_xpath(Status_xpath).text
                 status_list.append(Status)
                 #Sr No                
                 sr=sr+1
                 sr_no.append(sr)
                 count+=1
                 if count>len(class_card):
                     break
             except NoSuchElementException: 
                 print('try field')
                 p+=1
                 continue
             p+=1
        n+=1
       
driver.close()
                
df1 = pd.DataFrame(sr_no, columns=['sr_no'])
df2=pd.DataFrame(description_list, columns=['Description'])
df3=pd.DataFrame(price_list, columns=['Price'])
df4=pd.DataFrame(address_list, columns=['Address'])
df5=pd.DataFrame(category_list, columns=['Category'])
df6=pd.DataFrame(area_list, columns=['Area'])            
df7=pd.DataFrame(NumBath_list, columns=['Bathrooms'])            
df8=pd.DataFrame(status_list, columns=['Status'])         
            
            
df12=df1.join(df2)
df123=df12.join(df3)
df1234=df123.join(df4)
df12345=df1234.join(df5)
df123456=df12345.join(df6)
df1234567=df123456.join(df7)
df12345678=df1234567.join(df8)

writer = ExcelWriter('Property-data' + '.xlsx')
df12345678.to_excel(writer, 'Sheet1', index=False)
writer.save()   
