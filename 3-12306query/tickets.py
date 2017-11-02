# coding: utf-8

"""命令行火车票查看器

Usage:
    tickets [-gdtkz] [-S] <from> <to> <date>

Options:
    -h,--help   显示帮助菜单
    -g          高铁
    -d          动车
    -t          特快
    -k          快速
    -z          直达
    -S          学生票
Example:
    tickets 北京 上海 2017-10-10
    tickets -dg 北京 湖州 2017-10-10
"""
from docopt import docopt
from stations import stations
import requests
from prettytable import PrettyTable
from colorama import init, Fore
requests.packages.urllib3.disable_warnings() 
init()

new_station= dict([(v,k) for k,v in stations.items()])

class TrainCollection(object):
    header='车次 车站 时间 历时 商务座 一等座 二等座 高级软卧 软卧 动卧 硬卧 软座 硬座 无座'.split()

    def __init__(self,available_trains_list,options):
        self.available_trains_list=available_trains_list
        self.options=options

    @property
    def trains(self):
        for raw_train in self.available_trains_list:
            train_type=raw_train.split('|')[3][0].lower()
            if (not self.options) or train_type in self.options:
                raw_train=raw_train.split('|')
                train_no=raw_train[3]
                train_from=raw_train[6]
                train_to=raw_train[7]
                train_start_time=raw_train[8]
                train_end_time=raw_train[9]
                train_duration_time=raw_train[10]
                seat_swz=raw_train[32] #商务座
                seat_zy=raw_train[31]#一等座
                seat_ze=raw_train[30]#二等座            
                seat_gr=raw_train[21]# 高级软卧 
                seat_rw=raw_train[23]# 软卧 
                seat_srrb=raw_train[33]# 动卧 
                seat_yw=raw_train[28]# 硬卧 
                seat_rz=raw_train[24]# 软座 
                seat_yz=raw_train[29]# 硬座 
                seat_wz=raw_train[26]# 无座
                train=[       
                        train_no,
                        Fore.GREEN+new_station[train_from]+ Fore.RESET+'\n'+Fore.RED+new_station[train_to]+ Fore.RESET,
                        Fore.GREEN+train_start_time+ Fore.RESET+'\n'+Fore.RED+train_end_time+ Fore.RESET,
                        train_duration_time,
                        seat_swz, 
                        seat_zy,
                        seat_ze,            
                        seat_gr,
                        seat_rw, 
                        seat_srrb,
                        seat_yw, 
                        seat_rz, 
                        seat_yz, 
                        seat_wz
                    ]
                
                yield train

    def pretty_print(self):
        pt=PrettyTable()
        pt._set_field_names(self.header)
        for train in self.trains:
            pt.add_row(train)
        print(pt)

def cli():
    """command-line interface"""
    args=docopt(__doc__)
    from_station=stations.get(args['<from>'])
    to_station=stations.get(args['<to>'])
    stu_ticket=args['-S']
    date=args['<date>']
    if stu_ticket is True:
        url ="https://kyfw.12306.cn/otn/leftTicket/queryX?leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&leftTicketDTO.to_station={}&purpose_codes=0X00".format(date,from_station,to_station)
    else:
        url="https://kyfw.12306.cn/otn/leftTicket/queryX?leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&leftTicketDTO.to_station={}&purpose_codes=ADULT".format(date,from_station,to_station)  

    headers = {
 
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Connection'  :'keep-alive',
        'Cookie':'JSESSIONID=D10FCA9BD6E9D67F8AAB9EADE7CC586E; route=6f50b51faa11b987e576cdb301e545c4; BIGipServerotn=1190134282.38945.0000; fp_ver=4.5.1; RAIL_EXPIRATION=1505374038667; RAIL_DEVICEID=hgVoDOxI1ynw5daRKZjfzRvgetpJbXoKEUl6l63X2k6VnJVQ_iBtDlEpBiw5qBlCZlqdAx6HQ0BAs0z6rRiHVuB20979A8VqgvTx4eYnsBqu6QgTZWZCiqpW0wvREZ7jhPjhmJFouqRq-XC6ShWkj2iB39Km1J7N; _jc_save_fromStation=%u5317%u4EAC%2CBJP; _jc_save_toStation=%u4E0A%u6D77%2CSHH; _jc_save_fromDate=2017-09-16; _jc_save_toDate=2017-09-11; _jc_save_wfdc_flag=dc',
        'Host':'kyfw.12306.cn',
        'Upgrade-Insecure-Requests'   :'1',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0'
        
    }
    print(url)
    options=''.join([key for key,value in args.items() if value is True])
    print(options)

    r=requests.get(url,headers=headers,verify=False)  #verify=False参数不验证证书
    print(r.json())
    available_trains_list=r.json()['data']['result']
    TrainCollection(available_trains_list,options).pretty_print()


if __name__ == '__main__':
    cli()
