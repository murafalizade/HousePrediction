import os
import numpy as np
from selenium import webdriver
from bs4 import BeautifulSoup
import sqlalchemy
from sqlalchemy.exc import SQLAlchemyError

import csv

import time
chromrdriver = "C:/Users/HP/Downloads/chromedriver_win32 (1)/chromedriver.exe"
os.environ["webdriver.chrome.driver"] = chromrdriver
driver = webdriver.Chrome(chromrdriver)
for x in range(945,1400):
    page = "https://bina.az/alqi-satqi?page"+"="+str(x)
    driver.get(page)
    driver.execute_script("window.scrollTo(1,2000)")
    time.sleep(5)
    bina_soup = BeautifulSoup(driver.page_source,'html.parser')
    prices = bina_soup.findAll('div',attrs={"class":"price"})
    locs = bina_soup.findAll('div',attrs={"class":"location"}) 
    names = bina_soup.findAll('ul',attrs={"class":"name"})
    with open('bigs.csv','a',encoding='utf-8') as f1:
            for i in range(0,len(names)):
                f1.write(names[i].text+","+locs[i].text+","+prices[i].text+"\n")
                f1.closed
driver.close()
import pandas as pd
df = pd.read_csv('bigs.csv')
area = []
floor = []
room = []
for x in list(df['Names']):
    i = x.find('o')
    j = x.find('ı')
    k= x.find('m')
    q = x.find("ə")
    rm = x[i-2:i]
    try:
        int(rm)
    except:
        rm = np.nan
    ar = x[j+1:k]
    try:
        float(ar)
    except:
        ar = ar[0:ar.find('s')]
    fl = x[k+2:q-1]
    if fl.find("s") != -1 or fl=="":
        floor.append(np.nan)
    else:
        floor.append(fl)
    area.append(ar)
    room.append(rm)
dfs = pd.DataFrame({'Locations':df['Locations'],'Prices':df['Prices'],'Floor':floor,'Area':area,'Rooms':room,})
xf = pd.read_csv('allbina.csv')
xf = xf.drop(['Dates'],axis=1)
data = pd.concat([dfs, xf], ignore_index=True)
data['Prices'] = list(map(lambda x:int(x[0:x.find("A")].replace(" ","")) if str(x).find('A')!=-1 else x,list(data['Prices'])))
data.to_csv('all_binas.csv')

df = pd.read_csv('all_binas.csv')
df = df.drop(['Unnamed: 0'],axis=1)
try: 
   engine = sqlalchemy.create_engine("oracle://murad99:asd@localhost:1521")
   df.to_sql('estate',con=engine)
   print('Sucess') 
except SQLAlchemyError as e:
   print("Error")
   print(e)