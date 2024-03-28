import json
import csv
import requests
import time
from lxml import etree
import re
import random

# List of user agents for headers
USER_AGENTS = [

        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0",
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/82.0.4051.0 Safari/537.36 Edg/82.0.425.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0",

    ]

# Headers for requests
headers = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language':'zh,zh-CN;q=0.9',
    'Cache-Control':'max-age=0',
    'Connection':'keep-alive',
    'Cookie':'lianjia_uuid=04e2b6bb-c316-4fde-bd99-da6f523979ed; _smt_uid=62874aa1.1af00852; _ga=GA1.2.149600531.1653033654; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22180e07b8724aad-0963a9fbe639b2-34736704-1296000-180e07b8725dbe%22%2C%22%24device_id%22%3A%22180e07b8724aad-0963a9fbe639b2-34736704-1296000-180e07b8725dbe%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; Hm_lvt_9152f8221cb6243a53c83b956842be8a=1653033632,1654410939,1654502635; _jzqc=1; _jzqckmp=1; _gid=GA1.2.847477415.1654654714; _qzjc=1; crosSdkDT2019DeviceId=er5f4u-3d1r8d-m39srci5dbaoi66-j5gojjhuj; login_ucid=2000000141499983; lianjia_token=2.0010613e64728b4dc701cc1755b5bb8247; lianjia_token_secure=2.0010613e64728b4dc701cc1755b5bb8247; security_ticket=KcArx4xWnFsTLADvHxT+qqp2B+6xsiBRg6z8oY9MvmE8L/dqQVBkBj6xl1Ky+ur+E6IMkH+mvsfiE8on64cNDi4nlsrNOHdJupBQRibIrDCFc+8bz+XGAJ/YIlrLk+G3jxT/ZTVg3Z13i42xf0A+dN8HkEcpu5HNz/o8MJEUAuc=; select_city=310000; _jzqx=1.1654410920.1654659738.3.jzqsr=bing%2Ecom|jzqct=/.jzqsr=sh%2Elianjia%2Ecom|jzqct=/chengjiao/; lianjia_ssid=0fb27917-7348-4668-af9c-636df6981d17; Hm_lpvt_9152f8221cb6243a53c83b956842be8a=1654677695; _qzja=1.927548446.1653033672525.1654662857574.1654677695709.1654663350041.1654677695709.0.0.0.15.5; _qzjto=14.4.0; _jzqa=1.2848630643211846700.1653033634.1654662857.1654677696.7; srcid=eyJ0Ijoie1wiZGF0YVwiOlwiMjVhYjM2ZGRkYTFlNDI1NzFlZTM4Y2ZlNTI5MDI3ZmM4YmVjMWRlMzc4ZjYzNDczNDJjOTg4MjgzZjUwMWQ0Zjk3NjZkMTJkMDNhNTY5ZmQ4ZDdjMzZhMTQ5YzgzNDZlYzJjYzIxNjEyNjk4N2M4YTAwYmI5NDYwZjNiMDE1ZWQ4NDc0OWQxNDJjOTU5NjI5NDQ0MDc5NDlmZDI3NzcwNzg1NjdiMmYwMTc4Zjk2MWFmODI4NDg1OWRkYjBiOTdhZTRiYWNmMTYxMmYyNzBiNDA3NTk3NGIzOTc5NTE2MTA3MWRhNDRmOTI3Zjc1ZGE3YzUyMzc2Y2E3ODIwM2UwMFwiLFwia2V5X2lkXCI6XCIxXCIsXCJzaWduXCI6XCI3Mzg2YzY3ZFwifSIsInIiOiJodHRwczovL3NoLmxpYW5qaWEuY29tL2NoZW5namlhby8iLCJvcyI6IndlYiIsInYiOiIwLjEifQ==; _qzjb=1.1654677695709.1.0.0.0; _jzqb=1.1.10.1654677696.1; _gat=1; _gat_past=1; _gat_global=1; _gat_new_global=1; _gat_dianpu_agent=1',
    'Sec-Fetch-Dest':'document',
    'Sec-Fetch-Mode':'navigate',
    'Sec-Fetch-Site':'none',
    'Sec-Fetch-User':'?1',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent':random.choice(USER_AGENTS),
    'sec-ch-ua':'" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
    'sec-ch-ua-mobile':'?0',
    'sec-ch-ua-platform':'"macOS"',
}

def scrape_house_data():
    """
    Scrapes house data from lianjia.
    """
    url = 'https://sh.lianjia.com/chengjiao/'
    req = requests.get(url, headers=headers)
    if req.status_code == 200:
        response = etree.HTML(req.text)
        item = response.xpath('//div[@data-role="ershoufang"]/div/a/@href')
        for items in item:
            link = 'https://sh.lianjia.com' + items
            extract_house_links(link)
    else:
        print(f'error:  {req.status_code}')
        time.sleep(400)

def extract_house_links(link):
    """
    Extracts house links from the given list page URL.
    """
    req = requests.get(link, headers=headers)
    if req.status_code == 200:
        response = etree.HTML(req.text)
        item = response.xpath('//div[@data-role="ershoufang"]/div[2]/a/@href')
        for items in item:
            link_url = 'https://sh.lianjia.com' + items
            get_house_page_urls(link_url)
    else:
        print(f'error2:  {req.status_code}')
        time.sleep(400)

def get_house_page_urls(link_url):
    """
    Retrieves URLs for each page of house listings from the given link URL.
    """
    req = requests.get(link_url, headers=headers)
    if req.status_code == 200:
        next_page = re.findall('"totalPage":(\d+),', req.text)
        if next_page != []:
            next_pages = int(''.join(next_page))+1
            print('总页数', next_pages-1)
            for i in range(1, next_pages, 1):
                next_page_url = link_url + 'pg{}/'.format(i)
                print('下一页', next_page_url)
                extract_house_details(next_page_url)
    else:
        print(f'error3:  {req.status_code}')
        time.sleep(400)

def extract_house_details(next_page_url):
    """
    Extracts house URLs from each page of listings.
    """
    req = requests.get(next_page_url, headers=headers)
    if req.status_code == 200:
        response = etree.HTML(req.text)
        item = response.xpath('//ul[@class="listContent"]/li/a/@href')
        for house_url in item:
            scrape_house_details(house_url)
    else:
        print(f'error4:  {req.status_code}')
        time.sleep(400)


def scrape_house_details(house_url):
    """
    Scrapes details of individual houses.
    """
    req = requests.get(house_url, headers=headers)
    if req.status_code == 200:
        response = etree.HTML(req.text)
        # Title
        title = response.xpath('//h1[@class="index_h1"]/text()' or '//title/text()')
        if title == []:
            title = ['']
        print(title)
        # Price
        price = response.xpath('//div[@class="price"]/b/text()' or '//span[@class="record_price"]/text()')
        if price == []:
            price = ['']
        print(price)

        # House type
        house_type = response.xpath('//div[@class="base"]/div[2]/ul/li[1]/text()')
        if house_type == []:
            house_type = ['']
        print(house_type)

        # Floor
        floor = response.xpath('//div[@class="base"]/div[2]/ul/li[2]/text()')
        if floor == []:
            floor = ['']
        print(floor)

        # Building area
        area = response.xpath('//div[@class="base"]/div[2]/ul/li[3]/text()')
        if area == []:
            area = ['']
        print(area)

        # Layout structure
        structure = response.xpath('//div[@class="base"]/div[2]/ul/li[4]/text()')
        if structure == []:
            structure = ['']
        print(structure)

        # Inside area
        Inside_area = response.xpath('//div[@class="base"]/div[2]/ul/li[5]/text()')
        if Inside_area == []:
            Inside_area = ['']
        print(Inside_area)

        # Building type
        Building_Type = response.xpath('//div[@class="base"]/div[2]/ul/li[6]/text()')
        if Building_Type == []:
            Building_Type = ['']
        print(Building_Type)

        # House orientation
        towards = response.xpath('//div[@class="base"]/div[2]/ul/li[7]/text()')
        if towards == []:
            towards = ['']
        print(towards)

        # Building structure
        building_structure = response.xpath('//div[@class="base"]/div[2]/ul/li[10]/text()')
        if building_structure == []:
            building_structure = ['']
        print(building_structure)

        # Renovation condition
        renovation_condition = response.xpath('//div[@class="base"]/div[2]/ul/li[9]/text()')
        if renovation_condition == []:
            renovation_condition = ['']
        print(renovation_condition)
        # url
        url = house_url
        print(url)

        # Longitude
        resblockPosition = ''.join(re.findall("resblockPosition:'(.*?)'", req.text)).split(',')     
        longitude = resblockPosition[0]
        if longitude == '':
            longitude = ['']
        print(longitude)

        # Latitude
        latitude = resblockPosition[1]
        if latitude == '':
            latitude = ['']
        print(latitude)

        # Elevator
        elevator = response.xpath('//div[@class="base"]/div[2]/ul/li[13]/text()')
        if elevator == []:
            elevator = ['']
        print(elevator)

        # Year of construction
        year = response.xpath('//div[@class="base"]/div[2]/ul/li[8]/text()')
        if year == []:
            year = ['']
        print(year)

        # Transaction date
        data_year = response.xpath('//div[@class="wrapper"]/span/text()')
        if data_year == []:
            data_year = ['']
        print(data_year)

        # API Latitude and Longitude
        location = latitude + ',' + longitude
        print(location)

        # Transportation - Bus station
        bus_api = 'https://api.map.baidu.com/place/v2/search?query=%E5%85%AC%E4%BA%A4%E7%AB%99&location={}&radius=2000&output=json&ak=0SyW9kfIKx7G5j5YLAjAe7Yn02RGVsHE'.format(location)

        bus = requests.get(bus_api, headers=headers)
        bus_json = json.loads(bus.text)
        bus_results = len(bus_json['results'])
        print(bus_results)

        # Transportation - Subway station
        dt_url = 'https://api.map.baidu.com/place/v2/search?query=%E5%9C%B0%E9%93%81%E7%AB%99&location={}&radius=2000&output=json&ak=0SyW9kfIKx7G5j5YLAjAe7Yn02RGVsHE'.format(location)
        dt = requests.get(dt_url, headers=headers)
        dt_json = json.loads(dt.text)
        dt_results = len(dt_json['results'])
        print(dt_results)

        # Medical - Hospital
        yy_url = 'https://api.map.baidu.com/place/v2/search?query=%E5%8C%BB%E9%99%A2&location={}&radius=2000&output=json&ak=0SyW9kfIKx7G5j5YLAjAe7Yn02RGVsHE'.format(location)
        yy = requests.get(yy_url, headers=headers)
        yy_json = json.loads(yy.text)
        yy_results = len(yy_json['results'])
        print(yy_results)


        # Medical - Pharmacy
        yd_url = 'https://api.map.baidu.com/place/v2/search?query=%E8%8D%AF%E5%BA%97&location={}&radius=2000&output=json&ak=0SyW9kfIKx7G5j5YLAjAe7Yn02RGVsHE'.format(location)
        yd = requests.get(yd_url, headers=headers)
        yd_json = json.loads(yd.text)
        yd_results = len(yd_json['results'])
        print(yd_results)

        # Entertainment - Sports arena
        ty_url = 'https://api.map.baidu.com/place/v2/search?query=%E4%BD%93%E8%82%B2%E9%A6%86&location={}&radius=2000&output=json&ak=0SyW9kfIKx7G5j5YLAjAe7Yn02RGVsHE'.format(location)
        ty = requests.get(ty_url, headers=headers)
        ty_json = json.loads(ty.text)
        ty_results = len(ty_json['results'])
        print(ty_results)

        # Entertainment - Gym
        js_url = 'https://api.map.baidu.com/place/v2/search?query=%E5%81%A5%E8%BA%AB%E6%88%BF&location={}&radius=2000&output=json&ak=0SyW9kfIKx7G5j5YLAjAe7Yn02RGVsHE'.format(location)
        js = requests.get(js_url, headers=headers)
        js_json = json.loads(js.text)
        js_results = len(js_json['results'])
        print(js_results)

        # Entertainment - Park
        gy_url = 'https://api.map.baidu.com/place/v2/search?query=%E5%85%AC%E5%9B%AD&location={}&radius=2000&output=json&ak=0SyW9kfIKx7G5j5YLAjAe7Yn02RGVsHE'.format(location)
        gy = requests.get(gy_url, headers=headers)
        gy_json = json.loads(gy.text)
        gy_results = len(gy_json['results'])
        print(gy_results)

        # Entertainment - Cinema
        dy_url = 'https://api.map.baidu.com/place/v2/search?query=%E7%94%B5%E5%BD%B1%E9%99%A2&location={}&radius=2000&output=json&ak=0SyW9kfIKx7G5j5YLAjAe7Yn02RGVsHE'.format(location)
        dy = requests.get(dy_url, headers=headers)
        dy_json = json.loads(dy.text)
        dy_results = len(dy_json['results'])
        print(dy_results)


        # Education - Primary school
        xx_url = 'https://api.map.baidu.com/place/v2/search?query=%E5%B0%8F%E5%AD%A6&location={}&radius=2000&output=json&ak=0SyW9kfIKx7G5j5YLAjAe7Yn02RGVsHE'.format(location)
        xx = requests.get(xx_url, headers=headers)
        xx_json = json.loads(xx.text)
        xx_results = len(xx_json['results'])
        print(xx_results)

        # Education - Middle school
        zx_url = 'https://api.map.baidu.com/place/v2/search?query=%E4%B8%AD%E5%AD%A6&location={}&radius=2000&output=json&ak=0SyW9kfIKx7G5j5YLAjAe7Yn02RGVsHE'.format(location)
        zx = requests.get(zx_url, headers=headers)
        zx_json = json.loads(zx.text)
        zx_results = len(zx_json['results'])
        print(zx_results)

        # Education - University
        dx_url = 'https://api.map.baidu.com/place/v2/search?query=%E5%A4%A7%E5%AD%A6&location={}&radius=2000&output=json&ak=0SyW9kfIKx7G5j5YLAjAe7Yn02RGVsHE'.format(location)
        dx = requests.get(dx_url, headers=headers)
        dx_json = json.loads(dx.text)
        dx_results = len(dx_json['results'])
        print(dx_results)

        # Education - Kindergarten
        yey_url = 'https://api.map.baidu.com/place/v2/search?query=%E5%B9%BC%E5%84%BF%E5%9B%AD&location={}&radius=2000&output=json&ak=0SyW9kfIKx7G5j5YLAjAe7Yn02RGVsHE'.format(location)
        yey = requests.get(yey_url, headers=headers)
        yey_json = json.loads(yey.text)
        yey_results = len(yey_json['results'])
        print(yey_results)

        # Lifestyle - ATM
        atm_url = 'https://api.map.baidu.com/place/v2/search?query=ATM&location={}&radius=2000&output=json&ak=0SyW9kfIKx7G5j5YLAjAe7Yn02RGVsHE'.format(location)
        atm = requests.get(atm_url, headers=headers)
        atm_json = json.loads(atm.text)
        atm_results = len(atm_json['results'])
        print(atm_results)

        # Lifestyle - Coffee shop
        kf_url = 'https://api.map.baidu.com/place/v2/search?query=%E5%92%96%E5%95%A1%E9%A6%86&location={}&radius=2000&output=json&ak=0SyW9kfIKx7G5j5YLAjAe7Yn02RGVsHE'.format(location)
        kf = requests.get(kf_url, headers=headers)
        kf_json = json.loads(kf.text)
        kf_results = len(kf_json['results'])
        print(kf_results)

        # Lifestyle - Bank
        yh_url = 'https://api.map.baidu.com/place/v2/search?query=%E9%93%B6%E8%A1%8C&location={}&radius=2000&output=json&ak=0SyW9kfIKx7G5j5YLAjAe7Yn02RGVsHE'.format(location)
        yh = requests.get(yh_url, headers=headers)
        yh_json = json.loads(yh.text)
        yh_results = len(yh_json['results'])
        print(yh_results)


        # Lifestyle - Restaurant
        ct_url = 'https://api.map.baidu.com/place/v2/search?query=%E9%A4%90%E5%8E%85&location={}&radius=2000&output=json&ak=0SyW9kfIKx7G5j5YLAjAe7Yn02RGVsHE'.format(location)
        ct = requests.get(ct_url, headers=headers)
        ct_json = json.loads(ct.text)
        ct_results = len(ct_json['results'])
        print(ct_results)

        # Shopping - Shopping mall
        sc_url = 'https://api.map.baidu.com/place/v2/search?query=%E5%95%86%E5%9C%BA&location={}&radius=2000&output=json&ak=0SyW9kfIKx7G5j5YLAjAe7Yn02RGVsHE'.format(location)
        sc = requests.get(sc_url, headers=headers)
        sc = json.loads(sc.text)
        sc_results = len(sc['results'])
        print(sc_results)

        # Shopping - Market
        shc_url = 'https://api.map.baidu.com/place/v2/search?query=%E5%B8%82%E5%9C%BA&location={}&radius=2000&output=json&ak=0SyW9kfIKx7G5j5YLAjAe7Yn02RGVsHE'.format(location)
        shc = requests.get(shc_url, headers=headers)
        shc = json.loads(shc.text)
        shc_results = len(shc['results'])
        print(shc_results)

        # Shopping - Supermarket
        cs_url = 'https://api.map.baidu.com/place/v2/search?query=%E8%B6%85%E5%B8%82&location={}&radius=2000&output=json&ak=0SyW9kfIKx7G5j5YLAjAe7Yn02RGVsHE'.format(location)
        cs = requests.get(cs_url, headers=headers)
        cs = json.loads(cs.text)
        cs_results = len(cs['results'])
        print(cs_results)

        save = title+price+house_type+floor+area+structure+Inside_area+Building_Type+towards+building_structure+renovation_condition+[url]+[longitude]+[latitude]+elevator+year+ data_year + [bus_results]+[dt_results]+[yy_results]+[yd_results]+[ty_results]+[js_results]+[gy_results]+[dy_results]+[xx_results]+\
                       [zx_results]+[dx_results]+[yey_results]+[atm_results]+[kf_results]+[yh_results]+[ct_results]+[sc_results]+[shc_results]+[cs_results]
        print(save)
        with open('链家.csv', 'a+', encoding='utf-8-sig', newline='') as f:
            f = csv.writer(f)
            f.writerow(save)
            print('saccd')
    else:
        print(f'error4:  {req.status_code}')
        time.sleep(400)

if __name__ == '__main__':
    # Initialize CSV file
    save_name = ['标题'] + ['价格'] + ['房屋户型'] + ['所在楼层'] + ['建筑面积'] + ['户型结构'] + ['套内面积'] + ['建筑类型'] + ['房屋朝向'] + ['建筑结构'] + ['装修情况'] + ['url'] + ['经度'] + ['纬度'] + ['电梯'] + ['建成年代'] + ['成交时间'] + ['交通_公交站'] + ['交通_地铁站'] + ['医疗_医院'] + ['医疗_药店'] + ['娱乐_体育馆'] + ['娱乐_健身房'] + ['娱乐_公园'] + ['娱乐_电影院'] + ['教育_小学'] + ['教育_中学'] + ['教育_大学'] + ['教育_幼儿园'] + ['生活_ATM'] + ['生活_咖啡馆'] + ['生活_银行'] + ['生活_餐厅'] + ['购物_商场'] + ['购物_市场'] + ['购物_超市']
    with open('rawdata.csv', 'a+', encoding='utf-8-sig', newline='') as f:
        f = csv.writer(f)
        f.writerow(save_name)
    scrape_house_data()