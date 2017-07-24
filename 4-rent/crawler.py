#-*- coding:utf-8 -*-
from pyquery import PyQuery as pq
import csv
from urllib.parse import urljoin

url = "http://hz.58.com/pinpaigongyu/pn/{page}/?minprice=800_1500"
page=0
csv_file=open('rent.csv','w',newline='',encoding='utf8')
csv_writer=csv.writer(csv_file,delimiter=',')

while True:
    page+=1
    print('featch :',url.format(page=page))
    d=pq(url=url.format(page=page))
    house_list=d('.list>li')
    
    if not house_list:
        break

    for house in house_list:
        house=pq(house)
        house_title=house('.des h2').text()
        house_url=urljoin(url,house('a').attr('href'))
        house_info_list=house_title.split()
        house_loc=house_info_list[1]
        house_money=house('.money span b').text()
        
        csv_writer.writerow([house_title,house_loc,house_url,house_money])

csv_file.close()