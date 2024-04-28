import baostock as bs
import pandas as pd
import datetime 
from unicodedata import decimal
from utils import ZQ,dlbs
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator, close


# @dlbs
class GpJx(ZQ):
    '''
    股票交易信息。
    参数：
        zqdm: string, 证券代码
        data_date: string, 数据日期
    返回值：
        
    '''
    def __init__(self,zqdm,sj_rq):
        self.zqdm=zqdm
        self.sj_rq = sj_rq
        self.gp = bs.query_history_k_data_plus(
            self.zqdm,
            # "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,isST",
            "date,code,open,high,low,close,pctChg,isST",
            start_date=self.sj_rq,
            end_date=self.sj_rq,
            frequency="d",
            adjustflag="3").get_data()
        # print(self.gp)

    def hq_gp_spj(self):
        '''获取股票某日收盘价（闭市价格)函数'''
        gp_spj = self.gp['close'].astype(float)
        return gp_spj

    def hq_gp_zdf(self):
        '''获取股票某日涨跌幅函数
            1、没有涨跌幅的股票统一替换为0。
            （Todo:这里转化可能有问题，当遇到确实需要对自然涨跌和异常停牌的股票做出区分处理时候，代码要进行修改。）
        '''
        gp_zdf = self.gp['pctChg'].replace('',0).astype(float)
        return gp_zdf

    def hq_gp_sfst(self):
        '''获取股票某日是否ST（sfst）函数'''
        gp_sfst = self.gp['isST'].astype(str)
        return gp_sfst
    

if __name__ == '__main__':
    lg = bs.login()
    GpJx=GpJx('sh.000001','2024-01-19')
    print(GpJx.hq_gp_spj())
    print(GpJx.hq_gp_zdf())
    print(GpJx.hq_gp_sfst())
    bs.logout()
