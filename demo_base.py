from unicodedata import decimal
import baostock as bs
import pandas as pd
import datetime 
import time
from utils import * 
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator, close

plt.rcParams['font.sans-serif'] = ['SimHei'] #显示中文
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号

#### 获取交易日,T+1
# 当前日期
today = datetime.date.today()
yesterday = datetime.date.today() - datetime.timedelta(days=1)
now_time = time.strftime("%H:%M:%S", time.localtime())
if now_time < "15:30:00":
    # 当天关闭交易之前都取昨天作为最新的交易日
    lasttradeday = yesterday.strftime('%Y-%m-%d')
else:
    # 当天关闭交易之后都取今天为最新的交易日
    lasttradeday = today.strftime('%Y-%m-%d')

print(lasttradeday)



# 日期区间

#### 登陆系统 ####
lg = bs.login()
# 显示登陆返回信息
print('login respond error_code:' + lg.error_code)
print('login respond  error_msg:' + lg.error_msg)

rs =bs.query_stock_basic(code="sz.002156")
base_data =rs.get_data()



# 当前本金
bj = bs.query_history_k_data_plus(
    "sz.002156",
    # "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,isST",
    "date,code,open,high,low,close",
    start_date='2022-07-10',
    end_date='2022-07-13',
    frequency="d",
    adjustflag="3").get_data()

bjye = bj['close'].astype(float)*200
# print(bj)
print(bjye)




#### 获取沪深A股历史K线数据 ####

# rs = bs.query_history_k_data_plus(
#     "sz.002156",
#     # "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,isST",
#     "date,code,open,high,low,close",
#     start_date='2021-12-31',
#     end_date='2022-07-02',
#     frequency="d",
#     adjustflag="3")

# data_list=rs.get_data()
# print(data_list)
# # 设置X轴和Y轴的值，Y的值需要转变为数值型或者浮点型，才能在画图工具中正常构建排序的图片
# plt.plot(data_list['date'],data_list['close'].astype(float))
# #设置跨度与值,rotation斜着角度
# plt.xticks(data_list['date'][::10],rotation=30)
# #5 添加标题
# plt.xlabel(base_data['code_name'][0]+base_data['code'][0])
# plt.show()



# print('query_history_k_data_plus respond error_code:' + rs.error_code)
# print('query_history_k_data_plus respond  error_msg:' + rs.error_msg)

# #### 打印结果集 ####
# data_list = []
# while (rs.error_code == '0') & rs.next():
#     # 获取一条记录，将记录合并在一起
#     data_list.append(rs.get_row_data())
# result = pd.DataFrame(data_list, columns=rs.fields)

#### 结果集输出到csv文件 ####
# result.to_csv("C:\SoftwareZ\SProjects\PyProjects\Stock\data\history_A_stock_k_data.csv", index=False)
# print(result)

#### 登出系统 ####
bs.logout()