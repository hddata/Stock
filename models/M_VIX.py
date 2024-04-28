from mimetypes import init
import baostock as bs
import pandas as pd
import datetime 
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator, close

plt.rcParams['font.sans-serif'] = ['SimHei'] #显示中文
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号

# 第一份不成熟的class代码，留作纪念
# class Kmodels(object):

#     def __init__(self,zzcode,start_date,end_date):
#         self.zzcode=zzcode
#         self.start_date=start_date
#         self.end_date=end_date
#         #### 登陆系统 ####
#         lg = bs.login()
#         # 显示登陆返回信息
#         print('login respond error_code:' + lg.error_code)
#         print('login respond  error_msg:' + lg.error_msg)

#     # 波动率Volatility Index
#     def M_VIX(self):
#         print(self.zzcode,self.start_date,self.end_date)
#         VIXdata = bs.query_history_k_data_plus(
#             self.zzcode,
#             # "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,isST",
#             "date,code,open,high,low,close,preclose",
#             start_date=self.start_date,
#             end_date=self.end_date,
#             frequency="d",
#             adjustflag="3").get_data()

#         print(VIXdata)
#         VIXdata.loc[:,'VIX'] = VIXdata['close'].astype(float)-VIXdata['preclose'].astype(float)

#         print(VIXdata)

#         #### 登出系统 ####
#         bs.logout()

# if __name__ == '__main__':
    # K=Kmodels(zzcode='sz.002156',start_date='2022-07-10',end_date='2022-07-13')
    # K=Kmodels('sz.002156','2022-07-10','2022-07-13')
    # K.M_VIX()

class K_models():

    def __init__(self):
        #### 登陆系统 ####
        lg = bs.login()
        # 显示登陆返回信息
        print('login respond error_code:' + lg.error_code)
        print('login respond  error_msg:' + lg.error_msg)


    def M_VIX(self,zzcode,start_date,end_date):
        '''波动率Volatility Index'''
        #### 获取基本信息 ####
        zqxxxx = bs.query_stock_basic(code=zzcode).get_data()
        #### 获取基本价格信息 ####
        VIXdata = bs.query_history_k_data_plus(
            zzcode,
            # "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,isST",
            "date,code,open,high,low,close,preclose",
            start_date=start_date,
            end_date=end_date,
            frequency="d",
            adjustflag="3").get_data()

        VIXdata.loc[:,'VIX'] = VIXdata['close'].astype(float)-VIXdata['preclose'].astype(float)
        VIXdata.loc[:,'code_name'] = zqxxxx['code_name'][0]


        # 设置X轴和Y轴的值，Y的值需要转变为数值型或者浮点型，才能在画图工具中正常构建排序的图片
        plt.plot(VIXdata['date'],VIXdata['VIX'])
        #设置跨度与值,rotation斜着角度
        plt.xticks(VIXdata['date'][::10],rotation=30)
        #5 添加标题
        plt.xlabel(VIXdata['code_name'][0]+VIXdata['code'][0])  
        plt.axhline(y=0, ls='--', c='blue') 
        plt.show()

        #### 登出系统 ####
        bs.logout()

    
    def M_BaseVIX(self,zzcode,start_date,end_date):
        '''基于初始值波动率Volatility Index'''
        #### 获取基本信息 ####
        zqxxxx = bs.query_stock_basic(code=zzcode).get_data()
        #### 获取基本价格信息 ####
        VIXdata = bs.query_history_k_data_plus(
            zzcode,
            # "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,isST",
            "date,code,open,high,low,close,preclose",
            start_date=start_date,
            end_date=end_date,
            frequency="d",
            adjustflag="3").get_data()

 
        VIXdata.loc[:,'VIX'] = VIXdata['close'].astype(float)-float(VIXdata.loc[VIXdata.date == start_date,'close'][0])
        VIXdata.loc[:,'code_name'] = zqxxxx['code_name'][0]


        # 设置X轴和Y轴的值，Y的值需要转变为数值型或者浮点型，才能在画图工具中正常构建排序的图片
        plt.plot(VIXdata['date'],VIXdata['VIX'])
        #设置跨度与值,rotation斜着角度
        plt.xticks(VIXdata['date'][::10],rotation=30)
        #5 添加标题
        plt.xlabel(VIXdata['code_name'][0]+VIXdata['code'][0])  
        plt.axhline(y=0, ls='--', c='blue') 
        plt.show()

        #### 登出系统 ####
        bs.logout()


if __name__ == '__main__':
    # K_models().M_VIX('sz.002156','2022-01-10','2022-07-18')
    # K_models().M_BaseVIX('sz.002156','2022-01-10','2022-07-18')
    print(K_models().M_BaseVIX.__doc__)