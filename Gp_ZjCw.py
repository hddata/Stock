import baostock as bs
import pandas as pd
import datetime 
from unicodedata import decimal
from utils import ZQ,dlbs,hq_dqjd,hq_sjd
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator, close


# @dlbs
class GpZjCw(ZQ):
    '''
    股票最近财务信息。（当年当季或上季）
        经营活动产生的现金流量净额除以营业收入（现金流量比率）
        经营性现金净流量除以净利润（现金流量保障比率）
        经营性现金净流量除以营业总收入（现金收入比率）
    参数：
        zqdm: string, 证券代码
        sj_rq: string, 数据日期
    返回值：
        
    '''
    def __init__(self,zqdm,sj_rq):
        '''

        '''
        self.zqdm=zqdm
        self.sj_rq = sj_rq

    def hq_gp_zjcw(self):
        dqnf = self.sj_rq[0:4]
        jdlb = [1,2,3,4]
        dqjd = hq_dqjd(self.sj_rq)
        sjd = hq_sjd(self.sj_rq)


        jdlb_sy = jdlb.index(dqjd)
        x_jdlb = [jdlb[jdlb_sy]] + jdlb[:jdlb_sy][::-1] + jdlb[jdlb_sy+1:][::-1]
        # print(x_jdlb)

        for jd in x_jdlb:
            # print(x_jdlb.index(jd))
            if x_jdlb.index(jd)==0 or x_jdlb.index(jd)<x_jdlb.index(4):
                gp = bs.query_cash_flow_data(
                    code=self.zqdm, 
                    year=dqnf, 
                    quarter=jd
                    ).get_data()
            elif x_jdlb.index(jd)>=x_jdlb.index(4):
                gp = bs.query_cash_flow_data(
                    code=self.zqdm, 
                    year=str(int(dqnf) - 1), 
                    quarter=jd
                    ).get_data()
            if not gp.empty:
                break
        
        # print(gp)
        return gp


    def hq_gp_ldzccyzzc(self):
        '''获取股票流动资产除以总资产
           如值不存在则为0。
        '''
        gp=self.hq_gp_zjcw()
        # print(gp['CAToAsset'])
        if len(gp['CAToAsset'])==0:
            gp_ldzccyzzc = gp['CAToAsset'].astype(float)
        else:
            gp_ldzccyzzc = pd.Series('0',name='CAToAsset').astype(float)
        return gp_ldzccyzzc

    def hq_gp_xjllbl(self):
        '''获取股票经营活动产生的现金流量净额除以营业收入（现金流量比率）'''
        gp=self.hq_gp_zjcw()
        if gp['CFOToOR'].iloc[0]=='':
            gp_ldzccyzzc = pd.Series('0',name='CFOToOR').astype(float)
        else:
            gp_ldzccyzzc = gp['CFOToOR'].astype(float)        
        return gp_ldzccyzzc


if __name__ == '__main__':
    lg = bs.login()
    # GpZjCw=GpZjCw('sh.688302','2024-01-02')
    GpZjCw=GpZjCw('sh.688300','2024-01-02')
    
    # GpZjCw.hq_gp_zjcw()
    print(GpZjCw.hq_gp_ldzccyzzc())
    # print(type(GpZjCw.hq_gp_xjllbl()))
    print(GpZjCw.hq_gp_xjllbl())
    bs.logout()
