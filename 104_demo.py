import csv
import random
import time

import bs4
import requests

url_A = 'https://www.104.com.tw/jobs/search/?ro=0&kwop=7&keyword=python&order=15&asc=0&page='
url_B = '&mode=s&jobsource=2018indexpoc'

# 找五頁的資料
job_datas = []
for page in range(1, 5 + 1):
    url = url_A + str(page) + url_B
    print(url)
    htmlFile = requests.get(url)
    ObjSoup = bs4.BeautifulSoup(htmlFile.text, 'lxml')

    jobs = ObjSoup.find_all('article', class_='js-job-item')

    for job in jobs:
        # 職缺內容
        job_name = job.find('a', class_="js-job-link").text
        # 公司名稱
        job_company = job.get('data-cust-name')
        # 地址
        job_loc = job.find('ul', class_='job-list-intro').find('li').text
        # 薪資
        job_pay = job.find('span', class_='b-tag--default').text
        # 網址
        job_url = job.find('a').get('href')
        job_data = {'職缺內容': job_name, '公司名稱': job_company,
                    '地址': job_loc, '薪資': job_pay, '網址': job_url}
        job_datas.append(job_data)
    time.sleep(random.randint(1, 3))

fn = '104人力銀行python職缺內容.csv'  # 取CSV檔名
columns_name = ['職缺內容', '公司名稱', '地址', '薪資', '網址']  # 第一欄的名稱
with open(fn, 'w', newline='') as csvFile:
    dictWriter = csv.DictWriter(csvFile, fieldnames=columns_name)
    dictWriter.writeheader()
    for data in job_datas:
        dictWriter.writerow(data)