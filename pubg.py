# -*- coding: utf-8 -*-

'''
This a Spider that I wrote it for a short time at 2017...
'''


import numpy as np
from bs4 import BeautifulSoup
import requests
import xlwt

#The value of  __cfduid in the cookies maybe need to change
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
COOKIES = {'__cfduid': 'd44db92eab1474bde64206da8c5e0f5b11507046474',
           'cf_clearance': '187c74875d4cb11dd9c985baae1cb43c272bf631-1507209348-1800',
           'language': 'en-US',
           'cdmu': '1507082693368',
           'cdmblk2': '0:0:0:0:0:0:0:0:0:0:0:0:0:0,0:0:0:0:0:0:0:0:0:0:0:0:0:0,0:0:0:0:0:0:0:0:0:0:0:0:0:0,0:0:0:0:0:0:0:0:0:0:0:0:0:0,0:0:0:0:0:0:0:0:0:0:0:0:0:0,0:0:0:0:0:0:0:0:0:0:0:0:0:0,0:0:0:0:0:0:0:0:0:0:0:0:0:0,0:0:0:0:0:0:0:0:0:0:0:0:0:0; cdmblk=0:0:0:0:0:0:0:0:0:0:0:0:0:0,0:0:0:0:0:0:0:0:0:0:0:0:0:0,0:0:0:0:0:0:0:0:0:0:0:0:0:0,0:0:0:0:0:0:0:0:0:0:0:0:0:0,0:0:0:0:0:0:0:0:0:0:0:0:0:0,0:0:0:0:0:0:0:0:0:0:0:0:0:0,0:0:0:0:0:0:0:0:0:0:0:0:0:0,0:0:0:0:0:0:0:0:0:0:0:0:0:0',
           'cdmtlk': '0:0:0:0:0:0:0:0:0:0:0:0:0:0',
           'cdmgeo': 'us',
           'cdmbaserate': '2.1',
           'cdmbaseraterow': '1.1',
           'cdmint': '0'}


def get_soup(url, headers=HEADERS, cookies=COOKIES):
    req = requests.get(url, headers=headers, cookies=cookies)
    html = req.text
    soup = BeautifulSoup(html, 'lxml')
    return soup


def get_player(soup):
    url = 'https://pubg.me'
    players = (soup.body.div.next_sibling.div.div.next_sibling.div.div.next_sibling
              .table.tbody.find_all('tr'))
    link_pool = []
    for player in players:
        link = url + player.find_all(class_="sidebar-user-link")[0].attrs['href'] + '/solo'
        link_pool.append(link)
    return link_pool

# 获取每个页面的信息
def get_data(url):
    soup = get_soup(url)
    data = soup.find_all('div', class_='card mb-3')
    data_list = []
    for i in data:
        data_list += i.find_all('div', class_='col-md-4')
    value_list = []
    label_list = []
    for i in data_list:
        for j in i.contents:
            value_list.append(j.contents[0].string)
            label_list.append(j.contents[-1].string)
    return [label_list, value_list]

# 按顺序获取7*100个有效数据（想获取所有数据请把第73行后面的索引注释掉）
def get_all(link_pool):
    data_list = get_data(link_pool[0])
    for link in link_pool[1:]:
        user = get_data(link)[1]
        if user:                          # 确定user数据不空
            data_list.append(user)
    data_list = np.array(data_list)[:, (3, 30, 32, 18, 20, 13, 14)]
    return data_list


def exl(data, place):
    # initiate
    workbook = xlwt.Workbook(encoding='ascii')
    worksheet = workbook.add_sheet('%s Solo Top 100' % place)
    # write data
    for idx in range(data.shape[0]):
        for j in range(data.shape[1]):
            assert isinstance(worksheet, object)
            worksheet.write(idx, j, label=data[idx][j])
    # save
    workbook.save('pubg_%s.xls' % place)
    

def my_float(x):
    try:
        return float(x)
    except:
        try:
            return float(x[:-1])            
        except:
            return float(x[:-2])            
        
# 
def asfloat(data):
    new = np.zeros_like(data, dtype=np.float64)
    for i in range(new.shape[0]):
        for j in range(new.shape[1]):
            new[i, j] = my_float(data[i, j])
    return new

'''
获取各服务器数据并保存，建议这5组不要一起跑，可能会timeout出错
'''
if __name__ == '__main__':
    data_as = get_all(get_player(get_soup('https://pubg.me/players/rating/?season=2017-pre4&region=as&match=solo')))
    exl(data_as, 'as')

    data_eu = get_all(get_player(get_soup('https://pubg.me/players/rating/?season=2017-pre4&region=eu&match=solo')))
    exl(data_eu, 'eu')

    data_na = get_all(get_player(get_soup('https://pubg.me/players/rating/?season=2017-pre4&region=na&match=solo')))
    exl(data_na, 'na')

    data_oc = get_all(get_player(get_soup('https://pubg.me/players/rating/?season=2017-pre4&region=oc&match=solo')))
    exl(data_oc, 'oc')

    data_sea = get_all(get_player(get_soup('https://pubg.me/players/rating/?season=2017-pre4&region=sea&match=solo')))
    exl(data_sea, 'sea')