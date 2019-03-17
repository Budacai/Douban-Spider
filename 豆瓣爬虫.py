import time
import socks
import socket
import requests
from stem import Signal
from stem.control import Controller
from selenium import webdriver
import pandas as pd
from selenium.webdriver.common.action_chains import ActionChains
from lxml import etree
id = []
title = []
year = []
directors = []
rate = []
actors = []
type = []
countries = []
start_urls = []

# 设置不加载图片
chrome_options = webdriver.ChromeOptions()
prefs = {'profile.default_content_setting_values': {'images': 2}}
chrome_options.add_experimental_option('prefs', prefs)
driver = webdriver.Chrome(
        executable_path="C:\\Users\\12192\\Downloads\\chromedriver_win32\\chromedriver.exe",
        chrome_options=chrome_options)
driver.get(url="https://movie.douban.com/tag/#/?sort=T&range=0,10&tags=%E7%94%B5%E5%BD%B1")
time.sleep(3)
count1 = 0
##循环点击加载更多
while 1:
    left_click = driver.find_elements_by_xpath('//a[contains(text(),"加载更多")]')
    if len(left_click) == 0:
        break
    try:
        ActionChains(driver).move_to_element(left_click[0]).click(left_click[0]).perform()
        count1 += 1
        print(count1)
        time.sleep(2)
    except Exception as e:
        continue

##定位影片id
idlist = driver.find_elements_by_xpath('//a[@class="item"]/div')
print(len(idlist))
for ids in idlist:
    id_list = ids.get_attribute("data-id")
    id.append(id_list)
a = driver.find_elements_by_xpath('//a[@class="item"]')
print(len(a))

for myhref in a:
    websites = myhref.get_attribute("href")
    start_urls.append(websites)
##关闭浏览器
driver.quit()

##控制Tor改变ip
def change_ip():
    controller.authenticate()
    controller.signal(Signal.NEWNYM)
    print("ip has changed")

##使用Tor
controller = Controller.from_port(port=9151)
socks.set_default_proxy(socks.SOCKS5,"127.0.0.1",9150)
socket.socket = socks.socksocket
count2 = 0

##忽略warning
requests.packages.urllib3.disable_warnings()
for website in start_urls:
    req = requests.get(url=website,verify=False).text
    sel = etree.HTML(req)
    title_list = sel.xpath('//span[@property="v:itemreviewed"]/text()')
    ##一旦ip被封，改变ip
    while len(title_list) ==0:
        print("i got nothing")
        change_ip()
        req = requests.get(url=website,verify=False).text
        sel = etree.HTML(req)
        title_list = sel.xpath('//span[@property="v:itemreviewed"]/text()')

    ##提取影片信息
    title_item = title_list
    year_list = sel.xpath('//span[@class="year"]/text()')
    if len(year_list) ==0:
        year_list.append("Nan")
    year_item = year_list
    directors_list = sel.xpath('//a[@rel="v:directedBy"]/text()')
    if len(directors_list) ==0:
        directors_list.append("Nan")
    directors_item = directors_list
    rate_list = sel.xpath('//strong[@class="ll rating_num"]/text()')
    if len(rate_list) ==0:
        rate_list.append("Nan")
    rate_item = rate_list
    actors_list = sel.xpath('//a[@rel="v:starring"]/text()')
    if len(actors_list) ==0:
        actors_list.append("Nan")
    actors_item = actors_list
    type_list = sel.xpath('//span[@property="v:genre"]/text()')
    if len(type_list) ==0:
        type_list.append("Nan")
    type_item = type_list
    countries_list = sel.xpath(
        '//div[@id="info"]/span[contains(text(),"语言:")]/preceding-sibling::text()[2]')
    if len(countries_list) ==0:
        countries_list.append("Nan")
    countries_item = countries_list

    ##向列表中添加元素
    title.append(title_item)
    year.append(year_item)
    directors.append(directors_item)
    rate.append(rate_item)
    actors.append(actors_item)
    type.append(type_item)
    countries.append(countries_item)
    count2 +=1
    print("%d finished"%count2)

##将列表合成一个dataframe
doubanbd = pd.DataFrame(index=["title","id","year","directors","rate","actors","type","countries"],
                        data=[title,id,year,directors,rate,actors,type,countries]).T

##对生成的dataframe做数据清洗
doubanbd = doubanbd.drop(doubanbd.columns[0],axis=1)
for i in doubanbd.index:
    for j in doubanbd.columns:
        if type(doubanbd.loc[i,j]) == str:
            doubanbd.loc[i,j] = doubanbd.loc[i,j].strip("[]\'\"()").replace("'","").replace("\"","").replace("/","")
##保存
doubanbd.to_csv("newdoubandb.csv")
print("success")




