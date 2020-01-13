# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
import chromedriver_binary
import pandas as pd
import numpy as np
from time import sleep
import datetime

def scraping_stock_price(year,month):
    url = "https://indexes.nikkei.co.jp/nkave/archives/data"
    # Headless mode 
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)  # 今は chrome_options= ではなく options=
    driver.get(url)
    
    # Change the drop down
    drop_dwon_year = driver.find_element_by_xpath('/html/body/div[4]/div/div[2]/div[1]/div[1]/select')
    Select(drop_dwon_year).select_by_visible_text('{}年'.format(year))
    drop_dwon_month = driver.find_element_by_xpath('/html/body/div[4]/div/div[2]/div[1]/div[2]/select')
    Select(drop_dwon_month).select_by_visible_text('{}月'.format(month))
    
    # Click display button
    driver.find_element_by_class_name("disp-button").click()
    sleep(3)
    stock_list, start_point , end_point = [], 11 ,20
    for idx, value in pd.DataFrame(driver.find_element_by_css_selector("#data_list > table") .text.encode('utf-8').split('\n'))[1:].iterrows():
        year = value.str[0:4][0]
        month = value.str[5:7][0]
        day = value.str[8:10][0]
        date = datetime.datetime.strptime(year+ "-"+month+"-"+day, '%Y-%m-%d')
        unixtime_jst = datetime.date(
            date.year,
            date.month, 
            date.day
        ).strftime('%s')
        open_price = value.str[start_point:start_point+9].str.replace(",", "")[0]
        high_price = value.str[start_point +10:end_point+10].str.replace(",", "")[0]
        low_price = value.str[start_point +20:end_point +20].str.replace(",", "")[0]
        end_price = value.str[start_point +30:end_point +30].str.replace(",", "")[0]
        stock_list.append([year,month,day,date,unixtime_jst,open_price , high_price,  low_price,end_price])
    stock_df = pd.DataFrame(stock_list,columns=['year','month','day','date','unixtime_jst','opening_price','high_price', 'low_price','end_price'])
    stock_df[['opening_price','high_price','low_price','end_price']] = stock_df[['opening_price','high_price','low_price','end_price']].astype(float)
    #stock_df.to_csv('./data/price_{}_{}.csv'.format(year,month))
    return  stock_df
# 2019年6月を取得        
stock_df = scraping_stock_price(2019,6)
stock_df .head()
