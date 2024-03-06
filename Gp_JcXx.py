# -*- encoding: utf-8 -*-
'''
@File    :   ALLstock_data.py
@Time    :   2023/11/30 11:38:13
@Author  :   MacLyre 
@Version :   1.0
@Contact :   tiekaa@outlook.com
@WebSite :   www.tiekaa.com
下载baostock的股票名称数据。
'''
# Start typing your code from here

import baostock as bs
import pandas as pd
from utils import ZQ,dlbs
import datetime


# @dlbs
def hq_gp_jcxx(zqdm):
    '''
    获取股票基础信息
    '''
    # gp_jcxx = bs.query_stock_basic(code=zqdm).get_row_data()
    gp_jcxx = bs.query_stock_basic(code=zqdm).get_data()
    print(gp_jcxx)
    print(type(gp_jcxx["code_name"][0].find('STT')))
    print(gp_jcxx["code_name"][0].find('STT'))
    return gp_jcxx

def pd_jyr(sj_rq):
    '''
    判断是否交易日
    '''
    #### 获取交易日信息 ####
    # end_date：结束日期，为空时默认为当前日期。
    rs = bs.query_trade_dates(start_date=sj_rq)
    # print('query_trade_dates respond error_code:'+rs.error_code)
    # print('query_trade_dates respond  error_msg:'+rs.error_msg)

    #### 打印结果集 ####
    data_list = []
    while (rs.error_code == '0') & rs.next():
        # 获取一条记录，将记录合并在一起
        data_list.append(rs.get_row_data())
    result = pd.DataFrame(data_list, columns=rs.fields)
    return result['is_trading_day'][0]

@dlbs
def hq_sgjyr(sj_rq):
    '''
    获取上个交易日
    '''
    # 将字符串转换为datetime对象
    rqgs_sj_rq = datetime.datetime.strptime(sj_rq, "%Y-%m-%d")
    # 获取前一天的日期
    rqge_qyt = rqgs_sj_rq - datetime.timedelta(days=1)
    # 将结果转换回字符串格式
    zfc_qyt = rqge_qyt.strftime("%Y-%m-%d")

    while pd_jyr(zfc_qyt) == '0' :
        # 获取前一天的日期
        rqge_qyt = rqge_qyt - datetime.timedelta(days=1)
        # 将结果转换回字符串格式
        zfc_qyt = rqge_qyt.strftime("%Y-%m-%d")

    # print(zfc_qyt)
    return zfc_qyt


def XzGpMz(sj_rq):
    '''
    下载股票名字文件
    参数：
        etl_date: string, 数据日期
    返回值：
        无
    '''
    #### 登陆系统 ####
    lg = bs.login()
    # 显示登陆返回信息
    print('login respond error_code:'+lg.error_code)
    print('login respond  error_msg:'+lg.error_msg)

    #### 获取证券信息 ####
    rs = bs.query_all_stock(day=sj_rq)
    print('query_all_stock respond error_code:'+rs.error_code)
    print('query_all_stock respond  error_msg:'+rs.error_msg)


    #### 打印结果集 ####
    data_list = []
    while (rs.error_code == '0') & rs.next():
        # 获取一条记录，将记录合并在一起
        data_list.append(rs.get_row_data())
    result = pd.DataFrame(data_list, columns=rs.fields)

    #### 结果集输出到csv文件 ####   
    result.to_csv("C:\SoftwareZ\SProjects\PyProjects\Stock\data\\all_stock.csv", encoding="utf-8", index=False)
    print(result)

    #### 登出系统 ####
    bs.logout()


if __name__ == '__main__':
    #### 登陆系统 ####
    lg = bs.login()
    # XzGpMz('2023-11-29')
    # hq_gp_jcxx('sh.600864')
    # GpJcXx('sz.002156')
    pd_jyr('2024-03-04')
    hq_sgjyr('2024-03-04')
    #### 登出系统 ####
    bs.logout()