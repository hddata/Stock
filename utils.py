import baostock as bs
import pandas as pd
import datetime 
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator, close
import functools # 导入functools模块

def dlbs(func):
    '''
    登录装饰器。
        1、统一登录。
        2、统一执行时间打印。
    '''
    # 定义一个内部函数，用来包装原始函数
    @functools.wraps(func) # 使用@wraps装饰器
    def wrapper(*args, **kwargs):
        #### 登陆系统 ####
        lg = bs.login()
        # 显示登陆返回信息
        print('login respond error_code:' + lg.error_code)
        print('login respond  error_msg:' + lg.error_msg)
        # 在调用原始函数之前打印日志
        print('Start: ' + str(datetime.datetime.now()))
        print(f"Calling {func.__name__} with {args} and {kwargs}")
        # 调用原始函数并返回结果
        result = func(*args, **kwargs) # 将结果存储在变量中
        print('End: ' + str(datetime.datetime.now()))
        bs.logout()
        return result # 在最后返回结果
    # 返回包装后的函数
    return wrapper


def hq_dqjd(sj_rq):
    '''
    获取_当前季度
    参数：
        sj_rq: string, 数据日期
    返回值：
        dqjd: string, 当前季度
    '''
    # 数据日期对象
    sj_rq_dx = datetime.datetime.strptime(sj_rq, "%Y-%m-%d")

    # 判断日期是第几季度
    if sj_rq_dx.month < 4:
        dqjd = 1
    elif sj_rq_dx.month < 7:
        dqjd = 2
    elif sj_rq_dx.month < 10:
        dqjd = 3
    else:
        dqjd = 4
    return dqjd

def hq_sjd(sj_rq):
    '''
    获取_上季度
    参数：
        sj_rq: string, 数据日期
    返回值：
        sjd: string, 上季度
    '''
    # 数据日期对象
    sj_rq_dx = datetime.datetime.strptime(sj_rq, "%Y-%m-%d")

    # 判断日期是第几季度
    if sj_rq_dx.month < 4:
        sjd = 4
    elif sj_rq_dx.month < 7:
        sjd = 1
    elif sj_rq_dx.month < 10:
        sjd = 2
    else:
        sjd = 1
    return sjd





class ZQ:
    '''
    证券(ZQ)基础类（1）：
        1.定义证券模型跑批数据范围(CN-中国)
        2.定义证券模型跑批时间范围
    参数：
        sj_fw: string, 证券模型基础数据范围
        sj_rq: string, 证券模型基础数据日期
    '''

    def __init__(self,sj_fw=None,sj_rq=None):
        self.sj_fw = sj_fw
        self.sj_rq = sj_rq

class ZQSS:
    '''
    证券实时[实时证券](ZQSS)基础类（1）：
        1.定义证券模型跑批数据范围(CN-中国)
    参数：
        sj_fw: string, 证券模型基础数据范围
    '''

    def __init__(self,sj_fw=None):
        self.sj_fw = sj_fw



if __name__ == '__main__':
    # print(get_gp_close.__doc__)
    help(ZQ)
    # hq_gp_spj('sz.002156','2023-12-28')