# coding: utf-8

"""命令行火车票查看器

Usage:
    ticket [-gdtkz] [-S] <from> <to> <date>

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
        url ="https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&leftTicketDTO.to_station={}&purpose_codes=0X00".format(date,from_station,to_station)
    else:
        url="https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&leftTicketDTO.to_station={}&purpose_codes=ADULT".format(date,from_station,to_station)   
    options=''.join([key for key,value in args.items() if value is True])
    print(options)
    r=requests.get(url,verify=False)  #verify=False参数不验证证书
    available_trains_list=r.json()['data']['result']
    TrainCollection(available_trains_list,options).pretty_print()


if __name__ == '__main__':
    cli()
