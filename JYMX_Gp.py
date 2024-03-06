import pandas as pd
import datetime 
from unicodedata import decimal
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator, close

import baostock as bs
from Gp_Jy import GpJx
from utils import ZQ,dlbs
from GM_Gp import GmGp


class JymxGp(ZQ):
    '''
    校验模型股票类。
    参数：
        
    返回值：
        
    '''
    def __init__(self,sj_rq):
        self.sj_rq = sj_rq

    # @dlbs
    def jy_ycjg(self,bjye):
        '''
        校验_预测值-真实值
        参数：
            无
        返回值：
            无
        '''  
        #预测  
        ycjg=GmGp(self.sj_rq).hq_kgmgp_qd(bjye)
        print(ycjg)

        bj = bs.query_history_k_data_plus(
            "sz.002156",
            # "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,isST",
            "date,code,open,high,low,close",
            start_date=self.data_date,
            end_date=self.data_date,
            frequency="d",
            adjustflag="3").get_data()

        bjye_s = bj['close'].astype(float)*200
        # print(bj)
        bjye=bjye_s[0]
        # print(bjye)
        return bjye

    @dlbs
    def hq_kgmgp_qd(self,bjye):
        '''
        获取_可购买股票_清单_非ST股票模型
        参数：
            bjye: float, 本金余额
        返回值：
            无
        '''
        gm_qd = {'gpcode':[],'gpname':[],'gpspj':[],'gpzdf':[],'tdate':[]}
        #### 获取所有证券信息 ####
        zqxx = bs.query_all_stock(day=self.data_date).get_data()
        # print(zqxx)
        for zqcode in zqxx["code"]:
            #获取证券详细信息
            zqxxxx = bs.query_stock_basic(code=zqcode).get_data()
            #获取股票信息
            if not zqxxxx.empty :
                if zqxxxx["type"][0] == '1':
                    # print(zqxxxx["code"][0])
                    zqdm=zqxxxx["code"][0]
                    ## 获取满足本金条件的股票
                    #股票交易信息
                    GpJxxx=GpJx(zqdm,self.data_date)
                    gp_spj=GpJxxx.hq_gp_spj()
                    gp_zdf=GpJxxx.hq_gp_zdf()
                    gp_sfst=GpJxxx.hq_gp_sfst()
                    # print(gp_spj)
                    # print(gp_zdf)
                    # print(gp_sfst)
                    #能够购买，非st，昨日上涨
                    if gp_spj[0]*100 <= bjye and gp_sfst[0]=='0' and gp_zdf[0] > 0:
                        gm_qd['gpcode'].append(zqxxxx["code"][0])
                        gm_qd['gpname'].append(zqxxxx["code_name"][0])
                        gm_qd['gpspj'].append(gp_spj[0])
                        gm_qd['gpzdf'].append(gp_zdf[0])
                        gm_qd['tdate'].append(self.data_date)
                        # print(gm_qd)
                        
        gm_qd = pd.DataFrame(gm_qd)
        gm_qd.to_csv("C:\SoftwareZ\SProjects\PyProjects\Stock\data\k_gm_data.csv")


if __name__ == '__main__':
    # bjye=GmGp('sz.002156','2023-12-26').hq_bjyr()
    bjye=GmGp('2023-12-26').hq_bjyr()
    GmGp('2023-12-26').hq_kgmgp_qd(bjye)
