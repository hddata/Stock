from Gp_JcXx import hq_sgjyr
from GM_Gp import SjGmGp,GmGp
import datetime
import time

def hq_zxjyr():
    #### 获取最新交易日,T+1
    # 当前日期
    jr = datetime.date.today()
    dqsj = time.strftime("%H:%M:%S", time.localtime())
    if dqsj < "15:30:00":
        # 当天关闭交易之前都取昨天作为最新交易日
        zxjyr = hq_sgjyr(jr.strftime('%Y-%m-%d'))
    else:
        # 当天关闭交易之后都取今天为最新交易日
        zxjyr = jr.strftime('%Y-%m-%d')
    return zxjyr

def hq_gmqd_5000(sjrq):
    '''
    获取购买清单_5000模型（入门入门入门）
    '''
    #### 获取购买清单_5000元基准模型
    bjye=5000
    gm_qd=GmGp(sjrq).hq_kgmgp_qd(bjye) 
    #每日购买参考清单
    mrgmckqd="C:\SoftwareZ\SProjects\PyProjects\Stock\data\k_gm_data_"+sjrq+".csv"
    gm_qd.to_csv(mrgmckqd)

if __name__ == '__main__':
    '''
    购购购（基于当前的行为）
    '''

    sjrq=hq_zxjyr()
    print(sjrq)
    #取最新交易日的前一天取随机
    hq_gmqd_5000(sjrq)
    print(SjGmGp(hq_sgjyr(sjrq)).hq_sjgp())



