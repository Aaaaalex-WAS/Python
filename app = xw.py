#coding:utf-8
import win32com.client as win32
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import lxml
import requests
import threading
from time import sleep
import os, sys, re, time, datetime
from selenium import webdriver
import random
import pandas as pd
from colorama import Fore, Back, Style
import multiprocessing as mul
from urllib.parse import urlencode


base_url = 'https://car.autohome.com.cn/AsLeftMenu/As_LeftListNew.ashx?'
def f(x):
    return x ** 2
def getLongPage(url):
    #url = 'https://car.autohome.com.cn/AsLeftMenu/As_LeftListNew.ashx?typeId=1%20&brandId=0%20&fctId=0%20&seriesId=0'
    headers = {
        'Referer': 'https://car.autohome.com.cn/',
        'Sec-Fetch-Mode': 'no-cors',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'
    }
    try:
        r = requests.get(url ,headers = headers)
        if r.status_code == 200:
            r.encoding = r.apparent_encoding#此处将编码改成网页的编码样式，防止出现乱码
            soup = BeautifulSoup(r.text, "lxml")
            #soup=str(r.conent,encoding='utf-8')
            return soup
    except:
        print('cannot request '+ url)


def get_series(url_b,b_result,car_Result2,n):
    headers = {
        'authority': 'car.autohome.com.cn',
        'method': 'GET',
        'scheme': 'https',
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cookie': 'fvlid=156974583432110wygoXZiH; sessionid=D7FE9717-245E-4F8D-8D42-AAF453D1F470%7C%7C2019-09-29+16%3A30%3A35.298%7C%7C0; autoid=851072202da5829e1b4e6cbb05975388; cookieCityId=110100; __ah_uuid_ng=c_D7FE9717-245E-4F8D-8D42-AAF453D1F470; area=460106; ahpau=1; sessionuid=D7FE9717-245E-4F8D-8D42-AAF453D1F470%7C%7C2019-09-29+16%3A30%3A35.298%7C%7C0; ahsids=3170; sessionip=153.0.3.115; Hm_lvt_9924a05a5a75caf05dbbfb51af638b07=1585205934,1585207311,1585266321; clubUserShow=87236155|692|2|%E6%B8%B8%E5%AE%A2|0|0|0||2020-03-27+08%3A35%3A50|0; clubUserShowVersion=0.1; sessionvid=0F2198AC-5A75-47E2-B476-EAEC2AF05F04; Hm_lpvt_9924a05a5a75caf05dbbfb51af638b07=1585269508; ahpvno=45; v_no=8; visit_info_ad=D7FE9717-245E-4F8D-8D42-AAF453D1F470||0F2198AC-5A75-47E2-B476-EAEC2AF05F04||-1||-1||8; ref=www.baidu.com%7C0%7C0%7C0%7C2020-03-27+08%3A38%3A40.425%7C2019-10-07+22%3A52%3A34.733',
        'sec-fetch-mode': 'no-cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
    }
    parms = {
        'typeId': 1 ,
        'brandId': url_b[url_b.index('brand-')+6: url_b.index('.html')],#截取第一部分的链接中的参数，譬如（奥迪汽车是33）
        'fctId': 0 ,
        'seriesId': 0,
    }
    url1 = base_url + urlencode(parms)#此行代码连接根路径及参数字符串
    #print(url1)
    re = requests.get(url1)
    soup = BeautifulSoup(re.text,'lxml')#直接解析
    for i in soup.find_all('dd'):
        for j in i.find_all('a'):
            b_result[j.text]=n
            car_Result2[j.text] = 'https://car.autohome.com.cn'+j.get('href')

#####################################################################################################
def get_car_information(url):
    dic = {}
    headers = {
            'authority': 'car.autohome.com.cn',
            'method': 'GET',
            'scheme': 'https',
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cookie': 'fvlid=156974583432110wygoXZiH; sessionid=D7FE9717-245E-4F8D-8D42-AAF453D1F470%7C%7C2019-09-29+16%3A30%3A35.298%7C%7C0; autoid=851072202da5829e1b4e6cbb05975388; cookieCityId=110100; __ah_uuid_ng=c_D7FE9717-245E-4F8D-8D42-AAF453D1F470; area=460106; ahpau=1; sessionuid=D7FE9717-245E-4F8D-8D42-AAF453D1F470%7C%7C2019-09-29+16%3A30%3A35.298%7C%7C0; ahsids=3170; sessionip=153.0.3.115; Hm_lvt_9924a05a5a75caf05dbbfb51af638b07=1585205934,1585207311,1585266321; clubUserShow=87236155|692|2|%E6%B8%B8%E5%AE%A2|0|0|0||2020-03-27+08%3A35%3A50|0; clubUserShowVersion=0.1; sessionvid=0F2198AC-5A75-47E2-B476-EAEC2AF05F04; Hm_lpvt_9924a05a5a75caf05dbbfb51af638b07=1585269508; ahpvno=45; v_no=8; visit_info_ad=D7FE9717-245E-4F8D-8D42-AAF453D1F470||0F2198AC-5A75-47E2-B476-EAEC2AF05F04||-1||-1||8; ref=www.baidu.com%7C0%7C0%7C0%7C2020-03-27+08%3A38%3A40.425%7C2019-10-07+22%3A52%3A34.733',
            'sec-fetch-mode': 'no-cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
        }
    re = requests.get(url,headers=headers)
    soup = BeautifulSoup(re.text,'html.parser')
    for k in soup.find_all('span',{'class':'score-number'}):
        dic['用户评分'] = k.text
    for i in soup.find_all('ul',{'class':"lever-ul"}):
        for li in i.find_all('li'):
            s = li.text
            if '：' in s:
                dic[s[:s.index('：')]] = s[s.index('：')+1:]
    for j in soup.find_all('span' ,{'class': 'font-arial'}):
        dic['指导价'] = j.text
    return dic

def get_car_config(url):
    #print(datetime.datetime.now())
    #print(url)
    
    series_page=getLongPage(url)
    car_buffer=[]
    config_buffer=[]
    price_buffer=[]
    for car_box in series_page.find_all('ul',{'class':"interval01-list"}):
        for car_item in car_box.find_all('div',{'class':"interval01-list-cars-infor"}):
            for item in car_item.find_all('a',limit=1):
                config_container=[]
                config_container.append(item.text)
                car_page=getLongPage('https:' + item.get('href'))
                #print(ii.get('href'))
                for config_item in car_page.find_all('div',{'class':"cell"}):
                    for config_detail in config_item.find_all('p'):
                        config_container.append(config_detail.text)

            for add_info in car_item.find_all('span'):
                config_container.append(add_info.text)
            config_buffer.append(config_container)
        #print(len(tt))
        #print(len(testpage.find_all('div',{'class':"interval01-list-guidance"})))
        #print(len(page.find_all('div',{'class':"interval01-list-guidance"})))
        for price in car_box.find_all('div',{'class':"interval01-list-guidance"}):
            try:
                price_buffer.append(price.find_all('div')[0].text)
            except:
                pass
            #print(len(j.find_all('div')))
    #print(url+'-'+str(len(config_buffer))+'-'+str(len(price_buffer)))
    #global p2
    #p2= p2 + 1
    #sys.stdout.write('detail downloading {0:.2f}%'.format(p2*100/2085)+'\r')
    #sys.stdout.flush() 
    return config_buffer,price_buffer




def run_proc(name):
    print('Run child process %s (%s)...' % (name, os.getpid()))

#def f(a, b = value):
    #pass

def l(url):
    dr = webdriver.Firefox()
    dr.get(url)

if __name__=='__main__':

    #options = webdriver.FirefoxOptions()
    #options.add_argument('--headless')
    
    #print(os.cpu_count())
    #pool = mul.Pool() 
    #pool.map(l,['https://www.baidu.com/','https://www.autohome.com.cn/shanghai',https://sou.autohome.com.cn/zonghe?q='+'brz'+r'&mq=&pvareaid=3311667])
    #apply_async(f, args = (a,), kwds = {b : value})
    #pool.close()
    #pool.join()
    left_url = 'https://car.autohome.com.cn/AsLeftMenu/As_LeftListNew.ashx?typeId=1%20&brandId=0%20&fctId=0%20&seriesId=0'
    left_nav = getLongPage(left_url)
    brand_result = {}
    series_result = {}
    b_result={}
    dataheader=['Brand','Series','Type','Price','Class','Engine','HorsePower','Torque','Gearbox','Fuel','Env-Standard','Drive Mode','GearBox']

    brand_result={}
    
    for brand_letter in left_nav.find_all('li'):
        for brand in brand_letter.find_all('a'):
            brand_result[brand.text] = 'https://car.autohome.com.cn' + brand.get('href')
    #print('check1')
    #print(brand_result)
    p1=0
    #p2=0
    
    for n_brand in brand_result:
        #print(n)
        p1=p1+1
        
        sys.stdout.write('series downloading {0:.2f}%'.format(p1*100/len(brand_result))+'\r')
        sys.stdout.flush() 
        

        get_series(brand_result[n_brand],b_result,series_result,n_brand)
    #list1=[series_result[x] for x in series_result]
    program_start_time = datetime.datetime.now()
    p=mul.Pool()
    
    l2=p.map(get_car_config,list1)
    print(l2)
    
    program_end_time = datetime.datetime.now()


    print('总计运行时间: {}'.format(program_end_time - program_start_time))