import pandas as pd
import datetime 
from unicodedata import decimal
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator, close

import baostock as bs
from Gp_Jy import GpJx
from Gp_ZjCw import GpZjCw
from utils import ZQ,dlbs
from Gp_JcXx import hq_sgjyr


class GmGp(ZQ):
    '''
    购买股票类。
    参数：
        sj_rq: string, 数据日期
    返回值：
        
    '''
    def __init__(self,sj_rq):
        self.sj_rq = sj_rq

    @dlbs
    def hq_bjyr(self,dqzqdm,dqzqgf):
        '''
        获取_本金余额（当前）
        参数：
            dqzqdm: string, 当前证券代码
            dqzqgf: int, 当前证券股份
        返回值：
            bjye: float, 本金余额
        '''    
        bj = bs.query_history_k_data_plus(
            dqzqdm,
            # "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,isST",
            "date,code,open,high,low,close",
            start_date=self.sj_rq,
            end_date=self.sj_rq,
            frequency="d",
            adjustflag="3").get_data()

        bjye_s = bj['close'].astype(float)*dqzqgf
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

        #### 获取上证综合指数信息 ####
        shanghaiGpJx=GpJx('sh.000001',self.sj_rq)
        gm_qd['gpcode'].append('sh.000001')
        gm_qd['gpname'].append('上证综合指数')
        gm_qd['gpspj'].append(shanghaiGpJx.hq_gp_spj()[0])
        gm_qd['gpzdf'].append(shanghaiGpJx.hq_gp_zdf()[0])
        gm_qd['tdate'].append(self.sj_rq)
        #### 获取所有证券信息 ####
        zqxx = bs.query_all_stock(day=self.sj_rq).get_data()
        # print(zqxx)
        for zqcode in zqxx["code"]:
            #获取证券详细信息
            zqxxxx = bs.query_stock_basic(code=zqcode).get_data()
            #获取股票信息
            if not zqxxxx.empty :
                if zqxxxx["type"][0] == '1' :
                    # print(zqxxxx["code"][0])
                    zqdm=zqxxxx["code"][0]
                    ## 获取满足购买条件的股票
                    ### 获取满足本金条件的股票
                    #股票交易信息
                    GpJxxx=GpJx(zqdm,self.sj_rq)
                    gp_spj=GpJxxx.hq_gp_spj()
                    gp_zdf=GpJxxx.hq_gp_zdf()
                    gp_sfst=GpJxxx.hq_gp_sfst()
                    # print(gp_spj)
                    # print(gp_zdf)
                    # print(gp_sfst)
                    # 5000+ ----> 237
                    
                    #能够购买，非st，昨日上涨1~9 , 名字中不包含ST
                    if gp_spj[0]*100 <= bjye and gp_sfst[0]=='0' and gp_zdf[0] > 1 and gp_zdf[0] < 9 and zqxxxx["code_name"][0].find('ST') == -1:
                        ### 获取满足最近财务条件的股票
                        GpZjCwxx=GpZjCw(zqdm,self.sj_rq)
                        gp_ldzccyzzc=GpZjCwxx.hq_gp_ldzccyzzc()
                        gp_xjllbl=GpZjCwxx.hq_gp_xjllbl()        
                        # print(gp_ldzccyzzc[0])
                        # print(gp_xjllbl)
                        #最近财报的流动资产除以总资产为0.0或大于0.5,现金流量比率大于0.5
                        if (gp_ldzccyzzc[0]==0 or gp_ldzccyzzc[0]>0.5) and gp_xjllbl[0] > 0.5:
                            gm_qd['gpcode'].append(zqxxxx["code"][0])
                            gm_qd['gpname'].append(zqxxxx["code_name"][0])
                            gm_qd['gpspj'].append(gp_spj[0])
                            gm_qd['gpzdf'].append(gp_zdf[0])
                            gm_qd['tdate'].append(self.sj_rq)
                            # print(gm_qd)
                            

        gm_qd = pd.DataFrame(gm_qd)
        return gm_qd

class SjGmGp(ZQ):
    '''
    随机指定购买的股票。
    通过规则数据之后随机取数。
    参数：
        sj_rq: string, 数据日期
    返回值：
        
    '''
    def __init__(self,sj_rq):
        self.sj_rq = sj_rq
    
    def hq_sjgp(self):
        '''
        获取随机股票
        '''
        mrgmckqd="C:\SoftwareZ\SProjects\PyProjects\Stock\data\k_gm_data_"+self.sj_rq+".csv"
        df = pd.read_csv(mrgmckqd) 
        print(df['gpcode'].sample(n=1))

if __name__ == '__main__':
    # bjye=GmGp('sz.002156','2023-12-26').hq_bjyr()
    # ygmgq=GmGp('2024-01-15')
    # sz.002156 200
    sjrq='2024-03-04'
    bjye=GmGp(sjrq).hq_bjyr('sz.003008',200)
    print(bjye)
    gm_qd=GmGp(sjrq).hq_kgmgp_qd(bjye) 
    #每日购买参考清单
    mrgmckqd="C:\SoftwareZ\SProjects\PyProjects\Stock\data\k_gm_data_"+sjrq+".csv"
    gm_qd.to_csv(mrgmckqd)


